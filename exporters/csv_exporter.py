import os
import pandas as pd
from typing import List
from models.paper import Paper
from config.settings import EXPORTS_DIR
from utils.logging_config import logger

class CsvExporter:
    @classmethod
    def export_comparison(cls, papers: List[Paper], filename_prefix: str = "Paper_Comparison") -> str:
        """Exports comparative paper data to a structured CSV file."""
        rows = []
        for idx, p in enumerate(papers, 1):
            analysis = p.analysis or {}
            rows.append({
                "Rank": idx,
                "Title": p.title,
                "Authors": p.formatted_authors,
                "Year": p.year or "n.d.",
                "Venue": p.venue or "Unspecified",
                "Source": p.source,
                "Citations": p.citation_count,
                "Relevance_Score_%": p.relevance_percent,
                "DOI": p.doi or "",
                "URL": p.url or "",
                "Research_Problem": analysis.get("research_problem", ""),
                "Methodology": analysis.get("methodology", ""),
                "Dataset": analysis.get("dataset", ""),
                "Key_Findings": analysis.get("key_findings", ""),
                "Limitations": analysis.get("limitations", ""),
                "Future_Work": analysis.get("future_work", ""),
                "Domain": analysis.get("research_domain", ""),
                "Keywords": ", ".join(analysis.get("technical_keywords", []))
            })

        df = pd.DataFrame(rows)
        safe_prefix = "".join(c for c in filename_prefix if c.isalnum() or c in ("-", "_"))[:30]
        out_path = str(EXPORTS_DIR / f"{safe_prefix}.csv")
        df.to_csv(out_path, index=False, encoding="utf-8-sig")
        logger.info(f"Generated CSV paper comparison: {out_path}")
        return out_path
