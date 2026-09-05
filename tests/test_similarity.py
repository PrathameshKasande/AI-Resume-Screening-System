from src.feature_extractor import (
    create_tfidf_vectors
)

from src.similarity import (
    calculate_tfidf_similarity
)


def test_tfidf_similarity():

    resume = (
        "Python SQL Machine Learning"
    )

    jd = (
        "Python SQL Data Analysis"
    )

    resume_vector, jd_vector = (
        create_tfidf_vectors(
            resume,
            jd
        )
    )

    score = (
        calculate_tfidf_similarity(
            resume_vector,
            jd_vector
        )
    )

    assert score > 0
    assert score <= 1