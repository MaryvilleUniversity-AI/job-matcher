import streamlit as st
import io
from pathlib import Path
from docx import Document
from pypdf import PdfReader
from preprocess import preprocess
from vectorize import vectorize
from similarity import calculate_similarity
from skill_extractor import extract_skills, extract_skills_from_job
from common_skills import common_skills

st.set_page_config(page_title="Resume Matcher", layout="wide", initial_sidebar_state="expanded")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_RESUME_PATH = PROJECT_ROOT / "data" / "sample_resumes" / "resume1.txt"
SAMPLE_JOB_PATH = PROJECT_ROOT / "data" / "job_descriptions" / "job1.txt"

def read_sample_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def extract_uploaded_text(uploaded_file, input_label: str) -> str:
    filename = (uploaded_file.name or "").lower()
    file_bytes = uploaded_file.getvalue()

    try:
        if filename.endswith(".txt"):
            return file_bytes.decode("utf-8", errors="ignore")

        if filename.endswith(".pdf"):
            reader = PdfReader(io.BytesIO(file_bytes))
            return "\n".join((page.extract_text() or "") for page in reader.pages)

        if filename.endswith(".docx"):
            document = Document(io.BytesIO(file_bytes))
            return "\n".join(paragraph.text for paragraph in document.paragraphs)
    except Exception as exc:
        st.error(f"Could not read {input_label} file: {exc}")
        return ""

    st.error(f"Unsupported file type for {input_label}. Please upload .txt, .pdf, or .docx.")
    return ""

if "sample_resume_text" not in st.session_state:
    st.session_state.sample_resume_text = ""
if "sample_job_text" not in st.session_state:
    st.session_state.sample_job_text = ""
if "selected_resume_sample" not in st.session_state:
    st.session_state.selected_resume_sample = False
if "selected_job_sample" not in st.session_state:
    st.session_state.selected_job_sample = False

st.markdown("""
<style>
.block-container {padding-top: 1.2rem; padding-bottom: 1rem;}
.card {
    background: #111827;
    border: 1px solid #374151;
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 10px;
}
.badge-ok {color:#22c55e; font-weight:600;}
.badge-miss {color:#ef4444; font-weight:600;}
</style>
""", unsafe_allow_html=True)

st.title("🎯 Resume Matcher")
st.caption("Compare a resume against a job description using text similarity + skill coverage.")

# Sidebar inputs
with st.sidebar:
    st.header("Inputs")
    resume_file = st.file_uploader("Upload Resume (.txt, .pdf, .docx)", type=["txt", "pdf", "docx"])
    job_file = st.file_uploader("Upload Job Description (.txt, .pdf, .docx)", type=["txt", "pdf", "docx"])
    show_raw = st.toggle("Show raw processed text", value=False)

    st.divider()
    st.subheader("Quick Samples")
    c1, c2 = st.columns(2)
    resume_button_type = "primary" if st.session_state.selected_resume_sample else "secondary"
    job_button_type = "primary" if st.session_state.selected_job_sample else "secondary"

    if c1.button("Use Sample Resume", type=resume_button_type):
        if st.session_state.selected_resume_sample:
            st.session_state.sample_resume_text = ""
            st.session_state.selected_resume_sample = False
        else:
            st.session_state.sample_resume_text = read_sample_text(SAMPLE_RESUME_PATH)
            st.session_state.selected_resume_sample = True
        st.rerun()
    if c2.button("Use Sample Job", type=job_button_type):
        if st.session_state.selected_job_sample:
            st.session_state.sample_job_text = ""
            st.session_state.selected_job_sample = False
        else:
            st.session_state.sample_job_text = read_sample_text(SAMPLE_JOB_PATH)
            st.session_state.selected_job_sample = True
        st.rerun()
    if st.button("Clear Samples"):
        st.session_state.sample_resume_text = ""
        st.session_state.sample_job_text = ""
        st.session_state.selected_resume_sample = False
        st.session_state.selected_job_sample = False
        st.rerun()

# Prefer uploaded files; fallback to selected samples
raw_resume_text = (
    extract_uploaded_text(resume_file, "resume")
    if resume_file
    else st.session_state.sample_resume_text
)
raw_job_text = (
    extract_uploaded_text(job_file, "job description")
    if job_file
    else st.session_state.sample_job_text
)

if raw_resume_text and raw_job_text:
    with st.spinner("Processing files and calculating match..."):
        resume_text = preprocess(raw_resume_text)
        job_text = preprocess(raw_job_text)

        vectors = vectorize([resume_text, job_text])
        score = float(calculate_similarity(vectors[0], vectors[1]))

        job_skills = extract_skills_from_job(job_text, common_skills)
        matched, missing = extract_skills(resume_text, job_text, job_skills)

        total_skills = len(matched) + len(missing)
        skill_match_pct = (len(matched) / total_skills * 100) if total_skills > 0 else 0.0

    # KPI row
    c1, c2, c3 = st.columns(3)
    c1.metric("Text Similarity", f"{score:.2f}%")
    c2.metric("Skill Coverage", f"{skill_match_pct:.2f}%")
    c3.metric("Matched Skills", f"{len(matched)} / {total_skills}")

    st.divider()
    st.markdown("#### 📊 Overview")
    st.markdown("**Overall Text Similarity**")
    st.progress(max(0, min(100, int(score))))
    st.markdown("**Skill Coverage**")
    st.progress(max(0, min(100, int(skill_match_pct))))

    st.divider()
    st.markdown("#### 🧩 Skills")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### ✅ Matched Skills")
        if matched:
            for skill in sorted(matched):
                st.markdown(f"<div class='card'><span class='badge-ok'>{skill}</span></div>", unsafe_allow_html=True)
        else:
            st.info("No matched skills found.")
    with col2:
        st.markdown("##### ❌ Missing Skills")
        if missing:
            for skill in sorted(missing):
                st.markdown(f"<div class='card'><span class='badge-miss'>{skill}</span></div>", unsafe_allow_html=True)
        else:
            st.success("No missing skills.")

    st.divider()
    st.markdown("#### 📝 Processed Text")
    if show_raw:
        text_col1, text_col2 = st.columns(2)
        with text_col1:
            with st.expander("View Processed Resume Text", expanded=False):
                st.text(resume_text)
        with text_col2:
            with st.expander("View Processed Job Description Text", expanded=False):
                st.text(job_text)
    else:
        st.info("Enable **Show raw processed text** in the sidebar to view text.")
else:
    st.info("Upload both files, or click both sample buttons in the sidebar to begin.")