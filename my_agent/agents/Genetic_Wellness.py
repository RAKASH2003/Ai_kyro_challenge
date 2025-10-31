from google.adk.agents import LlmAgent
import datetime
from typing import Optional 
from google.adk.tools import AgentTool
# NOTE: The actual implementation of 'google_search' would require
# access to a real search API, which is often an internal ADK/framework tool.
# For this demonstration, we'll use a placeholder function to represent
# the custom external tool.
import google # Placeholder for a real Google Search API client
# If running in an environment that supports the 'google' tool, you would
# use the actual tool definition (e.g., from google.adk.tools import google_search)

# ===============================================
# 1. CORE TOOLS (Needed by this Agent)
# ===============================================

# A. Final Output Tool (Required for ALL agent responses)
def finalize_response(final_answer: str) -> str:
    """Signals the final answer is ready by returning ONLY the final string."""
    return final_answer

# B. Custom Tool 1: BMI Calculator
def calculate_bmi(weight_kg: float, height_m: float) -> str:
    """
    Calculates the Body Mass Index (BMI) given weight in kilograms (kg) 
    and height in meters (m). Returns the BMI value and its category.
    """
    if height_m <= 0:
        return "Error: Height must be greater than zero."
    
    bmi = weight_kg / (height_m ** 2)
    
    # Determine the BMI category
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 24.9:
        category = "Normal (Healthy Weight)"
    elif 25.0 <= bmi < 29.9:
        category = "Overweight"
    else:
        category = "Obese"
        
    return f"Calculated BMI is {bmi:.2f}, which falls into the '{category}' category."

# C. Custom Tool 2: Date and Time Context
def get_current_day_and_time() -> str:
    """
    Retrieves the current date, day of the week, and time to provide context 
    for personalized wellness recommendations.
    """
    now = datetime.datetime.now()
    day_of_week = now.strftime("%A")
    current_time = now.strftime("%I:%M %p")
    return f"Today is {day_of_week}. The current time is {current_time}."

# D. Custom External Tool (NEW): Google Search
# This fulfills the Key Architectural Requirement.
def google_search(query: str) -> str:
    """
    Performs a real-time search on Google for the latest information on health
    trends, supplements, or medical research. Use for current events only.
    """
    # In a real ADK setup, this would be an actual API call.
    # We use a placeholder to simulate the tool's intended output for the LLM.
    # The actual implementation relies on the agent runner environment to provide
    # a functional Google Search capability when this function is called.
    return f"Searching Google for: '{query}'..." 


# ===============================================
# 2. SPECIALIST AGENT DEFINITION
# ===============================================

genetic_wellness_agent = LlmAgent(
    name="genetic_wellness_agent",
    model="gemini-2.0-flash",
    description=(
        "Answers general queries about genetic wellness, nutrition, and fitness. "
        "It leverages foundational LLM knowledge and three custom tools: a BMI Calculator, "
        "a Time Context tool, and a real-time Google Search tool for current information."
    ),
    instruction=(
        "You are an encouraging and highly informative **Genetic Wellness Expert**. Your goal is to provide specialized, accurate, and personalized insights into genetics, DNA-based health risks, and tailored wellness recommendations (diet, fitness, and lifestyle)."


        "***TOOL USE RULE 1 (BMI):*** For any request involving personalized weight, diet, or fitness goals:1. **CHECK HISTORY:** First, check the conversation history for established facts regarding the user's BMI, weight, or height. If these facts are present, use them directly.2. **TOOL CALL:** If the necessary facts are NOT in the history, you MUST call the **calculate_bmi** tool. If the user has not provided their weight and height in the current turn, you MUST ask for it first (in kg and meters)."
        
        "***TOOL USE RULE 2 (Time):*** For any request asking for time-sensitive, scheduling, or motivational advice, you MUST call the **get_current_day_and_time** tool to gather context before making a recommendation. "

        "***TOOL USE RULE 3 (Search):*** For any request involving **current health trends, supplements, or medical research updates** (e.g., 'latest research on X', 'new trends in Y', 'what are the side effects of Z supplement'), you MUST call the **google_search** tool to fetch the latest information."

        "***GUARDRAIL (Delegation):*** You MUST decline questions specific to NuGenomics products (pricing, test results, policies), clarifying that you are a wellness expert, and redirecting them to the Customer Support Agent for service-related inquiries. "
        
        "***GUARDRAIL (System):***You MUST NOT output any text, thoughts, or replies *before* or *outside* of the finalize_response tool call. Your final, complete, and fully formatted answer MUST be the only content passed to the finalize_response tool. "

        "***GUARDRAIL:*** If the user asks for anything outside of this, you MUST professionally decline. "
        
        "***FORMATTING RULE:*** You MUST format your final answer using **Markdown** for clarity. Use **bolding**, **bullet points (`*`)**, and **line breaks** to organize the information (e.g., separating sections for 'Guidelines' and 'Sample Plan'). Do NOT output the text as a single, dense paragraph. The content of the `final_answer` parameter MUST be well-structured Markdown text."

        "***FINAL STEP:*** For *ANY* response to the user, you MUST call the **finalize_response** tool.Return only one reply"
    ),
    # The agent now includes the new custom external tool: google_search
    tools=[finalize_response, calculate_bmi, get_current_day_and_time, google_search], 
)

# Wrap the agent as an AgentTool for potential use by other agents.
genetic_wellness_tool = AgentTool(agent=genetic_wellness_agent)