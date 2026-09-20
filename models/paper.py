from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import hashlib
import re

@dataclass
class Paper:
    """
    Unified representation of an academic paper, whether retrieved from
    an academic database API or extracted from an uploaded PDF.
    """
    title: str
    authors: List[str] = field(default_factory=list)
    year: Optional[int] = None
    abstract: str = ""
    doi: Optional[str] = None
    url: Optional[str] = None
    venue: Optional[str] = None
    source: str = "Semantic Scholar"  # OpenAlex, Crossref, arXiv, Uploaded PDF
    citation_count: int = 0
    relevance_score: float = 0.0  # 0.0 to 1.0
    open_access_url: Optional[str] = None
    raw_text: str = ""
    file_path: Optional[str] = None
    file_size_mb: Optional[float] = None
    is_uploaded: bool = False
    selected: bool = False
    analysis: Optional[Dict[str, Any]] = None
    id: str = ""

    def __post_init__(self):
        if not self.id:
            # Generate a stable deterministic ID
            seed = f"{self.title.lower().strip()}_{self.doi or ''}_{self.year or ''}"
            self.id = hashlib.md5(seed.encode("utf-8")).hexdigest()[:10]
        # Clean title
        self.title = re.sub(r'\s+', ' ', self.title).strip()
        # Clean abstract
        self.abstract = re.sub(r'\s+', ' ', self.abstract).strip()

    @property
    def formatted_authors(self) -> str:
        """Returns author string formatted as 'Author A, Author B, ...' or 'Author A et al.'"""
        if not self.authors:
            return "Authors not reported"
        if len(self.authors) <= 3:
            return ", ".join(self.authors)
        return f"{self.authors[0]} et al. ({len(self.authors)} authors)"

    @property
    def citation_key(self) -> str:
        """Standard citation label e.g., 'Kumar et al., 2025'"""
        first = self.authors[0].split()[-1] if self.authors else "Anon"
        yr = str(self.year) if self.year else "n.d."
        if len(self.authors) > 1:
            return f"{first} et al., {yr}"
        return f"{first}, {yr}"

    @property
    def relevance_percent(self) -> int:
        return int(round(self.relevance_score * 100))

    @property
    def short_abstract(self) -> str:
        if len(self.abstract) > 240:
            return self.abstract[:237] + "..."
        return self.abstract or "Abstract not available for this publication."

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "authors": self.authors,
            "year": self.year,
            "abstract": self.abstract,
            "doi": self.doi,
            "url": self.url,
            "venue": self.venue,
            "source": self.source,
            "citation_count": self.citation_count,
            "relevance_score": self.relevance_score,
            "open_access_url": self.open_access_url,
            "raw_text": self.raw_text,
            "file_path": self.file_path,
            "file_size_mb": self.file_size_mb,
            "is_uploaded": self.is_uploaded,
            "selected": self.selected,
            "analysis": self.analysis
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Paper":
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            authors=data.get("authors", []) or [],
            year=data.get("year"),
            abstract=data.get("abstract", "") or "",
            doi=data.get("doi"),
            url=data.get("url"),
            venue=data.get("venue"),
            source=data.get("source", "Semantic Scholar"),
            citation_count=data.get("citation_count", 0),
            relevance_score=float(data.get("relevance_score", 0.0) or 0.0),
            open_access_url=data.get("open_access_url"),
            raw_text=data.get("raw_text", "") or "",
            file_path=data.get("file_path"),
            file_size_mb=float(data.get("file_size_mb")) if data.get("file_size_mb") is not None else None,
            is_uploaded=bool(data.get("is_uploaded", False)),
            selected=bool(data.get("selected", False)),
            analysis=data.get("analysis")
        )

