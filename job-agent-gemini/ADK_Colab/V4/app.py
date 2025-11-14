import streamlit as st
import os # Import os for file path operations
import io # Import io for handling in-memory binary streams
import PyPDF2 # Import PyPDF2 for PDF text extraction
from dotenv import load_dotenv

# Assuming `extract_text_from_url` is defined elsewhere or will be defined above this block.
# If `extract_text_from_url` is not in global scope, it needs to be included here or passed.
# For now, let's assume it's available from a previous cell.
# You might need to add: `from your_module import extract_text_from_url`
# For the sake of a single runnable cell, we'll include a dummy version if not present.

# Dummy extract_text_from_url if not already globally defined in the session
# (this block assumes it's defined in cell 'ae39e48c' previously)

# Re-defining Agent/Tool/CoordinatorAgent and analysis functions to ensure scope for Streamlit
# This is a full re-declaration to make the Streamlit app runnable in a single block context

# --- Start of necessary re-definitions for Streamlit to run independently ---

import asyncio
import nest_asyncio
import random
import re # Import regex for salary parsing
import json # Import json for parsing LLM output
import google.generativeai as gen
import requests
from bs4 import BeautifulSoup

# Ensure nest_asyncio is applied if not already done in the session
nest_asyncio.apply()

# Helper function to parse salary from string (might not be used in current workflow but kept for consistency)
def parse_salary(salary_str: str) -> int:
    if not salary_str: return 0
    # Remove non-numeric characters except comma, then remove comma, then convert to int
    numeric_str = re.sub(r'[^\\d,]', '', salary_str)
    numeric_str = numeric_str.replace(',', '')
    try:
        return int(numeric_str)
    except ValueError:
        return 0

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

# Helper function to extract text from URL
def extract_text_from_url(url: str) -> str:
    """Extracts text content from a given URL, typically for a job description."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style elements
        for script_or_style in soup(['script', 'style']):
            script_or_style.extract()

        # Get text and clean it
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return ""
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return ""


# LLM Model setup (copied from the most recent successful setup)
llm_model = None

# Load .env file
load_dotenv()

# Configure the Google Generative AI client
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY') # Assuming this is set up or user provides
#if not GOOGLE_API_KEY or GOOGLE_API_KEY == "YOUR_GOOGLE_API_KEY_HERE":
    # In Streamlit, you might use st.secrets or direct input in an actual app
#    st.error("GOOGLE_API_KEY environment variable not set or is a placeholder. Please set it.")
#    st.stop() # Stop the app if API key is missing
#gen.configure(api_key=GOOGLE_API_KEY)

try:
    # Get all models that support text generation
    available_generative_models = [m.name for m in gen.list_models() if "generateContent" in m.supported_generation_methods]
    if not available_generative_models:
        st.error("No generative models found with the provided API key that support 'generateContent'.")
        st.stop()

    chosen_model_name = None
    if 'models/gemini-2.5-flash' in available_generative_models:
        chosen_model_name = 'models/gemini-2.5-flash'
    elif 'models/gemini-1.5-flash' in available_generative_models:
        chosen_model_name = 'models/gemini-1.5-flash'
    else:
        chosen_model_name = available_generative_models[0]

    llm_model = gen.GenerativeModel(chosen_model_name)
    st.sidebar.success(f"Successfully loaded LLM model: {llm_model.model_name}")

except Exception as e:
    st.error(f"Error during LLM model loading: {e}. Please check your API key and region settings.")
    st.stop()


def analyze_skills_and_gaps(resume_text: str, job_description_text: str) -> str:
    """Analyzes a candidate's resume against a job description using the LLM to identify skills and gaps."""
    prompt = f"""You are an expert HR analyst. Your task is to compare a candidate's resume with a job description.

Here is the candidate's Resume:
---
{resume_text}
---

Here is the Job Description:
---
{job_description_text}
---

Please perform the following steps and provide your output as a JSON object ONLY. Do not include any other text or explanation outside the JSON.

JSON Schema:
{{
    "candidate_skills": ["string"], # List of key technical and soft skills explicitly mentioned in the resume.
    "required_job_skills": ["string"], # List of essential technical and soft skills mentioned in the job description.
    "matched_skills": ["string"], # Skills present in both the resume and the job description.
    "missing_skills": ["string"], # Skills required by the job description but NOT found in the resume.
    "additional_skills": ["string"], # Skills present in the resume but not explicitly required by the job description.
    "overall_fit_summary": "string" # A brief summary of how well the candidate's skills align with the job requirements.
}}
"""

    try:
        global llm_model
        if llm_model is None:
            return "Error: LLM model not initialized."

        response = llm_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error during LLM analysis: {e}"

# Update the analysis function to call the LLM-based logic and parse JSON
def analyze_resume_job_description_full(resume_text: str, job_description_text: str) -> dict:
    """Performs a full resume and job description analysis using the LLM.
    This function replaces the placeholder and calls analyze_skills_and_gaps.
    """
    # print(f"Initiating LLM-based analysis for resume (length: {len(resume_text)}) and job description (length: {len(job_description_text)}).") # Use st.write instead of print
    analysis_report = analyze_skills_and_gaps(resume_text, job_description_text)

    if "Error during LLM analysis" in analysis_report:
        return {"analysis_status": "failure", "message": analysis_report}
    else:
        try:
            # Remove markdown code block fences if present
            cleaned_report = analysis_report.strip()
            if cleaned_report.startswith('```json') and cleaned_report.endswith('```'):
                cleaned_report = cleaned_report[len('```json'):-len('```')].strip()

            parsed_report = json.loads(cleaned_report)
            return {"analysis_status": "success", "message": "LLM-based analysis completed and parsed.", "parsed_report": parsed_report}
        except json.JSONDecodeError as e:
            return {"analysis_status": "failure", "message": f"Failed to parse LLM output as JSON: {e}", "raw_report": analysis_report}
        except Exception as e:
            return {"analysis_status": "failure", "message": f"An unexpected error occurred during JSON parsing: {e}", "raw_report": analysis_report}

# 1. No modifications to Tool and Agent class structures are needed at this stage.

# 2. Remove instantiation of old tools and agents.
# job_search_tool, submit_application_tool, job_search_agent, and the original candidate_agent are removed.

# 3. Define a new Tool instance for analysis.
analysis_tool = Tool(
    func=analyze_resume_job_description_full, # Use the full analysis function
    name="analyze_resume_job_description",
    description="Analyzes a candidate's resume against a job description to identify skills and gaps using an LLM."
)

# 4. Re-instantiate the candidate_agent with the new analysis_tool.
candidate_agent = Agent(
    name="candidate_agent",
    instruction="I manage candidate profiles and analyze resumes against job descriptions.",
    tools=[analysis_tool]
)

# Redefine CoordinatorAgent to reflect new workflow
class CoordinatorAgent(Agent):
    def __init__(self, name: str, instruction: str, tools: list = None, sub_agents: list = None):
        super().__init__(name, instruction, tools if tools is not None else [])
        self.sub_agents = sub_agents if sub_agents is not None else []

    async def run_live(self, resume_text: str, job_description_text: str):
        yield f"🚀 CoordinatorAgent '{self.name}' initiating resume and job description analysis..."

        candidate_agent_found = next((agent for agent in self.sub_agents if agent.name == "candidate_agent"), None)
        if not candidate_agent_found:
            yield "❌ Error: candidate_agent not found."
            return

        analysis_tool_instance = next((tool for tool in candidate_agent_found.tools if tool.name == "analyze_resume_job_description"), None)
        if not analysis_tool_instance:
            yield "❌ Error: analyze_resume_job_description tool not found for candidate_agent."
            return

        yield f"⚙️ Delegating analysis to {candidate_agent_found.name} using {analysis_tool_instance.name} tool..."
        try:
            # In Streamlit, use st.spinner for long operations instead of printing 'Initiating LLM-based analysis'
            analysis_result = analysis_tool_instance.func(resume_text, job_description_text)
            if analysis_result.get('analysis_status') == 'success':
                yield f"✅ Analysis complete: {analysis_result.get('message', 'No message provided.')}"
                yield "--- LLM Analysis Report (JSON) ---"
                parsed_report = analysis_result.get('parsed_report', {})
                for key, value in parsed_report.items():
                    if isinstance(value, list):
                        yield f"\n{key.replace('_', ' ').title()}:\n  - " + "\n  - ".join(value)
                    else:
                        yield f"\n{key.replace('_', ' ').title()}: {value}"
                yield "-----------------------------------"
            else:
                yield f"❌ Analysis failed: {analysis_result.get('message', 'Unknown error.')}"
                if 'raw_report' in analysis_result:
                    yield f"Raw LLM output: {analysis_result['raw_report']}"
        except Exception as e:
            yield f"❌ Error during analysis: {e}"
            return

# Re-instantiate the CoordinatorAgent with the new class definition and updated sub-agents
root_agent = CoordinatorAgent(
    name="root_agent",
    instruction="I orchestrate the resume and job description analysis process.",
    sub_agents=[candidate_agent]
)

# --- End of necessary re-definitions ---


# Existing Streamlit setup (copying from previous cell for context/completeness if run independently)
st.set_page_config(
    page_title="AI-Powered Resume and Job Description Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("AI-Powered Resume and Job Description Analyzer")
st.sidebar.header("User Inputs")

# 5. Add input fields for Job URL and Resume Upload in the sidebar
job_url_input = st.sidebar.text_input(
    "Job Description URL",
    value="https://example.com/job_description", # Pre-fill with placeholder
    help="Enter the URL of the job description webpage."
)

uploaded_resume_file = st.sidebar.file_uploader(
    "Upload Your Resume (PDF)",
    type=["pdf"],
    help="Upload your resume in PDF format."
)

# 6. Basic validation for inputs
is_valid_job_url = False
if job_url_input:
    # Simple URL validation check
    if job_url_input.startswith("http://") or job_url_input.startswith("https://"):
        is_valid_job_url = True
    else:
        st.sidebar.error("Please enter a valid URL (starting with http:// or https://).")

is_resume_uploaded = False
if uploaded_resume_file is not None:
    is_resume_uploaded = True

# 7. Add a button to trigger the analysis
if st.sidebar.button("Run Analysis", disabled=(not is_valid_job_url or not is_resume_uploaded)):
    if is_valid_job_url and is_resume_uploaded:
        with st.spinner("Processing resume and fetching job description..."):
            # Read uploaded PDF file
            try:
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_resume_file.getvalue()))
                resume_text = "".join([page.extract_text() for page in pdf_reader.pages])
                st.success("Resume extracted successfully.")
            except Exception as e:
                st.error(f"Error reading resume PDF: {e}")
                resume_text = ""

            # Fetch job description from URL
            try:
                job_description_text = extract_text_from_url(job_url_input)
                if job_description_text:
                    st.success("Job description fetched successfully.")
                else:
                    st.error("Failed to fetch job description. Please check the URL.")
            except Exception as e:
                st.error(f"Error fetching job description from URL: {e}")
                job_description_text = ""

        if resume_text and job_description_text:
            st.subheader("Analysis Report")
            progress_bar = st.progress(0)
            status_text = st.empty()
            report_container = st.empty()

            async def run_analysis_workflow_streamlit(res_text: str, jd_text: str):
                output_lines = []
                total_steps = 7 # Estimate total steps for progress bar
                current_step = 0
                # Wrap the async generator iteration in a way that Streamlit can handle.
                # Since Streamlit runs in a synchronous loop, we'll collect outputs.
                # For a true streaming experience, you'd need more advanced Streamlit async patterns.
                async for step_output in root_agent.run_live(res_text, jd_text):
                    output_lines.append(step_output)
                    status_text.text(step_output)
                    current_step += 1
                    progress_bar.progress(min(current_step / total_steps, 1.0))
                return output_lines
            
            st.write("Starting AI analysis...")
            full_report_lines = []
            # Use asyncio.run to execute the async generator if outside an async function
            for step_output in asyncio.run(run_analysis_workflow_streamlit(resume_text, job_description_text)):
                 full_report_lines.append(step_output)
            
            progress_bar.empty()
            status_text.empty()
            
            # Display the collected report lines in markdown
            report_container.markdown("\n".join(full_report_lines))

        else:
            st.error("Analysis cannot be performed due to missing resume text or job description text.")
    else:
        st.error("Please fix the input errors before running analysis.")
else:
    # Display status in the main area or sidebar for user feedback (outside button click)
    if not is_valid_job_url or not is_resume_uploaded:
        st.warning("Please provide a valid Job URL and upload your resume to proceed.")
    else:
        st.success("Job URL and Resume uploaded successfully. Ready for analysis!")

# print("Streamlit UI adapted for workflow execution and output display.") # No need to print this in Streamlit app