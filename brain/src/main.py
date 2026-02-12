from fastapi import FastAPI, HTTPException, Header
from typing import Dict, Any, List, Optional
from .analyzer import SAPAnalyzer
from .vector_store.client import VectorStoreClient
from .rag_engine.engine import RAGEngine
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Antigravity Brain Service")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = SAPAnalyzer()

# Initialize Vector DB & RAG
db_url = os.getenv("DATABASE_URL", "postgresql://antigravity:antigravity_secret@db:5432/sap_pp_core")
try:
    vector_store = VectorStoreClient(db_url)
    rag_engine = RAGEngine(vector_store)
except Exception as e:
    print(f"Warning: Vector DB not ready. RAG disabled. {e}")
    rag_engine = None

@app.get("/")
def read_root():
    return {"service": "brain", "status": "active"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/brain/analyze/order")
def analyze_order(order_data: Dict[str, Any], x_tenant_id: Optional[str] = Header(None)):
    """
    Analyzes a Domain Order object with Tenant Context.
    """
    tenant_id = x_tenant_id or "default_tenant"
    try:
        # Future: Pass tenant_id to analyzer for tenant-specific rules
        insight = analyzer.analyze_order(order_data) 
        return {
            "tenant_id": tenant_id,
            "order_id": order_data.get("order_id"), 
            "analysis": insight
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/brain/rag/analyze")
def rag_analyze(
    payload: Dict[str, Any], 
    x_tenant_id: Optional[str] = Header(None),
    x_google_api_key: Optional[str] = Header(None)
):
    """
    Advanced RAG Analysis with Tenant Isolation.
    """
    if not rag_engine:
         raise HTTPException(status_code=503, detail="RAG Engine not initialized")
    
    tenant_id = x_tenant_id or "default_tenant"
    query = payload.get("query")
    context = payload.get("context", {})
    
    # Pass API Key dynamically
    response = rag_engine.analyze_with_context(query, context, tenant_id=tenant_id, api_key=x_google_api_key)
    return {"tenant_id": tenant_id, "response": response}


