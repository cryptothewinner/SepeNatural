from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict
from datetime import datetime

class ProductionOrder(BaseModel):
    """
    Canonical Domain Model for a Production Order (Discrete or Process).
    Combines fields from AUFK, AFKO.
    """
    order_id: str = Field(..., description="SAP Order Number (AUFNR)")
    order_type: str = Field(..., description="Order Type (AUART) e.g., PP01, PI01")
    material_id: str = Field(..., description="Material Number (MATNR)")
    plant: str = Field(..., description="Plant (WERKS)")
    
    target_quantity: float = Field(..., description="Total Order Quantity (GAMNG)")
    uom: str = Field(..., description="Unit of Measure (GMEIN)")
    
    basic_finish_date: Optional[datetime] = Field(None, description="Basic Finish Date (GLTRP)")
    
    status_string: str = Field(..., description="Raw Status String (JEST/System Status)")
    
    # Computed / Semantic Fields
    is_process_order: bool = Field(False, description="True if Process Industry Order")
    has_shortage: bool = Field(False, description="Derived from status MSCP")

class Material(BaseModel):
    """
    Canonical Domain Model for Material (MARC/MARA).
    """
    material_id: str
    description: str

class Ingredient(BaseModel):
    """
    Canonical Domain Model for a Product Ingredient.
    """
    name: str
    amount: Optional[float] = None
    unit: Optional[str] = None
    percentage: Optional[str] = None
    raw_text: Optional[str] = None

class Product(BaseModel):
    """
    Canonical Domain Model for a finished product (from Scraper or SAP).
    """
    sku: str
    name: str
    barcode: Optional[str] = None
    price: Optional[float] = None
    currency: str = "TRY"
    categories: List[str] = []
    attributes: Dict[str, str] = {}
    ingredients: List[Ingredient] = []
    
    usage_text: Optional[str] = None
    warnings_text: Optional[str] = None
    storage_text: Optional[str] = None
    description_html: Optional[str] = None
    url: Optional[str] = None
    source: Literal["scraper", "sap"] = "scraper"
