from google.adk.agents import LlmAgent # **CRUCIAL FIX #1: Use LlmAgent**
import requests # <--- YOU MUST ADD THIS IMPORT AT THE TOP OF YOUR agent.py
from bs4 import BeautifulSoup # <--- OPTIONAL: For cleaning content
from google.adk.tools import AgentTool

# Define the constant for the required FAQ link.
NUGENOMICS_FAQ_URL = "https://www.nugenomics.in/faqs/" 

# --- A. Define the Final Output Tool (Kept from before) ---
def finalize_response(final_answer: str) -> str:
    """Signals the final answer is ready."""
    return  final_answer

# --- B. Define the Constrained Browsing Tool ---
# You are defining a tool that the LLM will see as 'browse_nugenomics_faq'
# and the function should execute the implicit ADK browsing capability.

def browse_nugenomics_faq(query: str) -> str:
    """
    Retrieves and cleans the content from the NuGenomics FAQ page.
    """
    try:
        # Use the fixed, constrained URL
        response = requests.get(NUGENOMICS_FAQ_URL, timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        
        soup = BeautifulSoup(response.content, 'html.parser')
        # This attempts to get all body text, which the LLM will then summarize
        content = soup.get_text(separator=' ', strip=True) 

        # Return the raw content for the LLM to process
        return content

    except requests.exceptions.RequestException as e:
        return f"Error retrieving FAQ content: {e}. Cannot answer the query."

# --- 2. Define the Agent as 'root_agent' ---
customer_support_agent = LlmAgent( # **MUST use LlmAgent**
    name="my_agent",
    model="gemini-2.0-flash",
    description=(
        "Customer Support Agent: This agent answers queries exclusively related to "
        "NuGenomics using the provided FAQ link."
    ),
    instruction=(
       f"You are a helpful, highly specialized, and strictly professional Customer Support Agent for NuGenomics. "
        f"Your SOLE purpose is to answer questions based on the official FAQ page. "
        f"The ONLY source of truth is: {NUGENOMICS_FAQ_URL}. "
        
        "***CRITICAL RULE:*** For any query related to NuGenomics facts, you MUST call the **browse_nugenomics_faq** tool to find the answer. "
        
        "***GUARDRAIL:*** If the user asks for anything outside of this, you MUST professionally decline. "
        
        "***FINAL STEP:*** For *ANY* response to the user, you MUST call the **finalize_response** tool. "
        
        "***SUGGESTIONS RULE:*** When providing a **factual answer** (i.e., when you have used the **browse_nugenomics_faq** tool), you **MUST** ensure the `final_answer` parameter includes the main answer **followed by** 1-2 highly relevant, concise follow-up questions formatted clearly for the user (e.g., 'Suggested next questions:'). "
        "For simple greetings or non-factual responses, provide a standard, concise reply and **do NOT** include follow-up questions."
        "Do NOT output code blocks or text directly."
    ),
    tools=[finalize_response, browse_nugenomics_faq], # **Add the new tool**
)

customer_support_tool=AgentTool(agent=customer_support_agent)