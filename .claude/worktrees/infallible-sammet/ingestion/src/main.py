from fastapi import FastAPI, HTTPException
from .connectors.odata import ODataConnector

app = FastAPI(title="Antigravity Ingestion Service")

# Initialize Connector (Mock URL)
connector = ODataConnector(base_url="https://mock.sap.corp/odata")

@app.get("/")
def read_root():
    return {"service": "ingestion", "status": "active"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/ingest/production-orders")
def get_production_orders():
    """
    Fetches raw production orders from SAP (Mock).
    """
    data = connector.get_entity_set("ProductionOrder")
    if not data:
        raise HTTPException(status_code=404, detail="No orders found")
    return data

