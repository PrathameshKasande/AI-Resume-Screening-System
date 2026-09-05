from src.text_preprocessor import (
    clean_text
)

from src.skill_extractor import (
    extract_skills
)


def test_clean_text():

    text = (
        "Python!!! Machine Learning"
    )

    result = clean_text(text)

    assert "python" in result

    assert (
        "machine learning"
        in result
    )


def test_skill_extraction():

    text = """
    Python, SQL, Machine Learning,
    Power BI
    """

    skills = extract_skills(
        text
    )

    assert "python" in skills
    assert "sql" in skills
    assert (
        "machine learning"
        in skills
    )
    assert "power bi" in skills