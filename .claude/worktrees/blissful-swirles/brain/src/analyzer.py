from typing import Dict, Any

class SAPAnalyzer:
    """
    The Intelligence Core.
    Analyzes Domain objects to find anomalies, shortages, or schedule risks.
    """
    
    def analyze_order(self, order_data: Dict[str, Any]) -> str:
        """
        Basic Sprint 1 Analysis: Check status and quantity.
        """
        insights = []
        
        # 1. Parse Data
        order_id = order_data.get("order_id")
        status = order_data.get("status_string", "")
        qty = order_data.get("target_quantity", 0)
        
        # 2. Logic: Material Shortage
        if "MSCP" in status:
            insights.append(f"CRITICAL: Order {order_id} has a MATERIAL SHORTAGE (MSCP status).")
            
        # 3. Logic: Order Type Check
        if order_data.get("is_process_order"):
            insights.append(f"Info: This is a Process Order. Checking vessel capacity... (Mock)")
        else:
            insights.append(f"Info: This is a Discrete Production Order.")
            
        # 4. Logic: Quantity warning
        if qty > 1000:
            insights.append("Warning: Large order quantity detected. Check line capacity.")

        # 5. RAG / LLM Simulation
        # In future, we would send `insights` + `order_data` to OpenAI to generate a summary.
        
        return "\n".join(insights)
