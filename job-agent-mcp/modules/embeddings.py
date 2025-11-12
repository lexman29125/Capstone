from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def rank_jobs_by_query(query: str, jobs: list):
    if not jobs:
        return []

    query_vec = model.encode(query, convert_to_tensor=True)
    job_vecs = model.encode([job['description'] for job in jobs], convert_to_tensor=True)

    cosine_scores = util.cos_sim(query_vec, job_vecs)[0]
    ranked_jobs = sorted(
        zip(jobs, cosine_scores.tolist()),
        key=lambda x: x[1],
        reverse=True
    )
    return [job for job, score in ranked_jobs]