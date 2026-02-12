from fastapi import FastAPI, HTTPException, Header, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx
import asyncio
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("API_Gateway")

app = FastAPI(title="Antigravity API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

INGESTION_URL = os.getenv("INGESTION_SERVICE_URL", "http://ingestion:8001")
SEMANTIC_URL = os.getenv("SEMANTIC_SERVICE_URL", "http://semantic-layer:8002")
BRAIN_URL = os.getenv("BRAIN_SERVICE_URL", "http://brain:8003")

TIMEOUT = httpx.Timeout(30.0, connect=5.0)


async def get_tenant_id(x_tenant_id: Optional[str] = Header(None)) -> str:
    if not x_tenant_id:
        logger.warning("No X-Tenant-ID provided. Using 'default_tenant'.")
        return "default_tenant"
    if not all(c.isalnum() or c in "-_" for c in x_tenant_id):
        raise HTTPException(status_code=400, detail="Invalid Tenant ID format")
    return x_tenant_id


@app.middleware("http")
async def add_tenant_context(request: Request, call_next):
    tenant_id = request.headers.get("X-Tenant-ID", "default_tenant")
    response = await call_next(request)
    response.headers["X-Tenant-ID"] = tenant_id
    return response


@app.get("/")
def read_root():
    return {
        "service": "api-gateway",
        "status": "ready",
        "endpoints": ["/analyze/full/{order_id}", "/products/sepenatural"],
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/products/sepenatural")
async def get_sepenatural_products(tenant_id: str = Depends(get_tenant_id)):
    headers = {"X-Tenant-ID": tenant_id}
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            resp = await client.get(f"{INGESTION_URL}/ingest/sepenatural/products", headers=headers)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Ingestion Service Error: {str(e)}")


@app.get("/ingestion/production-orders")
async def get_production_orders(tenant_id: str = Depends(get_tenant_id)):
    headers = {"X-Tenant-ID": tenant_id}
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            resp = await client.get(f"{INGESTION_URL}/ingest/production-orders", headers=headers)
            resp.raise_for_status()
            return resp.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Ingestion Service Error: {str(e)}")


@app.get("/analyze/full/{order_id}")
async def full_analysis(order_id: str, tenant_id: str = Depends(get_tenant_id)):
    """
    Orchestrates the full SAP PP Analysis Pipeline.
    Steps 3 (Brain Analysis) and 4 (RAG) run in parallel for performance.
    """
    headers = {"X-Tenant-ID": tenant_id}
    logger.info(f"Processing Order {order_id} for Tenant: {tenant_id}")

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        # Step 1: Ingest
        try:
            ingest_resp = await client.get(f"{INGESTION_URL}/ingest/production-orders", headers=headers)
            ingest_resp.raise_for_status()
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Ingestion Service Error: {str(e)}")

        all_orders = ingest_resp.json()
        raw_order = next((o for o in all_orders if o["Aufnr"] == order_id), None)
        if not raw_order:
            raise HTTPException(status_code=404, detail="Order not found in SAP (Mock)")

        # Step 2: Semantic Map
        try:
            map_resp = await client.post(f"{SEMANTIC_URL}/semantic/map/order", json=raw_order, headers=headers)
            map_resp.raise_for_status()
            domain_order = map_resp.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Semantic Layer Error: {str(e)}")

        # Steps 3 & 4: Brain Analysis + RAG — parallel
        rag_payload = {"query": "Are there any material shortages or risks?", "context": domain_order}

        async def call_brain():
            try:
                r = await client.post(f"{BRAIN_URL}/brain/analyze/order", json=domain_order, headers=headers)
                r.raise_for_status()
                return r.json()
            except Exception as e:
                raise HTTPException(status_code=502, detail=f"Brain Service Error: {str(e)}")

        async def call_rag():
            try:
                r = await client.post(f"{BRAIN_URL}/brain/rag/analyze", json=rag_payload, headers=headers)
                if r.status_code == 200:
                    return r.json().get("response")
                return "RAG Service Unavailable"
            except Exception as e:
                return f"RAG Error: {str(e)}"

        analysis_result, rag_result = await asyncio.gather(call_brain(), call_rag())

        return {
            "tenant_id": tenant_id,
            "order_id": order_id,
            "status": "Success",
            "pipeline_trace": ["Ingestion", "Semantic Mapping", "Brain Analysis + RAG (parallel)"],
            "raw_data_summary": f"SystemStatus: {raw_order.get('SystemStatus')}",
            "semantic_data": domain_order,
            "core_analysis": analysis_result.get("analysis"),
            "rag_insight": rag_result,
        }


@app.post("/brain/analyze/order")
async def proxy_analyze_order(order_data: dict, tenant_id: str = Depends(get_tenant_id)):
    headers = {"X-Tenant-ID": tenant_id}
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            resp = await client.post(f"{BRAIN_URL}/brain/analyze/order", json=order_data, headers=headers)
            resp.raise_for_status()
            return resp.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Brain Service Error: {str(e)}")


@app.post("/brain/rag/analyze")
async def proxy_rag_analyze(
    payload: dict,
    tenant_id: str = Depends(get_tenant_id),
    x_google_api_key: Optional[str] = Header(None),
):
    headers = {"X-Tenant-ID": tenant_id, "x-google-api-key": x_google_api_key or ""}
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            resp = await client.post(f"{BRAIN_URL}/brain/rag/analyze", json=payload, headers=headers)
            resp.raise_for_status()
            return resp.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Brain Service Error: {str(e)}")
