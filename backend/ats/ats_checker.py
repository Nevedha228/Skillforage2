import re


# Important skills/keywords for a software developer resume
ATS_KEYWORDS = [
    "java",
    "python",
    "sql",
    "javascript",
    "html",
    "css",
    "react",
    "spring boot",
    "fastapi",
    "rest api",
    "git",
    "github",
    "mysql",
    "mongodb",
    "oops",
    "object oriented programming",
    "data structures",
    "algorithms",
    "dsa",
    "dbms",
    "operating systems",
    "computer networks"
]


def calculate_ats_score(text):

    text_lower = text.lower()

    found_keywords = []
    missing_keywords = []

    for keyword in ATS_KEYWORDS:

        if re.search(r"\b" + re.escape(keyword) + r"\b", text_lower):
            found_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)

    total_keywords = len(ATS_KEYWORDS)

    if total_keywords > 0:
        keyword_score = (len(found_keywords) / total_keywords) * 100
    else:
        keyword_score = 0

    suggestions = []

    if len(missing_keywords) > 0:
        suggestions.append(
            "Consider adding relevant missing technical keywords "
            "if you genuinely have experience with them."
        )

    if "summary" not in text_lower:
        suggestions.append(
            "Add a professional summary at the beginning of your resume."
        )

    if "project" not in text_lower:
        suggestions.append(
            "Add relevant academic or personal projects."
        )

    if "experience" not in text_lower and "internship" not in text_lower:
        suggestions.append(
            "Add internship, training, or relevant experience."
        )

    if len(text) < 1000:
        suggestions.append(
            "Your resume appears short. Add relevant technical details "
            "and measurable achievements."
        )

    return {
        "ats_score": round(keyword_score),
        "found_keywords": found_keywords,
        "missing_keywords": missing_keywords,
        "suggestions": suggestions
    }