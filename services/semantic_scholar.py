import requests
from typing import List
from models.paper import Paper
from utils.logging_config import logger
from config.settings import SEMANTIC_SCHOLAR_API_KEY, API_REQUEST_TIMEOUT

class SemanticScholarService:
    BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

    @classmethod
    def search(cls, query: str, start_year: int = 2020, end_year: int = 2026, limit: int = 15) -> List[Paper]:
        papers: List[Paper] = []
        try:
            params = {
                "query": query,
                "limit": min(limit, 25),
                "year": f"{start_year}-{end_year}",
                "fields": "title,authors,year,abstract,citationCount,venue,url,externalIds,openAccessPdf"
            }
            headers = {}
            if SEMANTIC_SCHOLAR_API_KEY:
                headers["x-api-key"] = SEMANTIC_SCHOLAR_API_KEY

            logger.info(f"Querying Semantic Scholar for: '{query}'")
            resp = requests.get(cls.BASE_URL, params=params, headers=headers, timeout=API_REQUEST_TIMEOUT)

            if resp.status_code == 429:
                logger.warning("Semantic Scholar rate limit reached. Proceeding with other sources.")
                return []
            if resp.status_code != 200:
                logger.warning(f"Semantic Scholar returned status {resp.status_code}")
                return []

            data = resp.json()
            items = data.get("data", [])

            for item in items:
                title = item.get("title")
                if not title:
                    continue

                authors = [a.get("name") for a in item.get("authors", []) if a.get("name")]
                year = item.get("year")
                abstract = item.get("abstract") or ""
                citation_count = item.get("citationCount") or 0
                venue = item.get("venue")
                url = item.get("url")
                
                ext_ids = item.get("externalIds") or {}
                doi = ext_ids.get("DOI")
                
                oa_info = item.get("openAccessPdf") or {}
                open_access_url = oa_info.get("url")

                paper = Paper(
                    title=title,
                    authors=authors,
                    year=year,
                    abstract=abstract,
                    doi=doi,
                    url=url,
                    venue=venue,
                    source="Semantic Scholar",
                    citation_count=citation_count,
                    open_access_url=open_access_url
                )
                papers.append(paper)

            logger.info(f"Semantic Scholar returned {len(papers)} papers.")
        except Exception as e:
            logger.error(f"Error fetching from Semantic Scholar: {e}")
        return papers
