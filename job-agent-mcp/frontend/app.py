import sys
import os
import streamlit as st
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agent.agent import run_agent_sync  # use synchronous wrapper

st.set_page_config(page_title="AI Job Chatbot", layout="wide")
st.title("AI-Driven Job Recommendation Chatbot")

query = st.text_input("Enter job search query (e.g., 'Data Analyst Singapore'):")
resume = st.text_area("Paste your resume text (optional):")

output_area = st.empty()  # placeholder to show LLM output

if st.button("Submit"):
    if not query:
        st.warning("Please enter a query first!")
    else:
        output_area.text("Processing …")
        result = run_agent_sync(query, resume if resume else None)
        output_area.markdown(result if result else "No output received from agent.")