import streamlit as st
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from job_agent.agent import root_agent # Import the ADK agent

# Load API key from .env file for local development
load_dotenv()

# --- ADK Setup ---

# Initialize the Runner once per session
@st.cache_resource
def initialize_runner():
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

    # 2. Run the ADK Agent synchronously using .run()
    with st.chat_message("assistant"):
        with st.spinner("ADK Agent is processing..."):
            
            try:
                # FIXED: Passing prompt as the third positional argument (user_id, session_id, prompt)
                response_event = adk_runner.run(
                    st.session_state.user_id,
                    st.session_state.session_id,
                    prompt
                )
                
                # Extract the final text response from the event object
                # We check for the final_response field and then the text_response part
                final_response = response_event.final_response.text_response
                
            except Exception as e:
                # Catch any errors during the ADK execution
                final_response = f"An error occurred during agent execution: {e}"

            st.markdown(final_response)

    # 3. Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": final_response})