import re


def extract_section(text, section_name, next_sections):
    """
    Extract text between one resume section heading
    and the next section heading.
    """

    next_pattern = "|".join(
        re.escape(section) for section in next_sections
    )

    pattern = rf"""
        ^\s*{re.escape(section_name)}\s*:?\s*$
        (.*?)
        (?=
            ^\s*(?:{next_pattern})\s*:?\s*$
            |\Z
        )
    """

    match = re.search(
        pattern,
        text,
        re.IGNORECASE | re.MULTILINE | re.DOTALL | re.VERBOSE
    )

    if match:
        return match.group(1).strip()

    return ""


def parse_resume(text):

    education = extract_section(
        text,
        "EDUCATION",
        [
            "TECHNICAL SKILLS",
            "PROJECTS",
            "INTERNSHIP",
            "EXPERIENCE",
            "CERTIFICATIONS",
            "ACHIEVEMENTS"
        ]
    )

    skills = extract_section(
        text,
        "TECHNICAL SKILLS",
        [
            "PROJECTS",
            "INTERNSHIP",
            "EXPERIENCE",
            "CERTIFICATIONS",
            "ACHIEVEMENTS"
        ]
    )

    projects = extract_section(
        text,
        "PROJECTS",
        [
            "INTERNSHIP",
            "EXPERIENCE",
            "CERTIFICATIONS",
            "ACHIEVEMENTS"
        ]
    )

    experience = extract_section(
        text,
        "INTERNSHIP",
        [
            "CERTIFICATIONS",
            "ACHIEVEMENTS"
        ]
    )

    if not experience:
        experience = extract_section(
            text,
            "EXPERIENCE",
            [
                "CERTIFICATIONS",
                "ACHIEVEMENTS"
            ]
        )

    return {
        "skills": skills,
        "education": education,
        "projects": projects,
        "experience": experience
    }