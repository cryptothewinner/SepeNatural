import requests
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class ODataConnector:
    """
    Generic OData Connector for fetching SAP data.
    """
    def __init__(self, base_url: str, auth: tuple = None):
        self.base_url = base_url.rstrip('/')
        self.auth = auth

    def get_entity_set(self, entity_set_name: str, filters: str = None, top: int = 100) -> List[Dict]:
        """
        Fetch a list of entities from an OData service.
        """
        url = f"{self.base_url}/{entity_set_name}"
        params = {
            "$format": "json",
            "$top": top
        }
        if filters:
            params["$filter"] = filters

        try:
            logger.info(f"Fetching {entity_set_name} from {url}")
            # In a real scenario, we would make the request:
            # response = requests.get(url, auth=self.auth, params=params)
            # response.raise_for_status()
            # return response.json()['d']['results']
            
            # MOCK IMPLEMENTATION FOR SPRINT 1
            return self._mock_data(entity_set_name)
        except Exception as e:
            logger.error(f"Failed to fetch {entity_set_name}: {e}")
            return []

    def _mock_data(self, entity_name: str) -> List[Dict]:
        """
        Return mock data for testing.
        """
        if entity_name == "ProductionOrder":
            return [
                {
                    "Aufnr": "1000001",
                    "Auart": "PP01", # Standard Discrete Order
                    "Matnr": "MAT-PUMP-001",
                    "Werks": "1000",
                    "Gamng": 10.0, # Quantity
                    "Gmein": "PC",
                    "Gltrp": "/Date(1739318400000)/", # Basic finish date
                    "SystemStatus": "REL MSCP",    # Released, Material shortage
                },
                {
                    "Aufnr": "1000002",
                    "Auart": "PI01", # Process Order
                    "Matnr": "MAT-PAINT-RED",
                    "Werks": "2000",
                    "Gamng": 500.0, 
                    "Gmein": "L",
                    "Gltrp": "/Date(1739404800000)/",
                    "SystemStatus": "CRTD",   # Created
                }
            ]
        elif entity_name == "Material":
            return [
                 {"Matnr": "MAT-PUMP-001", "Maktx": "Industrial Pump X100"},
                 {"Matnr": "MAT-PAINT-RED", "Maktx": "Red Paint Bucket 5L"}
            ]
        return []
