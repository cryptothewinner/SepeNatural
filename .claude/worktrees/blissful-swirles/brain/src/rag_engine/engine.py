import os
import google.generativeai as genai
from typing import List, Dict, Optional
from ..data.mock_sap_data import retrieve_relevant_data
import logging

logger = logging.getLogger(__name__)

class RAGEngine:
    """
    Retrieval-Augmented Generation Engine using Google Gemini Pro.
    """
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            logger.warning("GOOGLE_API_KEY not found. RAG will fail if called.")
            self.model = None

    def analyze_with_context(self, query: str, context_data: Dict, tenant_id: str = "default_tenant", api_key: Optional[str] = None) -> str:
        """
        1. Retrieve relevant data from Mock SAP Data (Mirror).
        2. Construct Prompt.
        3. Call Gemini.
        """
        # Configure Key (Dynamic Override or Env Fallback)
        details_api_key = api_key or self.api_key
        
        if not details_api_key:
            return "⚠️ Google API Key is missing. Please enter it in the AI Center or configure it in settings."
            
        try:
            genai.configure(api_key=details_api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        except Exception as e:
            return f"⚠️ API Key Error: {str(e)}"


        # 1. Retrieve Context (Hybrid: Mock Data + Vector DB if needed)
        # For this phase, we rely heavily on the Mock Data Mirror
        relevant_sap_data = retrieve_relevant_data(query)
        
        # 2. Construct Prompt
        prompt = f"""
        Role: You are an expert SAP Consultant for a Production Planning (PP) module.
        Task: Analyze the provided SAP data to answer the user's question.
        
        User Context:
        - Query: "{query}"
        - Tenant: {tenant_id}
        
        Available SAP Data (JSON):
        {relevant_sap_data}
        
        Instructions:
        - Analyze the data specifically to answer the query.
        - If the answer is found in the data, provide a clear, concise summary.
        - If the data suggests a problem (e.g., low stock, production delay), highlight it.
        - Format the response in Markdown (use bullet points, bold text).
        - If the answer is NOT in the data, state that clearly.
        
        Answer:
        """
        
        try:
            # 3. Call Gemini
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API Error: {e}")
            return f"Error analyzing data: {str(e)}"

    def _mock_llm_response(self, query, context, docs):
        # Deprecated
        return "Legacy Mock Response"
