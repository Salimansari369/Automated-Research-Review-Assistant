import os
import re
from typing import Tuple

SUPPORTED_EXTENSIONS = [".pdf", ".docx", ".doc", ".txt", ".md"]

def validate_document(file_path: str, max_size_mb: int = 50) -> Tuple[bool, str]:
    """Validates that a file is an accessible document within the size limit."""
    if not os.path.exists(file_path):
        return False, "File does not exist."
    
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        return False, f"Unsupported file type '{ext}'. Supported formats: {', '.join(SUPPORTED_EXTENSIONS)}"
    
    size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if size_mb > max_size_mb:
        return False, f"File size ({size_mb:.1f} MB) exceeds maximum allowed limit of {max_size_mb} MB."
    
    # Format specific magic validation
    if ext == ".pdf":
        try:
            with open(file_path, "rb") as f:
                header = f.read(5)
                if not header.startswith(b"%PDF"):
                    return False, "File is not a valid PDF document (missing %PDF signature)."
        except Exception as e:
            return False, f"Could not read PDF file: {str(e)}"
            
    return True, ""

def validate_pdf(file_path: str, max_size_mb: int = 50) -> Tuple[bool, str]:
    """Alias for backwards compatibility."""
    return validate_document(file_path, max_size_mb)

def clean_doi(doi_raw: str) -> str:
    """Extracts and normalizes a clean DOI from URLs or strings."""
    if not doi_raw:
        return ""
    match = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', doi_raw)
    return match.group(0) if match else doi_raw.strip()

def clean_text(text: str) -> str:
    """Removes weird encoding artifacts and unifies whitespace."""
    if not text:
        return ""
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
