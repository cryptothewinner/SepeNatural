from fastapi import FastAPI, HTTPException, Header, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
import requests
import logging
from typing import Optional

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("API_Gateway")

app = FastAPI(title="Antigravity API Gateway")

# --- CORS MIDDLEWARE ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service URLs from Env
INGESTION_URL = os.getenv("INGESTION_SERVICE_URL", "http://ingestion:8001")
SEMANTIC_URL = os.getenv("SEMANTIC_SERVICE_URL", "http://semantic-layer:8002")
BRAIN_URL = os.getenv("BRAIN_SERVICE_URL", "http://brain:8003")

# --- MULTI-TENANCY MIDDLEWARE ---
async def get_tenant_id(x_tenant_id: Optional[str] = Header(None)):
    """
    Extracts X-Tenant-ID from headers.
    In a real scenario, this would validate against a Tenant Service.
    For local dev, we default to 'default_tenant' if missing.
    """
    if not x_tenant_id:
        logger.warning("No X-Tenant-ID provided. Using 'default_tenant'.")
        return "default_tenant"
    
    # Basic validation (alphanumeric only to prevent injection)
    if not x_tenant_id.isalnum():
        raise HTTPException(status_code=400, detail="Invalid Tenant ID format")
        
    return x_tenant_id

@app.middleware("http")
async def add_tenant_context(request: Request, call_next):
    """
    Middleware to log tenant context for every request.
    """
    tenant_id = request.headers.get("X-Tenant-ID", "default_tenant")
    # In a real app, we'd set this to a context var
    response = await call_next(request)
    response.headers["X-Tenant-ID"] = tenant_id
    return response


@app.get("/")
def read_root():
    return {
        "service": "api-gateway",
        "status": "ready",
        "endpoints": ["/analyze/full/{order_id}"]
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/analyze/full/{order_id}")
def full_analysis(order_id: str, tenant_id: str = Depends(get_tenant_id)):
    """
    Orchestrates the full SAP PP Analysis Pipeline with Tenant Context:
    1. Ingest Raw Data (Ingestion Service)
    2. Map to Domain Object (Semantic Layer)
    3. Analyze & RAG (Brain Service)
    """
    headers = {"X-Tenant-ID": tenant_id}
    logger.info(f"Processing Order {order_id} for Tenant: {tenant_id}")

    try:
        # Step 1: Ingest
        logger.info(f"Step 1: Fetching Order {order_id} from Ingestion...")
        # Note: In a real app, we'd pass order_id to the ingestion service. 
        # For this mocks/sprint 1, we fetch the list and filter.
        ingest_resp = requests.get(f"{INGESTION_URL}/ingest/production-orders", headers=headers)
        ingest_resp.raise_for_status()
        all_orders = ingest_resp.json()
        
        raw_order = next((o for o in all_orders if o["Aufnr"] == order_id), None)
        if not raw_order:
            raise HTTPException(status_code=404, detail="Order not found in SAP (Mock)")

        # Step 2: Semantic Map
        logger.info(f"Step 2: Mapping Order {order_id}...")
        map_resp = requests.post(f"{SEMANTIC_URL}/semantic/map/order", json=raw_order, headers=headers)
        map_resp.raise_for_status()
        domain_order = map_resp.json()

        # Step 3: Brain Analysis
        logger.info(f"Step 3: Analyzing Order {order_id}...")
        analy_resp = requests.post(f"{BRAIN_URL}/brain/analyze/order", json=domain_order, headers=headers)
        analy_resp.raise_for_status()
        analysis_result = analy_resp.json()
        
        # Step 4: RAG Context (Optional/Parallel)
        logger.info(f"Step 4: RAG Check...")
        rag_payload = {
            "query": "Are there any material shortages or risks?",
            "context": domain_order
        }
        # We wrap RAG in try/except so it doesn't fail the whole request if Vector DB is cold
        try:
             rag_resp = requests.post(f"{BRAIN_URL}/brain/rag/analyze", json=rag_payload, headers=headers)
             if rag_resp.status_code == 200:
                 rag_result = rag_resp.json().get("response")
             else:
                 rag_result = "RAG Service Unavailable"
        except Exception as e:
            rag_result = f"RAG Error: {str(e)}"

        return {
            "tenant_id": tenant_id,
            "order_id": order_id,
            "status": "Success",
            "pipeline_trace": ["Ingestion", "Semantic Mapping", "Brain Analysis", "RAG"],
            "raw_data_summary": f"SystemStatus: {raw_order.get('SystemStatus')}",
            "semantic_data": domain_order,
            "core_analysis": analysis_result.get("analysis"),
            "rag_insight": rag_result
        }

    except requests.exceptions.RequestException as e:
        logger.error(f"Pipeline Error: {e}")
        raise HTTPException(status_code=502, detail=f"Service Communication Error: {str(e)}")

@app.post("/brain/analyze/order")
def proxy_analyze_order(order_data: dict, tenant_id: str = Depends(get_tenant_id)):
    """Proxies request to Brain Service"""
    headers = {"X-Tenant-ID": tenant_id}
    try:
        resp = requests.post(f"{BRAIN_URL}/brain/analyze/order", json=order_data, headers=headers)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Brain Service Error: {str(e)}")

@app.post("/brain/rag/analyze")
def proxy_rag_analyze(payload: dict, tenant_id: str = Depends(get_tenant_id), x_google_api_key: Optional[str] = Header(None)):
    """Proxies RAG request to Brain Service"""
    headers = {
        "X-Tenant-ID": tenant_id,
        "x-google-api-key": x_google_api_key
    }
    try:
        resp = requests.post(f"{BRAIN_URL}/brain/rag/analyze", json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Brain Service Error: {str(e)}")
