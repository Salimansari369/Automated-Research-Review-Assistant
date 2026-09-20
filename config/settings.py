import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
EXPORTS_DIR = BASE_DIR / "exports"
UPLOADS_DIR = BASE_DIR / "uploads"

# Ensure directories exist
STATIC_DIR.mkdir(exist_ok=True)
EXPORTS_DIR.mkdir(exist_ok=True)
UPLOADS_DIR.mkdir(exist_ok=True)

# Application Config
APP_NAME = "LiteratureAI"
APP_TAGLINE = "AI-Powered Literature Review Assistant"
DEFAULT_TOPIC = "Agentic AI for Autonomous Space Communication Networks"
DEFAULT_YEAR_START = 2020
DEFAULT_YEAR_END = 2026
DEFAULT_MAX_PAPERS = 20
MAX_UPLOAD_SIZE_MB = 50

# Academic API Config
SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY", "")
OPENALEX_EMAIL = os.getenv("OPENALEX_EMAIL", "researcher@literatureai.org")
CROSSREF_MAILTO = os.getenv("CROSSREF_MAILTO", "researcher@literatureai.org")
ARXIV_ENABLED = os.getenv("ARXIV_ENABLED", "true").lower() == "true"

# LLM Config
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()  # openai, groq, anthropic, gemini, local, fallback
LLM_API_KEY = os.getenv("LLM_API_KEY", "") or os.getenv("OPENAI_API_KEY", "") or os.getenv("GROQ_API_KEY", "") or os.getenv("GEMINI_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "openai/gpt-oss-120b" if LLM_PROVIDER == "groq" else "gpt-4o-mini")
LLM_API_BASE = os.getenv("LLM_API_BASE", "")

# Timeouts & Request Limits
API_REQUEST_TIMEOUT = 12  # seconds
MAX_PAPERS_PER_SOURCE = 30
