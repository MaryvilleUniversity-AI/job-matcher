import streamlit as st
from preprocess import preprocess
from vectorize import vectorize
from similarity import calculate_similarity
from skill_extractor import extract_skills, extract_skills_from_job
from common_skills import common_skills

st.set_page_config(page_title="Resume Matcher", layout="wide")
st.title("Resume Matcher")
st.write("Compare a resume with a job description to see skill match and fit score.")

# File uploads
resume_file = st.file_uploader("Upload Resume (.txt)", type=["txt"])
job_file = st.file_uploader("Upload Job Description (.txt)", type=["txt"])

if resume_file and job_file:
    # Read and preprocess files
    resume_text = preprocess(resume_file.read().decode("utf-8"))
    job_text = preprocess(job_file.read().decode("utf-8"))

    with st.expander("View Resume"):
        st.text(resume_text)
    with st.expander("View Job Description"):
        st.text(job_text)

    # Vectorize and calculate similarity
    vectors = vectorize([resume_text, job_text])
    score = calculate_similarity(vectors[0], vectors[1])

    # Extract skills dynamically from the job description
    job_skills = extract_skills_from_job(job_text, common_skills)

    # Compare resume vs job skills
    matched, missing = extract_skills(resume_text, job_text, job_skills)

    # Skill coverage percentage
    skill_match_pct = (
        len(matched) / (len(matched) + len(missing)) * 100 
        if (len(matched) + len(missing)) > 0 
        else 0
    )

    # Display Text Similarity score with progress bar
    st.markdown("### Overall Text Similarity")
    st.progress(int(score))
    st.write(f"**Text Similarity Score:** {score:.2f}%")

    # Display skill coverage match
    st.markdown("### Skill Coverage")
    st.progress(int(skill_match_pct))
    st.write(f"**Skill Coverage:** {skill_match_pct:.2f}%")

    # Display matched and missing skills side by side
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Matched Skills")
        if matched:
            for skill in matched:
                st.markdown(f"<span style='color:green'>✅ {skill}</span>", unsafe_allow_html=True)
        else:
            st.write("No matched skills found.")
    with col2:
        st.markdown("### Missing Skills")
        if missing:
            for skill in missing:
                st.markdown(f"<span style='color:red'>❌ {skill}</span>", unsafe_allow_html=True)
        else:
            st.write("No missing skills!")
else:
    st.info("Upload both a resume and a job description to see the match results.")