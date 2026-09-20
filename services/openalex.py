import requests
from typing import List
from models.paper import Paper
from utils.helpers import reconstruct_openalex_abstract
from utils.logging_config import logger
from config.settings import OPENALEX_EMAIL, API_REQUEST_TIMEOUT

class OpenAlexService:
    BASE_URL = "https://api.openalex.org/works"

    @classmethod
    def search(cls, query: str, start_year: int = 2020, end_year: int = 2026, limit: int = 15) -> List[Paper]:
        papers: List[Paper] = []
        try:
            params = {
                "search": query,
                "per_page": min(limit, 25),
                "filter": f"publication_year:{start_year}-{end_year}",
                "mailto": OPENALEX_EMAIL
            }
            logger.info(f"Querying OpenAlex for: '{query}' (years {start_year}-{end_year})")
            resp = requests.get(cls.BASE_URL, params=params, timeout=API_REQUEST_TIMEOUT)
            
            if resp.status_code != 200:
                logger.warning(f"OpenAlex responded with status {resp.status_code}")
                return []

            data = resp.json()
            results = data.get("results", [])

            for item in results:
                title = item.get("title")
                if not title:
                    continue

                # Authors
                authors = []
                for auth in item.get("authorships", []):
                    name = auth.get("author", {}).get("display_name")
                    if name:
                        authors.append(name)

                # Year
                year = item.get("publication_year")

                # Abstract
                abstract = reconstruct_openalex_abstract(item.get("abstract_inverted_index"))

                # DOI
                raw_doi = item.get("doi") or ""
                doi = raw_doi.replace("https://doi.org/", "") if raw_doi else None

                # URL
                primary_loc = item.get("primary_location") or {}
                url = primary_loc.get("landing_page_url") or item.get("id")
                open_access_url = primary_loc.get("pdf_url")

                # Venue
                venue = None
                source_info = primary_loc.get("source")
                if source_info and isinstance(source_info, dict):
                    venue = source_info.get("display_name")

                # Citations
                citation_count = item.get("cited_by_count", 0)

                paper = Paper(
                    title=title,
                    authors=authors,
                    year=year,
                    abstract=abstract,
                    doi=doi,
                    url=url,
                    venue=venue,
                    source="OpenAlex",
                    citation_count=citation_count,
                    open_access_url=open_access_url
                )
                papers.append(paper)

            logger.info(f"OpenAlex returned {len(papers)} papers.")
        except Exception as e:
            logger.error(f"Error fetching from OpenAlex: {e}")
        return papers
