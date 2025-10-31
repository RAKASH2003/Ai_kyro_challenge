import os
import traceback
import asyncio
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# --- Load environment variables ---
import google.generativeai as genai

load_dotenv()
# NOTE: Replace the environment variable lookup with your actual API key handling
# if not using a .env file.
# We configure the SDK here to ensure any tools that use it (like Google Search) are initialized.
genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) 

# --- ADK Imports ---
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types

# --- Import your integrated router agent ---
# Make sure to replace 'my_agent.agent' with the correct path to your agent definition file
from my_agent.agent import root_agent 

# --- Initialize session and runner ---
APP_NAME = "MultiAgentApp"
# Using a fixed USER_ID and session_id for simplicity, but in a real app, 
# USER_ID should come from authentication and SESSION_ID from the client.
USER_ID = "web_user" 
session_service = InMemorySessionService()

manager_runner = Runner(
    agent=root_agent,
    session_service=session_service,
    app_name=APP_NAME
)

# --- GLOBAL SESSION TRACKER (NEW) ---
# Use a global flag to ensure the session is created only once.
session_initialized = False

# --- Flask setup ---
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
async def ask_agent():
    data = request.get_json()
    query = data.get("query", "").strip()
    
    # We need to declare the flag as global to modify it within the function
    global session_initialized 

    if not query:
        return jsonify({"answer": "Please enter a valid question."}), 400

    # The session_id remains constant, allowing the conversation history to persist.
    session_id = "main_session" 
    full_response = ""

    try:
        # --- MODIFIED SESSION CREATION LOGIC ---
        # Only create the session if this is the very first request since the server started.
        if not session_initialized:
            print(f"DEBUG: Session '{session_id}' not initialized. Creating session now for the first time.")
            await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)
            session_initialized = True
        # --- END MODIFIED LOGIC ---

        # Send query to router
        content = types.Content(role="user", parts=[types.Part(text=query)])
        async for event in manager_runner.run_async(
            user_id=USER_ID,
            session_id=session_id,
            new_message=content
        ):
            if event.content and hasattr(event.content, "parts"):
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        full_response += part.text

            if hasattr(event, "is_final_response") and event.is_final_response():
                break

        return jsonify({"answer": full_response})

    except Exception as e:
        # We catch the exception again here in case the race condition fix failed 
        # but provide a better traceback in the console.
        traceback.print_exc()
        return jsonify({"answer": f"Error: {type(e).__name__} - {str(e)}"}), 500


if __name__ == "__main__":
    
    app.run(debug=True, port=5000)
