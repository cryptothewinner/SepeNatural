from fastapi import FastAPI, HTTPException
from .connectors.odata import ODataConnector
from .connectors.sqlite import SQLiteConnector
import os

app = FastAPI(title="Antigravity Ingestion Service")

# Initialize Connectors
connector = ODataConnector(base_url="https://mock.sap.corp/odata")

# SQLite db path (mapped via Docker volume)
DB_PATH = os.getenv("SEPENATURAL_DB_PATH", "/app/data/sepenatural.db")
sqlite_connector = SQLiteConnector(db_path=DB_PATH)

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

@app.get("/ingest/sepenatural/products")
def get_sepenatural_products():
    """
    Fetches raw products from Sepenatural SQLite DB.
    """
    data = sqlite_connector.get_all_products()
    if not data:
        raise HTTPException(status_code=404, detail="No products found in Sepenatural DB")
    return data

