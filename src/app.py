import streamlit as st
from preprocess import preprocess
from vectorize import vectorize
from similarity import calculate_similarity
from skill_extractor import extract_skills

with open("data/sample_resumes/resume1.txt") as r:
    resume = preprocess(r.read())

with open("data/job_descriptions/job1.txt") as j:
    job = preprocess(j.read())

# Debug: Make sure text is being read
print("RESUME:", resume[:200])
print("JOB:", job[:200])

# Vectorize
vectors = vectorize([resume, job])
score = calculate_similarity(vectors[0], vectors[1])

skills = ["python", "sql", "machine learning", "data analysis"]
matched, missing = extract_skills(resume, job, skills)

st.write(f"**Match Score:** {score:.2f}%")
st.write("**Matched Skills:**")
for skill in matched:
    st.write(f"- {skill}")
st.write("**Missing Skills:**")
for skill in missing:
    st.write(f"- {skill}")