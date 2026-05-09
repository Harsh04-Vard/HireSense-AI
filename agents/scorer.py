def score_candidate(jd_data, resume_data):

    required_skills = jd_data["skills"]

    candidate_skills = resume_data["skills"]

    # ---------------- SKILL MATCH ---------------- #

    matched_skills = list(
        set(required_skills).intersection(candidate_skills)
    )

    if len(required_skills) == 0:
        skills_score = 0
    else:
        skills_score = (
            len(matched_skills) / len(required_skills)
        ) * 10

    # ---------------- EXPERIENCE SCORE ---------------- #

    experience_score = 7

    text = resume_data["raw_text"].lower()

    if "intern" in text:
        experience_score += 1

    if "project" in text:
        experience_score += 1

    experience_score = min(experience_score, 10)

    # ---------------- EDUCATION SCORE ---------------- #

    education_score = 6

    if "b.tech" in text:
        education_score += 2

    if "computer science" in text:
        education_score += 1

    if "electronics" in text:
        education_score += 1

    education_score = min(education_score, 10)

    # ---------------- PROJECT SCORE ---------------- #

    project_score = 5

    project_keywords = [
        "github",
        "live",
        "api",
        "ai",
        "ml",
        "streamlit"
    ]

    found_projects = 0

    for word in project_keywords:

        if word in text:
            found_projects += 1

    project_score += min(found_projects, 5)

    project_score = min(project_score, 10)

    # ---------------- COMMUNICATION SCORE ---------------- #

    communication_score = 7

    if len(text) > 1500:
        communication_score += 1

    if "leadership" in text:
        communication_score += 1

    if "teamwork" in text:
        communication_score += 1

    communication_score = min(communication_score, 10)

    # ---------------- FINAL WEIGHTED SCORE ---------------- #

    total_score = (
        skills_score * 0.30 +
        experience_score * 0.25 +
        education_score * 0.15 +
        project_score * 0.20 +
        communication_score * 0.10
    )

    # ---------------- RECOMMENDATION ---------------- #

    recommendation = (
        "Hire"
        if total_score >= 7
        else "No Hire"
    )

    # ---------------- OUTPUT ---------------- #

    return {

        "matched_skills": matched_skills,

        "skills_score": round(skills_score, 2),

        "experience_score": round(experience_score, 2),

        "education_score": round(education_score, 2),

        "project_score": round(project_score, 2),

        "communication_score": round(communication_score, 2),

        "total_score": round(total_score, 2),

        "recommendation": recommendation
    }