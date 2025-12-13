"""
Measure how similar resume and job description are.
"""

from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(resume_vector, job_vector):
    score = cosine_similarity(resume_vector, job_vector)
    return score[0][0] * 100