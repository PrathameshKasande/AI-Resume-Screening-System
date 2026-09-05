from functools import lru_cache

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_model():
    """
    Load the semantic model once.

    Caching prevents unnecessary model reloads.
    """

    return SentenceTransformer(MODEL_NAME)


def calculate_tfidf_similarity(resume_vector, jd_vector):
    """Calculate cosine similarity between TF-IDF vectors."""

    score = cosine_similarity(
        resume_vector,
        jd_vector
    )[0][0]

    return float(score)


def calculate_semantic_similarity(resume_text, jd_text):
    """
    Calculate semantic similarity between resume
    and job description using sentence embeddings.
    """

    model = get_model()

    embeddings = model.encode(
        [resume_text, jd_text],
        show_progress_bar=False
    )

    score = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return float(score)