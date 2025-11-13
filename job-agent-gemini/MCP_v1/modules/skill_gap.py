# modules/skill_gap.py
def analyze_skill_gap(resume_text, jobs):
    # Simple comparison: list skills missing in resume
    resume_skills = set(resume_text.lower().split())
    gaps = {}
    for job in jobs:
        missing = [skill for skill in job["skills"] if skill.lower() not in resume_skills]
        gaps[job["title"]] = missing
    return gaps