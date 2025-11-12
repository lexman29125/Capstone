import asyncio
from mcp.server.lowlevel import Server
from mcp.types import TextContent, Tool

# Import from modules package
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
    # Start the MCP server using the callable Server object
    import asyncio
    asyncio.run(app.start(host="0.0.0.0", port=8080))