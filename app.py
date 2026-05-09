import streamlit as st
import tempfile
import pandas as pd
import plotly.express as px

from agents.resume_parser import parse_resume
from agents.ranker import rank_candidates
from agents.scorer import score_candidate
from agents.jd_parser import parse_jd

from utils.report_generator import generate_pdf_report
from utils.override_logger import save_override

from utils.pdf_reader import (
    extract_text_from_pdf,
    extract_text_from_docx
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="HireSense AI",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0E1117;
        color: white;
    }

    h1, h2, h3 {
        color: #00E5FF;
    }

    .stButton>button {
        background-color: #00E5FF;
        color: black;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-size: 16px;
        font-weight: bold;
    }

    .stDownloadButton>button {
        background-color: #00E5FF;
        color: black;
        border-radius: 10px;
        font-size: 16px;
        font-weight: bold;
    }

    textarea {
        background-color: #262730 !important;
        color: white !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("HireSense AI")

st.sidebar.info(
    """
    AI Resume Shortlisting System

    Features:
    - Resume Parsing
    - Candidate Ranking
    - AI Evaluation
    - PDF Reports
    - HR Override
    """
)

# =========================================================
# TITLE
# =========================================================

st.title("HireSense AI")
st.subheader("AI Resume Shortlisting Agent")

# =========================================================
# FILE UPLOADS
# =========================================================

jd = st.file_uploader(
    "Upload Job Description",
    type=["pdf", "docx", "txt"]
)

resumes = st.file_uploader(
    "Upload Resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

# =========================================================
# ANALYZE BUTTON
# =========================================================

if st.button("Analyze"):

    all_candidates = []

    st.success("Files Uploaded Successfully!")

    # =====================================================
    # JD PROCESSING
    # =====================================================

    if jd:

        jd_bytes = jd.getvalue()

        # PDF
        if jd.name.endswith(".pdf"):

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as tmp:

                tmp.write(jd_bytes)

                tmp_path = tmp.name

            jd_text = extract_text_from_pdf(tmp_path)

        # DOCX
        elif jd.name.endswith(".docx"):

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".docx"
            ) as tmp:

                tmp.write(jd_bytes)

                tmp_path = tmp.name

            jd_text = extract_text_from_docx(tmp_path)

        # TXT
        else:

            jd_text = jd_bytes.decode("utf-8")

        st.subheader("Extracted JD Text")

        st.text_area(
            "JD Content",
            jd_text,
            height=250
        )

        # =================================================
        # PARSED JD
        # =================================================

        parsed_jd = parse_jd(jd_text)

        st.subheader("AI Parsed JD")

        st.json(parsed_jd)

    # =====================================================
    # RESUME PROCESSING
    # =====================================================

    if resumes:

        st.header("Resume Analysis")

        for resume in resumes:

            st.markdown(f"# {resume.name}")

            resume_bytes = resume.getvalue()

            # PDF
            if resume.name.endswith(".pdf"):

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as tmp:

                    tmp.write(resume_bytes)

                    tmp_path = tmp.name

                resume_text = extract_text_from_pdf(tmp_path)

            # DOCX
            else:

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".docx"
                ) as tmp:

                    tmp.write(resume_bytes)

                    tmp_path = tmp.name

                resume_text = extract_text_from_docx(tmp_path)

            # =================================================
            # SHOW RESUME TEXT
            # =================================================

            with st.expander(f"View Resume Content - {resume.name}"):

                st.text_area(
                    "Resume Content",
                    resume_text[:3000],
                    height=250
                )

            # =================================================
            # PARSE RESUME
            # =================================================

            parsed_resume = parse_resume(resume_text)

            st.subheader("Parsed Resume Data")

            st.json(parsed_resume)

            # =================================================
            # SCORE CANDIDATE
            # =================================================

            candidate_scores = score_candidate(
                parsed_jd,
                parsed_resume
            )

            st.subheader("Candidate Evaluation")

            st.json(candidate_scores)

            # =================================================
            # STORE DATA
            # =================================================

            candidate_data = {

                "name": parsed_resume["name"],

                "email": parsed_resume["email"],

                "phone": parsed_resume["phone"],

                "matched_skills": candidate_scores["matched_skills"],

                "skills_score": candidate_scores["skills_score"],

                "experience_score": candidate_scores["experience_score"],

                "education_score": candidate_scores["education_score"],

                "project_score": candidate_scores["project_score"],

                "communication_score": candidate_scores["communication_score"],

                "total_score": candidate_scores["total_score"],

                "recommendation": candidate_scores["recommendation"]
            }

            all_candidates.append(candidate_data)

        # =====================================================
        # FINAL RANKING
        # =====================================================

        st.header("Final Candidate Ranking")

        ranked_candidates = rank_candidates(all_candidates)

        df = pd.DataFrame(ranked_candidates)

        st.dataframe(df)

        # =====================================================
        # CHARTS
        # =====================================================

        st.subheader("Candidate Score Comparison")

        fig = px.bar(
            df,
            x="name",
            y="total_score",
            color="recommendation",
            text="total_score",
            title="Candidate Ranking Scores"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("Skill Match Comparison")

        skill_fig = px.bar(
            df,
            x="name",
            y="skills_score",
            text="skills_score",
            title="Skill Match Scores"
        )

        st.plotly_chart(
            skill_fig,
            use_container_width=True
        )

        # =====================================================
        # PDF REPORT
        # =====================================================

        report_path = "outputs/reports/candidate_report.pdf"

        generate_pdf_report(
            ranked_candidates,
            report_path
        )

        with open(report_path, "rb") as pdf_file:

            st.download_button(
                label="Download PDF Report",
                data=pdf_file,
                file_name="candidate_report.pdf",
                mime="application/pdf"
            )

        # =====================================================
        # TOP CANDIDATE METRICS
        # =====================================================

        top_candidate = ranked_candidates[0]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Top Candidate",
                top_candidate["name"]
            )

        with col2:
            st.metric(
                "Top Score",
                top_candidate["total_score"]
            )

        with col3:
            st.metric(
                "Recommendation",
                top_candidate["recommendation"]
            )

        # =====================================================
        # LEADERBOARD
        # =====================================================

        st.header("Candidate Leaderboard")

        for idx, candidate in enumerate(ranked_candidates):

            with st.expander(
                f"#{idx + 1} {candidate['name']} "
                f"({candidate['total_score']}/10)"
            ):

                st.markdown(
                    f"""
                    ### Contact Information

                    - Email: {candidate['email']}
                    - Phone: {candidate['phone']}

                    ### Recommendation

                    - {candidate['recommendation']}

                    ### Matched Skills

                    {candidate['matched_skills']}
                    """
                )

                score_df = pd.DataFrame({

                    "Category": [
                        "Skills",
                        "Experience",
                        "Education",
                        "Projects",
                        "Communication"
                    ],

                    "Score": [
                        candidate['skills_score'],
                        candidate['experience_score'],
                        candidate['education_score'],
                        candidate['project_score'],
                        candidate['communication_score']
                    ]
                })

                chart = px.bar(
                    score_df,
                    x="Category",
                    y="Score",
                    text="Score",
                    title="Candidate Score Breakdown"
                )

                st.plotly_chart(
                    chart,
                    use_container_width=True
                )

        # =====================================================
        # HUMAN OVERRIDE PANEL
        # =====================================================

        st.header("Human Override Panel")

        candidate_names = [
            candidate["name"]
            for candidate in ranked_candidates
        ]

        selected_candidate = st.selectbox(
            "Select Candidate",
            candidate_names
        )

        new_score = st.slider(
            "Override Total Score",
            min_value=0.0,
            max_value=10.0,
            value=5.0,
            step=0.1
        )

        override_reason = st.text_area(
            "Reason for Override"
        )

        if st.button("Save Override"):

            override_data = {

                "candidate": selected_candidate,

                "new_score": new_score,

                "reason": override_reason
            }

            save_override(override_data)

            st.success(
                "Override Saved Successfully!"
            )
