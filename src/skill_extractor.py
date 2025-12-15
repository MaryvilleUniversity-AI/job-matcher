"""
Highlight matching and missing skills.
"""

import string

def clean_text(text):
    """
    Converts text to lowercase and removes punctuation.
    """
    return text.lower().translate(str.maketrans('', '', string.punctuation))

# Extract skills from resume and job description
def extract_skills(resume_text, job_text, skills):
    """
    Compare resume text against a list of skills

    Args:
        resume_text (str): The text of the resume.
        job_text (str): The text of the job description.
        skills (list): A list of skills to check against.
    
    Returns:
        matched (list): Skills found in the resume.
        missing (list): Skills not found in the resume.
    """
    resume_clean = clean_text(resume_text)

    matched = [skill for skill in skills if skill.lower() in resume_clean]
    missing = [skill for skill in skills if skill.lower() not in resume_clean]

    return matched, missing

# Extract required skills from job description
def extract_skills_from_job(job_text, skills):
    """
    Extracts skills from the job description based on a predefined list.

    Args:
        job_text (str): The text of the job description.
        skills (list): A list of skills to check against.

    Returns:
        skills_found (list): Skills found in the job description.
    """
    job_clean = clean_text(job_text)
    skills_found = [skill for skill in skills if skill.lower() in job_clean]
    return skills_found