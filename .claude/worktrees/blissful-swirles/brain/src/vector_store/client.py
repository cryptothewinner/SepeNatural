import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class VectorStoreClient:
    """
    Client for interacting with PostgreSQL via pgvector with Multi-Tenancy support.
    """
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self._init_db()

    def _init_db(self):
        """
        Enable vector extension and create tables if not exist.
        Added tenant_id column for isolation.
        """
        with self.Session() as session:
            session.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            session.execute(text("""
                CREATE TABLE IF NOT EXISTS documents (
                    id SERIAL PRIMARY KEY,
                    tenant_id VARCHAR(50) NOT NULL DEFAULT 'default_tenant',
                    content TEXT,
                    metadata JSONB,
                    embedding VECTOR(1536)
                )
            """))
            # Index for performance? 
            # session.execute(text("CREATE INDEX IF NOT EXISTS idx_tenant ON documents (tenant_id)"))
            session.commit()

    def add_documents(self, documents: List[Dict[str, Any]], tenant_id: str = "default_tenant"):
        """
        Add documents with embeddings to the store for a specific tenant.
        """
        if not documents:
            return

        with self.Session() as session:
            for doc in documents:
                session.execute(text("""
                    INSERT INTO documents (tenant_id, content, metadata, embedding)
                    VALUES (:tenant_id, :content, :metadata, :embedding)
                """), {**doc, "tenant_id": tenant_id})
            session.commit()
    
    def search(self, query_embedding: List[float], tenant_id: str = "default_tenant", limit: int = 5) -> List[Dict]:
        """
        Semantic search scoped to a specific tenant_id.
        """
        with self.Session() as session:
            results = session.execute(text("""
                SELECT content, metadata, 1 - (embedding <=> :embedding) as similarity
                FROM documents
                WHERE tenant_id = :tenant_id
                ORDER BY embedding <=> :embedding
                LIMIT :limit
            """), {
                "embedding": str(query_embedding), 
                "limit": limit,
                "tenant_id": tenant_id
            }).fetchall()
            
            return [
                {"content": r[0], "metadata": r[1], "similarity": r[2]}
                for r in results
            ]
