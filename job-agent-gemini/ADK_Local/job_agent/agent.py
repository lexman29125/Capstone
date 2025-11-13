from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from typing import Dict, Any

# Define the model to be used by the agent.
# Assumes GEMINI_API_KEY is set in the environment (.env file).
model = LiteLlm("gemini-2.5-flash")

# --- Tool Definitions (Standard Python Functions) ---

def job_search(query: str, location: str) -> Dict[str, Any]:
    """
    Searches the mock job database for relevant job postings.
    Returns a dictionary with a list of matching job IDs and titles. Use this FIRST for finding jobs.
    """
    if "senior software engineer" in query.lower() and "london" in location.lower():
        return {
            "status": "success",
            "jobs": [
                {"id": 101, "title": "Senior S/W Eng, TechCorp"},
                {"id": 102, "title": "Lead Dev, Global Systems"}
            ],
            "message": "Found 2 matching senior roles in London. Please ask the user which ID to apply for."
        }
    else:
        return {"status": "success", "jobs": [], "message": f"Found 1 general job matching '{query}' in {location}: JobID 99."}

def submit_application(job_id: int, user_id: str) -> Dict[str, Any]:
    """
    Submits the application for the specified job ID using the candidate's profile.
    This simulates the Candidate Agent's final action. ONLY call this after a job_id is known.
    """
    if job_id in [101, 102]:
        return {"status": "submitted", "message": f"Application for JobID {job_id} submitted successfully for candidate {user_id}. A proactive follow-up reminder has been set."}
    else:
        return {"status": "error", "message": f"JobID {job_id} not found or application failed."}

# --- Coordinator Agent Definition ---

root_agent = Agent(
    model=model,
    name="JobChatbotCoordinator",
    description="An expert coordinator for job search and application.",
    instruction=(
        "You are the **Job Chatbot Coordinator Agent**. Your goal is to fulfill complex user requests "
        "by intelligently calling the appropriate tools. Analyze the user request, plan the necessary steps "
        "(Search, Apply), and use the output from the tools to provide a final, helpful response. "
        "The user ID is always 'User_A'. Always use the tools when appropriate."
    ),
    # ADK automatically converts these functions into callable tools:
    tools=[job_search, submit_application] 
)