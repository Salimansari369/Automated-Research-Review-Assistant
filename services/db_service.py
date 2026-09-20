import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from config.settings import DATA_DIR
from models.paper import Paper
from utils.logging_config import logger

DB_PATH = DATA_DIR / "database.db"

class DatabaseService:
    """
    SQLite Relational Database Service for LiteratureAI.
    Provides persistent ACID storage for uploaded documents, academic search results,
    AI analyses, detected research gaps, and full literature reviews.
    """

    @classmethod
    def get_connection(cls) -> sqlite3.Connection:
        os.makedirs(str(DATA_DIR), exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH), timeout=15.0)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def init_db(cls):
        """Initializes database schema and tables."""
        conn = cls.get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS uploaded_documents (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                authors TEXT,
                year INTEGER,
                abstract TEXT,
                doi TEXT,
                url TEXT,
                venue TEXT,
                source TEXT DEFAULT 'Uploaded Document',
                citation_count INTEGER DEFAULT 0,
                relevance_score REAL DEFAULT 0.0,
                raw_text TEXT,
                file_path TEXT,
                file_size_mb REAL DEFAULT 0.0,
                analysis_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS searched_papers (
                id TEXT PRIMARY KEY,
                topic TEXT,
                title TEXT NOT NULL,
                authors TEXT,
                year INTEGER,
                abstract TEXT,
                doi TEXT,
                url TEXT,
                venue TEXT,
                source TEXT,
                citation_count INTEGER DEFAULT 0,
                relevance_score REAL DEFAULT 0.0,
                analysis_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS session_state (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            conn.commit()
            logger.info(f"SQLite Database initialized successfully at {DB_PATH}")
        except Exception as e:
            logger.error(f"Error initializing SQLite database: {e}")
        finally:
            conn.close()

    @classmethod
    def save_uploaded_paper(cls, paper: Paper):
        """Inserts or replaces an uploaded paper in the SQLite database."""
        conn = cls.get_connection()
        try:
            cur = conn.cursor()
            authors_json = json.dumps(paper.authors, ensure_ascii=False)
            analysis_json = json.dumps(paper.analysis, ensure_ascii=False) if paper.analysis else None

            cur.execute("""
            INSERT OR REPLACE INTO uploaded_documents (
                id, title, authors, year, abstract, doi, url, venue, source,
                citation_count, relevance_score, raw_text, file_path, file_size_mb,
                analysis_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                paper.id,
                paper.title,
                authors_json,
                paper.year,
                paper.abstract,
                paper.doi,
                paper.url,
                paper.venue,
                paper.source,
                paper.citation_count,
                paper.relevance_score,
                paper.raw_text,
                paper.file_path,
                paper.file_size_mb,
                analysis_json,
                datetime.now().isoformat()
            ))

            cur.execute(
                "INSERT INTO activity_logs (event_type, message) VALUES (?, ?)",
                ("UPLOAD", f"Saved document '{paper.title}' ({paper.file_size_mb or 0.0:.1f} MB)")
            )
            conn.commit()
            logger.info(f"Saved paper '{paper.title}' to SQLite DB.")
        except Exception as e:
            logger.error(f"Failed to save paper to SQLite DB: {e}")
        finally:
            conn.close()

    @classmethod
    def get_all_uploaded_papers(cls) -> List[Paper]:
        """Loads all uploaded papers from SQLite."""
        conn = cls.get_connection()
        papers = []
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM uploaded_documents ORDER BY created_at ASC")
            rows = cur.fetchall()
            for r in rows:
                authors = json.loads(r["authors"]) if r["authors"] else []
                analysis = json.loads(r["analysis_json"]) if r["analysis_json"] else None
                p = Paper(
                    id=r["id"],
                    title=r["title"],
                    authors=authors,
                    year=r["year"],
                    abstract=r["abstract"] or "",
                    doi=r["doi"],
                    url=r["url"],
                    venue=r["venue"],
                    source=r["source"] or "Uploaded Document",
                    citation_count=r["citation_count"] or 0,
                    relevance_score=r["relevance_score"] or 0.0,
                    raw_text=r["raw_text"] or "",
                    file_path=r["file_path"],
                    file_size_mb=r["file_size_mb"],
                    is_uploaded=True,
                    selected=True,
                    analysis=analysis
                )
                papers.append(p)
        except Exception as e:
            logger.error(f"Error fetching uploaded papers from DB: {e}")
        finally:
            conn.close()
        return papers

    @classmethod
    def save_searched_papers(cls, papers: List[Paper], topic: str = ""):
        """Stores searched papers from academic APIs into SQLite."""
        conn = cls.get_connection()
        try:
            cur = conn.cursor()
            # Clear old search results for clean state
            cur.execute("DELETE FROM searched_papers")
            for p in papers:
                authors_json = json.dumps(p.authors, ensure_ascii=False)
                analysis_json = json.dumps(p.analysis, ensure_ascii=False) if p.analysis else None
                cur.execute("""
                INSERT OR REPLACE INTO searched_papers (
                    id, topic, title, authors, year, abstract, doi, url, venue, source,
                    citation_count, relevance_score, analysis_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    p.id,
                    topic,
                    p.title,
                    authors_json,
                    p.year,
                    p.abstract,
                    p.doi,
                    p.url,
                    p.venue,
                    p.source,
                    p.citation_count,
                    p.relevance_score,
                    analysis_json,
                    datetime.now().isoformat()
                ))
            conn.commit()
        except Exception as e:
            logger.error(f"Error saving searched papers to DB: {e}")
        finally:
            conn.close()

    @classmethod
    def get_all_searched_papers(cls) -> List[Paper]:
        """Loads searched academic papers from SQLite."""
        conn = cls.get_connection()
        papers = []
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM searched_papers ORDER BY relevance_score DESC, citation_count DESC")
            rows = cur.fetchall()
            for r in rows:
                authors = json.loads(r["authors"]) if r["authors"] else []
                analysis = json.loads(r["analysis_json"]) if r["analysis_json"] else None
                p = Paper(
                    id=r["id"],
                    title=r["title"],
                    authors=authors,
                    year=r["year"],
                    abstract=r["abstract"] or "",
                    doi=r["doi"],
                    url=r["url"],
                    venue=r["venue"],
                    source=r["source"] or "Academic Search",
                    citation_count=r["citation_count"] or 0,
                    relevance_score=r["relevance_score"] or 0.0,
                    is_uploaded=False,
                    analysis=analysis
                )
                papers.append(p)
        except Exception as e:
            logger.error(f"Error fetching searched papers from DB: {e}")
        finally:
            conn.close()
        return papers

    @classmethod
    def save_session_state(cls, sess: Any):
        """Saves entire session state (metadata, gaps, review) into SQLite."""
        cls.init_db()
        # 1. Save uploaded papers
        for p in sess.uploaded_papers:
            cls.save_uploaded_paper(p)

        # 2. Save searched papers
        if sess.searched_papers:
            cls.save_searched_papers(sess.searched_papers, sess.research_topic)

        # 3. Save session metadata in session_state table
        conn = cls.get_connection()
        try:
            cur = conn.cursor()
            state_items = {
                "research_topic": sess.research_topic,
                "year_start": str(sess.year_start),
                "year_end": str(sess.year_end),
                "selected_sources": json.dumps(sess.selected_sources),
                "max_papers": str(sess.max_papers),
                "detected_gaps": json.dumps(sess.detected_gaps, ensure_ascii=False),
                "literature_review": json.dumps(sess.literature_review, ensure_ascii=False),
                "ai_summary": sess.ai_summary,
                "pipeline_step": str(sess.pipeline_step),
                "pipeline_progress": str(sess.pipeline_progress),
                "pipeline_status_text": sess.pipeline_status_text,
                "pipeline_status": json.dumps(sess.pipeline_status),
                "last_updated": datetime.now().isoformat()
            }

            for k, v in state_items.items():
                cur.execute(
                    "INSERT OR REPLACE INTO session_state (key, value, updated_at) VALUES (?, ?, ?)",
                    (k, v, datetime.now().isoformat())
                )
            conn.commit()
            logger.info("Session state saved to SQLite database.")
        except Exception as e:
            logger.error(f"Error saving session state to SQLite: {e}")
        finally:
            conn.close()

    @classmethod
    def load_session_state(cls) -> Dict[str, Any]:
        """Loads session metadata from SQLite."""
        cls.init_db()
        conn = cls.get_connection()
        data = {}
        try:
            cur = conn.cursor()
            cur.execute("SELECT key, value FROM session_state")
            rows = cur.fetchall()
            for r in rows:
                k = r["key"]
                v = r["value"]
                if k in ("selected_sources", "detected_gaps", "literature_review", "pipeline_status"):
                    try:
                        data[k] = json.loads(v)
                    except Exception:
                        data[k] = v
                elif k in ("year_start", "year_end", "max_papers", "pipeline_step", "pipeline_progress"):
                    try:
                        data[k] = int(v)
                    except Exception:
                        data[k] = 0
                else:
                    data[k] = v
        except Exception as e:
            logger.error(f"Error reading session state from SQLite: {e}")
        finally:
            conn.close()
        return data

    @classmethod
    def clear_database(cls):
        """Wipes all data in the SQLite database."""
        conn = cls.get_connection()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM uploaded_documents")
            cur.execute("DELETE FROM searched_papers")
            cur.execute("DELETE FROM session_state")
            cur.execute("DELETE FROM activity_logs")
            conn.commit()
            logger.info("Cleared all SQLite database tables.")
        except Exception as e:
            logger.error(f"Error clearing database: {e}")
        finally:
            conn.close()

    @classmethod
    def get_database_stats(cls) -> Dict[str, Any]:
        """Returns statistical overview of the SQLite database."""
        cls.init_db()
        conn = cls.get_connection()
        stats = {
            "uploaded_count": 0,
            "searched_count": 0,
            "total_size_mb": 0.0,
            "db_path": str(DB_PATH),
            "db_size_kb": os.path.getsize(str(DB_PATH)) / 1024 if os.path.exists(str(DB_PATH)) else 0.0,
            "last_activity": "None"
        }
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*), SUM(file_size_mb) FROM uploaded_documents")
            row = cur.fetchone()
            if row:
                stats["uploaded_count"] = row[0] or 0
                stats["total_size_mb"] = round(row[1] or 0.0, 2)

            cur.execute("SELECT COUNT(*) FROM searched_papers")
            s_row = cur.fetchone()
            if s_row:
                stats["searched_count"] = s_row[0] or 0

            cur.execute("SELECT message, created_at FROM activity_logs ORDER BY id DESC LIMIT 1")
            act_row = cur.fetchone()
            if act_row:
                stats["last_activity"] = f"{act_row['message']} ({act_row['created_at']})"
        except Exception as e:
            logger.error(f"Error retrieving database stats: {e}")
        finally:
            conn.close()
        return stats
