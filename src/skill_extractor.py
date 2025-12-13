"""
Highlight matching and missing skills.
"""

def extract_skills(resume_text, job_text, skills):
    resume_words = set(word.lower().strip(".,") for word in resume_text.split())
    job_words = set(word.lower().strip(".,") for word in job_text.split())
    skills_set = set(skill.lower() for skill in skills)

    matched = skills_set & resume_words & job_words
    missing = skills_set - resume_words

    return list(matched), list(missing)