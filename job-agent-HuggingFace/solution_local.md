Perfect — here’s a ready-to-run local setup for your job-agent project using Hugging Face LLM, with Gradio as frontend, including .env support, agent testing, and Streamlit/Gradio launch. You can drop this into your root folder and run.

⸻

1. Folder structure

job-agent-local/
│
├─ agent/
│   ├─ __init__.py
│   ├─ agent.py
│   ├─ resume_parser.py
│
├─ modules/
│   ├─ __init__.py
│   ├─ job_api.py
│   ├─ embeddings.py
│   └─ skill_gap.py
│
├─ frontend/
│   ├─ __init__.py
│   ├─ app.py            # Streamlit frontend
│   └─ gradio_interface.py  # Gradio frontend
│
├─ test_agent.py
├─ test_gradio.py
├─ requirements.txt
└─ .env


⸻

2. .env example

HF_API_KEY=your_huggingface_api_key


⸻

3. agent/agent.py

import os
import asyncio
from dotenv import load_dotenv
from modules.job_api import fetch_live_jobs
from modules.embeddings import rank_jobs_by_query
from modules.skill_gap import analyze_skill_gap
from transformers import pipeline

# Load API key
load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")

# Initialize Hugging Face LLM pipeline
llm_pipeline = pipeline(
    "text-generation",
    model="google/flan-t5-large",  # You can replace with any Hugging Face model
    device=-1,  # CPU (-1), GPU (0+)
    use_auth_token=HF_API_KEY,
)

async def run_agent(query: str, resume_text: str = None):
    # Step 1: Fetch jobs
    jobs = await asyncio.to_thread(fetch_live_jobs)

    # Step 2: Rank jobs
    ranked_jobs = await asyncio.to_thread(rank_jobs_by_query, query, jobs)

    # Step 3: Skill gap
    gaps = None
    if resume_text:
        gaps = await asyncio.to_thread(analyze_skill_gap, resume_text, ranked_jobs)

    # Step 4: Construct prompt
    prompt = f"Query: {query}\nTop Jobs: {ranked_jobs[:5]}"
    if gaps:
        prompt += f"\nSkill Gaps: {gaps}"

    # Step 5: Call LLM
    def call_llm(prompt_text):
        resp = llm_pipeline(prompt_text, max_length=300)
        return resp[0]['generated_text'] if resp else "No response"

    response_text = await asyncio.to_thread(call_llm, prompt)
    return response_text

def run_agent_sync(query: str, resume_text: str = None):
    return asyncio.run(run_agent(query, resume_text))


⸻

4. frontend/gradio_interface.py

import gradio as gr
from agent.agent import run_agent_sync

def gradio_predict(query, resume):
    return run_agent_sync(query, resume)

def create_interface():
    iface = gr.Interface(
        fn=gradio_predict,
        inputs=[
            gr.Textbox(label="Job Query"),
            gr.Textbox(label="Resume (optional)", lines=10),
        ],
        outputs="text",
        title="Job Recommendation & Skill Gap Analyzer",
        description="Enter your job search criteria and optionally your resume. The LLM will provide insights.",
    )
    return iface

if __name__ == "__main__":
    iface = create_interface()
    iface.launch()


⸻

5. frontend/app.py (Streamlit alternative)

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

6. test_agent.py

from agent.agent import run_agent_sync

query = "Data Scientist"
resume_text = "Experienced in Python, ML, SQL, and cloud computing."

result = run_agent_sync(query, resume_text)
print("=== LLM Output ===")
print(result)


⸻

7. requirements.txt

streamlit==1.30.0
gradio==3.41
python-dotenv==1.0
requests==2.31
transformers==4.34.0
torch==2.1.0
aiohttp==3.8.4


⸻

8. Deployment / Local Run Steps
	1.	Create virtual environment and activate

python -m venv jobagent_env
source jobagent_env/bin/activate  # macOS/Linux

	2.	Install dependencies

pip install --upgrade pip
pip install -r requirements.txt

	3.	Set .env with your Hugging Face API key
	4.	Test Agent locally

python test_agent.py

	5.	Run Streamlit frontend

streamlit run frontend/app.py

	6.	Run Gradio frontend

python frontend/gradio_interface.py

	•	Gradio will output a public link for testing.

⸻

This setup gives you:
	•	Modular agent logic
	•	LLM integration via Hugging Face (transformers)
	•	Both Streamlit and Gradio frontends
	•	Easy .env API key configuration
	•	Fully testable locally before deploying to Hugging Face Spaces

⸻

If you want, I can also provide a full Hugging Face Spaces deployment-ready structure with app.py, requirements.txt, and .env support so you can push and run immediately.