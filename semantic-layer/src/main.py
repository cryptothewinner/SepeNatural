from fastapi import FastAPI, HTTPException, Header
from typing import Dict, Any, Optional, List
from .mappings.sap_mapper import SAPMapper
from .mappings.sepenatural_mapper import SepenaturalMapper
from .models.domain import ProductionOrder, Product

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
    try:
        domain_obj = SAPMapper.map_production_order(raw_data)
        return domain_obj
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/semantic/map/sepenatural/products", response_model=List[Product])
def map_sepenatural_products(raw_data: List[Dict[str, Any]], x_tenant_id: Optional[str] = Header(None)):
    """
    Maps a list of raw Sepenatural product dicts to standard Product models.
    """
    try:
        domain_products = SepenaturalMapper.map_list(raw_data)
        return domain_products
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Mapping Error: {str(e)}")

