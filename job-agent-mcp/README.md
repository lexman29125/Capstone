# AI Job Recommendation & Skill Gap Chatbot (Local MCP Prototype)

## Setup

1. Create virtual environment
2. Install dependencies:
```
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```
### Run
1. Start MCP server:
Instead of running server.py directly from mcp_server/, run it from job-agent-mcp/:
```
python -m mcp_server.server
```
2. Run frontend chatbot:
```
streamlit run frontend/app.py
```
3. Enter your job query and optionally paste your resume. Results will display in the Streamlit UI.

### Notes

- MCP server exposes tools: `fetch_jobs` and `skill_gap`.
- Agent connects to MCP server using ADK.
- All modules are Python-based; no Docker required.