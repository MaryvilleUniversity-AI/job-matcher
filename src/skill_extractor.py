"""
Highlight matching and missing skills.
"""

# Extract skills from resume and job description
def extract_skills(resume_text, job_text, skills):
    resume_words = resume_text.lower()
    job_words = job_text.lower()
    skills_lower = [skill.lower() for skill in skills]

    matched = []
    missing = []

    for skill in skills_lower:
        if skill in resume_text:
            matched.append(skill)
        else:
            missing.append(skill)

    return matched, missing

# Extract required skills from job description
def extract_skills_from_job(job_text, skills):
    """
    Returns a list of skills mentioned in the job description
    from a predefined list of common skills.
    """
    job_words = job_text.lower()
    skills_found = [skill for skill in skills if skill.lower() in job_words]
    return skills_found