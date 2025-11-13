import os
from langchain_google_genai import ChatGoogleGenerativeAI
# FIX 1: New paths for modular LangChain components
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.prompts.chat import MessagesPlaceholder 
# FIX: Using the standard, top-level import for Agent components
from langchain_core.agents import AgentExecutor
from langchain.agents import create_tool_calling_agent
from langchain_core.tools import tool 
from dotenv import load_dotenv

# Load environment variables from .env or Streamlit secrets
load_dotenv()

# --- Tool Definitions (Simulating Agent Actions) ---
# These mock the Job Search Agent and Candidate Agent functionality

@tool
def job_search(query: str, location: str) -> str:
    """
    Searches the mock job database for relevant job postings.
    Returns a list of matching job IDs and titles. Use this FIRST for finding jobs.
    """
    if "senior software engineer" in query.lower() and "london" in location.lower():
        return "Found 3 jobs: JobID 101 (Senior S/W Eng, TechCorp); JobID 102 (Lead Dev, Global Systems); JobID 103 (Architect, London Startups). Ask the user which JobID to apply for."
    elif "marketing" in query.lower():
        return "Found 2 jobs: JobID 201 (Marketing Manager, Remote); JobID 202 (SEO Specialist, UK)."
    else:
        return f"Found 1 general job matching '{query}' in {location}: JobID 99 (General Position)."

@tool
def submit_application(job_id: int, user_id: str) -> str:
    """
    Submits the application for the specified job ID using the candidate's profile.
    This simulates the Candidate Agent's final action. ONLY call this after a job_id is known.
    """
    return f"Application for JobID {job_id} submitted successfully for candidate {user_id}. A proactive follow-up reminder has been set for status updates."

@tool
def check_chat_history_for_context(user_id: str) -> str:
    """
    Retrieves the user's past interaction context to personalize the response or action.
    Use this to retrieve memory or preferences. The user ID is always 'User_A'.
    """
    return f"Retrieved context for {user_id}: Candidate prefers hybrid work, is willing to relocate, and previously applied to a role at TechCorp 2 weeks ago."

# Create a list of all available tools
available_tools = [job_search, submit_application, check_chat_history_for_context]

# --- Coordinator Agent Initialization ---

def get_agent_executor():
    """Initializes and returns the LangChain AgentExecutor (the Coordinator Agent)."""
    
    # 1. Initialize the Gemini Model (Pulls GEMINI_API_KEY from environment)
    # Use gemini-2.5-flash for its speed and strong function calling capabilities
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    except Exception as e:
        # Note: In a real deployment, you should ensure the API key is passed securely
        return f"Error initializing LLM: {e}. Please ensure GEMINI_API_KEY is set correctly."
    
    # 2. Define the System Prompt for the Coordinator Agent
    system_prompt = (
        "You are the powerful **Job Chatbot Coordinator Agent**. "
        "Your goal is to fulfill complex user requests by calling the appropriate tools. "
        "Analyze the user request, plan the necessary steps (Search, Context Check, Apply), "
        "and use the output from the tools to provide a final, helpful response. "
        "The user ID is always 'User_A'. Always use the tools when appropriate."
    )

    # 3. Create the Prompt Template
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            # Use MessagesPlaceholder for chat history (list of BaseMessages)
            MessagesPlaceholder(variable_name="chat_history"), 
            ("human", "{input}"),
            # Use MessagesPlaceholder for agent's internal thought/action sequence
            MessagesPlaceholder(variable_name="agent_scratchpad"), 
        ]
    )

    # 4. Create the Tool Calling Agent and Executor
    agent = create_tool_calling_agent(llm, available_tools, prompt)
    
    # Note: verbose=True prints the Thought/Action/Observation to the terminal
    agent_executor = AgentExecutor(agent=agent, tools=available_tools, verbose=True)
    
    return agent_executor