import re


def extract_section(text, section_name, next_sections):
    pattern = rf"{section_name}:\s*(.*?)(?=\n(?:{'|'.join(next_sections)}):|\Z)"
    
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)

    if match:
        return match.group(1).strip()

    return ""


def parse_resume(text):

    sections = [
        "PROFESSIONAL SUMMARY",
        "EDUCATION",
        "TECHNICAL SKILLS",
        "PROJECTS",
        "INTERNSHIP",
        "CERTIFICATIONS",
        "ACHIEVEMENTS"
    ]

    education = extract_section(
        text,
        "EDUCATION",
        [
            "TECHNICAL SKILLS",
            "PROJECTS",
            "INTERNSHIP",
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
            "CERTIFICATIONS",
            "ACHIEVEMENTS"
        ]
    )

    projects = extract_section(
        text,
        "PROJECTS",
        [
            "INTERNSHIP",
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

    return {
        "skills": skills,
        "education": education,
        "projects": projects,
        "experience": experience
    }
