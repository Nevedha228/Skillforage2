import pytest
from market_engine.skill_extractor import extract_skills
from market_engine.processor import clean_text, is_duplicate, process_jobs
from market_engine.models import JobPosting as EngineJobPosting

def test_skill_extraction_word_boundary_cases():
    # 1. "Java" vs "JavaScript": Text containing only JavaScript should not extract Java
    js_text = "Frontend Engineer proficient in JavaScript, React, and HTML."
    extracted_js = extract_skills(js_text)
    assert "JavaScript" in extracted_js
    assert "Java" not in extracted_js

    # 2. Text containing both Java and JavaScript
    both_text = "Full Stack Engineer with Java Spring Boot backend and JavaScript React frontend."
    extracted_both = extract_skills(both_text)
    assert "Java" in extracted_both
    assert "JavaScript" in extracted_both

    # 3. "C" vs "CSS"
    css_text = "Web styling with CSS and HTML5."
    extracted_css = extract_skills(css_text)
    assert "CSS" in extracted_css
    assert "C" not in extracted_css

    # 4. Abbreviation and synonym normalization
    sql_text = "Proficient in structured query language and postgresql."
    extracted_sql = extract_skills(sql_text)
    assert "SQL" in extracted_sql
    assert "PostgreSQL" in extracted_sql


def test_text_cleaning_and_duplicate_detection():
    raw_html = "<p>Looking for a <b>Python</b> developer &amp; data analyst. Visit https://example.com</p>"
    cleaned = clean_text(raw_html)
    assert "<p>" not in cleaned
    assert "https://" not in cleaned
    assert "Python" in cleaned

    # Duplicate job postings
    job1 = EngineJobPosting(
        source="demo", source_job_id="1", title="Data Analyst",
        company="Apex Tech", location="Bengaluru",
        description="Looking for SQL and Python analyst in Bengaluru." * 3,
        url="http://job1"
    )
    job2 = EngineJobPosting(
        source="demo", source_job_id="2", title="Data Analyst",
        company="Apex Tech", location="Bengaluru",
        description="Looking for SQL and Python analyst in Bengaluru." * 3,
        url="http://job2"
    )
    job3 = EngineJobPosting(
        source="demo", source_job_id="3", title="Frontend Engineer",
        company="Apex Tech", location="Bengaluru",
        description="Looking for React and CSS frontend developer in Bengaluru." * 3,
        url="http://job3"
    )

    # process_jobs deduplicates identical jobs from the same company and title
    unique_jobs = process_jobs([job1, job2, job3])
    assert len(unique_jobs) == 2


def test_market_analytics_and_skill_gap(client, create_test_user):
    user, token = create_test_user("market_student", "market_user@college.edu")
    client.cookies.set("sf_session", token)

    # 1. Market analytics: Verify data origin labeling
    analytics_res = client.get("/api/v1/market/analytics?data_origin=synthetic_demo")
    assert analytics_res.status_code == 200
    data = analytics_res.json()
    assert data["data_origin"] == "synthetic_demo"
    assert data["is_synthetic"] is True
    assert "top_skills" in data
    assert len(data["top_skills"]) > 0

    # 2. Skill gap comparison
    gap_res = client.get("/api/v1/market/skill-gap?role_id=data-analyst")
    assert gap_res.status_code == 200
    gap_data = gap_res.json()
    assert gap_data["target_role"] == "data-analyst"
    assert "prioritized_gaps" in gap_data
    assert len(gap_data["prioritized_gaps"]) > 0
    # Prioritized categories must exist
    priorities = [g["priority"] for g in gap_data["prioritized_gaps"]]
    assert any(p in ["Critical", "High", "Medium"] for p in priorities)
