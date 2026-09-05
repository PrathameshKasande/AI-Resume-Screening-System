def calculate_skill_match(resume_skills, jd_skills):
    """
    Calculate the percentage of JD skills
    found in the candidate's resume.
    """

    if not jd_skills:
        return 0.0

    resume_set = set(
        skill.lower() for skill in resume_skills
    )

    jd_set = set(
        skill.lower() for skill in jd_skills
    )

    matched = resume_set.intersection(jd_set)

    return len(matched) / len(jd_set)


def calculate_final_score(
    semantic_score,
    tfidf_score,
    skill_score
):
    """
    Calculate the final hybrid NLP/ML score.

    Scores received as decimals (0 to 1).
    Returns a percentage (0 to 100).
    """

    semantic_weight = 0.45
    skill_weight = 0.35
    tfidf_weight = 0.20

    final_score = (
        semantic_score * semantic_weight
        + skill_score * skill_weight
        + tfidf_score * tfidf_weight
    ) * 100

    return round(
        min(max(final_score, 0), 100),
        2
    )