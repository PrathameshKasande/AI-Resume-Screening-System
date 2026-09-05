
"""
Generate synthetic evaluation data for the
AI Resume Screening System.

This script creates:

1. Four Job Description files
2. 100 synthetic resumes
3. Ground-truth labels

Run from the project root:

    python scripts\generate_evaluation_data.py
"""

from pathlib import Path
import csv
import random


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


JOB_DESCRIPTION_DIR = (
    BASE_DIR
    / "data"
    / "job_descriptions"
)


EVALUATION_DIR = (
    BASE_DIR
    / "data"
    / "evaluation"
)


RESUME_DIR = (
    EVALUATION_DIR
    / "synthetic_resumes"
)


LABEL_FILE = (
    EVALUATION_DIR
    / "labeled_matches.csv"
)


# ============================================================
# CREATE DIRECTORIES
# ============================================================

JOB_DESCRIPTION_DIR.mkdir(
    parents=True,
    exist_ok=True
)

RESUME_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# RANDOM SEED
# ============================================================

random.seed(42)


# ============================================================
# JOB DESCRIPTIONS
# ============================================================

JOB_DESCRIPTIONS = {

    "data_analyst": {
        "title": "Data Analyst",

        "skills": [
            "Python",
            "SQL",
            "Excel",
            "Power BI",
            "Pandas",
            "NumPy",
            "Statistics",
            "Data Analysis",
            "Data Visualization"
        ],

        "responsibilities": [
            "Analyze structured datasets.",
            "Write SQL queries.",
            "Create dashboards and reports.",
            "Identify trends and patterns.",
            "Prepare business insights."
        ]
    },


    "ml_engineer": {
        "title": "Machine Learning Engineer",

        "skills": [
            "Python",
            "Machine Learning",
            "Scikit-learn",
            "TensorFlow",
            "Feature Engineering",
            "Model Evaluation",
            "Deep Learning",
            "Docker",
            "Git"
        ],

        "responsibilities": [
            "Build machine learning models.",
            "Preprocess datasets.",
            "Perform feature engineering.",
            "Evaluate machine learning models.",
            "Deploy machine learning applications."
        ]
    },


    "data_scientist": {
        "title": "Data Scientist",

        "skills": [
            "Python",
            "SQL",
            "Machine Learning",
            "Statistics",
            "Pandas",
            "NumPy",
            "Scikit-learn",
            "Data Visualization",
            "Feature Engineering"
        ],

        "responsibilities": [
            "Analyze complex datasets.",
            "Build predictive models.",
            "Perform statistical analysis.",
            "Create data visualizations.",
            "Develop machine learning solutions."
        ]
    },


    "nlp_engineer": {
        "title": "NLP Engineer",

        "skills": [
            "Python",
            "NLP",
            "Machine Learning",
            "Text Preprocessing",
            "Tokenization",
            "TF-IDF",
            "Transformers",
            "Sentence Transformers",
            "Deep Learning"
        ],

        "responsibilities": [
            "Build NLP pipelines.",
            "Process text data.",
            "Develop semantic similarity systems.",
            "Work with transformer models.",
            "Build machine learning applications."
        ]
    }
}


# ============================================================
# UNRELATED SKILLS
# ============================================================

UNRELATED_SKILLS = [
    "Java",
    "JavaScript",
    "React",
    "HTML",
    "CSS",
    "Angular",
    "PHP",
    "Kotlin",
    "Android",
    "C++",
    "MongoDB",
    "Flutter",
    "WordPress",
    "Spring Boot"
]


# ============================================================
# SAMPLE NAMES
# ============================================================

FIRST_NAMES = [
    "Aarav",
    "Rohan",
    "Priya",
    "Ananya",
    "Rahul",
    "Sneha",
    "Arjun",
    "Neha",
    "Vikram",
    "Kavya",
    "Aditya",
    "Isha",
    "Karan",
    "Pooja",
    "Aman",
    "Meera",
    "Siddharth",
    "Riya",
    "Nikhil",
    "Anjali"
]


LAST_NAMES = [
    "Sharma",
    "Patil",
    "Kumar",
    "Singh",
    "Joshi",
    "Gupta",
    "Verma",
    "Rao",
    "Kulkarni",
    "Deshmukh"
]


# ============================================================
# GENERATE NAME
# ============================================================

def generate_name():

    return (
        f"{random.choice(FIRST_NAMES)} "
        f"{random.choice(LAST_NAMES)}"
    )


# ============================================================
# CREATE JOB DESCRIPTION
# ============================================================

def create_job_descriptions():

    print()
    print("Creating Job Description files...")
    print()

    for job_id, job in JOB_DESCRIPTIONS.items():

        skill_text = "\n".join(
            f"- {skill}"
            for skill in job["skills"]
        )

        responsibility_text = "\n".join(
            f"- {item}"
            for item in job["responsibilities"]
        )

        content = f"""
JOB TITLE

{job["title"]}


REQUIRED TECHNICAL SKILLS

{skill_text}


RESPONSIBILITIES

{responsibility_text}


EDUCATION

Bachelor's degree in Computer Science,
Information Technology, Data Science,
or a related field.
""".strip()

        file_path = (
            JOB_DESCRIPTION_DIR
            / f"{job_id}.txt"
        )

        file_path.write_text(
            content,
            encoding="utf-8"
        )

        print(
            f"[CREATED] {file_path.name}"
        )


# ============================================================
# CREATE RESUME TEXT
# ============================================================

def create_resume(
    name,
    target_role,
    skills,
    category
):

    role = JOB_DESCRIPTIONS[
        target_role
    ]["title"]

    skill_text = ", ".join(
        skills
    )

    return f"""
{name}

PROFESSIONAL SUMMARY

Motivated Computer Science graduate
interested in {role}.

Strong interest in data, programming,
machine learning and practical problem solving.

TECHNICAL SKILLS

{skill_text}

PROJECT EXPERIENCE

Completed academic and personal projects
involving data processing, programming,
analysis and technology-driven problem solving.

EDUCATION

Bachelor of Technology in Computer Science

TARGET ROLE

{role}

EVALUATION CATEGORY

{category}
""".strip()


# ============================================================
# GENERATE ONE GROUP
# ============================================================

def generate_for_job(
    job_id,
    starting_number
):

    rows = []

    required_skills = JOB_DESCRIPTIONS[
        job_id
    ]["skills"]


    resume_number = starting_number


    # ========================================================
    # 15 STRONG MATCHES
    # ========================================================

    for _ in range(15):

        resume_id = (
            f"resume_{resume_number:03d}"
        )

        name = generate_name()

        selected_skills = random.sample(
            required_skills,
            k=min(
                7,
                len(required_skills)
            )
        )

        resume_text = create_resume(
            name,
            job_id,
            selected_skills,
            "Strong Match"
        )

        file_path = (
            RESUME_DIR
            / f"{resume_id}.txt"
        )

        file_path.write_text(
            resume_text,
            encoding="utf-8"
        )

        rows.append({
            "resume_id": resume_id,
            "target_jd": job_id,
            "actual_label": 1,
            "match_type": "strong"
        })

        resume_number += 1


    # ========================================================
    # 5 MODERATE MATCHES
    # ========================================================

    for _ in range(5):

        resume_id = (
            f"resume_{resume_number:03d}"
        )

        name = generate_name()

        relevant_skills = random.sample(
            required_skills,
            k=min(
                4,
                len(required_skills)
            )
        )

        unrelated_skills = random.sample(
            UNRELATED_SKILLS,
            k=3
        )

        selected_skills = (
            relevant_skills
            + unrelated_skills
        )

        resume_text = create_resume(
            name,
            job_id,
            selected_skills,
            "Moderate Match"
        )

        file_path = (
            RESUME_DIR
            / f"{resume_id}.txt"
        )

        file_path.write_text(
            resume_text,
            encoding="utf-8"
        )

        rows.append({
            "resume_id": resume_id,
            "target_jd": job_id,
            "actual_label": 1,
            "match_type": "moderate"
        })

        resume_number += 1


    # ========================================================
    # 5 IRRELEVANT MATCHES
    # ========================================================

    for _ in range(5):

        resume_id = (
            f"resume_{resume_number:03d}"
        )

        name = generate_name()

        selected_skills = random.sample(
            UNRELATED_SKILLS,
            k=6
        )

        resume_text = create_resume(
            name,
            job_id,
            selected_skills,
            "Low Match"
        )

        file_path = (
            RESUME_DIR
            / f"{resume_id}.txt"
        )

        file_path.write_text(
            resume_text,
            encoding="utf-8"
        )

        rows.append({
            "resume_id": resume_id,
            "target_jd": job_id,
            "actual_label": 0,
            "match_type": "low"
        })

        resume_number += 1


    return rows, resume_number


# ============================================================
# MAIN DATA GENERATION
# ============================================================

def generate_dataset():

    print()
    print("=" * 70)
    print("AI RESUME SCREENING - EVALUATION DATA GENERATOR")
    print("=" * 70)


    # --------------------------------------------------------
    # First create JDs
    # --------------------------------------------------------

    create_job_descriptions()


    # --------------------------------------------------------
    # Generate resumes
    # --------------------------------------------------------

    all_rows = []

    resume_number = 1


    for job_id in JOB_DESCRIPTIONS:

        rows, resume_number = generate_for_job(
            job_id,
            resume_number
        )

        all_rows.extend(
            rows
        )


    # --------------------------------------------------------
    # Save labels
    # --------------------------------------------------------

    with open(
        LABEL_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "resume_id",
                "target_jd",
                "actual_label",
                "match_type"
            ]
        )

        writer.writeheader()

        writer.writerows(
            all_rows
        )


    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    strong = sum(
        row["match_type"] == "strong"
        for row in all_rows
    )

    moderate = sum(
        row["match_type"] == "moderate"
        for row in all_rows
    )

    low = sum(
        row["match_type"] == "low"
        for row in all_rows
    )


    print()
    print("=" * 70)
    print("EVALUATION DATASET CREATED SUCCESSFULLY")
    print("=" * 70)

    print(
        f"Job descriptions : "
        f"{len(JOB_DESCRIPTIONS)}"
    )

    print(
        f"Total resumes    : "
        f"{len(all_rows)}"
    )

    print(
        f"Strong matches   : "
        f"{strong}"
    )

    print(
        f"Moderate matches : "
        f"{moderate}"
    )

    print(
        f"Low matches      : "
        f"{low}"
    )

    print()
    print(
        f"JD folder:"
    )

    print(
        JOB_DESCRIPTION_DIR
    )

    print()
    print(
        f"Resume folder:"
    )

    print(
        RESUME_DIR
    )

    print()
    print(
        f"Labels file:"
    )

    print(
        LABEL_FILE
    )

    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    generate_dataset()
