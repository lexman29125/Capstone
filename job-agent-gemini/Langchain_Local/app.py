import streamlit as st
from agent_core import get_agent_executor # Import your agent logic
# NEW: Import LangChain message classes for history conversion
from langchain_core.messages import HumanMessage, AIMessage 

# Function to convert Streamlit history format to LangChain BaseMessage format
def convert_streamlit_history_to_langchain(messages):
    """
    Converts the list of dicts in st.session_state.messages 
    into a list of LangChain BaseMessage objects for agent memory.
    """
    langchain_messages = []
    # Skip the very first initial message, as it's not part of the agent's turn history
    for message in messages[1:]: 
        if message["role"] == "user":
            langchain_messages.append(HumanMessage(content=message["content"]))
        # It's important to keep the content of the assistant messages intact for memory
        elif message["role"] == "assistant":
            langchain_messages.append(AIMessage(content=message["content"]))
    return langchain_messages


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
            
            # **NEW: Convert and pass the full chat history**
            history_for_agent = convert_streamlit_history_to_langchain(st.session_state.messages)

            # Run the agent with the user's prompt
            response = agent_executor.invoke({
                "input": prompt,
                "chat_history": history_for_agent # Pass the converted history
            })
            
            # Get the final response
            final_response = response["output"]
            st.markdown(final_response)

    # 3. Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": final_response})