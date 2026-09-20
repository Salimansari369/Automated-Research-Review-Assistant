import pymupdf as fitz  # PyMuPDF
import os
import re
import docx
from typing import Tuple, Optional, Dict, Any, List
from models.paper import Paper
from utils.validators import validate_document, clean_doi, clean_text
from utils.logging_config import logger

class PDFProcessor:
    """
    Extracts text, metadata, and structure from uploaded academic documents:
    - PDF (.pdf) using PyMuPDF layout analysis
    - Word (.docx, .doc) using python-docx
    - Plaintext & Markdown (.txt, .md)
    """

    @classmethod
    def process_pdf(cls, file_path: str) -> Tuple[Optional[Paper], str]:
        """
        Alias for processing any supported document format.
        Returns (Paper, warning_message) on success, or (None, error_message) on failure.
        """
        return cls.process_document(file_path)

    @classmethod
    def process_document(cls, file_path: str) -> Tuple[Optional[Paper], str]:
        """
        Processes an uploaded PDF, DOCX, DOC, TXT, or MD file and returns a Paper model.
        """
        is_valid, err_msg = validate_document(file_path)
        if not is_valid:
            logger.warning(f"Document validation failed for {file_path}: {err_msg}")
            return None, err_msg

        ext = os.path.splitext(file_path)[1].lower()
        file_name = os.path.basename(file_path)

        # Copy to persistent uploads directory so it survives temp cleanup and refreshes
        try:
            import shutil
            from config.settings import UPLOADS_DIR
            os.makedirs(str(UPLOADS_DIR), exist_ok=True)
            persistent_path = os.path.join(str(UPLOADS_DIR), file_name)
            if os.path.abspath(file_path) != os.path.abspath(persistent_path):
                shutil.copy2(file_path, persistent_path)
            file_path = persistent_path
        except Exception as e:
            logger.warning(f"Could not copy document to persistent uploads: {e}")

        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)

        try:

            if ext == ".pdf":
                return cls._process_pdf_file(file_path, file_name, file_size_mb)
            elif ext in (".docx", ".doc"):
                return cls._process_docx_file(file_path, file_name, file_size_mb)
            elif ext in (".txt", ".md"):
                return cls._process_text_file(file_path, file_name, file_size_mb)
            else:
                return None, f"Unsupported file extension: {ext}"

        except Exception as e:
            logger.error(f"Failed to process document {file_path}: {e}")
            return None, f"Failed to extract document contents: {str(e)}"

    @classmethod
    def _process_pdf_file(cls, file_path: str, file_name: str, file_size_mb: float) -> Tuple[Optional[Paper], str]:
        doc = fitz.open(file_path)
        num_pages = len(doc)
        if num_pages == 0:
            doc.close()
            return None, "The PDF file contains 0 pages."

        pages_text: List[str] = []
        total_chars = 0
        for page in doc:
            text = page.get_text("text") or ""
            pages_text.append(text)
            total_chars += len(text.strip())

        avg_chars_per_page = total_chars / max(1, num_pages)
        is_scanned = avg_chars_per_page < 60
        full_text = "\n\n".join(pages_text)

        meta = doc.metadata or {}
        first_page = doc[0]
        title, authors, abstract, year, doi = cls._extract_first_page_metadata(first_page, meta, file_name, full_text)
        doc.close()

        warning = "⚠️ Scanned or image-only PDF detected. Direct text layer is missing." if (is_scanned and not full_text.strip()) else ""

        paper = Paper(
            title=title or file_name.replace(".pdf", "").replace("_", " "),
            authors=authors or ["Authors not detected"],
            year=year,
            abstract=abstract or (warning if is_scanned else "Abstract not explicitly separated in extracted text."),
            doi=doi,
            venue="Uploaded Document",
            source="Uploaded PDF",
            raw_text=clean_text(full_text),
            file_path=file_path,
            file_size_mb=round(file_size_mb, 2),
            is_uploaded=True,
            selected=True
        )

        logger.info(f"Successfully processed PDF: '{paper.title}' ({file_size_mb:.1f} MB, {num_pages} pages)")
        return paper, warning

    @classmethod
    def _process_docx_file(cls, file_path: str, file_name: str, file_size_mb: float) -> Tuple[Optional[Paper], str]:
        """Extracts text and metadata from Word .docx / .doc files."""
        try:
            doc = docx.Document(file_path)
            paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
            
            # Also extract text from any tables
            for table in doc.tables:
                for row in table.rows:
                    row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                    if row_text:
                        paragraphs.append(row_text)

            full_text = "\n\n".join(paragraphs)
            if not full_text.strip():
                return None, "Word document contains no readable text paragraphs."

            # Metadata from core properties
            core_props = doc.core_properties
            raw_title = (core_props.title or "").strip()
            generic_titles = {"word document", "microsoft word", "untitled", "document1", "document", "docx", "presentation", "header", "title"}
            title = raw_title if (raw_title and raw_title.lower() not in generic_titles and len(raw_title) > 3) else ""
            author = (core_props.author or "").strip()
            
            authors = [author] if author else []

            # Infer Title from first prominent paragraph if missing
            if not title and paragraphs:
                first_p = paragraphs[0].strip()
                if len(first_p) < 200 and not first_p.lower().startswith("table of contents") and len(first_p) > 3 and first_p.lower() not in generic_titles:
                    title = first_p
                else:
                    base_name = file_name
                    for ext in [".docx", ".doc"]:
                        if base_name.lower().endswith(ext):
                            base_name = base_name[:-len(ext)]
                    title = base_name.replace("_", " ").strip()

            # DOI extraction
            doi = None
            doi_match = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', full_text[:4000])
            if doi_match:
                doi = clean_doi(doi_match.group(0))

            # Year extraction
            year = None
            year_match = re.search(r'\b(20[12]\d)\b', full_text[:3000])
            if year_match:
                try:
                    year = int(year_match.group(1))
                except ValueError:
                    pass

            # Abstract extraction
            abstract = ""
            for p in paragraphs[:8]:
                if re.match(r'^(abstract|summary|executive summary)[:\s]', p, re.IGNORECASE):
                    abstract = p
                    break

            if not abstract and len(paragraphs) > 1:
                abstract = paragraphs[1][:800]

            paper = Paper(
                title=title or file_name.replace(".docx", "").replace(".doc", "").replace("_", " "),
                authors=authors or ["Authors not detected"],
                year=year or 2024,
                abstract=abstract or "Word Document content indexed for comparative analytics.",
                doi=doi,
                venue="Uploaded Word Document",
                source="Uploaded DOCX",
                raw_text=clean_text(full_text),
                file_path=file_path,
                file_size_mb=round(file_size_mb, 2),
                is_uploaded=True,
                selected=True
            )

            logger.info(f"Successfully processed Word DOCX: '{paper.title}' ({file_size_mb:.1f} MB, {len(paragraphs)} paragraphs)")
            return paper, ""

        except Exception as e:
            # Fallback for plain .doc binary text extraction
            try:
                with open(file_path, "rb") as f:
                    content = f.read().decode("latin-1", errors="ignore")
                printable = "".join([c for c in content if c.isprintable() or c in '\n\r\t'])
                lines = [l.strip() for l in printable.splitlines() if len(l.strip()) > 20]
                full_text = "\n\n".join(lines)
                if len(full_text) > 100:
                    paper = Paper(
                        title=file_name.replace(".doc", "").replace("_", " "),
                        authors=["Uploaded Author"],
                        year=2024,
                        abstract=full_text[:800],
                        venue="Uploaded Word Document",
                        source="Uploaded DOC",
                        raw_text=clean_text(full_text),
                        file_path=file_path,
                        file_size_mb=round(file_size_mb, 2),
                        is_uploaded=True,
                        selected=True
                    )
                    return paper, ""
            except Exception:
                pass
            return None, f"Failed to parse Word document: {str(e)}"

    @classmethod
    def _process_text_file(cls, file_path: str, file_name: str, file_size_mb: float) -> Tuple[Optional[Paper], str]:
        """Extracts text from plain .txt and .md files."""
        for enc in ("utf-8", "latin-1", "cp1252"):
            try:
                with open(file_path, "r", encoding=enc) as f:
                    full_text = f.read()
                break
            except UnicodeDecodeError:
                continue
        else:
            return None, "Unable to decode text file with UTF-8 or Latin-1."

        lines = [l.strip() for l in full_text.splitlines() if l.strip()]
        if not lines:
            return None, "Text file is empty."

        # Title heuristic
        title = lines[0].lstrip("#").strip()
        if len(title) > 200:
            title = file_name.replace(".txt", "").replace(".md", "").replace("_", " ")

        # DOI
        doi = None
        doi_match = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', full_text[:4000])
        if doi_match:
            doi = clean_doi(doi_match.group(0))

        # Year
        year = None
        year_match = re.search(r'\b(20[12]\d)\b', full_text[:3000])
        if year_match:
            try:
                year = int(year_match.group(1))
            except ValueError:
                pass

        abstract = lines[1][:800] if len(lines) > 1 else lines[0][:800]

        paper = Paper(
            title=title or file_name.replace(".txt", "").replace(".md", "").replace("_", " "),
            authors=["Uploaded Author"],
            year=year or 2024,
            abstract=abstract,
            doi=doi,
            venue="Uploaded Text File",
            source="Uploaded TXT",
            raw_text=clean_text(full_text),
            file_path=file_path,
            file_size_mb=round(file_size_mb, 2),
            is_uploaded=True,
            selected=True
        )

        logger.info(f"Successfully processed Text file: '{paper.title}' ({file_size_mb:.2f} MB)")
        return paper, ""

    @classmethod
    def _extract_first_page_metadata(cls, page: fitz.Page, meta: Dict[str, Any], file_name: str, full_text: str):
        """Uses PyMuPDF font size layout analysis to identify title, authors, and abstract."""
        title = meta.get("title", "").strip()
        if not title or title.lower().endswith(".docx") or len(title) < 4:
            title = ""

        authors: List[str] = []
        abstract = ""
        year = None
        doi = None

        doi_match = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', full_text[:4000])
        if doi_match:
            doi = clean_doi(doi_match.group(0))

        year_match = re.search(r'\b(20[12]\d)\b', full_text[:3000])
        if year_match:
            try:
                year = int(year_match.group(1))
            except ValueError:
                pass

        blocks = page.get_text("dict").get("blocks", [])
        spans_by_size = []
        for b in blocks:
            if "lines" in b:
                for line in b["lines"]:
                    line_text = " ".join(s.get("text", "").strip() for s in line.get("spans", []))
                    if not line_text:
                        continue
                    max_span_size = max((s.get("size", 0) for s in line.get("spans", [])), default=0)
                    spans_by_size.append((max_span_size, line_text))

        if not title and spans_by_size:
            max_size = max(s[0] for s in spans_by_size)
            title_candidates = [text for size, text in spans_by_size if size >= max_size * 0.92]
            candidate_str = " ".join(title_candidates[:3]).strip()
            if len(candidate_str) > 5 and not candidate_str.lower().startswith("arxiv:"):
                title = candidate_str

        abstract_patterns = [
            r'(?:ABSTRACT|Abstract)[:\.\s\n]+(.*?)(?=\n\s*(?:(?:I|1)[\.\s]+)?(?:INTRODUCTION|Introduction|Index Terms|Keywords)|$)',
            r'(?:Summary)[:\.\s\n]+(.*?)(?=\n\s*(?:Introduction|Keywords)|$)'
        ]
        first_page_text = page.get_text("text") or ""
        for pat in abstract_patterns:
            m = re.search(pat, first_page_text, re.DOTALL | re.IGNORECASE)
            if m:
                cand_abs = m.group(1).strip()
                if len(cand_abs) > 50:
                    abstract = re.sub(r'\s+', ' ', cand_abs[:2000])
                    break

        meta_author = meta.get("author", "").strip()
        if meta_author:
            authors = [a.strip() for a in re.split(r'[,;]|\band\b', meta_author) if a.strip()]

        return title, authors, abstract, year, doi
