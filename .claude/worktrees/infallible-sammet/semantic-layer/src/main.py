from fastapi import FastAPI, HTTPException, Header
from typing import Dict, Any, Optional
from .mappings.sap_mapper import SAPMapper
from .models.domain import ProductionOrder

app = FastAPI(title="Antigravity Semantic Layer Service")

@app.get("/")
def read_root():
    return {"service": "semantic-layer", "status": "active"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/semantic/map/order", response_model=ProductionOrder)
def map_order(raw_data: Dict[str, Any], x_tenant_id: Optional[str] = Header(None)):
    """
    Maps a raw SAP Order dict to the Domain Model.
    """
    tenant_id = x_tenant_id or "default_tenant"
    # Logger could use tenant_id here
    try:
        domain_obj = SAPMapper.map_production_order(raw_data)
        # If tenant-specific mapping rules existed, we'd use tenant_id here
        return domain_obj
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

