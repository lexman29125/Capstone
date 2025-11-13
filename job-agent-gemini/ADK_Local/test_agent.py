import os
import sys
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

# --- CRITICAL ASSUMPTION ---
# We must import the Query object to run the agent.
# Based on previous failures, we assume this is the most likely simple path.
try:
    from google.adk.messages import Query
except ImportError as e:
    # If this fails, the ADK installation is likely broken or the path is unknown.
    print(f"\nCRITICAL IMPORT FAILURE: Could not import Query object.")
    print(f"Error: {e}")
    print("\nAction Required: Please try running 'pip uninstall google-adk -y' followed by 'pip install google-adk'.")
    sys.exit(1)

# Load environment variables (for API keys, etc.)
load_dotenv()

# Load the agent entry point
try:
    from job_agent.agent import root_agent
except ImportError:
    print("\nCRITICAL: Failed to import root_agent. Ensure 'agent.py' is inside a 'job_agent' folder.")
    sys.exit(1)

def run_test_query(prompt: str):
    """Initializes the runner and executes a single query against the agent."""
    print(f"\n--- Running ADK Agent Functional Test ---")
    print(f"User Query: '{prompt}'")
    
    # Initialize Runner
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="job_chatbot_test_app",
        session_service=session_service
    )
    
    # Define session parameters
    user_id = "Test_User"
    session_id = "Test_Session"

    try:
        # Create the Query object
        query_object = Query(
            user_id=user_id,
            session_id=session_id,
            text=prompt
        )

        # Run the agent synchronously using the Query object
        print("Executing runner.run(query_object)...")
        response_event = runner.run(query_object)

        # Extract and display the response
        final_response = response_event.final_response.text_response
        print("\nAGENT EXECUTION SUCCESSFUL.")
        print("\n--- AGENT RESPONSE ---")
        print(final_response)
        print("------------------------")

    except Exception as e:
        print(f"\nAN EXECUTION ERROR OCCURRED: {e}")
        print("This error is related to the agent's logic (e.g., tool execution, API key, model failure), NOT the frontend.")

# --- Execute Test ---
test_prompt = "I need a Senior Software Engineer job in London. Can you apply for Job ID 101?"
run_test_query(test_prompt)