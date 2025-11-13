import streamlit as st
import asyncio
import nest_asyncio
import random
import re # Import regex for salary parsing

# Ensure nest_asyncio is applied if not already done in the session
nest_asyncio.apply()

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
    if random.random() < 0.9:
        return {"status": "success", "message": f"Application for job {job_id} submitted.", "job_id": job_id, "candidate_name": candidate_profile.get('name')}
    else:
        return {"status": "failure", "message": f"Failed to submit application for job {job_id}.", "job_id": job_id, "candidate_name": candidate_profile.get('name')}

# Re-create Tool instances
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

# Re-create Agent instances
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

# Redefine CoordinatorAgent with the full run_live method (job selection and error handling)
class CoordinatorAgent(Agent):
    def __init__(self, name: str, instruction: str, tools: list = None, sub_agents: list = None):
        super().__init__(name, instruction, tools if tools is not None else [])
        self.sub_agents = sub_agents if sub_agents is not None else []

    async def run_live(self, query: str, candidate_profile: dict):
        yield f"CoordinatorAgent '{self.name}' initiating job search for '{query}' and application process for candidate '{candidate_profile.get('name')}'..."

        # 2a. Find the job_search_agent
        job_search_agent_found = next((agent for agent in self.sub_agents if agent.name == "job_search_agent"), None)
        if not job_search_agent_found:
            yield "Error: job_search_agent not found."
            return
        job_search_tool_instance = next((tool for tool in job_search_agent_found.tools if tool.name == "job_search"), None)
        if not job_search_tool_instance:
            yield "Error: job_search tool not found for job_search_agent."
            return

        # 2b. Simulate job_search_agent using its job_search_tool with error handling
        yield f"Delegating job search to {job_search_agent_found.name}..."
        jobs = []
        try:
            jobs = job_search_tool_instance.func(query, max_results=5) # Increased max_results to have more options
        except Exception as e:
            yield f"Error during job search: {e}"
            return

        # 2c. Yield message about jobs found
        yield f"Job search complete. Found {len(jobs)} jobs:" \
              + "\n" + "\n".join([f"- {job['title']} at {job['company']} (Salary: {job.get('salary', 'N/A')})" for job in jobs])

        if not jobs:
            yield "No jobs found, unable to apply."
            return

        # 2d. Enhanced Job Selection Logic
        candidate_skills = [s.lower() for s in candidate_profile.get('skills', [])]
        salary_expectation = candidate_profile.get('salary_expectation', 0)

        def score_job(job: dict) -> int:
            score = 0
            job_text = (job.get('title', '') + ' ' + job.get('description', '')).lower()
            job_salary = parse_salary(job.get('salary', ''))

            # Skill matching
            matched_skills_count = sum(1 for skill in candidate_skills if skill in job_text)
            score += matched_skills_count * 10 # Each skill match adds 10 points

            # Salary matching
            if job_salary >= salary_expectation:
                score += 5 # Meeting salary expectation adds 5 points

            # Prioritize 'Senior Engineer' in title if specifically searched for and available
            if "senior engineer" in job.get('title', '').lower() and "senior engineer" in query.lower():
                score += 2 # Small boost for direct title match

            return score

        scored_jobs = []
        for job in jobs:
            scored_jobs.append((score_job(job), job))

        # Sort by score in descending order
        scored_jobs.sort(key=lambda x: x[0], reverse=True)

        selected_job = None
        if scored_jobs and scored_jobs[0][0] > 0: # If at least one job has a positive score
            selected_job = scored_jobs[0][1]
            yield f"Selected job based on skills and salary expectations: '{selected_job['title']}' at '{selected_job['company']}' (Score: {scored_jobs[0][0]})."
        else: # Fallback if no job scores positively or scored_jobs is empty
            # Original fallback logic: try to find a 'Senior Engineer' job or take the first one
            selected_job = next((job for job in jobs if "Senior Engineer" in job['title']), jobs[0])
            yield f"No jobs matched criteria strongly. Falling back to default selection: '{selected_job['title']}' at '{selected_job['company']}' (Score: 0)."

        # Assign a dummy job_id for demonstration
        job_id = f"JOB-{random.randint(1000, 9999)}"

        # 2e. Find the candidate_agent
        candidate_agent_found = next((agent for agent in self.sub_agents if agent.name == "candidate_agent"), None)
        if not candidate_agent_found:
            yield "Error: candidate_agent not found."
            return
        submit_application_tool_instance = next((tool for tool in candidate_agent_found.tools if tool.name == "submit_application"), None)
        if not submit_application_tool_instance:
            yield "Error: submit_application tool not found for candidate_agent."
            return

        # 2f. Simulate candidate_agent using its submit_application_tool with error handling
        yield f"Delegating application submission to {candidate_agent_found.name} for job ID {job_id}..."
        application_status = {}
        try:
            application_status = submit_application_tool_instance.func(job_id, candidate_profile)
        except Exception as e:
            yield f"Error during application submission: {e}"
            return

        # 2g. Yield application submission status
        yield f"Application submission status: {application_status.get('status', 'unknown')}. Message: {application_status.get('message', 'An unknown error occurred.')}"


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
            if not name or not email or not skills_input or not job_query:
                st.error("Name, Email, Skills, and Desired Job Title are required fields.")
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

            st.subheader("\n--- Starting the multi-agent workflow ---")
            progress_messages = []

            # Use a placeholder for live updates, if possible, or collect messages
            status_placeholder = st.empty()

            try:
                # asyncio.run() needs to be called within an event loop. nest_asyncio handles this.
                # The run_live method is an async generator, so we need to iterate over it.
                # We run it in a new event loop if necessary or in the existing one.
                # For Streamlit, using create_task and a loop is generally safer for responsiveness.

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
                    # In a real Streamlit app, you might want to manage the task more explicitly
                    # or ensure the UI can update while async tasks run.
                    # For this demonstration, we let it run and update the placeholder.
                    # We cannot await directly here as it would block the Streamlit thread.
                    # The placeholder will update as messages arrive.
                else:
                    asyncio.run(run_workflow_and_display())

            except Exception as e:
                st.error(f"An error occurred during workflow execution: {e}")

            st.subheader("--- Multi-agent workflow finished ---")
run_streamlit_app()