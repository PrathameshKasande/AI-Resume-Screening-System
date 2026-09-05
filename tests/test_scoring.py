from src.scoring import (
    calculate_skill_match,
    calculate_final_score
)


def test_skill_match():

    resume_skills = [
        "python",
        "sql"
    ]

    jd_skills = [
        "python",
        "sql",
        "machine learning"
    ]

    score = calculate_skill_match(
        resume_skills,
        jd_skills
    )

    assert round(
        score,
        2
    ) == 0.67


def test_final_score():

    score = calculate_final_score(
        semantic_score=0.8,
        tfidf_score=0.7,
        skill_score=0.9
    )

    assert score > 0
    assert score <= 100