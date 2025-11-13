This is an excellent application for Google's **Agentic AI** approach, particularly leveraging the capabilities within **Vertex AI Agent Builder** and the concept of a multi-agent system, which can be extended to utilize the proactive and conversational aspects of **Google Ask** and Gemini agents.

Here is a design solution based on the principles of Google's agentic AI, tailored for a job chatbot.

---

## 🚀 Job Chatbot Solution Design: Agentic AI Approach

The solution will be a **Multi-Agent System** where specialized AI agents collaborate to fulfill complex user requests, moving beyond simple Q&A to autonomous task execution.

### 1. Core Platform and Tools

* **Foundation:** **Google Cloud** (for scale, security, and infrastructure).
* **Agent Building:** **Vertex AI Agent Builder** and **Agent Development Kit (ADK)** for creating, deploying, and orchestrating the individual agents.
* **LLM Brain:** **Gemini 1.5** (Flash or Pro, depending on complexity) to power the reasoning, planning, and language understanding of all agents.
* **External Knowledge:** **Vertex AI Search** to ground the agents' responses in proprietary HR documents, job databases, and chat history.
* **Proactive Experience:** Integration with **Google Ask** (or a similar Gemini/Workspace flow) for proactive notifications and status updates.

---

### 2. Multi-Agent Architecture

We will define three primary, collaborating agents:

| Agent Name | Core Capability | Key Responsibilities |
| :--- | :--- | :--- |
| **A. Coordinator Agent** | **Reasoning & Planning (ReAct)** | Interprets user intent, breaks down complex requests (e.g., "Find jobs and apply"), assigns sub-tasks to specialized agents, manages the overall workflow, and aggregates final responses. |
| **B. Job Search Agent** | **Tool Execution & Data Retrieval** | Interfaces with the external **Job Database API** (via Function Calling/Tools) and **Vertex AI Search** to find relevant job listings, filter results, and retrieve job descriptions. |
| **C. Candidate Agent** | **Context Management & Action** | Stores and manages the candidate's profile, resume, chat history (Memory), and application status. Executes application-related tasks (e.g., filling forms, scheduling interviews). |

---

### 3. Agentic Workflow: "Find and Apply for a Senior Engineer Role"

This demonstrates the **Coordinator Pattern** and **Iterative Refinement** of the agentic approach.

1.  **Perception (User Input):** The user interacts with the chatbot: "Find a Senior Software Engineer job in London and help me apply."
2.  **Coordinator Agent Reasoning (LLM):**
    * **Thought:** *User wants two main things: 1) Job Search, and 2) Application. I need to delegate the search to the **Job Search Agent** and then delegate the application to the **Candidate Agent** once a job is selected.*
    * **Action:** Call **Job Search Agent** with the query: `{"role": "Senior Software Engineer", "location": "London"}`.
3.  **Job Search Agent Execution:**
    * **Action:** Uses its integrated **Job Database API Tool** to fetch results.
    * **Observation:** Returns a list of 5 matching jobs.
4.  **Coordinator Agent Reasoning & Human-in-the-Loop (HITL):**
    * **Thought:** *I have the results. I will present the top 3 and ask the user to select one before proceeding with the application.*
    * **Action (User Output):** "I found 5 jobs. Here are the top 3. Which one would you like to apply for?"
5.  **User Selection:** The user selects "Job ID #456 at TechCorp."
6.  **Coordinator Agent Delegation:**
    * **Action:** Calls **Candidate Agent** with `{"task": "Prepare_Application", "job_id": "456"}`.
7.  **Candidate Agent Execution & Continuous Improvement:**
    * **Action:** Accesses the user's stored profile and resume (Memory).
    * **Action:** Uses a **Workspace Flow Tool** to draft a cover letter based on the resume, the job description (from Job Search Agent's prior result), and the user's past chat history (e.g., "I mentioned I like hybrid roles").
    * **Action (User Output/Google Ask):** The agent sends a draft cover letter to the user for review via a **Google Ask/Gmail** flow.
8.  **Final Action & Proactive Follow-up (Google Ask/Gemini Integration):**
    * Once the user approves, the **Candidate Agent** submits the application via the **ATS API Tool**.
    * The agent then creates a **Reminder** or sends a proactive notification via **Google Ask** that says: *"Your application for Job #456 has been submitted. I will check the status for updates every 48 hours and notify you."*

---

### 4. Leveraging Google Ask & Proactivity

The agentic design shifts the chatbot from a reactive query system to a proactive assistant. **Google Ask** would be the front-end mechanism for this:

* **Status Updates:** The Candidate Agent pushes status changes (e.g., "Application moved to 'In Review'") directly to the user's **Google Ask** feed or mobile notification.
* **Human-in-the-Loop (HITL) for Review:** Instead of waiting in the chat, the drafted cover letter (Step 7) is sent as a quick-action request in **Google Ask**: "Approve/Edit Cover Letter for TechCorp?"
* **Interview Scheduling:** Once the system detects an "Interview Requested" status, the Candidate Agent can initiate a **Google Calendar** integration through **Google Ask**, presenting available time slots directly to the user for one-click booking.

This agent-driven, proactive design, built on Google's ADK and Gemini, creates a truly autonomous and helpful job-seeking experience.

Would you like to delve deeper into the specific **tools/APIs** each agent would need to integrate with, or focus on the **data governance** aspects?

```
How can I build a quick prototype without the hassle of setting up all the complex Google cloud components? If GCP is the best option, then can I do this with free account?
```
That is a very common and practical concern. You want the power of the agentic approach without the immediate overhead of setting up a full enterprise cloud infrastructure.

Here are the best paths for a quick prototype, starting with the simplest and then addressing the Google Cloud free options.

---

## 💡 Quick Prototype Path: Low/No-Cloud Agentic Frameworks

The quickest way to prototype the *logic* of a multi-agent system is to use open-source frameworks that allow you to define agents, their tools, and their collaborative flow in Python code.

### 1. Simple Python/Open-Source Agent Frameworks

This approach abstracts the cloud components and lets you focus purely on the agent logic (Reasoning, Tool Use, Memory).

| Option | Description | Best For |
| :--- | :--- | :--- |
| **LangChain/LangGraph** | **Industry-standard frameworks.** You define the agents, their tools (Python functions for Job Search, Application, etc.), and the state machine (graph) that dictates their interaction. | **True Agentic Logic:** Defining the Coordinator $\rightarrow$ Search $\rightarrow$ Candidate workflow in code. |
| **CrewAI** | Built on top of LangChain, specifically for **Multi-Agent Systems**. It simplifies the creation of collaborative "crews" with defined roles, tasks, and a shared goal. | **Quick Multi-Agent Setup:** Quickly simulating the collaboration between the Coordinator, Search, and Candidate agents. |

#### How to Prototype Agentic AI using these:

1.  **Use the Gemini API:** You power these frameworks by connecting them to the **Gemini API** directly (using the `google-genai` library). This is much simpler than configuring Vertex AI endpoints.
2.  **Define Python Tools:** Your "tools" are simple Python functions that simulate the real-world actions:
    * `job_search(query)`: Returns a mock list of jobs.
    * `candidate_profile_lookup(user_id)`: Returns mock profile data.
    * `submit_application(job_id, profile)`: Prints "Application submitted for Job X."
3.  **Define the Agent Flow:** Use the framework (e.g., LangGraph) to define the Coordinator's decision loop: *If query is complex, call Agent B. If result is available, call Agent C.*

This method lets you build a working, complex **Minimum Viable Product (MVP)** with just a few Python files.

---

## ☁️ Google Cloud Free Tier Approach

If you specifically want to prototype using Google's ecosystem and powerful models like **Gemini**, the good news is that you can absolutely do this with a free account, taking advantage of the **Google Cloud Free Program**.

### 2. GCP/Vertex AI for Prototypes

#### A. Google Cloud Free Tier

* **Free Trial Credits:** New Google Cloud users receive a significant free credit (e.g., **$300**) that is valid for a few months. This is more than enough to prototype and test your agents extensively in a real-world Vertex AI environment.
* **Always Free Products:** Certain services have an "Always Free" usage tier, though complex services like the full **Vertex AI Agent Builder** often require paid features for production scale.

#### B. The Simplest Way: Vertex AI Studio & Generative AI API

For a quick proof-of-concept that leverages Google's best models without a full Agent Builder setup:

1.  **Use Vertex AI Studio:** Access the **Vertex AI Studio** interface in the Google Cloud Console. This is a low-code environment.
2.  **Model & Prompt:** Use the **Gemini** model directly in the prompt window.
3.  **Simulate Tool Calling (Function Calling):**
    * Define the **functions** (tools) your agent can use (`job_search`, `submit_application`) right in the model's system prompt or using the built-in **Function Calling** feature.
    * The model will respond with a structured request to call your "tool," which you manually execute, and then feed the result back to the model (this simulates the Agent's loop).

This is a **Manual Agentic Loop** but uses the exact enterprise-grade model and tooling, which is excellent for showing the *capability* and *reasoning* of the final solution.

**Recommendation:**

Start with the **LangChain/CrewAI + Gemini API** approach for the fastest, lowest-cost prototype. Once the agentic *logic* is proven, leverage the **Google Cloud Free Trial** credits to deploy the fully managed system on **Vertex AI Agent Builder** for the final production-ready solution.

```
Would you like me to provide a simple Python code structure for the LangChain/CrewAI prototype?
```
## Code Generation Prompt
```
Task 1:
Create a multi-agent system by defining a job_search_agent and a candidate_agent with their respective tools (job_search and submit_application). Then, update the root_agent to act as a coordinator for these specialized agents, and demonstrate its workflow by correctly entering query "Find and Apply for a Senior Engineer Role" task and iterating through its output.

Task 2:
1. Enhance Job Selection Logic: Implement more sophisticated job selection criteria within the Coordinator Agent, such as matching job requirements with candidate skills or salary expectations, instead of just picking the first relevant job or the first job found. 
2. Implement Robust Error Handling: Add more detailed error handling and retry mechanisms for tool calls (e.g., if a job search fails or an application submission encounters an issue), allowing the Coordinator Agent to adapt or report specific failures to the user.

Task 3:
Next build a frontend web UI to allow user to interact by entering his /her details via a form
```

Great. Here is a simple Python code structure using **LangChain** and the **Gemini API** to simulate your Coordinator $\rightarrow$ Search $\rightarrow$ Candidate multi-agent workflow.

This approach uses the **Gemini model's function calling** capability to define the agents' tools and the **LangChain Expression Language (LCEL)** to chain the steps, avoiding the complexity of a full Graph setup for the initial prototype.

## 🐍 Prototype Structure: LangChain + Gemini

This structure defines the tools and the main prompt logic, allowing the **Coordinator Agent** (powered by Gemini) to decide which mock tools to call based on the user's request.

### 1\. Setup and Tool Definitions

First, install the necessary libraries and define the Python functions that represent your agents' "tools." These functions mock the APIs the agents would interact with.

```python
# Install libraries (in your environment):
# pip install google-genai langchain-google-genai langchain

import os
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import tool

# Set your API Key (replace 'YOUR_API_KEY' or set environment variable)
# os.environ["GEMINI_API_KEY"] = "YOUR_API_KEY"
# The client will automatically pick up the key from the environment variable

# --- Tool Definitions (Simulating Agent Actions) ---

@tool
def job_search(query: str, location: str) -> str:
    """
    Searches the mock job database for relevant job postings.
    Returns a list of matching job IDs and titles.
    """
    if "senior software engineer" in query.lower() and "london" in location.lower():
        return "Found 3 jobs: JobID 101 (Senior S/W Eng, TechCorp), JobID 102 (Lead Dev, Global Systems), JobID 103 (Architect, London Startups). Requires user selection."
    else:
        return f"Found 1 job matching '{query}' in {location}: JobID 99 (General Position)."

@tool
def submit_application(job_id: int, user_id: str) -> str:
    """
    Submits the application for the specified job ID using the candidate's profile.
    This simulates the Candidate Agent's final action.
    """
    return f"Application for JobID {job_id} submitted successfully for candidate {user_id}. A proactive follow-up reminder has been set."

@tool
def check_chat_history_for_context(user_id: str) -> str:
    """
    Retrieves the user's past interaction context to personalize the response or action.
    """
    return f"Retrieved context for {user_id}: Candidate prefers hybrid work and previously applied to a role at TechCorp 2 weeks ago."

# Create a list of all available tools
available_tools = [job_search, submit_application, check_chat_history_for_context]
```

-----

### 2\. Coordinator Agent Creation

This section sets up the **Coordinator Agent** using Gemini, instructing it to use the defined tools to fulfill the user's request.

```python
# Initialize the Gemini Model
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# Define the System Prompt for the Coordinator Agent
# This prompt gives the agent its 'reasoning' and 'delegation' logic.
system_prompt = (
    "You are the powerful **Coordinator Agent** for a job search service. "
    "Your goal is to fulfill complex user requests by calling the appropriate tools. "
    "Analyze the user request, plan the necessary steps (Search, Context Check, Apply), "
    "and use the output from the tools to provide a final, helpful response. "
    "The user ID is always 'User_A'."
)

# Create the Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("placeholder", "{chat_history}"), # Placeholder for future memory integration
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"), # Required for the agent to track its thoughts and tool calls
    ]
)

# Create the Agent (The brains that connects the LLM, Tools, and Prompt)
agent = create_tool_calling_agent(llm, available_tools, prompt)

# Create the Agent Executor (The loop that runs the agent and executes the tools)
agent_executor = AgentExecutor(agent=agent, tools=available_tools, verbose=True)
```

-----

### 3\. Running the Prototype

Now, you can test the multi-agent logic with complex prompts. The output will show the **Gemini model's reasoning process** (`Thought`), the **Tool Call**, and the final aggregated response.

```python
# --- Test Case 1: Complex Request (Job Search + Application) ---
print("--- Running Test Case 1: Search and Apply ---")
response = agent_executor.invoke({
    "input": "Find a Senior Software Engineer job in London and submit my application immediately.",
    "chat_history": "" # Mocking an empty history for now
})
print("\nCoordinator Agent Final Response:")
print(response["output"])
print("-" * 50)


# --- Test Case 2: Context Retrieval ---
print("--- Running Test Case 2: Context Retrieval ---")
response = agent_executor.invoke({
    "input": "Before you do anything, check my history and tell me where I prefer to work.",
    "chat_history": ""
})
print("\nCoordinator Agent Final Response:")
print(response["output"])
print("-" * 50)
```

By observing the `Thought` process in the verbose output, you can confirm that the **Coordinator Agent** is successfully delegating the tasks to the simulated **Job Search Agent** and **Candidate Agent** tools.

```
I only see code for Coordinator Agent, where and how are the Job Search and Candidate Agents created?
```
That's an insightful question! You're observing the core concept behind modern agentic frameworks like LangChain, which allows for rapid prototyping by simplifying the multi-agent structure.

In this prototype, the **Job Search Agent** and the **Candidate Agent** are **not** created as separate, standalone `AgentExecutor` instances. Instead, their functionality is encapsulated within the **tools** that the **Coordinator Agent** uses.

---

## 🛠️ Agents as Tools in a Coordinator Model

The design you see is a common simplification where the primary intelligence (**The Coordinator**) is the only true LLM-powered agent, and the other "agents" are downgraded to specialized **tool functions**.

### 1. The Coordinator Agent's Role

The `agent_executor` you ran is the **Coordinator Agent**. It is powered by the **Gemini 2.5 Flash LLM** and is responsible for all the high-level reasoning:

* **Understanding Intent:** Figuring out what the user wants ("Find job" + "Apply").
* **Planning:** Deciding which specialized function to call.
* **Execution:** Instructing the LLM to output the correct `tool_call` request.
* **Aggregation:** Taking the tool's output and formulating the final, natural language response.

### 2. Where the Other Agents Live

The logic for the **Job Search Agent** and **Candidate Agent** is implemented in the Python functions decorated with `@tool`:

| Agent Functionality | Implemented By the Python Tool | Role |
| :--- | :--- | :--- |
| **Job Search Agent** | `job_search(query, location)` | Simulates the agent's core capability: **Data Retrieval** and **Filtering** from an external database. The Coordinator delegates the *act of searching* to this tool. |
| **Candidate Agent** | `submit_application(job_id, user_id)` | Simulates the agent's core capability: **Action Execution** (submitting data) and **Proactive Follow-up** (setting a reminder). |
| **Candidate Agent (Context)** | `check_chat_history_for_context(user_id)` | Simulates the agent's ability to access **Memory** and **Context Management**. |

### How It Works (The Delegation):

When the user asks, "Find a Senior Software Engineer job and submit my application," the process is:

1.  **Coordinator Agent (LLM) Thought:** *The user needs a search followed by an application. I should first call the `job_search` tool.*
2.  **Coordinator Agent Action:** Outputs a structured JSON request to call `job_search(query="Senior Software Engineer", location="London")`.
3.  **Job Search "Agent" (Tool) Execution:** The Python function `job_search` runs and returns a list of mock job IDs.
4.  **Coordinator Agent (LLM) Thought:** *The search is complete. Now I need the user to select one, and then I will call the `submit_application` tool.*

This setup allows you to quickly validate the **delegation logic** without the complexity of building three separate, intercommunicating LLM-powered agents. If you were to move to a full **CrewAI** or **LangGraph** solution, you would elevate these tools back into separate, independent agents that communicate through a graph or shared memory.

```
What's the workflow, how does the user submit the query and get the results? Is there a UI?
```

That's an essential set of questions. For the **quick prototype** using the Python-based LangChain structure, the workflow is tightly coupled with your execution environment, and the "UI" is initially text-based.

Here is the breakdown of the workflow and how you would interact with the agent.

---

## 🔁 Prototype Workflow: Query Submission and Execution

The prototype follows a simple but powerful command-line workflow that demonstrates the **Agentic Loop** (Observe $\rightarrow$ Think $\rightarrow$ Act).

| Step | Action | Description |
| :--- | :--- | :--- |
| **1. User Submission (Input)** | `agent_executor.invoke({"input": "..."})` | The user submits their request (the query) via a **Python function call** in your script or an interactive Python session. |
| **2. Coordinator Thinking (LLM)** | **`Thought`** (in verbose output) | The **Gemini LLM** inside the Coordinator Agent analyzes the request, checks its available tools (`job_search`, `submit_application`), and formulates a plan. |
| **3. Tool Execution (Action)** | **`Tool Call`** $\rightarrow$ **`Observation`** | The Coordinator Agent calls one of the specialized Python functions (the simulated agents). The function executes and returns its result (the `Observation`). |
| **4. Final Response** | `response["output"]` | The Coordinator Agent incorporates the observation into its final answer, which is then printed back to the user's **console/terminal**. |

Essentially, the entire interaction happens within a **single Python function call** (`.invoke()`), which executes the full multi-step loop.

---

## 🖥️ The User Interface (UI)

For a quick prototype, the UI is minimal. To move toward a more user-friendly demo, you need to add a simple web layer.

### 1. The Current "UI": The Command Line

* **Submission:** The input is a **string variable** passed to the `agent_executor.invoke()` method.
* **Result:** The output is a **dictionary** printed directly to the Python console, with the final answer being the value of the `"output"` key.
* **Verbosity:** The `verbose=True` setting in the `AgentExecutor` *acts as the UI* by showing the agent's internal thought process, tool calls, and observations, which is crucial for debugging and understanding the agent's logic.

### 2. Quick UI Enhancement: Streamlit or Gradio

If you want to rapidly add a true conversational interface without building a complex web application, the recommended tools are **Streamlit** or **Gradio**.

| Tool | How it Works | Submission/Result |
| :--- | :--- | :--- |
| **Streamlit (Recommended)** | A Python library that turns scripts into beautiful, interactive web apps. You can easily create a **chatbot interface** (text input and output history). | The user types into a chat box in a web browser, and the Streamlit app passes the input string to `agent_executor.invoke()` and displays the result as a chat message. |
| **Gradio** | Similar to Streamlit, it's fast for creating web demos, often used for quickly wrapping ML models or functions with a UI. | You define an input box and an output box, and it handles the basic web serving for your Python function. |

**Next Step:** You would take the code you have for the `agent_executor` and integrate it into a few lines of Streamlit code to create a functional, shareable web app.

That's a crucial point when prototyping: the fastest way to get a visual interface is by wrapping your existing Python code with a simple web framework. The recommended quick-win solution is to use **Streamlit**.

## 🖥️ Streamlit UI for the Agent Prototype

Streamlit allows you to convert your Python script into an interactive, web-based chatbot with minimal extra code. This immediately provides the conversational **UI** you're looking for.

### 1\. Workflow with Streamlit

| Action | User/System | Description |
| :--- | :--- | :--- |
| **User Query** | **User** (Web Browser) | The user types the request (e.g., "Find me a Senior SWE job in London") into the **`st.chat_input`** widget and hits Enter. |
| **Input Handling** | **Streamlit App** | The app captures the input, adds it to the **session state** (to maintain history), and passes the string to your existing `agent_executor.invoke()`. |
| **Agent Execution** | **Python/Gemini** (Backend) | Your Coordinator Agent runs its full logic (Tool Call $\rightarrow$ Observation $\rightarrow$ Final Answer) in the background. |
| **Result Display** | **Streamlit App** | The app receives the final text output from the `agent_executor` and renders it instantly as a reply bubble in the chat history using **`st.chat_message`**. |

### 2\. Streamlit Code Snippet (Conceptual)

You would take your existing `agent_executor` setup and wrap it in a file named `app.py`:

```python
import streamlit as st
# Import your existing agent_executor and tools here

# --- Initialize Session State for Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Render Previous Messages ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Handle User Input ---
if prompt := st.chat_input("Ask the Job Agent..."):
    # 1. Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Run the Coordinator Agent
    with st.chat_message("assistant"):
        # Display a loading spinner or streaming output here
        with st.spinner("Agent is planning..."):
            # Pass the prompt to your LangChain Agent Executor
            response = agent_executor.invoke({"input": prompt, "chat_history": ""})
            
            # 3. Get the final response
            final_response = response["output"]
            st.markdown(final_response)

    # 4. Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": final_response})
```

### 3\. Execution

1.  Save the complete Python file (including your agent and tool definitions) as `app.py`.
2.  Run it from your terminal: `streamlit run app.py`

This command launches a local web server, providing a **live conversational interface** that is powered by your multi-agent logic.

For a deeper dive into building a conversational AI application using Streamlit and LangChain, check out the video below.

-----

You can learn how to set up the chat history and input box for a quick conversational UI in this video: [How to Build an AI Chatbot in Python with LangChain & Streamlit](https://www.youtube.com/watch?v=Dyvad5vruIA).
http://googleusercontent.com/youtube_content/0

```
Provide a deployment plan, what is the folder /files structure and how to run the solution with streamlit as the UI
```

The shift from a command-line script to a deployable web application requires a standard **file structure** and a **deployment plan** focused on managing dependencies.

## 📁 Project Structure: Best Practices

A clean, structured folder helps manage the different components (UI, Agent Logic, and Dependencies) for deployment.

Your prototype structure should look like this:

```
job-chatbot-prototype/
├── app.py                      # The Streamlit UI and entry point
├── requirements.txt            # Lists all Python dependencies
├── agent_core.py               # Contains the Agent Executor and Tool definitions
└── .streamlit/                 # (Optional) For configuration files
    └── config.toml             # Configuration for Streamlit settings
```

### Key Files Explained:

| File Name | Purpose | Content |
| :--- | :--- | :--- |
| **`app.py`** | **UI Entry Point** | Handles the Streamlit layout, chat history (`st.session_state`), and calls the functions from `agent_core.py` to process the user's input. |
| **`agent_core.py`** | **Agent Logic** | Contains the reusable core functions: the `@tool` definitions (`job_search`, `submit_application`), the `system_prompt`, and the initialized `agent_executor`. |
| **`requirements.txt`** | **Deployment Dependencies** | A simple text file listing all necessary Python packages. **This is mandatory for cloud deployment.** |

-----

## 🚀 Deployment Plan: Running the Solution

The deployment plan covers two phases: **Local Execution** (development/testing) and **Cloud Deployment** (sharing).

### Phase 1: Local Execution

This is how you run the application on your computer using the command line.

#### 1\. Configure the Environment

Create a virtual environment to isolate your project dependencies:

```bash
# 1. Create a project directory and navigate into it
mkdir job-chatbot-prototype
cd job-chatbot-prototype

# 2. Create and activate the virtual environment
python3 -m venv venv
source venv/bin/activate  # Use '.\venv\Scripts\activate' on Windows

# 3. Create the requirements.txt file
# You will need at least: streamlit, google-genai, langchain, langchain-google-genai
pip install streamlit google-genai langchain langchain-google-genai
pip freeze > requirements.txt
```

#### 2\. Separate the Code

Move the Agent logic from the previous answer into a new file, `agent_core.py`, and adjust `app.py` to import it.

In **`agent_core.py`**:

  * Define all the `@tool` functions.
  * Define the `system_prompt`.
  * Define a single function, e.g., `get_agent_response(user_input)`, which initializes and runs the `agent_executor.invoke()`.

In **`app.py`**:

  * Import `get_agent_response` from `agent_core`.
  * Call this function when the user submits input (as shown in the previous answer's Streamlit snippet).

#### 3\. Run the App

Execute the Streamlit application from the root directory:

```bash
streamlit run app.py
```

This will open your application in your web browser, typically at `http://localhost:8501`.

### Phase 2: Cloud Deployment (Sharing)

For quick, free, and hassle-free deployment, **Streamlit Community Cloud** (or services like Hugging Face Spaces or Koyeb) is the best choice.

1.  **Version Control:** Commit your entire `job-chatbot-prototype` folder (including `app.py`, `agent_core.py`, and `requirements.txt`) to a **public GitHub repository**.
2.  **Secrets Management:** Since your agent relies on the `GEMINI_API_KEY`, you must secure it.
      * Create a folder named **`.streamlit`** in your project root.
      * Inside it, create a file named **`secrets.toml`**.
      * Add your API key to this file:
        ```toml
        # .streamlit/secrets.toml
        GEMINI_API_KEY = "your-actual-api-key-here"
        ```
      * *Note: Streamlit Community Cloud will automatically load this secret as an environment variable.*
3.  **Deployment Platform:** Use Streamlit Community Cloud (or another service) to connect to your GitHub repository.
4.  **Launch:** Select the repository and the main file (`app.py`). The platform reads `requirements.txt` to install dependencies, loads the secret, and runs `streamlit run app.py` for you.

-----

The video below provides a step-by-step guide on how to structure a Streamlit app and is relevant for organizing your agent components.

[Structuring and Organising Streamlit Apps](https://www.youtube.com/watch?v=MdjMC0PLJ2s)

The video is relevant because it demonstrates best practices for organizing a Streamlit application, which is necessary for a clean and successful deployment.
http://googleusercontent.com/youtube_content/1

```
Is Streamlit Community Cloud or HuggingFace Spaces better for phase 2?
```

For Phase 2 deployment of your Streamlit application, **Hugging Face Spaces** is generally the superior choice, as it is designed specifically for hosting Machine Learning (ML) and AI demos like your agent.

While **Streamlit Community Cloud** is simpler and highly integrated with Streamlit, Hugging Face Spaces offers greater flexibility and resource guarantees, even on its free tier.

Here is a comparison:

---

## 🆚 Comparison for Agent Deployment (Free Tier)

| Feature | Streamlit Community Cloud | Hugging Face Spaces (Streamlit SDK) | **Verdict for Your Agent** |
| :--- | :--- | :--- | :--- |
| **Primary Focus** | General data apps, dashboards. | ML/AI demos, models, and associated apps. | **Hugging Face Spaces** (Better context). |
| **Free Hardware** | Limited CPU/Memory; apps may sleep or time out easily under load. | **"CPU Basic" (2 vCPU, 16 GB RAM)** is generous for a free tier. | **Hugging Face Spaces** (More resources). |
| **Sleep Policy** | Apps often **sleep** after periods of inactivity. | Apps on the free tier also **sleep** but generally offer more stability when active. | Tie, both are free. |
| **Secrets Management** | Uses a dedicated `.streamlit/secrets.toml` file. | Uses **Hugging Face Secrets** (secure environment variables). | Tie, both are secure. |
| **Setup** | Extremely simple, just point to your GitHub repo. | Very simple: Point to your GitHub repo and select **Streamlit** as the SDK. | **Streamlit Community Cloud** (Slightly simpler). |
| **Visibility/Audience** | General Streamlit community. | Deeply embedded within the **ML/AI community** (Hugging Face Hub). | **Hugging Face Spaces** (Better visibility to target audience). |

---

## 🏆 Recommendation: Hugging Face Spaces

You should choose **Hugging Face Spaces** for the following reasons:

1.  **Resource Allocation:** Your agent uses the **Gemini API** for reasoning, which can be computationally intensive compared to a simple data visualization. Hugging Face's free **16 GB RAM and 2 vCPUs** provide a more stable and powerful environment than Streamlit Cloud's more constrained free tier, minimizing timeouts.
2.  **ML Ecosystem:** Spaces are designed for sharing ML-related applications. Your project aligns perfectly with this ecosystem, potentially increasing its visibility to people interested in multi-agent systems and LLM applications.
3.  **Flexibility for Growth:** Should you later decide to include a local, smaller LLM or a vector database for internal retrieval, Hugging Face provides competitive paid tiers with **GPU access** (like T4 or A10G), which is essential for scaling ML/AI components.

### Setup Checklist for Hugging Face Spaces

1.  Ensure your GitHub repository has the three required files: `app.py`, `agent_core.py`, and `requirements.txt`.
2.  Log into Hugging Face and click **"Create New Space."**
3.  Choose:
    * **Space name** (e.g., `Job-Chatbot-Agent`)
    * **SDK:** Select **Streamlit**
    * **Hardware:** Select **CPU Basic** (Free)
4.  After creation, link your **GitHub repository**.
5.  In the Space's settings, go to **"Secrets"** and create a new secret named **`GEMINI_API_KEY`**, pasting your actual API key as the value. This ensures your key is secure and available as an environment variable to your running app.

```
Is this a Sequential or Parallel Agent approach?
```

This agent design, as prototyped using the LangChain `AgentExecutor` with distinct tools, represents a **Sequential Agent Approach**, specifically employing a **Coordinator Pattern**.

Here's why and how it relates to the two concepts:

---

## 🔁 Sequential Agent Approach (Coordinator Pattern)

The prototype you created is sequential because the **Coordinator Agent** (the LLM) processes tasks one step at a time, relying on the output of the previous step to determine the next action.

* **The Flow is Linear:** When you submit a query like "Find a job and apply," the Coordinator must first call the **`job_search`** tool (simulated Agent) and *wait for the results* (Observation). Only after getting the job ID can it then proceed to call the **`submit_application`** tool (simulated Agent).
    * **Step 1:** User Query $\rightarrow$ **Coordinator** decides.
    * **Step 2:** Coordinator calls **Job Search Tool**.
    * **Step 3:** Job Search Tool returns job list.
    * **Step 4:** Coordinator asks User to select a job (Implicit step).
    * **Step 5:** Coordinator calls **Candidate Tool** (Application).
    * **Step 6:** Final Response.

This dependency structure, where one agent's action (or tool's output) is a prerequisite for the next agent's action, is the defining characteristic of a **Sequential** process.

---

## ⏸️ Difference from a Parallel Agent Approach

A **Parallel Agent Approach** would be structured very differently, generally requiring a more complex framework like **LangGraph** or **CrewAI** to manage the simultaneous operations.

* **No Inter-Dependency:** In a true parallel system, the agents work simultaneously on non-dependent tasks to save time.
    * *Example:* If the user asked, "Find me a Senior Engineer job **AND** summarize the company's recent stock performance," these two tasks are independent. A parallel coordinator could send the job search request and the financial summary request to two different agents *at the same time* and aggregate both results when they are complete.
* **The Job Chatbot Constraint:** The job application process fundamentally requires sequential steps (you can't apply for a job *before* you find one). Therefore, even in a more advanced multi-agent framework, the core workflow would still need to be **sequential**.

```

```

That's the most efficient way to build a prototype\! To ensure a smooth setup in VS Code, we'll create the three necessary files and the requirements list.

Here is the complete code, separated by filename, ready for copy-ppaste into your `job-chatbot-prototype` directory.

-----

## 📁 File Structure

```
job-chatbot-prototype/
├── app.py                      # Streamlit UI (Frontend)
├── agent_core.py               # Agent Logic and Tools (Backend)
└── requirements.txt            # Dependencies
```

-----

## 1\. `requirements.txt`

This file lists all the Python packages needed to run the application.

```txt
streamlit
google-genai
langchain
langchain-google-genai
```

-----

## 2\. `agent_core.py`

This file contains the core Sequential Agent logic, defining the tools and setting up the Coordinator Agent Executor.

```python
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import tool
from dotenv import load_dotenv

# Load environment variables from .env or Streamlit secrets
load_dotenv()

# --- Tool Definitions (Simulating Agent Actions) ---
# These mock the Job Search Agent and Candidate Agent functionality

@tool
def job_search(query: str, location: str) -> str:
    """
    Searches the mock job database for relevant job postings.
    Returns a list of matching job IDs and titles. Use this FIRST for finding jobs.
    """
    if "senior software engineer" in query.lower() and "london" in location.lower():
        return "Found 3 jobs: JobID 101 (Senior S/W Eng, TechCorp); JobID 102 (Lead Dev, Global Systems); JobID 103 (Architect, London Startups). Ask the user which JobID to apply for."
    elif "marketing" in query.lower():
        return "Found 2 jobs: JobID 201 (Marketing Manager, Remote); JobID 202 (SEO Specialist, UK)."
    else:
        return f"Found 1 general job matching '{query}' in {location}: JobID 99 (General Position)."

@tool
def submit_application(job_id: int, user_id: str) -> str:
    """
    Submits the application for the specified job ID using the candidate's profile.
    This simulates the Candidate Agent's final action. ONLY call this after a job_id is known.
    """
    return f"Application for JobID {job_id} submitted successfully for candidate {user_id}. A proactive follow-up reminder has been set for status updates."

@tool
def check_chat_history_for_context(user_id: str) -> str:
    """
    Retrieves the user's past interaction context to personalize the response or action.
    Use this to retrieve memory or preferences. The user ID is always 'User_A'.
    """
    return f"Retrieved context for {user_id}: Candidate prefers hybrid work, is willing to relocate, and previously applied to a role at TechCorp 2 weeks ago."

# Create a list of all available tools
available_tools = [job_search, submit_application, check_chat_history_for_context]

# --- Coordinator Agent Initialization ---

def get_agent_executor():
    """Initializes and returns the LangChain AgentExecutor (the Coordinator Agent)."""
    
    # 1. Initialize the Gemini Model (Pulls GEMINI_API_KEY from environment)
    # Use gemini-2.5-flash for its speed and strong function calling capabilities
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    except Exception as e:
        return f"Error initializing LLM: {e}. Please ensure GEMINI_API_KEY is set correctly."
    
    # 2. Define the System Prompt for the Coordinator Agent
    system_prompt = (
        "You are the powerful **Job Chatbot Coordinator Agent**. "
        "Your goal is to fulfill complex user requests by calling the appropriate tools. "
        "Analyze the user request, plan the necessary steps (Search, Context Check, Apply), "
        "and use the output from the tools to provide a final, helpful response. "
        "The user ID is always 'User_A'. Always use the tools when appropriate."
    )

    # 3. Create the Prompt Template
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    # 4. Create the Tool Calling Agent and Executor
    agent = create_tool_calling_agent(llm, available_tools, prompt)
    
    # Note: verbose=True prints the Thought/Action/Observation to the terminal
    agent_executor = AgentExecutor(agent=agent, tools=available_tools, verbose=True)
    
    return agent_executor
```

-----

## 3\. `app.py`

This file integrates the Streamlit UI with the Agent Executor, handling the chat history and input.

```python
import streamlit as st
from agent_core import get_agent_executor # Import your agent logic

# Initialize the Agent Executor once per session
@st.cache_resource
def initialize_agent():
    return get_agent_executor()

# --- Streamlit Application Setup ---
st.set_page_config(page_title="🤖 Job Chatbot Agent Prototype", layout="centered")
st.title("🤖 Job Chatbot Agent Prototype")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your Job Agent. How can I help you with your job search today?"}
    ]

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get the Agent Executor instance
agent_executor = initialize_agent()

# Handle user input
if prompt := st.chat_input("Find a Senior Software Engineer job in London..."):
    # 1. Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Run the Coordinator Agent
    with st.chat_message("assistant"):
        # Use a placeholder/spinner to show the agent is working
        with st.spinner("Agent is analyzing the request and executing tools..."):
            
            # Run the agent with the user's prompt
            # NOTE: We are ignoring chat_history for this simple prototype, but it can be used for memory.
            response = agent_executor.invoke({
                "input": prompt,
                "chat_history": "" 
            })
            
            # Get the final response
            final_response = response["output"]
            st.markdown(final_response)

    # 3. Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": final_response})

```
Provide me the full code by filename, ready to copy and paste into my vscode to run the prototype
```

## 💡 How to Run the Prototype

1.  **Create Files:** Create the three files (`app.py`, `agent_core.py`, `requirements.txt`) in a dedicated directory.
2.  **API Key:** For local running, create a file named **`.env`** in the same directory and add your key:
    ```
    # .env
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
    ```
3.  **Install Dependencies:** Open your terminal in the project directory and run:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Launch Streamlit:** Run the application:
    ```bash
    streamlit run app.py
    ```

The application will open in your browser, and you can test complex queries like "Find a Senior Software Engineer job in London and submit my application."

The video below gives an overview of how to build an AI agent interface with Streamlit, which directly relates to the structure we've implemented. [Building an Intelligent Multi-Tool AI Agent Interface Using Streamlit for Seamless Real-Time Interaction](https://www.google.com/search?q=https://www.youtube.com/watch%3Fv%3DFjIu29QWl-0) This video is relevant as it provides a visual context for the Streamlit-LangChain integration used in the prototype.

```
Looks like there are deployment issues using Langchain as there are many deprecated functions. Suggest a more stable tool, consider using google adk
```
That's a very common pain point with fast-moving open-source frameworks like LangChain. The best and most stable tool for building agents in the Google ecosystem is the **Google Agent Development Kit (ADK)**.

ADK is a **code-first, open-source Python framework** developed by Google, specifically designed for stability and integration with Gemini and Google Cloud services.

---

## 🚀 Recommended Tool: Google Agent Development Kit (ADK)

The Google ADK is the direct evolution of Google's internal agent development framework, providing a much more structured and production-ready environment than the constantly changing abstractions found in community-driven frameworks.

### Why ADK is More Stable and Better for Google AI

| Feature | Google ADK | LangChain (General OSS) |
| :--- | :--- | :--- |
| **Code Stability** | **High.** It has a bi-weekly release cadence and a stable branch (`pip install google-adk`), reducing breaking changes common in rapid OSS development. | **Moderate.** Extremely fast-moving, leading to frequent deprecation warnings and API changes, requiring constant code updates. |
| **Model Integration** | **Native & Optimized.** Built specifically for **Gemini** and Vertex AI, ensuring immediate support for features like enhanced Function Calling and advanced safety controls. | **Abstracted.** Connects via a generic wrapper (`langchain-google-genai`), which can sometimes lag behind native Gemini features. |
| **Multi-Agent Design** | **First-Class Support.** Provides built-in constructs like `SequentialAgent`, `ParallelAgent`, and an `Orchestrator` to manage complex flows, often simplifying the need for complex graph libraries. | Requires an additional layer like LangGraph or CrewAI to achieve robust multi-agent coordination. |
| **Deployment** | **"Deploy Anywhere."** Optimized for containerization and one-click scaling on Google Cloud services like **Vertex AI Agent Engine** or Cloud Run. | Requires manual configuration of containers, MLOps tooling, and integration with cloud-native features. |
| **Observability** | **Built-in.** Includes rich tracing, logging, and observability tools out-of-the-box, essential for debugging agent decisions in production. | Requires manual integration with third-party tools (e.g., LangSmith, Weights & Biases). |

---

## 🗺️ Migration Plan: From LangChain to ADK

Migrating your prototype's core logic to ADK will give you a cleaner, more robust structure, while still using the familiar concept of Tools (Functions).

### 1. Separate the Agent Components

Your current architecture already separates the logic well, which is perfect for ADK:

* **`app.py` (UI):** Stays mostly the same (Streamlit frontend).
* **`requirements.txt`:** Remove LangChain and add `google-adk`.
* **`agent_core.py` (Logic):** This is where the core changes occur. You'll switch from the LangChain `AgentExecutor` to defining an **ADK Agent** and its **Tools**.

### 2. Conceptual Code Transformation (ADK)

In ADK, you define the tools and the agent class directly.

| LangChain Prototype Concept | Google ADK Implementation |
| :--- | :--- |
| `@tool` decorator | The `@tool` decorator in ADK (or a simple Python function wrapped as a Tool) |
| `ChatGoogleGenerativeAI` | Configured directly in the ADK Agent, which is optimized for Gemini. |
| `agent_executor.invoke()` | Calling the ADK Agent's `.query()` method. |

This migration will give you a **stable, code-first foundation** that is ready for enterprise-grade deployment on Google Cloud when you are ready to scale.

```
Provide updated full code and dependencies ready to deploy, include deployment steps.
```
You're absolutely right to prioritize stability and look towards the **Google Agent Development Kit (ADK)** for a production-ready solution. ADK provides native, stable integration with Gemini and is designed for easy deployment to Google Cloud Run.

This solution uses the **ADK's `LlmAgent` with tools** to replicate the Coordinator $\rightarrow$ Tool workflow, which is the most robust starting point for an ADK-based agent.

-----

## 📁 Project Structure: ADK Standard

For ADK, the standard project structure requires a dedicated folder for your agent's core logic.

```
job-chatbot-adk/
├── job_agent/                  # The agent directory (becomes an ADK package)
│   ├── __init__.py             # Makes the directory a Python package
│   └── agent.py                # Contains the Agent definition and Tools
├── .env                        # Local environment variables (API Key)
├── requirements.txt            # Python dependencies
└── app.py                      # Streamlit UI (Frontend)
```

-----

## 1\. `requirements.txt`

This file lists the necessary packages. Note the shift from LangChain to `google-adk` and the removal of `langchain-google-genai`.

```txt
streamlit
google-adk
python-dotenv
```

-----

## 2\. `job_agent/agent.py`

This file defines the **ADK Agent** and its custom tools (functions).

```python
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import tool
from typing import Dict, Any

# Define the model to be used by the agent
# LiteLlm is a flexible wrapper that handles environment-based auth (e.g., GEMINI_API_KEY)
# In a full Vertex AI deployment, this would use a VertexAILlm class.
model = LiteLlm("gemini-2.5-flash")

# --- Tool Definitions (Functions) ---

@tool
def job_search(query: str, location: str) -> Dict[str, Any]:
    """
    Searches the mock job database for relevant job postings.
    Returns a dictionary with a list of matching job IDs and titles. Use this FIRST for finding jobs.
    """
    if "senior software engineer" in query.lower() and "london" in location.lower():
        return {
            "status": "success",
            "jobs": [
                {"id": 101, "title": "Senior S/W Eng, TechCorp"},
                {"id": 102, "title": "Lead Dev, Global Systems"}
            ],
            "message": "Found 2 matching senior roles in London. Please ask the user which ID to apply for."
        }
    else:
        return {"status": "success", "jobs": [], "message": f"Found 1 general job matching '{query}' in {location}: JobID 99."}

@tool
def submit_application(job_id: int, user_id: str) -> Dict[str, Any]:
    """
    Submits the application for the specified job ID using the candidate's profile.
    This simulates the Candidate Agent's final action. ONLY call this after a job_id is known.
    """
    if job_id in [101, 102]:
        return {"status": "submitted", "message": f"Application for JobID {job_id} submitted successfully for candidate {user_id}. A proactive follow-up reminder has been set."}
    else:
        return {"status": "error", "message": f"JobID {job_id} not found or application failed."}

# --- Coordinator Agent Definition ---

root_agent = Agent(
    model=model,
    name="JobChatbotCoordinator",
    description="An expert coordinator for job search and application.",
    instruction=(
        "You are the **Job Chatbot Coordinator Agent**. Your goal is to fulfill complex user requests "
        "by intelligently calling the appropriate tools. Analyze the user request, plan the necessary steps "
        "(Search, Apply), and use the output from the tools to provide a final, helpful response. "
        "The user ID is always 'User_A'. Always use the tools when appropriate."
    ),
    tools=[job_search, submit_application] # Register the tools here
)

# You must define an agent instance named 'root_agent' for ADK to find it.
# In a SequentialAgent scenario, root_agent would be the SequentialAgent instance.
```

-----

## 3\. `job_agent/__init__.py`

This file can be empty, but must exist to define the `job_agent` directory as a Python package.

```python
# Leave this file empty
```

-----

## 4\. `app.py`

This Streamlit UI now imports and uses the ADK agent via the ADK's `Runner` component, which manages the session.

```python
import streamlit as st
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from job_agent.agent import root_agent # Import the ADK agent

# Load API key from .env file for local development
load_dotenv()

# --- ADK Setup ---

# Initialize the Runner, which handles agent execution and state
@st.cache_resource
def initialize_runner():
    # Use InMemorySessionService for the prototype; use a database for production
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="job_chatbot_adk_app",
        session_service=session_service
    )
    return runner

# --- Streamlit Application Setup ---

st.set_page_config(page_title="🤖 ADK Job Chatbot Prototype", layout="centered")
st.title("🤖 ADK Job Chatbot Prototype")

# Initialize chat history and session IDs
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your stable ADK Job Agent. How can I help you today?"}
    ]
if "session_id" not in st.session_state:
    # Use a fixed ID for the prototype
    st.session_state.session_id = "streamlit_session_1"
if "user_id" not in st.session_state:
    st.session_state.user_id = "User_A"

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get the Runner instance
adk_runner = initialize_runner()

# Handle user input
if prompt := st.chat_input("Find a Senior Software Engineer job in London..."):
    # 1. Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Run the ADK Agent asynchronously
    with st.chat_message("assistant"):
        with st.spinner("ADK Agent is processing..."):
            
            # ADK uses async streams, but we wrap it for the Streamlit synchronous execution
            import asyncio
            
            async def stream_agent_response():
                full_response = ""
                # Use async_stream_query to interact with the agent
                async for event in adk_runner.async_stream_query(
                    user_id=st.session_state.user_id,
                    session_id=st.session_state.session_id,
                    message=prompt
                ):
                    # ADK returns events; we look for the final text response
                    if event.final_response and event.final_response.text_response:
                        return event.final_response.text_response
                return "The agent returned no final response."

            # Execute the async function using asyncio
            try:
                final_response = asyncio.run(stream_agent_response())
            except Exception as e:
                final_response = f"An error occurred during agent execution: {e}"

            st.markdown(final_response)

    # 3. Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": final_response})
```

-----

## 5\. Deployment Steps: Local & Cloud Run

### Phase 1: Local Execution

1.  **Setup Environment:**
    ```bash
    # Create project directory
    mkdir job-chatbot-adk
    cd job-chatbot-adk

    # Create the agent folder
    mkdir job_agent

    # Create .env (for local testing only)
    echo 'GEMINI_API_KEY="YOUR_API_KEY_HERE"' > .env

    # Install dependencies
    pip install -r requirements.txt
    ```
2.  **Copy Code:** Copy the code snippets into their respective files.
3.  **Run Streamlit:**
    ```bash
    streamlit run app.py
    ```

### Phase 2: Cloud Run Deployment (Recommended for ADK)

For a production-ready, scalable deployment, **Google Cloud Run** is the optimal choice for ADK agents, and ADK provides a dedicated CLI tool.

1.  **Install Google Cloud CLI (gcloud):** Ensure you have gcloud installed and authenticated (`gcloud auth login`).
2.  **Containerize (Optional but good practice):** Create a minimal `Dockerfile` to package your app.
3.  **Use `adk deploy` (Recommended):** The ADK command-line interface is designed to automate this process.

Assuming your agent folder is structured as above (`job_agent/`):

```bash
# Set your environment variables in the terminal
export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1" # Or another region

# Deploy the agent using the ADK CLI command
# The `--with_ui` flag deploys the built-in ADK Web UI for testing!
adk deploy cloud_run \
    --project=$GOOGLE_CLOUD_PROJECT \
    --region=$GOOGLE_CLOUD_LOCATION \
    --app_name="job_chatbot" \
    --agent_path="./job_agent" \
    --with_ui
```

*Alternatively, if you must use the Streamlit UI on Cloud Run, you would deploy the `app.py` script as a standard Streamlit app using a custom Dockerfile.*

This video demonstrates how to transition your ADK agent to a scalable service on Cloud Run. [Deploy ADK Agent to Cloud Run | Google Cloud ADK Tutorial](https://www.youtube.com/watch?v=zA0Y3smlavA)
http://googleusercontent.com/youtube_content/2