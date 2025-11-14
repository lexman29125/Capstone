import streamlit as st
import asyncio
import nest_asyncio
import random
import re # Import regex for salary parsing
import google.generativeai as genai
import os # Import os to potentially get API key from environment variables
from dotenv import load_dotenv

# Apply nest_asyncio to allow nested event loops, common in notebooks
nest_asyncio.apply()

# Load API key from .env file for local development
load_dotenv()


# Assuming Tool, Agent are defined in previous cells and are available in scope.
# Re-defining them here for clarity in this single block if notebook state is reset
class Tool:
    def __init__(self, func, name, description):
        self.func = func
        self.name = name
        self.description = description

class Agent:
    def __init__(self, name, instruction, tools: list):
        self.name = name
        self.instruction = instruction
        self.tools = tools
        # Removed print statement to avoid duplicate output as per instructions

# Helper function to parse salary from string
def parse_salary(salary_str: str) -> int:
    if not salary_str: return 0
    # Remove non-numeric characters except comma, then remove comma, then convert to int
    numeric_str = re.sub(r'[^\\d,]', '', salary_str)
    numeric_str = numeric_str.replace(',', '')
    try:
        return int(numeric_str)
    except ValueError:
        return 0

# Re-create dummy functions for independent execution of this cell if needed
def job_search(query: str, max_results: int = 5) -> list:
    print(f"Executing job_search tool with query='{query}' and max_results={max_results}")
    sample_jobs = [
        {"title": f"Software Engineer - {query}", "company": "Tech Corp", "location": "San Francisco, CA", "description": "Develop and maintain software, good with Python, Cloud.", "salary": "$120,000"},
        {"title": f"Data Scientist - {query}", "company": "Data Inc.", "location": "New York, NY", "description": "Analyze large datasets, using AI/ML, good with Python.", "salary": "$130,000"},
        {"title": f"Product Manager - {query}", "company": "Innovate Co.", "location": "Seattle, WA", "description": "Define product vision and roadmap.", "salary": "$140,000"},
        {"title": f"UX Designer - {query}", "company": "Creative Hub", "location": "Austin, TX", "description": "Design user interfaces, on Cloud platforms.", "salary": "$110,000"},
        {"title": f"DevOps Engineer - {query}", "company": "Cloud Solutions", "location": "Remote", "description": "Manage infrastructure and deployments on Cloud.", "salary": "$125,000"}
    ]
    random.shuffle(sample_jobs)
    return sample_jobs[:max_results]

def submit_application(job_id: str, candidate_profile: dict) -> dict:
    print(f"Executing submit_application tool for Job ID: {job_id} by candidate: {candidate_profile.get('name', 'N/A')}")
    if random.random() < 0.9:
        return {"status": "success", "message": f"Application for job {job_id} submitted.", "job_id": job_id, "candidate_name": candidate_profile.get('name')}
    else:
        return {"status": "failure", "message": f"Failed to submit application for job {job_id}.", "job_id": job_id, "candidate_name": candidate_profile.get('name')}

# Re-create Tool instances (these are now managed by the LLM, but keeping for Agent class compatibility if needed elsewhere)
job_search_tool = Tool(
    func=job_search,
    name="job_search",
    description="Searches for job listings based on a query and returns a list of job details."
)
submit_application_tool = Tool(
    func=submit_application,
    name="submit_application",
    description="Submits a job application with a given job ID and candidate profile."
)

# Re-create Agent instances (these are now largely symbolic, LLM handles logic)
job_search_agent = Agent(
    name="job_search_agent",
    instruction="I search for jobs based on a given query.",
    tools=[job_search_tool]
)
candidate_agent = Agent(
    name="candidate_agent",
    instruction="I manage candidate profiles and submit job applications.",
    tools=[submit_application_tool]
)

# Redefine CoordinatorAgent to use LLM for orchestration
class CoordinatorAgent(Agent):
    def __init__(self, name: str, instruction: str, tools: list = None, sub_agents: list = None):
        super().__init__(name, instruction, tools if tools is not None else [])
        self.sub_agents = sub_agents if sub_agents is not None else []

        # Store the list of tools passed to the LLM (functions themselves)
        self.llm_tools = [job_search, submit_application]

        # Instantiate the GenerativeModel with tools
        self.llm = genai.GenerativeModel(model_name='gemini-2.5-flash', tools=self.llm_tools)
        self.conversation = self.llm.start_chat(enable_automatic_function_calling=True)

        # This print statement is for CoordinatorAgent specific initialization.
        print(f"CoordinatorAgent '{self.name}' created with instruction: '{self.instruction}' and sub-agents: {[agent.name for agent in self.sub_agents]} and LLM with tools: {[tool.__name__ for tool in self.llm_tools]}")

    async def run_live(self, query: str, candidate_profile: dict):
        # Initial prompt to the LLM to start the workflow
        initial_prompt = (
            f"You are a helpful assistant that helps candidates find jobs and apply for them. "
            f"The candidate's profile is: {candidate_profile}. "
            f"The candidate is looking for a '{query}' position. "
            f"Your goal is to first find suitable jobs using the `job_search` tool, then carefully select the best job based on the candidate's skills and salary expectations, and finally apply for that job using the `submit_application` tool. "
            f"Prioritize jobs that mention skills like {', '.join(candidate_profile.get('skills', []))} and meet the salary expectation of {candidate_profile.get('salary_expectation', 0)}. "
            f"Once you have applied, provide a summary of the application status."
        )

        yield f"🚀 CoordinatorAgent '{self.name}' initiating LLM-driven job search for '{query}' and application process for candidate '{candidate_profile.get('name')}'..."
        yield f"🤖 LLM received initial prompt: {initial_prompt}"

        try:
            response = await self.conversation.send_message(initial_prompt)

            # Loop to handle multi-turn conversations and tool calls
            while True:
                if response.candidates and response.candidates[0].content.parts:
                    part = response.candidates[0].content.parts[0]

                    if part.function_call:
                        tool_call = part.function_call
                        tool_name = tool_call.name
                        tool_args = {k: v for k, v in tool_call.args.items()} # Convert protobuf map to dict

                        yield f"🛠️ LLM requested tool call: {tool_name} with arguments {tool_args}"

                        # Dynamically find and execute the tool function
                        tool_func = next((t for t in self.llm_tools if t.__name__ == tool_name), None)
                        if tool_func:
                            # Special handling for submit_application to pass candidate_profile
                            if tool_name == "submit_application":
                                tool_args['candidate_profile'] = candidate_profile

                            tool_output = tool_func(**tool_args)
                            yield f"✅ Tool '{tool_name}' executed. Output: {tool_output}"
                            response = await self.conversation.send_message(genai.tool_code(tool_output))
                        else:
                            yield f"❌ Error: LLM attempted to call unknown tool: {tool_name}"
                            break
                    elif part.text:
                        yield f"💬 LLM response: {part.text}"
                        # Assume that if the LLM generates text and no more tool calls, it's done
                        if "application submitted" in part.text.lower() or "no jobs found" in part.text.lower() or "workflow finished" in part.text.lower() or "summary" in part.text.lower():
                            break
                        # For simplicity, if it's text, we can also try to send a follow-up or break
                        # Here, we'll try sending an empty message to see if it generates more tool calls or concludes.
                        # In a real scenario, LLM might need a more sophisticated follow-up.
                        response = await self.conversation.send_message("Continue if necessary, or provide final summary.")
                    else:
                        yield "⚠️ LLM response did not contain text or tool calls. Ending workflow."
                        break
                else:
                    yield "⚠️ No valid response from LLM. Ending workflow."
                    break
        except Exception as e:
            yield f"❌ An unexpected error occurred during LLM interaction: {e}"

        yield "--- Multi-agent workflow finished ---"

# Re-instantiate the CoordinatorAgent with the new class definition
root_agent = CoordinatorAgent(
    name="root_agent",
    instruction="I orchestrate the job search and application process by coordinating between the job search and candidate agents to find suitable jobs and submit applications.",
    sub_agents=[job_search_agent, candidate_agent]
)

def run_streamlit_app():
    st.title('Multi-Agent Job Application System')

    with st.form(key='job_application_form'):
        st.header('Candidate Information')

        name = st.text_input('Name', key='name')
        email = st.text_input('Email', key='email')
        resume_link = st.text_input('Resume Link', key='resume_link')
        experience = st.text_area('Experience (e.g., "10+ years as Software Engineer")', key='experience')
        skills_input = st.text_input('Skills (comma-separated, e.g., Python, Cloud, AI/ML)', key='skills_input')
        salary_expectation = st.number_input('Salary Expectation', min_value=0, value=100000, step=10000, key='salary_expectation')
        job_query = st.text_input('Desired Job Title (e.g., Senior Engineer)', value='Senior Engineer', key='job_query') # New input field for job_query

        submit_button = st.form_submit_button(label='Submit Application')

        if submit_button:
            if not name or not email or not skills_input:
                st.error("Name, Email, and Skills are required fields.")
                return

            # Parse skills input
            skills_list = [s.strip() for s in skills_input.split(',') if s.strip()]

            candidate_profile = {
                "name": name,
                "email": email,
                "resume_link": resume_link,
                "experience": experience,
                "skills": skills_list,
                "salary_expectation": salary_expectation
            }
            # job_query is now dynamic from user input

            st.subheader("✨ Starting Job Search...")
            progress_messages = []

            # Use a placeholder for live updates, if possible, or collect messages
            status_placeholder = st.empty()

            try:
                async def run_workflow_and_display():
                    nonlocal progress_messages # Allow modification of progress_messages from outer scope
                    async for step_output in root_agent.run_live(job_query, candidate_profile):
                        progress_messages.append(step_output)
                        status_placeholder.markdown("\n".join(progress_messages))
                        await asyncio.sleep(0.1) # Small delay to allow UI updates

                # Execute the async generator
                loop = asyncio.get_event_loop()
                task = loop.create_task(run_workflow_and_display())
                # Wait for the task to complete if a loop is already running, or run the loop until complete
                if loop.is_running():
                    st.write("Scheduling workflow as a background task...")
                else:
                    asyncio.run(run_workflow_and_display())

            except Exception as e:
                st.error(f"An error occurred during workflow execution: {e}")

            st.subheader("🎉 Congratulations, you have successfully applied for matched jobs!")

# This line ensures the Streamlit app runs when the script is executed by Streamlit
run_streamlit_app()