
"""
Evaluate the AI Resume Screening System.

Run from project root:

    python evaluation\evaluate_matching.py
"""

from pathlib import Path
import sys


# ============================================================
# FIX PYTHON IMPORT PATH
# ============================================================

PROJECT_ROOT = Path(
    __file__
).resolve().parent.parent


if str(PROJECT_ROOT) not in sys.path:

    sys.path.insert(
        0,
        str(PROJECT_ROOT)
    )


# ============================================================
# IMPORTS
# ============================================================

import pandas as pd

from sklearn.feature_extraction.text import (
    TfidfVectorizer
)


from src.text_preprocessor import (
    clean_text
)


from src.skill_extractor import (
    extract_skills
)


from src.similarity import (
    calculate_tfidf_similarity,
    calculate_semantic_similarity
)


from src.scoring import (
    calculate_skill_match,
    calculate_final_score
)


from evaluation.metrics import (
    calculate_metrics,
    print_metrics
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = PROJECT_ROOT


LABEL_FILE = (
    BASE_DIR
    / "data"
    / "evaluation"
    / "labeled_matches.csv"
)


RESUME_DIR = (
    BASE_DIR
    / "data"
    / "evaluation"
    / "synthetic_resumes"
)


JD_DIR = (
    BASE_DIR
    / "data"
    / "job_descriptions"
)


RESULT_DIR = (
    BASE_DIR
    / "data"
    / "evaluation"
    / "results"
)


RESULT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


RESULT_FILE = (
    RESULT_DIR
    / "evaluation_results.csv"
)


# ============================================================
# SCREENING THRESHOLD
# ============================================================

THRESHOLD = 65.0


# ============================================================
# READ TEXT
# ============================================================

def read_text(
    file_path: Path
) -> str:

    if not file_path.exists():

        raise FileNotFoundError(
            f"\nFile not found:\n"
            f"{file_path}\n"
        )

    return file_path.read_text(
        encoding="utf-8"
    )


# ============================================================
# CHECK DATASET BEFORE RUNNING
# ============================================================

def validate_dataset(df):

    missing_files = []


    for _, row in df.iterrows():

        resume_id = str(
            row["resume_id"]
        )

        jd_id = str(
            row["target_jd"]
        )


        resume_file = (
            RESUME_DIR
            / f"{resume_id}.txt"
        )


        jd_file = (
            JD_DIR
            / f"{jd_id}.txt"
        )


        if not resume_file.exists():

            missing_files.append(
                str(resume_file)
            )


        if not jd_file.exists():

            missing_files.append(
                str(jd_file)
            )


    if missing_files:

        print()
        print("=" * 70)
        print("DATASET VALIDATION FAILED")
        print("=" * 70)

        print(
            f"Missing files: "
            f"{len(missing_files)}"
        )

        print()


        for file_path in missing_files[:20]:

            print(
                f"[MISSING] {file_path}"
            )


        if len(missing_files) > 20:

            print(
                f"... and "
                f"{len(missing_files) - 20}"
                f" more"
            )


        print()
        print(
            "Recommended fix:"
        )

        print(
            "python scripts\\generate_evaluation_data.py"
        )

        print("=" * 70)

        return False


    return True


# ============================================================
# CALCULATE ONE RESUME SCORE
# ============================================================

def calculate_resume_score(
    resume_text,
    jd_text
):

    # --------------------------------------------------------
    # Text preprocessing
    # --------------------------------------------------------

    clean_resume = clean_text(
        resume_text
    )

    clean_jd = clean_text(
        jd_text
    )


    # --------------------------------------------------------
    # Skill extraction
    # --------------------------------------------------------

    resume_skills = extract_skills(
        clean_resume
    )

    jd_skills = extract_skills(
        clean_jd
    )


    # --------------------------------------------------------
    # Skill matching
    # --------------------------------------------------------

    skill_score = calculate_skill_match(
        resume_skills,
        jd_skills
    )


    # --------------------------------------------------------
    # TF-IDF
    # --------------------------------------------------------

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )


    tfidf_matrix = vectorizer.fit_transform(
        [
            clean_resume,
            clean_jd
        ]
    )


    resume_vector = (
        tfidf_matrix[0:1]
    )


    jd_vector = (
        tfidf_matrix[1:2]
    )


    tfidf_score = (
        calculate_tfidf_similarity(
            resume_vector,
            jd_vector
        )
    )


    # --------------------------------------------------------
    # Semantic similarity
    # --------------------------------------------------------

    semantic_score = (
        calculate_semantic_similarity(
            clean_resume,
            clean_jd
        )
    )


    # --------------------------------------------------------
    # Final score
    # --------------------------------------------------------

    final_score = (
        calculate_final_score(
            semantic_score,
            tfidf_score,
            skill_score
        )
    )


    return {
        "semantic_score": semantic_score,
        "tfidf_score": tfidf_score,
        "skill_score": skill_score,
        "final_score": final_score,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills
    }


# ============================================================
# EVALUATION
# ============================================================

def evaluate():

    print()
    print("=" * 70)
    print(
        "AI RESUME SCREENING SYSTEM"
    )
    print(
        "MODEL EVALUATION"
    )
    print("=" * 70)


    # --------------------------------------------------------
    # Check labels
    # --------------------------------------------------------

    if not LABEL_FILE.exists():

        print()
        print(
            "ERROR: labeled_matches.csv "
            "was not found."
        )

        print()
        print(
            "Run:"
        )

        print(
            "python scripts\\generate_evaluation_data.py"
        )

        return


    # --------------------------------------------------------
    # Load CSV
    # --------------------------------------------------------

    df = pd.read_csv(
        LABEL_FILE
    )


    required_columns = {
        "resume_id",
        "target_jd",
        "actual_label"
    }


    missing_columns = (
        required_columns
        - set(df.columns)
    )


    if missing_columns:

        raise ValueError(
            "Missing CSV columns: "
            f"{missing_columns}"
        )


    # --------------------------------------------------------
    # Validate files BEFORE evaluation
    # --------------------------------------------------------

    if not validate_dataset(df):

        return


    # --------------------------------------------------------
    # Information
    # --------------------------------------------------------

    total_samples = len(df)


    print()
    print(
        f"Project root       : {BASE_DIR}"
    )

    print(
        f"Evaluation samples : {total_samples}"
    )

    print(
        f"Threshold          : {THRESHOLD:.2f}%"
    )

    print()


    # --------------------------------------------------------
    # Storage
    # --------------------------------------------------------

    actual_labels = []

    predicted_labels = []

    results = []


    # --------------------------------------------------------
    # Process each sample
    # --------------------------------------------------------

    for index, row in df.iterrows():

        resume_id = str(
            row["resume_id"]
        )

        jd_id = str(
            row["target_jd"]
        )

        actual_label = int(
            row["actual_label"]
        )


        resume_file = (
            RESUME_DIR
            / f"{resume_id}.txt"
        )


        jd_file = (
            JD_DIR
            / f"{jd_id}.txt"
        )


        resume_text = read_text(
            resume_file
        )


        jd_text = read_text(
            jd_file
        )


        scores = calculate_resume_score(
            resume_text,
            jd_text
        )


        final_score = float(
            scores["final_score"]
        )


        predicted_label = (
            1
            if final_score >= THRESHOLD
            else 0
        )


        actual_labels.append(
            actual_label
        )


        predicted_labels.append(
            predicted_label
        )


        resume_skill_set = set(
            scores["resume_skills"]
        )


        jd_skill_set = set(
            scores["jd_skills"]
        )


        matched_skills = sorted(
            resume_skill_set
            .intersection(
                jd_skill_set
            )
        )


        results.append({

            "resume_id": resume_id,

            "job_description": jd_id,

            "actual_label": actual_label,

            "predicted_label": predicted_label,

            "match_score": round(
                final_score,
                2
            ),

            "semantic_score": round(
                float(
                    scores["semantic_score"]
                ),
                4
            ),

            "tfidf_score": round(
                float(
                    scores["tfidf_score"]
                ),
                4
            ),

            "skill_score": round(
                float(
                    scores["skill_score"]
                ),
                4
            ),

            "matched_skills": (
                ", ".join(
                    matched_skills
                )
            ),

            "correct": (
                actual_label
                == predicted_label
            )
        })


        current = index + 1


        if (
            current % 10 == 0
            or current == total_samples
        ):

            print(
                f"Processed "
                f"{current}/{total_samples}"
            )


    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    metrics = calculate_metrics(
        actual_labels,
        predicted_labels
    )


    print_metrics(
        metrics
    )


    # --------------------------------------------------------
    # Save results
    # --------------------------------------------------------

    results_df = pd.DataFrame(
        results
    )


    results_df.to_csv(
        RESULT_FILE,
        index=False
    )


    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    correct = int(
        results_df["correct"].sum()
    )


    incorrect = (
        total_samples
        - correct
    )


    print()
    print("=" * 70)
    print("EVALUATION COMPLETED")
    print("=" * 70)

    print(
        f"Total samples       : "
        f"{total_samples}"
    )

    print(
        f"Correct predictions : "
        f"{correct}"
    )

    print(
        f"Incorrect           : "
        f"{incorrect}"
    )

    print()

    print(
        "Results saved to:"
    )

    print(
        RESULT_FILE
    )

    print("=" * 70)
    print()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    evaluate()
