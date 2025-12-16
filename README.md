# Resume Matcher

A **Resume Matcher** web application that compares a resume against a job
description, calculates overall fit, and highlights matched and missing
skills. Built with **Python** and **Streamlit**, it leverages natural language processing to provide insights on skill alignment and resume fit.

---

## Features

- **File Uploads**: Upload resume and job description as `.txt` files.
- **Text Similarity**: Calculates overall text similarity between resume and job description.
- **Matched & Missing Skills**: Displays matched and missing skills clearly with visual indicators.
- **Skill Coverage Score**: Shows the percentage of required skills covered by the resume.
- **User-Friendly Interface**: Expandable sections to view full text and clean column layout for matched/missing skills.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/MaryvilleUniversity-AI/job-matcher.git
cd resume-matcher
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

**Dependencies include**:

- `streamlit`
- `nltk`
- `scikit-learn`

## Usage

1. Run the Streamlit app:

```bash
streamlit run src/app.py
```

2. Upload your **resume** and **job description** as `.txt` files.
3. View the results:

- **Overall Text Similarity**
- **Skill Coverage %**
- **Matched Skills** ✅
- **Missing Skills** ❌

## Project Structure

```powershell
resume-matcher/
│
├── src/
│   ├── app.py                # Main Streamlit app
│   ├── preprocess.py         # Text preprocessing functions
│   ├── vectorize.py          # Text vectorization
│   ├── similarity.py         # Cosine similarity calculation
│   ├── skill_extractor.py    # Skill extraction functions
│   └── common_skills.py      # Predefined list of common skills
│
├── data/
│   ├── sample_resumes/       # Example resume files
│   └── job_descriptions/     # Example job description files
│
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## How it Works

1. **Preprocessing**: Clean and tokenizes text from uploaded files.
2. **Vectorization**: Converts txt into numerical vectors using `CountVectorizer` or `TF-IDF`.
3. **Similarity Calculation**: Computes cosine similarity between the resume and job description vectors.
4. **Skill Extraction**: Extracts skills from job description based on a predefined list (`common_skills`).
5. **Skill Matching**: Compares resume content against extracted skills to determine matched and missing skills.
6. **UI Display**: Shows results in a Streamlit interface with progress bars and clear visual indicators.

## Example Output

**Text Similarity Score**: 43.93%
**Skill Coverage**: 82%

**Matched Skills**:
✅ python
✅ sql
✅ pandas
✅ numpy

**Missing Skills**:
❌ aws
❌ communication skills

## Future Improvements

- Add support for PDF and DOCX resume uploads.
- Use NLP models for semantic skill matching.
- Highlight missing skills in suggested resume improvements.
- Weight skills differently based on importance in job description.
- Add charts for visual comparison of skills coverage.

## License
This project is open-source under the MIT License.
