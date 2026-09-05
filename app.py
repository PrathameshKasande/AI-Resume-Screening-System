import streamlit as st
import pandas as pd

from src.resume_parser import extract_resume_data
from src.text_preprocessor import clean_text
from src.skill_extractor import extract_skills
from src.feature_extractor import create_tfidf_vectors
from src.similarity import (
    calculate_tfidf_similarity,
    calculate_semantic_similarity
)
from src.scoring import calculate_skill_match, calculate_final_score
from src.skill_gap import find_skill_gap
from src.explanation import generate_explanation
from src.ranking import rank_candidates


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Resume Intelligence Screening System",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #94a3b8;
        margin-bottom: 2rem;
    }

    .section-heading {
        font-size: 1.35rem;
        font-weight: 700;
        margin-top: 1.2rem;
        margin-bottom: 0.5rem;
    }

    .pipeline-card {
        padding: 1rem;
        border: 1px solid #334155;
        border-radius: 12px;
        text-align: center;
        min-height: 120px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "results" not in st.session_state:
    st.session_state.results = None

if "analyzed_jd" not in st.session_state:
    st.session_state.analyzed_jd = ""

if "analyzed_jd_skills" not in st.session_state:
    st.session_state.analyzed_jd_skills = []

if "jd_input" not in st.session_state:
    st.session_state.jd_input = ""

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0


# ============================================================
# CLEAR ANALYSIS CALLBACK
# ============================================================

def clear_analysis():
    """
    Clear all previous analysis data.

    This function is used as a Streamlit button callback.
    Callbacks run before widgets are recreated, which allows
    the Job Description and file uploader to reset safely.
    """

    # Clear dashboard and analysis results
    st.session_state.results = None
    st.session_state.analyzed_jd = ""
    st.session_state.analyzed_jd_skills = []

    # Clear Job Description text area
    st.session_state.jd_input = ""

    # Create a new file uploader instance
    st.session_state.uploader_key += 1


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_match_label(score):
    """Return a readable match category based on the final score."""

    if score >= 80:
        return "Excellent Match 🟢"
    elif score >= 65:
        return "Strong Match 🔵"
    elif score >= 50:
        return "Moderate Match 🟡"
    return "Low Match 🔴"


def process_candidate(resume_file, jd_text, jd_skills):
    """
    Run the complete NLP/ML screening pipeline
    for one candidate resume.
    """

    # Extract resume text
    resume_data = extract_resume_data(resume_file)

    if not resume_data:
        return None

    resume_text = resume_data.get("text", "")
    candidate_name = resume_data.get(
        "candidate_name",
        resume_file.name
    )

    if not resume_text.strip():
        return None

    # --------------------------------------------------------
    # NLP PREPROCESSING
    # --------------------------------------------------------

    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(jd_text)

    # --------------------------------------------------------
    # SKILL EXTRACTION
    # --------------------------------------------------------

    resume_skills = extract_skills(cleaned_resume)

    # --------------------------------------------------------
    # TF-IDF FEATURE EXTRACTION
    # --------------------------------------------------------

    resume_vector, jd_vector = create_tfidf_vectors(
        cleaned_resume,
        cleaned_jd
    )

    tfidf_score = calculate_tfidf_similarity(
        resume_vector,
        jd_vector
    )

    # --------------------------------------------------------
    # SEMANTIC SIMILARITY
    # --------------------------------------------------------

    semantic_score = calculate_semantic_similarity(
        cleaned_resume,
        cleaned_jd
    )

    # --------------------------------------------------------
    # SKILL MATCHING
    # --------------------------------------------------------

    skill_score = calculate_skill_match(
        resume_skills,
        jd_skills
    )

    # --------------------------------------------------------
    # HYBRID FINAL SCORE
    # --------------------------------------------------------

    final_score = calculate_final_score(
        semantic_score=semantic_score,
        tfidf_score=tfidf_score,
        skill_score=skill_score
    )

    # --------------------------------------------------------
    # SKILL GAP ANALYSIS
    # --------------------------------------------------------

    skill_gap = find_skill_gap(
        resume_skills,
        jd_skills
    )

    # --------------------------------------------------------
    # EXPLAINABLE RESULT
    # --------------------------------------------------------

    explanation = generate_explanation(
        final_score=final_score,
        matched_skills=skill_gap["matched_skills"],
        missing_skills=skill_gap["missing_skills"],
        semantic_score=semantic_score
    )

    # Return complete candidate analysis
    return {
        "candidate_name": candidate_name,
        "file_name": resume_file.name,
        "final_score": round(final_score, 2),
        "semantic_score": round(semantic_score * 100, 2),
        "tfidf_score": round(tfidf_score * 100, 2),
        "skill_score": round(skill_score * 100, 2),
        "resume_skills": resume_skills,
        "matched_skills": skill_gap["matched_skills"],
        "missing_skills": skill_gap["missing_skills"],
        "explanation": explanation
    }


# ============================================================
# SIDEBAR - RESUME UPLOAD ONLY
# ============================================================

with st.sidebar:

    st.title("📄 Resume Upload")

    st.caption(
        "Upload one or more candidate resumes in PDF format."
    )

    resume_files = st.file_uploader(
        "Upload Resume PDFs",
        type=["pdf"],
        accept_multiple_files=True,
        key=f"resume_uploader_{st.session_state.uploader_key}"
    )

    if resume_files:
        st.success(
            f"✓ {len(resume_files)} resume(s) ready for analysis"
        )
    else:
        st.info("Upload resume PDFs to begin.")

    st.divider()

    st.caption(
        "🤖 Powered by NLP, TF-IDF, semantic similarity "
        "and skill matching."
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    '<div class="hero-title">🤖 AI Resume Intelligence Screening System</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-subtitle">
        AI-powered candidate screening using Natural Language Processing,
        semantic similarity, skill matching and hybrid scoring.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# NLP PIPELINE
# ============================================================

with st.expander("🧠 View AI/NLP Screening Pipeline"):

    cols = st.columns(5)

    pipeline_steps = [
        ("📄", "Resume Parsing", "Extract PDF text"),
        ("🧹", "NLP Processing", "Clean & normalize"),
        ("🔍", "Feature Extraction", "Skills + TF-IDF"),
        ("🧠", "AI Matching", "Semantic similarity"),
        ("🏆", "Ranking", "Score candidates")
    ]

    for col, step in zip(cols, pipeline_steps):

        icon, title, description = step

        col.markdown(
            f"""
            <div class="pipeline-card">
                <h3>{icon}</h3>
                <b>{title}</b><br>
                <small>{description}</small>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# JOB DESCRIPTION INPUT
# ============================================================

st.markdown(
    '<div class="section-heading">📋 Job Description</div>',
    unsafe_allow_html=True
)

st.caption(
    "Copy and paste the complete job description below. "
    "The system will automatically analyze the requirements "
    "and compare them with uploaded resumes."
)

jd_text = st.text_area(
    "Paste Job Description",
    height=280,
    placeholder=(
        "Paste the complete job description here...\n\n"
        "Example:\n"
        "We are looking for a Data Analyst with skills in Python, "
        "SQL, Pandas, Power BI and data visualization."
    ),
    label_visibility="collapsed",
    key="jd_input"
)


# ============================================================
# ACTION BUTTONS
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

button_col1, button_col2 = st.columns([4, 1])

with button_col1:
    analyze_clicked = st.button(
        "🚀 Analyze Resumes with AI",
        type="primary",
        use_container_width=True
    )

with button_col2:
    # IMPORTANT: on_click callback prevents the Session State error
    st.button(
        "🗑️ Clear",
        use_container_width=True,
        on_click=clear_analysis
    )


# ============================================================
# RUN ANALYSIS
# ============================================================

if analyze_clicked:

    if not jd_text.strip():

        st.error(
            "⚠️ Please paste a Job Description before analysis."
        )

        st.stop()

    if not resume_files:

        st.error(
            "⚠️ Please upload at least one resume PDF "
            "from the sidebar."
        )

        st.stop()

    # --------------------------------------------------------
    # JOB DESCRIPTION PROCESSING
    # --------------------------------------------------------

    cleaned_jd = clean_text(jd_text)
    jd_skills = extract_skills(cleaned_jd)

    results = []

    st.divider()
    st.subheader("🧠 AI Analysis in Progress")

    progress = st.progress(0)
    status = st.empty()

    # --------------------------------------------------------
    # ANALYZE EACH RESUME
    # --------------------------------------------------------

    for index, resume_file in enumerate(resume_files):

        status.info(
            f"Analyzing {index + 1} of {len(resume_files)}: "
            f"{resume_file.name}"
        )

        result = process_candidate(
            resume_file,
            jd_text,
            jd_skills
        )

        if result:
            results.append(result)

        progress_value = int(
            ((index + 1) / len(resume_files)) * 100
        )

        progress.progress(progress_value)

    status.empty()

    # --------------------------------------------------------
    # VALIDATE RESULTS
    # --------------------------------------------------------

    if not results:

        st.error(
            "No readable text could be extracted from the "
            "uploaded resumes."
        )

        st.stop()

    # --------------------------------------------------------
    # STORE RESULTS
    # --------------------------------------------------------

    st.session_state.results = rank_candidates(results)
    st.session_state.analyzed_jd = jd_text
    st.session_state.analyzed_jd_skills = jd_skills

    st.success(
        "✅ AI-powered resume analysis completed successfully!"
    )


# ============================================================
# RESUME INTELLIGENCE DASHBOARD
# ============================================================

if st.session_state.results:

    results = st.session_state.results

    st.divider()
    st.header("📊 Resume Intelligence Dashboard")

    # --------------------------------------------------------
    # CREATE DASHBOARD DATAFRAME
    # --------------------------------------------------------

    dashboard_rows = []

    for candidate in results:

        dashboard_rows.append({
            "Rank": candidate["rank"],
            "Candidate": candidate["candidate_name"],
            "Overall Match (%)": candidate["final_score"],
            "Semantic (%)": candidate["semantic_score"],
            "Skills (%)": candidate["skill_score"],
            "TF-IDF (%)": candidate["tfidf_score"]
        })

    df = pd.DataFrame(dashboard_rows)

    # --------------------------------------------------------
    # DASHBOARD TOP METRICS
    # --------------------------------------------------------

    best_candidate = results[0]
    average_score = df["Overall Match (%)"].mean()

    strong_matches = len(
        df[df["Overall Match (%)"] >= 65]
    )

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric(
        "👥 Candidates",
        len(results)
    )

    metric2.metric(
        "🏆 Top Candidate",
        best_candidate["candidate_name"]
    )

    metric3.metric(
        "🎯 Best Match",
        f"{best_candidate['final_score']}%"
    )

    metric4.metric(
        "📈 Average Match",
        f"{average_score:.1f}%"
    )

    st.caption(
        f"Strong matches (65%+): {strong_matches} candidate(s)"
    )


    # ========================================================
    # JOB DESCRIPTION NLP ANALYSIS
    # ========================================================

    st.subheader("🧠 Job Description NLP Analysis")

    jd_skills = st.session_state.analyzed_jd_skills

    jd_col1, jd_col2 = st.columns([1, 3])

    with jd_col1:

        st.metric(
            "Skills Detected",
            len(jd_skills)
        )

    with jd_col2:

        if jd_skills:

            st.write("**Detected Skills:**")

            st.write(
                " • ".join(jd_skills)
            )

        else:

            st.info(
                "No predefined skills were detected. "
                "You can add additional skills in "
                "src/skill_extractor.py."
            )


    # ========================================================
    # CANDIDATE RANKING
    # ========================================================

    st.subheader("🏆 Candidate Ranking")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # OVERALL MATCH SCORE CHART
    # ========================================================

    st.subheader("📈 Overall Candidate Match Scores")

    st.bar_chart(
        df.set_index("Candidate")["Overall Match (%)"]
    )


    # ========================================================
    # NLP / ML COMPONENT ANALYSIS
    # ========================================================

    st.subheader("🔬 NLP/ML Scoring Analysis")

    component_data = df.set_index("Candidate")[
        ["Semantic (%)", "Skills (%)", "TF-IDF (%)"]
    ]

    st.bar_chart(component_data)


    # ========================================================
    # EXPORT RESULTS
    # ========================================================

    st.subheader("⬇️ Export Screening Results")

    csv_data = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Screening Results (CSV)",
        data=csv_data,
        file_name="ai_resume_screening_results.csv",
        mime="text/csv"
    )


    # ========================================================
    # INDIVIDUAL CANDIDATE ANALYSIS
    # ========================================================

    st.divider()
    st.header("🔍 Candidate-Level AI Analysis")

    for candidate in results:

        score = candidate["final_score"]

        with st.expander(
            f"#{candidate['rank']} | "
            f"{candidate['candidate_name']} | "
            f"{score}% — {get_match_label(score)}"
        ):

            # SCORE METRICS
            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Overall", f"{score}%")

            col2.metric(
                "Semantic",
                f"{candidate['semantic_score']}%"
            )

            col3.metric(
                "Skill Match",
                f"{candidate['skill_score']}%"
            )

            col4.metric(
                "TF-IDF",
                f"{candidate['tfidf_score']}%"
            )

            st.progress(
                min(max(int(score), 0), 100)
            )

            # MATCHED AND MISSING SKILLS
            skill_col1, skill_col2 = st.columns(2)

            with skill_col1:

                st.markdown("### ✅ Matched Skills")

                if candidate["matched_skills"]:

                    for skill in candidate["matched_skills"]:
                        st.success(skill)

                else:
                    st.info(
                        "No direct predefined skill matches detected."
                    )

            with skill_col2:

                st.markdown(
                    "### ⚠️ Missing Skills / Skill Gap"
                )

                if candidate["missing_skills"]:

                    for skill in candidate["missing_skills"]:
                        st.warning(skill)

                else:
                    st.success(
                        "No major predefined skill gaps detected."
                    )

            # ALL RESUME SKILLS
            st.markdown("### 🛠️ Skills Found in Resume")

            if candidate["resume_skills"]:

                st.write(
                    " • ".join(candidate["resume_skills"])
                )

            else:
                st.info(
                    "No predefined skills found in this resume."
                )

            # AI EXPLANATION
            st.markdown("### 💡 AI Screening Explanation")

            st.info(candidate["explanation"])

            # TECHNICAL INFORMATION
            st.caption(
                "The final match score is calculated using a hybrid "
                "NLP/ML approach combining transformer-based semantic "
                "similarity, TF-IDF cosine similarity and technical "
                "skill overlap."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🤖 AI Resume Intelligence Screening System | "
    "NLP • Semantic Similarity • TF-IDF • Skill Matching • "
    "Explainable Candidate Ranking"
)