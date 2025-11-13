# frontend/app.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from agent.agent import run_agent_sync

st.title("Job Recommendations & Skill Gap Analysis")

query = st.text_input("Enter job search query:")
resume = st.text_area("Paste your resume (optional)")

if st.button("Submit"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Fetching jobs, analyzing gaps, and synthesizing insights..."):
            result = run_agent_sync(query, resume if resume else None)
            st.subheader("LLM Insights")
            st.write(result)