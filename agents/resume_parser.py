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


def clean_text(text):

    text = text.replace("", " ")
    text = text.replace("#", " ")
    text = text.replace("ï", " ")
    text = text.replace("•", " ")

    return text


def extract_email(text):

    emails = re.findall(
        r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        text
    )

    return emails[0] if emails else "Not Found"


def extract_phone(text):

    phones = re.findall(
        r"(?:\+91[-\s]?)?[6-9]\d{9}",
        text
    )

    return phones[0] if phones else "Not Found"


def extract_skills(text):

    found_skills = []

    for skill in SKILL_DB:

        if skill.lower() in text.lower():
            found_skills.append(skill)

    return list(set(found_skills))


def extract_name(text):

    lines = text.split("\n")

    for line in lines[:10]:

        line = line.strip()

        if (
            len(line.split()) >= 2 and
            len(line) < 40 and
            "resume" not in line.lower() and
            "github" not in line.lower()
        ):
            return line

    return "Unknown"


def parse_resume(text):

    text = clean_text(text)

    candidate_data = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "raw_text": text
    }

    return candidate_data