import concurrent.futures
import re
from typing import List, Dict, Tuple
from models.paper import Paper
from services.openalex import OpenAlexService
from services.semantic_scholar import SemanticScholarService
from services.crossref import CrossrefService
from services.arxiv import ArxivService
from services.tavily_service import TavilyService
from services.relevance import RelevanceScorer
from utils.logging_config import logger

class SearchAggregator:
    """
    Coordinates multi-source concurrent academic literature search.
    Handles per-source failures gracefully and deduplicates findings.
    """

    @classmethod
    def execute_search(
        cls,
        topic: str,
        start_year: int = 2020,
        end_year: int = 2026,
        sources: List[str] = None,
        max_papers: int = 20
    ) -> Tuple[List[Paper], Dict[str, bool], List[str]]:
        if sources is None:
            sources = ["Semantic Scholar", "OpenAlex", "Crossref", "arXiv"]

        api_status = {s: True for s in sources}
        errors: List[str] = []
        all_retrieved: List[Paper] = []

        per_source_limit = max(8, max_papers // max(1, len(sources)) + 4)

        def query_source(source_name: str) -> List[Paper]:
            try:
                if source_name == "OpenAlex":
                    return OpenAlexService.search(topic, start_year, end_year, limit=per_source_limit)
                elif source_name == "Semantic Scholar":
                    return SemanticScholarService.search(topic, start_year, end_year, limit=per_source_limit)
                elif source_name == "Crossref":
                    return CrossrefService.search(topic, start_year, end_year, limit=per_source_limit)
                elif source_name == "arXiv":
                    return ArxivService.search(topic, start_year, end_year, limit=per_source_limit)
                elif source_name in ("Tavily", "Tavily Web & Code"):
                    return TavilyService.search(topic, limit=per_source_limit)
            except Exception as e:
                logger.error(f"Failed query for {source_name}: {e}")
                errors.append(f"{source_name}: {str(e)}")
                api_status[source_name] = False
            return []

        # Run concurrent queries
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(sources) or 1) as executor:
            future_to_source = {executor.submit(query_source, s): s for s in sources}
            for future in concurrent.futures.as_completed(future_to_source):
                src = future_to_source[future]
                try:
                    results = future.result()
                    if results:
                        all_retrieved.extend(results)
                    else:
                        logger.info(f"No results or failure from {src}")
                except Exception as exc:
                    logger.error(f"{src} generated an exception: {exc}")
                    errors.append(f"{src} error: {str(exc)}")
                    api_status[src] = False

        # Deduplicate
        deduped = cls._deduplicate_papers(all_retrieved)

        # Relevance scoring
        scored_papers = RelevanceScorer.score_papers(deduped, topic)

        # Truncate to user-requested maximum
        final_papers = scored_papers[:max_papers]

        logger.info(f"Aggregated {len(final_papers)} unique ranked papers across {len(sources)} sources.")
        return final_papers, api_status, errors

    @classmethod
    def _deduplicate_papers(cls, papers: List[Paper]) -> List[Paper]:
        """Deduplicates papers based on normalized title or DOI."""
        unique_papers: List[Paper] = []
        seen_keys = set()

        for p in papers:
            # DOI key if available
            if p.doi:
                doi_clean = p.doi.lower().strip()
                if doi_clean in seen_keys:
                    continue
                seen_keys.add(doi_clean)

            # Title key
            norm_title = re.sub(r'[^a-z0-9]', '', p.title.lower())
            if not norm_title or norm_title in seen_keys:
                continue
            seen_keys.add(norm_title)

            unique_papers.append(p)

        return unique_papers
