import os
import asyncio
from dotenv import load_dotenv
from modules.job_api import fetch_live_jobs
from modules.embeddings import rank_jobs_by_query
from modules.skill_gap import analyze_skill_gap
import google.generativeai as genai

# Load Gemini API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def run_agent(query: str, resume_text: str = None):
    # Step 1: Fetch jobs
    jobs = await asyncio.to_thread(fetch_live_jobs)

    # Step 2: Rank jobs by relevance to query
    ranked_jobs = await asyncio.to_thread(rank_jobs_by_query, query, jobs)

    # Step 3: Analyze skill gaps if resume is provided
    gaps = None
    if resume_text:
        gaps = await asyncio.to_thread(analyze_skill_gap, resume_text, ranked_jobs)

    # Step 4: Construct prompt for LLM
    prompt = f"Query: {query}\nTop Jobs: {ranked_jobs[:5]}"
    if gaps:
        prompt += f"\nSkill Gaps: {gaps}"

    # Step 5: Call Gemini LLM via ChatSession
    def call_gemini(prompt_text):
        from google.generativeai import ChatSession, get_model
        model_obj = get_model("gemini-1.5")  # fetch the model object
        session = ChatSession(model=model_obj)
        response = session.send_message(prompt_text)
        return response.last if response else "No response from LLM"

    response_text = await asyncio.to_thread(call_gemini, prompt)
    return response_text

def run_agent_sync(query: str, resume_text: str = None):
    """Synchronous wrapper for Streamlit"""
    return asyncio.run(run_agent(query, resume_text))