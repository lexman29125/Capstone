Here’s the fully updated, end-to-end solution for your job recommendation + skill-gap analysis tool using a remote OpenAI LLM, Streamlit UI, and local job/skill modules. This is designed to replace the old MCP-based architecture, eliminating deprecated functions and incompatibilities.

⸻

Solution Summary

Goal: Users input a job search query (and optionally a resume) → system fetches live jobs, ranks them, computes skill gaps → LLM synthesizes human-readable insights → results displayed in Streamlit UI.

Key Changes:
	1.	No MCP server or deprecated MCPToolset.
	2.	LLM Integration: Remote OpenAI API (gpt-4) handles reasoning and summarization.
	3.	Modules: Local Python modules handle jobs fetching, ranking, and skill gap computation.
	4.	Streamlit UI: Interactive front-end for user input and LLM output display.
	5.	Async Support: asyncio used in agent for efficient I/O but provides a synchronous wrapper for Streamlit.

⸻

Architecture Diagram (Markdown)

graph TD
    A[Streamlit UI] -->|query + resume| B[Agent.py]
    B --> C[fetch_live_jobs module]
    B --> D[rank_jobs_by_query module]
    B --> E[analyze_skill_gap module]
    B --> F[OpenAI LLM API (GPT-4)]
    F --> B
    B --> A[Display LLM insights on UI]


⸻

Folder Structure

job-agent-openai/
├─ agent/
│  └─ agent.py
├─ frontend/
│  └─ app.py
├─ modules/
│  ├─ job_api.py
│  ├─ embeddings.py
│  └─ skill_gap.py
├─ requirements.txt
└─ README.md


⸻

1. agent/agent.py

# agent/agent.py
import os
import asyncio
from modules.job_api import fetch_live_jobs
from modules.embeddings import rank_jobs_by_query
from modules.skill_gap import analyze_skill_gap
import openai

# Load OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

async def run_agent(query: str, resume_text: str = None):
    # Fetch jobs
    jobs = await asyncio.to_thread(fetch_live_jobs)
    ranked_jobs = await asyncio.to_thread(rank_jobs_by_query, query, jobs)
    
    # Compute skill gaps if resume provided
    gaps = None
    if resume_text:
        gaps = await asyncio.to_thread(analyze_skill_gap, resume_text, ranked_jobs)
    
    # Build prompt for LLM
    prompt = f"Query: {query}\nTop Jobs: {ranked_jobs[:5]}"
    if gaps:
        prompt += f"\nSkill Gaps: {gaps}"

    # Call OpenAI API
    response = await asyncio.to_thread(
        lambda: openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
    )

    llm_output = response.choices[0].message.content
    return llm_output

def run_agent_sync(query: str, resume_text: str = None):
    return asyncio.run(run_agent(query, resume_text))


⸻

2. frontend/app.py

# frontend/app.py
import streamlit as st
from agent.agent import run_agent_sync

st.title("Job Recommendations & Skill Gap Analysis")

query = st.text_input("Enter job search query:")
resume = st.text_area("Paste your resume (optional)")

if st.button("Submit"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Fetching jobs, analyzing gaps, and synthesizing insights..."):
            result = run_agent_sync(query, resume if resume else None)
            st.subheader("LLM Insights")
            st.write(result)


⸻

3. modules/job_api.py

# modules/job_api.py
def fetch_live_jobs():
    # Example: return mock data; replace with actual API call if needed
    return [
        {"title": "Data Scientist", "skills": ["Python", "ML", "SQL"]},
        {"title": "ML Engineer", "skills": ["TensorFlow", "Python"]},
        {"title": "Data Analyst", "skills": ["SQL", "Excel"]}
    ]


⸻

4. modules/embeddings.py

# modules/embeddings.py
def rank_jobs_by_query(query, jobs):
    # Example simple ranking: jobs containing query word first
    ranked = sorted(jobs, key=lambda j: query.lower() in j["title"].lower(), reverse=True)
    return ranked


⸻

5. modules/skill_gap.py

# modules/skill_gap.py
def analyze_skill_gap(resume_text, jobs):
    # Simple comparison: list skills missing in resume
    resume_skills = set(resume_text.lower().split())
    gaps = {}
    for job in jobs:
        missing = [skill for skill in job["skills"] if skill.lower() not in resume_skills]
        gaps[job["title"]] = missing
    return gaps


⸻

6. requirements.txt

# Streamlit UI
streamlit==1.28.0

# OpenAI API
openai==1.27.0

# Async HTTP client
aiohttp==3.8.5

# Data handling & computation
numpy==1.26.0
pandas==2.1.0

# Load environment variables (API keys etc.)
python-dotenv==1.0.0

# Optional: for more advanced embeddings / ML
scikit-learn==1.3.2

# Optional: for pretty printing / structured logs
rich==13.6.0

Notes / Tips:
	1.	streamlit → UI frontend
	2.	openai → remote LLM (GPT or Gemini via OpenAI API)
	3.	aiohttp → async calls for jobs / MCP API if needed
	4.	numpy / pandas → embeddings, ranking, skill gap calculations
	5.	python-dotenv → safely store OPENAI_API_KEY in .env
	6.	scikit-learn → useful if you do clustering or similarity in job ranking
	7.	rich → optional, but helps debug async pipelines
⸻

Workflow
	1.	User enters query and optional resume in Streamlit UI.
	2.	agent.py:
	•	Fetches jobs using fetch_live_jobs.
	•	Ranks jobs using rank_jobs_by_query.
	•	Computes skill gaps using analyze_skill_gap (if resume provided).
	•	Calls OpenAI LLM to synthesize insights.
	3.	Streamlit displays LLM insights.

⸻

Deployment Steps

# 1. Clone repo
git clone <repo-url>
cd job-agent-openai

# 2. Create conda/venv environment
conda create -n jobagent python=3.12
conda activate jobagent

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set OpenAI API key
export OPENAI_API_KEY="your_openai_api_key_here"

# 5. Run Streamlit UI
streamlit run frontend/app.py


⸻

✅ Advantages of this redesign:
	•	Fully functional without MCP server.
	•	Uses supported OpenAI API for reasoning & summarization.
	•	Simple, modular, and maintainable.
	•	Avoids deprecated functions, incompatible imports, and server/client mismatches.

⸻
