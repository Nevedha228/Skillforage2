import re


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


def keyword_exists(text, keyword):

    text = text.lower()
    keyword = keyword.lower()

    # Special handling for abbreviations
    if keyword in ["dsa", "oops"]:

        return re.search(
            r"\b" + re.escape(keyword) + r"\b",
            text
        ) is not None

    # Normal keyword search
    return re.search(
        r"(?<![a-z0-9])"
        + re.escape(keyword)
        + r"(?![a-z0-9])",
        text
    ) is not None


def calculate_ats_score(text):

    if not text:
        return {
            "ats_score": 0,
            "found_keywords": [],
            "missing_keywords": ATS_KEYWORDS,
            "suggestions": [
                "No resume text could be extracted."
            ]
        }

    text_lower = text.lower()

    found_keywords = []
    missing_keywords = []

    for keyword in ATS_KEYWORDS:

        if keyword_exists(
            text_lower,
            keyword
        ):

            found_keywords.append(keyword)

        else:

            missing_keywords.append(keyword)

    total_keywords = len(ATS_KEYWORDS)

    keyword_score = round(
        len(found_keywords)
        / total_keywords
        * 100
    )

    suggestions = []

    # ------------------------------------------
    # Resume sections
    # ------------------------------------------

    if "summary" not in text_lower:

        suggestions.append(
            "Add a professional summary at the beginning of your resume."
        )

    if "project" not in text_lower:

        suggestions.append(
            "Add relevant academic or personal projects."
        )

    if (
        "experience" not in text_lower
        and "internship" not in text_lower
    ):

        suggestions.append(
            "Add internship, training, or relevant experience."
        )

    if "education" not in text_lower:

        suggestions.append(
            "Add a clearly labelled Education section."
        )

    if "technical skills" not in text_lower:

        suggestions.append(
            "Add a clearly labelled Technical Skills section."
        )

    # ------------------------------------------
    # Resume length
    # ------------------------------------------

    if len(text.strip()) < 1000:

        suggestions.append(
            "Your resume appears short. "
            "Add relevant technical details and achievements."
        )

    # ------------------------------------------
    # Missing keywords
    # ------------------------------------------

    if missing_keywords:

        suggestions.append(
            "Consider adding relevant missing technical "
            "keywords only when you genuinely have "
            "experience with them."
        )

    return {

        "ats_score": keyword_score,

        "found_keywords": found_keywords,

        "missing_keywords": missing_keywords,

        "total_keywords": total_keywords,

        "keyword_match_count": len(found_keywords),

        "suggestions": suggestions
    }