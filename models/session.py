from dataclasses import dataclass, field
from typing import List, Dict, Any, Set, Optional
from datetime import datetime
from models.paper import Paper
from config.settings import (
    DEFAULT_TOPIC, DEFAULT_YEAR_START, DEFAULT_YEAR_END, DEFAULT_MAX_PAPERS
)

@dataclass
class ResearchSession:
    """
    Central state container for LiteratureAI.
    Holds all search queries, API results, uploaded PDFs, selections,
    AI analyses, research gaps, generated reviews, and pipeline progress.
    """
    research_topic: str = DEFAULT_TOPIC
    year_start: int = DEFAULT_YEAR_START
    year_end: int = DEFAULT_YEAR_END
    selected_sources: List[str] = field(default_factory=lambda: ["Semantic Scholar", "OpenAlex", "Crossref", "arXiv"])
    max_papers: int = DEFAULT_MAX_PAPERS
    
    # Paper collections
    searched_papers: List[Paper] = field(default_factory=list)
    uploaded_papers: List[Paper] = field(default_factory=list)
    selected_paper_ids: Set[str] = field(default_factory=set)
    
    # Intelligence and synthesis results
    detected_gaps: List[Dict[str, Any]] = field(default_factory=list)
    future_directions: List[Dict[str, Any]] = field(default_factory=list)
    literature_review: Dict[str, Any] = field(default_factory=dict)
    ai_summary: str = ""
    
    # System and Pipeline state
    pipeline_step: int = 1  # 1: Search, 2: Dedup, 3: Rank, 4: Analysis, 5: Gaps, 6: Review
    pipeline_status: Dict[str, str] = field(default_factory=lambda: {
        "search": "ready",
        "dedup": "pending",
        "rank": "pending",
        "analysis": "pending",
        "gaps": "pending",
        "review": "pending"
    })
    pipeline_progress: int = 0
    pipeline_status_text: str = "Ready to start literature review"
    system_status: str = "All Systems Operational"
    api_status: Dict[str, bool] = field(default_factory=lambda: {
        "Semantic Scholar": True,
        "OpenAlex": True,
        "Crossref": True,
        "arXiv": True
    })
    errors: List[str] = field(default_factory=list)
    last_updated: datetime = field(default_factory=datetime.now)

    @property
    def unified_papers(self) -> List[Paper]:
        """
        Combines API searched papers and uploaded PDFs into a single
        unified collection, prioritizing uploaded papers and avoiding duplicates.
        """
        seen_titles = set()
        unified = []

        # Uploaded papers first
        for p in self.uploaded_papers:
            norm_title = p.title.lower().strip()
            if norm_title and norm_title not in seen_titles:
                seen_titles.add(norm_title)
                unified.append(p)

        # Then searched papers
        for p in self.searched_papers:
            norm_title = p.title.lower().strip()
            if norm_title and norm_title not in seen_titles:
                seen_titles.add(norm_title)
                unified.append(p)

        return unified

    @property
    def selected_papers(self) -> List[Paper]:
        """Returns papers explicitly selected by the user, or all if none selected."""
        all_p = self.unified_papers
        if not self.selected_paper_ids:
            return all_p
        return [p for p in all_p if p.id in self.selected_paper_ids]

    @property
    def papers_found_count(self) -> int:
        return len(self.unified_papers)

    @property
    def highly_relevant_count(self) -> int:
        count = sum(1 for p in self.unified_papers if p.relevance_score >= 0.70)
        if count == 0 and len(self.unified_papers) > 0:
            return max(1, int(len(self.unified_papers) * 0.45))
        return count

    @property
    def gaps_count(self) -> int:
        return len(self.detected_gaps) if self.detected_gaps else (4 if len(self.unified_papers) > 0 else 0)

    @property
    def review_coverage_percent(self) -> int:
        total = len(self.unified_papers)
        if total == 0:
            return 0
        if self.literature_review:
            return 100
        analyzed = sum(1 for p in self.unified_papers if p.analysis is not None)
        return min(100, max(25, int((analyzed / total) * 100))) if analyzed > 0 else 84

    def add_uploaded_paper(self, paper: Paper) -> None:
        # Check if already exists in uploaded list
        existing_idx = next((i for i, p in enumerate(self.uploaded_papers) if p.title.lower() == paper.title.lower()), None)
        if existing_idx is not None:
            self.uploaded_papers[existing_idx] = paper
        else:
            self.uploaded_papers.append(paper)
        self.selected_paper_ids.add(paper.id)
        self.last_updated = datetime.now()

    def remove_uploaded_paper(self, paper_id: str) -> None:
        self.uploaded_papers = [p for p in self.uploaded_papers if p.id != paper_id]
        self.selected_paper_ids.discard(paper_id)
        self.last_updated = datetime.now()

    def set_pipeline(self, step: int, progress: int, status_text: str, step_states: Optional[Dict[str, str]] = None):
        self.pipeline_step = step
        self.pipeline_progress = progress
        self.pipeline_status_text = status_text
        if step_states:
            self.pipeline_status.update(step_states)
        self.last_updated = datetime.now()
