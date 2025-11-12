# modules/__init__.py
from .utils import extract_skills_from_resume
from .skill_gap import analyze_skill_gap
from .job_api import fetch_live_jobs
from .embeddings import rank_jobs_by_query