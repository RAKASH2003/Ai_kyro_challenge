from google.adk.agents import LlmAgent

# --- 1. IMPORT SPECIALIST AGENTS ---
# Assumes 'agents' folder with __init__.py exporting these agent tools
from .agents import customer_support_tool
from .agents import genetic_wellness_tool




# --- 2. DEFINE THE ROUTER AGENT ---
router_agent = LlmAgent(
    name="router_agent",
    model="gemini-2.0-flash",
    description=(
        "The primary agent that receives all user input and delegates the query "
        "to the Customer Support Agent for NuGenomics topics, or the Genetic Wellness Agent "
        "for general health and wellness topics."
    ),
    instruction=(
        "You are the main conversational router. Your SOLE purpose is to route the user's request to one of the agents.And specify your function when greeted when giving a reply along with result from another agent,start the agent response in newline"

        "give which agent served the request"
        
"**Prioritize routing to the First Agent if the user query contains high-value, specific terms such as 'Genetic test', 'Blood report', '70+ parameters', '3-month plan', 'Reschedule', 'Counselling session', '.**"



),
    tools=[customer_support_tool, genetic_wellness_tool],
)

# --- 3. SET THE ROOT AGENT ---
# This line is crucial: the ADK environment looks for this variable to know which agent to start the conversation with.
root_agent = router_agent

