import re


SKILL_DB = [
    "Python",
    "Java",
    "C++",
    "SQL",
    "Machine Learning",
    "Deep Learning",
    "Data Structures",
    "Algorithms",
    "Git",
    "GitHub",
    "AWS",
    "Docker",
    "React",
    "Node.js",
    "NLP",
    "Streamlit",
    "LangChain",
    "LLM",
    "Generative AI"
]


def parse_jd(jd_text):

    found_skills = []

    for skill in SKILL_DB:

        if skill.lower() in jd_text.lower():
            found_skills.append(skill)

    # EXPERIENCE
    exp_match = re.search(
        r'(\\d+\\+?\\s?(?:years|year))',
        jd_text,
        re.IGNORECASE
    )

    experience = (
        exp_match.group(1)
        if exp_match
        else "Not Mentioned"
    )

    # EDUCATION
    education_keywords = [
        "B.Tech",
        "B.E",
        "M.Tech",
        "Bachelor",
        "Computer Science",
        "Electronics"
    ]

    education_found = []

    for edu in education_keywords:

        if edu.lower() in jd_text.lower():
            education_found.append(edu)

    # KEYWORDS
    keyword_patterns = [
        "backend",
        "frontend",
        "AI",
        "ML",
        "automation",
        "semantic search",
        "API"
    ]

    keywords = []

    for word in keyword_patterns:

        if word.lower() in jd_text.lower():
            keywords.append(word)

    return {
        "skills": found_skills,
        "experience": experience,
        "education": education_found,
        "keywords": keywords
    }