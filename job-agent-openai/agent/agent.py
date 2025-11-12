# agent/agent.py
import os
import asyncio
from dotenv import load_dotenv
from modules.job_api import fetch_live_jobs
from modules.embeddings import rank_jobs_by_query
from modules.skill_gap import analyze_skill_gap

# Gemini SDK
import google.generativeai as genai

# Load Gemini API key
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

    # Step 4: Construct prompt
    prompt = f"Query: {query}\nTop Jobs: {ranked_jobs[:5]}"
    if gaps:
        prompt += f"\nSkill Gaps: {gaps}"

    # Step 5: Call Gemini LLM
    response = await asyncio.to_thread(
        lambda: genai.chat.create(
            model="gemini-1.5",  # use the model you have access to
            messages=[{"author": "user", "content": prompt}],
            temperature=0.5
        )
    )

    return response.last.message["content"]

def run_agent_sync(query: str, resume_text: str = None):
    return asyncio.run(run_agent(query, resume_text))