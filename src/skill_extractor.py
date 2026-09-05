SKILLS = [

    # Programming
    "python",
    "java",
    "c++",
    "javascript",
    "sql",

    # Databases
    "mysql",
    "postgresql",
    "mongodb",
    "oracle",

    # Data
    "pandas",
    "numpy",
    "scipy",
    "excel",
    "power bi",
    "tableau",

    # ML
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "scikit-learn",
    "tensorflow",
    "keras",
    "pytorch",
    "xgboost",
    "lightgbm",

    # NLP
    "nlp",
    "natural language processing",
    "transformers",
    "sentence transformers",
    "bert",
    "text classification",

    # Computer Vision
    "computer vision",
    "opencv",
    "cnn",

    # Data Science
    "data science",
    "data analysis",
    "data visualization",
    "statistics",
    "feature engineering",
    "eda",

    # Cloud
    "aws",
    "azure",
    "gcp",

    # Deployment
    "docker",
    "fastapi",
    "flask",
    "streamlit",

    # Dev tools
    "git",
    "github",
    "linux",

    # Big Data
    "spark",
    "hadoop"
]


def extract_skills(text):

    if not text:
        return []

    text = text.lower()

    found = []

    for skill in SKILLS:

        if skill.lower() in text:

            found.append(skill)

    return sorted(
        list(set(found))
    )