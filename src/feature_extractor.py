from sklearn.feature_extraction.text import TfidfVectorizer


def create_tfidf_vectors(
    resume_text,
    jd_text
):

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    vectors = vectorizer.fit_transform(
        [
            resume_text,
            jd_text
        ]
    )

    return vectors[0], vectors[1]