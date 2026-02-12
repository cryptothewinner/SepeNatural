from datetime import datetime
from typing import Dict, Any
import re
from ..models.domain import ProductionOrder

class SAPMapper:
    """
    Transforms raw SAP OData dictionaries into clean Domain Objects.
    """
    
    @staticmethod
    def map_production_order(raw_data: Dict[str, Any]) -> ProductionOrder:
        # 1. Date Conversion: /Date(1739318400000)/ -> datetime
        finish_date = None
        raw_date = raw_data.get("Gltrp")
        if raw_date and "/Date(" in raw_date:
            timestamp = int(re.search(r'\d+', raw_date).group()) / 1000
            finish_date = datetime.fromtimestamp(timestamp)

        # 2. Status Analysis
        status_str = raw_data.get("SystemStatus", "")
        
        # 3. Type Logic
        order_type = raw_data.get("Auart")
        is_process = order_type in ["PI01", "PI02"] # Simple rule
        
        return ProductionOrder(
            order_id=raw_data.get("Aufnr"),
            order_type=order_type,
            material_id=raw_data.get("Matnr"),
            plant=raw_data.get("Werks"),
            target_quantity=float(raw_data.get("Gamng", 0.0)),
            uom=raw_data.get("Gmein"),
            basic_finish_date=finish_date,
            status_string=status_str,
            is_process_order=is_process,
            has_shortage=("MSCP" in status_str)
        )
