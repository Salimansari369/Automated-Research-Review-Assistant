import os
import requests
from typing import List, Dict, Any
from models.paper import Paper
from utils.logging_config import logger

class TavilyService:
    """
    Integrates Tavily AI Research Search Engine.
    Discovers real-time preprints, GitHub code implementations,
    benchmarks, and NASA/industry whitepapers.
    """
    ENDPOINT = "https://api.tavily.com/search"

    @classmethod
    def search(cls, query: str, limit: int = 5) -> List[Paper]:
        api_key = os.getenv("TAVILY_API_KEY", "")
        if not api_key:
            logger.info("TAVILY_API_KEY not set in .env. Skipping Tavily live search.")
            return []

        papers: List[Paper] = []
        try:
            payload = {
                "api_key": api_key,
                "query": f"{query} academic research paper implementation github benchmark",
                "search_depth": "advanced",
                "include_answer": True,
                "max_results": min(limit, 10),
                "include_domains": [
                    "arxiv.org",
                    "github.com",
                    "paperswithcode.com",
                    "semanticscholar.org",
                    "ieee.org",
                    "sciencedirect.com"
                ]
            }
            logger.info(f"Querying Tavily AI Search for: '{query}'")
            resp = requests.post(cls.ENDPOINT, json=payload, timeout=12)

            if resp.status_code != 200:
                logger.warning(f"Tavily returned status {resp.status_code}: {resp.text}")
                return []

            data = resp.json()
            results = data.get("results", [])

            for item in results:
                title = item.get("title", "")
                url = item.get("url", "")
                content = item.get("content", "")
                
                # Detect if GitHub code implementation
                is_github = "github.com" in url.lower()
                venue = "GitHub Repository" if is_github else "Web Preprint / Benchmark"
                
                paper = Paper(
                    title=title or "Implementation & Benchmark Resource",
                    authors=["Open Source / Research Community"],
                    year=2025,
                    abstract=content,
                    url=url,
                    venue=venue,
                    source="Tavily Web & Code",
                    citation_count=0
                )
                papers.append(paper)

            logger.info(f"Tavily returned {len(papers)} live research & code references.")
        except Exception as e:
            logger.error(f"Error querying Tavily API: {e}")
        return papers
