import requests

FIND_SG_JOBS_API = "https://api.findsgjobs.gov.sg/v1/jobs"

def fetch_live_jobs():
    try:
        response = requests.get(FIND_SG_JOBS_API)
        response.raise_for_status()
        jobs_raw = response.json().get('jobs', [])
    except Exception:
        jobs_raw = []

    jobs = []
    for j in jobs_raw:
        jobs.append({
            'title': j.get('jobTitle', 'Unknown'),
            'company': j.get('companyName', 'Unknown'),
            'description': j.get('jobDescription', ''),
            'skills': j.get('skills', [])
        })
    return jobs