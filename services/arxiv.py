import requests
import xml.etree.ElementTree as ET
from typing import List
from models.paper import Paper
from utils.logging_config import logger
from config.settings import API_REQUEST_TIMEOUT

class ArxivService:
    BASE_URL = "http://export.arxiv.org/api/query"
    ATOM_NS = "{http://www.w3.org/2005/Atom}"
    ARXIV_NS = "{http://arxiv.org/schemas/atom}"

    @classmethod
    def search(cls, query: str, start_year: int = 2020, end_year: int = 2026, limit: int = 15) -> List[Paper]:
        papers: List[Paper] = []
        try:
            # Clean query for arXiv API syntax
            clean_q = query.replace(" ", "+")
            params = {
                "search_query": f"all:{clean_q}",
                "start": 0,
                "max_results": min(limit, 25),
                "sortBy": "relevance",
                "sortOrder": "descending"
            }
            logger.info(f"Querying arXiv for: '{query}'")
            resp = requests.get(cls.BASE_URL, params=params, timeout=API_REQUEST_TIMEOUT)

            if resp.status_code != 200:
                logger.warning(f"arXiv returned status {resp.status_code}")
                return []

            root = ET.fromstring(resp.content)
            entries = root.findall(f"{cls.ATOM_NS}entry")

            for entry in entries:
                title_elem = entry.find(f"{cls.ATOM_NS}title")
                title = title_elem.text.strip().replace("\n", " ") if title_elem is not None and title_elem.text else ""
                if not title:
                    continue

                # Abstract / Summary
                summary_elem = entry.find(f"{cls.ATOM_NS}summary")
                abstract = summary_elem.text.strip().replace("\n", " ") if summary_elem is not None and summary_elem.text else ""

                # Published date & year
                pub_elem = entry.find(f"{cls.ATOM_NS}published")
                year = None
                if pub_elem is not None and pub_elem.text:
                    try:
                        year = int(pub_elem.text[:4])
                    except ValueError:
                        pass

                # Filter by year range if year exists
                if year and (year < start_year or year > end_year):
                    continue

                # Authors
                authors = []
                for author_elem in entry.findall(f"{cls.ATOM_NS}author"):
                    name_elem = author_elem.find(f"{cls.ATOM_NS}name")
                    if name_elem is not None and name_elem.text:
                        authors.append(name_elem.text.strip())

                # Links
                id_elem = entry.find(f"{cls.ATOM_NS}id")
                url = id_elem.text.strip() if id_elem is not None and id_elem.text else ""
                
                open_access_url = None
                for link in entry.findall(f"{cls.ATOM_NS}link"):
                    if link.attrib.get("title") == "pdf" or link.attrib.get("type") == "application/pdf":
                        open_access_url = link.attrib.get("href")
                        break

                # DOI
                doi_elem = entry.find(f"{cls.ARXIV_NS}doi")
                doi = doi_elem.text.strip() if doi_elem is not None and doi_elem.text else None

                paper = Paper(
                    title=title,
                    authors=authors,
                    year=year,
                    abstract=abstract,
                    doi=doi,
                    url=url,
                    venue="arXiv Preprint",
                    source="arXiv",
                    citation_count=0,
                    open_access_url=open_access_url
                )
                papers.append(paper)

            logger.info(f"arXiv returned {len(papers)} papers.")
        except Exception as e:
            logger.error(f"Error fetching from arXiv: {e}")
        return papers
