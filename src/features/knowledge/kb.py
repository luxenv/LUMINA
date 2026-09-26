"""Local SQLite knowledge base for factual information."""
import sqlite3
from pathlib import Path
from datetime import datetime


class KnowledgeBase:
    """SQLite-backed knowledge base for storing facts, documents, and references."""
    
    def __init__(self, db_path="src/data/lumina.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()
    
    def init_db(self):
        """Initialize database schema if not exists."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS facts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT NOT NULL,
                    category TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    tags TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL,
                    response TEXT NOT NULL,
                    used_kb BOOLEAN DEFAULT 1,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
    
    def add_fact(self, key, value, category="general"):
        """Add or update a fact in the knowledge base.
        
        Args:
            key: Unique identifier for the fact (e.g., "capital_france")
            value: The fact value (e.g., "Paris")
            category: Optional category tag
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO facts (key, value, category, updated_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET
                    value = excluded.value,
                    updated_at = ?
            """, (key, value, category, datetime.now().isoformat(), datetime.now().isoformat()))
            conn.commit()
    
    def get_fact(self, key):
        """Retrieve a fact by key.
        
        Returns:
            Fact value or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT value FROM facts WHERE key = ?",
                (key,)
            )
            row = cursor.fetchone()
            return row[0] if row else None
    
    def search_facts(self, query, category=None):
        """Search facts by key or value.
        
        Args:
            query: Search string (case-insensitive)
            category: Optional category filter
            
        Returns:
            List of (key, value, category) tuples
        """
        with sqlite3.connect(self.db_path) as conn:
            if category:
                cursor = conn.execute("""
                    SELECT key, value, category FROM facts
                    WHERE (key LIKE ? OR value LIKE ?) AND category = ?
                    LIMIT 10
                """, (f"%{query}%", f"%{query}%", category))
            else:
                cursor = conn.execute("""
                    SELECT key, value, category FROM facts
                    WHERE key LIKE ? OR value LIKE ?
                    LIMIT 10
                """, (f"%{query}%", f"%{query}%"))
            return cursor.fetchall()
    
    def add_document(self, title, content, tags=""):
        """Add a reference document to the knowledge base.
        
        Args:
            title: Document title
            content: Document content
            tags: Comma-separated tags
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO documents (title, content, tags)
                VALUES (?, ?, ?)
            """, (title, content, tags))
            conn.commit()
    
    def search_documents(self, query):
        """Search documents by title or content.
        
        Args:
            query: Search string
            
        Returns:
            List of (id, title, content) tuples
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT id, title, content FROM documents
                WHERE title LIKE ? OR content LIKE ?
                LIMIT 5
            """, (f"%{query}%", f"%{query}%"))
            return cursor.fetchall()
    
    def log_query(self, query, response, used_kb=True):
        """Log a query and response for analytics.
        
        Args:
            query: User's query
            response: Model's response
            used_kb: Whether knowledge base was used
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO queries (query, response, used_kb)
                VALUES (?, ?, ?)
            """, (query, response, used_kb))
            conn.commit()
