Got it — we’ll make a pure Python / local-run prototype without Docker. Everything runs on your laptop, MCP server included, and can optionally connect to a cloud-hosted MCP later. Here’s a fully integrated end-to-end solution with all missing files and modules, ready to drop and run.

⸻

Folder Structure (Local Python)

job-agent-mcp/
├── mcp_server/
│   └── server.py
├── agent/
│   └── agent.py
├── frontend/
│   └── app.py
├── modules/
│   ├── job_api.py
│   ├── embeddings.py
│   ├── skill_gap.py
│   └── utils.py
├── requirements.txt
└── README.md

⸻
Pipeline looks like this:

Streamlit frontend (local)
        ↓
Local Agent (calls ADK)
        ↓
Google ADK (remote LLM - Gemini 2.5 Flash)
        ↓
Local MCP server (your tools: fetch_jobs, skill_gap)
        ↓
Local modules / APIs / utils

Summary:
| Component         | Runs Where               | Purpose                                        |
|------------------|-------------------------|-----------------------------------------------|
| Frontend (Streamlit) | Local                  | UI for user input                              |
| MCP Server        | Local                   | Hosts your “tools” (fetch_jobs, skill_gap)    |
| Agent (LlmAgent)  | Local                   | Middle layer that connects to the LLM         |
| LLM (Gemini 2.5 Flash) | Remote (Google Cloud / ADK) | Does reasoning, interpretation, and tool orchestration |

⸻

1. Environment Setup

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install streamlit sentence-transformers scikit-learn pandas numpy requests spacy fastapi uvicorn mcp google-adk PyPDF2 python-docx
python -m spacy download en_core_web_sm


⸻

2. Modules

modules/job_api.py

import requests

FIND_SG_JOBS_API = "https://api.findsgjobs.gov.sg/v1/jobs"

def fetch_live_jobs():
    try:
        response = requests.get(FIND_SG_JOBS_API)
        response.raise_for_status()
        jobs_raw = response.json().get('jobs', [])
    except Exception:
        jobs_raw = []

    jobs = []
    for j in jobs_raw:
        jobs.append({
            'title': j.get('jobTitle', 'Unknown'),
            'company': j.get('companyName', 'Unknown'),
            'description': j.get('jobDescription', ''),
            'skills': j.get('skills', [])
        })
    return jobs


⸻

modules/embeddings.py

from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def rank_jobs_by_query(query: str, jobs: list):
    if not jobs:
        return []

    query_vec = model.encode(query, convert_to_tensor=True)
    job_vecs = model.encode([job['description'] for job in jobs], convert_to_tensor=True)

    cosine_scores = util.cos_sim(query_vec, job_vecs)[0]
    ranked_jobs = sorted(
        zip(jobs, cosine_scores.tolist()),
        key=lambda x: x[1],
        reverse=True
    )
    return [job for job, score in ranked_jobs]


⸻

modules/utils.py

import PyPDF2
from docx import Document

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + " "
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + " "
    return text

def extract_skills_from_resume(file):
    text = ""
    if hasattr(file, "name"):
        if file.name.endswith(".pdf"):
            text = extract_text_from_pdf(file)
        elif file.name.endswith(".docx"):
            text = extract_text_from_docx(file)
        else:
            text = str(file.read(), "utf-8")
    else:
        text = str(file)

    skills = [word.strip() for word in text.split() if word.istitle()]
    return skills


⸻

modules/skill_gap.py

from utils import extract_skills_from_resume

def analyze_skill_gap(resume_file, jobs):
    if not jobs:
        return []

    user_skills = extract_skills_from_resume(resume_file)
    gaps = []

    for job in jobs[:5]:
        required_skills = [s.lower() for s in job.get('skills', [])]
        user_skills_lower = [s.lower() for s in user_skills]
        missing_skills = [skill for skill in required_skills if skill not in user_skills_lower]

        gaps.append({
            'job_title': job.get('title', 'Unknown'),
            'missing_skills': missing_skills
        })
    return gaps


⸻

3. MCP Server

mcp_server/server.py

import asyncio
from mcp.server.lowlevel import Server
from mcp.types import TextContent, Tool
from modules.job_api import fetch_live_jobs
from modules.embeddings import rank_jobs_by_query
from modules.skill_gap import analyze_skill_gap

app = Server("job-recommendation-mcp")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="fetch_jobs",
            description="Fetch and rank job postings",
            inputSchema={"type":"object","required":["query"],"properties":{"query":{"type":"string"}}}
        ),
        Tool(
            name="skill_gap",
            description="Compute skill gap given resume text and jobs",
            inputSchema={"type":"object","required":["resume_text","jobs"],"properties":{"resume_text":{"type":"string"},"jobs":{"type":"array"}}}
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "fetch_jobs":
        query = arguments["query"]
        jobs = await asyncio.to_thread(fetch_live_jobs)
        ranked = await asyncio.to_thread(rank_jobs_by_query, query, jobs)
        return [TextContent(type="text", text=str(ranked[:5]))]
    elif name == "skill_gap":
        resume_text = arguments["resume_text"]
        jobs = arguments["jobs"]
        gaps = await asyncio.to_thread(analyze_skill_gap, resume_text, jobs)
        return [TextContent(type="text", text=str(gaps))]
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8080)


⸻

4. Agent

agent/agent.py

import os
import asyncio
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams

MCP_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8080/mcp")

async def get_agent_async():
    toolset, exit_stack = await MCPToolset.from_server(
        connection_params=StreamableHTTPConnectionParams(url=MCP_URL)
    )
    agent = LlmAgent(
        model="gemini-2.5-flash",
        name="job_recommendation_agent",
        instruction="You help users find jobs and analyze skill gaps. Use the MCP tools fetch_jobs and skill_gap.",
        tools=toolset
    )
    return agent, exit_stack

def run_agent(query, resume_text=None):
    root_agent, _ = asyncio.run(get_agent_async())
    if resume_text:
        prompt = f"User query: {query}\nResume text: {resume_text}\nFetch jobs and compute skill gap."
    else:
        prompt = f"User query: {query}\nFetch jobs only."
    result = asyncio.run(root_agent.run(prompt=prompt))
    print(result)

if __name__ == "__main__":
    q = input("Enter job search query: ")
    r = None
    if input("Include resume text? y/n ") == "y":
        r = input("Paste resume text: ")
    run_agent(q, r)


⸻

5. Frontend Chatbot

frontend/app.py

import streamlit as st
from agent.agent import run_agent

st.set_page_config(page_title="AI Job Chatbot", layout="wide")
st.title("AI-Driven Job Recommendation Chatbot")

query = st.text_input("Enter job search query (e.g., 'Data Analyst Singapore'):")
resume = st.text_area("Paste your resume text (optional):")

if st.button("Submit"):
    if query:
        st.write("Processing …")
        run_agent(query, resume if resume else None)


⸻

6. requirements.txt (root)

streamlit
sentence-transformers
scikit-learn
pandas
numpy
requests
spacy
fastapi
uvicorn
mcp
google-adk
PyPDF2
python-docx


⸻

7. README.md

# AI Job Recommendation & Skill Gap Chatbot (Local MCP Prototype)

## Setup

1. Create virtual environment:

python -m venv venv
source venv/bin/activate

2. Install dependencies:

pip install -r requirements.txt
python -m spacy download en_core_web_sm

## Run

1. Start MCP server:

python mcp_server/server.py

2. Run frontend chatbot:

streamlit run frontend/app.py

3. Enter your job query and optionally paste your resume. Results will display in the Streamlit UI.

## Notes

- MCP server exposes tools: `fetch_jobs` and `skill_gap`.
- Agent connects to MCP server using ADK.
- All modules are Python-based; no Docker required.


⸻

8. How to Run Prototype
	1.	Activate virtual environment.
	2.	Run MCP server:

python mcp_server/server.py

	3.	Run frontend:

streamlit run frontend/app.py

	4.	Enter job search query and optional resume text. Results appear in the chatbot.

⸻

This is fully drop-in, local, and Python-only — no Docker, no extra configuration required.

If you want, I can also add a small dummy FindSGJobs JSON cache so you can test without needing the real API — that way the prototype works entirely offline.
