import asyncio
import os
import aiohttp

async def run_agent(query: str, resume: str = None):
    mcp_url = os.getenv("MCP_SERVER_URL", "http://localhost:8080/mcp")

    async with aiohttp.ClientSession() as session:
        # Call fetch_jobs
        async with session.post(f"{mcp_url}/fetch_jobs", json={"query": query}) as resp:
            jobs = await resp.text()

        gaps = None
        if resume:
            async with session.post(f"{mcp_url}/skill_gap", json={"resume_text": resume, "jobs": jobs}) as resp:
                gaps = await resp.text()

    return {"jobs": jobs, "gaps": gaps}

def run_agent_sync(query: str, resume: str = None):
    """
    Synchronous wrapper for Streamlit or other sync frameworks.
    Uses asyncio.create_task if inside a running event loop.
    """
    try:
        loop = asyncio.get_running_loop()
        return asyncio.create_task(run_agent(query, resume))
    except RuntimeError:
        return asyncio.run(run_agent(query, resume))