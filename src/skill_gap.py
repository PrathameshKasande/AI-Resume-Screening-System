def find_skill_gap(
    resume_skills,
    jd_skills
):

    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    matched = jd_set.intersection(
        resume_set
    )

    missing = jd_set - resume_set

    return {
        "matched_skills": sorted(
            matched
        ),
        "missing_skills": sorted(
            missing
        )
    }