import requests
import re
from typing import List
from models.paper import Paper
from utils.logging_config import logger
from config.settings import CROSSREF_MAILTO, API_REQUEST_TIMEOUT

class CrossrefService:
    BASE_URL = "https://api.crossref.org/works"

    @classmethod
    def search(cls, query: str, start_year: int = 2020, end_year: int = 2026, limit: int = 15) -> List[Paper]:
        papers: List[Paper] = []
        try:
            params = {
                "query": query,
                "rows": min(limit, 25),
                "filter": f"from-pub-date:{start_year}-01-01,until-pub-date:{end_year}-12-31",
                "mailto": CROSSREF_MAILTO
            }
            logger.info(f"Querying Crossref for: '{query}'")
            resp = requests.get(cls.BASE_URL, params=params, timeout=API_REQUEST_TIMEOUT)

            if resp.status_code != 200:
                logger.warning(f"Crossref returned status {resp.status_code}")
                return []

            data = resp.json()
            items = data.get("message", {}).get("items", [])

            for item in items:
                title_list = item.get("title", [])
                if not title_list or not title_list[0]:
                    continue
                title = title_list[0]

                # Authors
                authors = []
                for auth in item.get("author", []):
                    given = auth.get("given", "")
                    family = auth.get("family", "")
                    full = f"{given} {family}".strip()
                    if full:
                        authors.append(full)

                # Year
                published = item.get("published", {}).get("date-parts", [[]])
                year = published[0][0] if published and published[0] else None

                # Abstract (Crossref sometimes embeds JATS XML tags like <jats:p>)
                abstract_raw = item.get("abstract", "")
                abstract = re.sub(r'<[^>]+>', '', abstract_raw).strip()

                # DOI
                doi = item.get("DOI")
                url = item.get("URL") or (f"https://doi.org/{doi}" if doi else None)

                # Venue
                venue_list = item.get("container-title", [])
                venue = venue_list[0] if venue_list else None

                # Citations
                citation_count = item.get("is-referenced-by-count", 0)

                paper = Paper(
                    title=title,
                    authors=authors,
                    year=year,
                    abstract=abstract,
                    doi=doi,
                    url=url,
                    venue=venue,
                    source="Crossref",
                    citation_count=citation_count
                )
                papers.append(paper)

            logger.info(f"Crossref returned {len(papers)} papers.")
        except Exception as e:
            logger.error(f"Error fetching from Crossref: {e}")
        return papers
