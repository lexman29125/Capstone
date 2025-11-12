# modules/embeddings.py
def rank_jobs_by_query(query, jobs):
    # Example simple ranking: jobs containing query word first
    ranked = sorted(jobs, key=lambda j: query.lower() in j["title"].lower(), reverse=True)
    return ranked