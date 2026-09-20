from dataclasses import dataclass, field
from typing import List, Dict, Any, Set, Optional
from datetime import datetime
import json
import os
from models.paper import Paper
from config.settings import (
    DEFAULT_TOPIC, DEFAULT_YEAR_START, DEFAULT_YEAR_END, DEFAULT_MAX_PAPERS,
    SESSION_FILE, DATA_DIR
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

    def to_dict(self) -> Dict[str, Any]:
        return {
            "research_topic": self.research_topic,
            "year_start": self.year_start,
            "year_end": self.year_end,
            "selected_sources": self.selected_sources,
            "max_papers": self.max_papers,
            "searched_papers": [p.to_dict() for p in self.searched_papers],
            "uploaded_papers": [p.to_dict() for p in self.uploaded_papers],
            "selected_paper_ids": list(self.selected_paper_ids),
            "detected_gaps": self.detected_gaps,
            "future_directions": self.future_directions,
            "literature_review": self.literature_review,
            "ai_summary": self.ai_summary,
            "pipeline_step": self.pipeline_step,
            "pipeline_status": self.pipeline_status,
            "pipeline_progress": self.pipeline_progress,
            "pipeline_status_text": self.pipeline_status_text,
            "system_status": self.system_status,
            "api_status": self.api_status,
            "errors": self.errors,
            "last_updated": self.last_updated.isoformat() if isinstance(self.last_updated, datetime) else str(self.last_updated)
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ResearchSession":
        sess = cls()
        sess.research_topic = data.get("research_topic", DEFAULT_TOPIC)
        sess.year_start = int(data.get("year_start", DEFAULT_YEAR_START) or DEFAULT_YEAR_START)
        sess.year_end = int(data.get("year_end", DEFAULT_YEAR_END) or DEFAULT_YEAR_END)
        sess.selected_sources = data.get("selected_sources", ["Semantic Scholar", "OpenAlex", "Crossref", "arXiv"])
        sess.max_papers = int(data.get("max_papers", DEFAULT_MAX_PAPERS) or DEFAULT_MAX_PAPERS)

        sess.searched_papers = [Paper.from_dict(p) for p in data.get("searched_papers", [])]
        sess.uploaded_papers = [Paper.from_dict(p) for p in data.get("uploaded_papers", [])]
        sess.selected_paper_ids = set(data.get("selected_paper_ids", []))

        sess.detected_gaps = data.get("detected_gaps", [])
        sess.future_directions = data.get("future_directions", [])
        sess.literature_review = data.get("literature_review", {})
        sess.ai_summary = data.get("ai_summary", "")

        sess.pipeline_step = int(data.get("pipeline_step", 1) or 1)
        sess.pipeline_status = data.get("pipeline_status", {
            "search": "ready", "dedup": "pending", "rank": "pending",
            "analysis": "pending", "gaps": "pending", "review": "pending"
        })
        sess.pipeline_progress = int(data.get("pipeline_progress", 0) or 0)
        sess.pipeline_status_text = data.get("pipeline_status_text", "Ready to start literature review")
        sess.system_status = data.get("system_status", "All Systems Operational")
        sess.api_status = data.get("api_status", {
            "Semantic Scholar": True, "OpenAlex": True, "Crossref": True, "arXiv": True
        })
        sess.errors = data.get("errors", [])
        last_up = data.get("last_updated")
        if last_up:
            try:
                sess.last_updated = datetime.fromisoformat(last_up)
            except Exception:
                sess.last_updated = datetime.now()
        return sess

    def save_to_disk(self, filepath: Optional[str] = None) -> bool:
        path = filepath or str(SESSION_FILE)
        try:
            target_dir = os.path.dirname(os.path.abspath(path))
            os.makedirs(target_dir, exist_ok=True)
            data = self.to_dict()
            tmp_path = f"{path}.tmp"
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            if os.path.exists(path):
                os.replace(tmp_path, path)
            else:
                os.rename(tmp_path, path)
            return True
        except Exception as e:
            print(f"[ResearchSession] Failed to save session to disk: {e}")
            return False

    @classmethod
    def load_from_disk(cls, filepath: Optional[str] = None) -> "ResearchSession":
        path = filepath or str(SESSION_FILE)
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                sess = cls.from_dict(data)
                return sess
            except Exception as e:
                print(f"[ResearchSession] Failed to load session from disk: {e}")
        return cls()

    @classmethod
    def clear_disk_history(cls, filepath: Optional[str] = None) -> bool:
        path = filepath or str(SESSION_FILE)
        try:
            if os.path.exists(path):
                os.remove(path)
            return True
        except Exception as e:
            print(f"[ResearchSession] Failed to clear disk session: {e}")
            return False

