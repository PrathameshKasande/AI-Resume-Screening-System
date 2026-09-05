def generate_explanation(
    final_score,
    matched_skills,
    missing_skills,
    semantic_score
):

    explanations = []

    if final_score >= 80:

        explanations.append(
            "Excellent overall match for the role."
        )

    elif final_score >= 65:

        explanations.append(
            "Strong candidate with good alignment "
            "to the job requirements."
        )

    elif final_score >= 50:

        explanations.append(
            "Moderate match with some relevant "
            "skills and experience."
        )

    else:

        explanations.append(
            "Low match because several important "
            "requirements may be missing."
        )

    if matched_skills:

        explanations.append(
            "Matched skills: "
            + ", ".join(matched_skills[:10])
            + "."
        )

    if missing_skills:

        explanations.append(
            "Potential skill gaps: "
            + ", ".join(missing_skills[:10])
            + "."
        )

    if semantic_score >= 0.75:

        explanations.append(
            "Resume content has strong semantic "
            "similarity with the job description."
        )

    elif semantic_score >= 0.55:

        explanations.append(
            "Resume has moderate semantic alignment "
            "with the job description."
        )

    else:

        explanations.append(
            "Semantic similarity is relatively low."
        )

    return " ".join(explanations)