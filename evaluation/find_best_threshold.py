
"""
Find the best classification threshold
for the AI Resume Screening System.

Run from the project root:

    python evaluation\find_best_threshold.py

Purpose:
    Test multiple score thresholds and determine
    which threshold provides the best balance
    between Precision, Recall and F1 Score.
"""

from pathlib import Path
import sys


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent.parent
)


if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT)
    )


# ============================================================
# IMPORTS
# ============================================================

import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


# ============================================================
# EVALUATION RESULT FILE
# ============================================================

RESULT_FILE = (
    PROJECT_ROOT
    / "data"
    / "evaluation"
    / "results"
    / "evaluation_results.csv"
)


# ============================================================
# MAIN
# ============================================================

def find_best_threshold():

    print()
    print("=" * 75)
    print("AI RESUME SCREENING")
    print("THRESHOLD OPTIMIZATION")
    print("=" * 75)


    # --------------------------------------------------------
    # Check result file
    # --------------------------------------------------------

    if not RESULT_FILE.exists():

        print()
        print(
            "ERROR: evaluation_results.csv "
            "was not found."
        )

        print()
        print(
            "First run:"
        )

        print(
            "python evaluation\\evaluate_matching.py"
        )

        print()

        return


    # --------------------------------------------------------
    # Load evaluation results
    # --------------------------------------------------------

    df = pd.read_csv(
        RESULT_FILE
    )


    required_columns = {
        "actual_label",
        "match_score"
    }


    missing_columns = (
        required_columns
        - set(df.columns)
    )


    if missing_columns:

        raise ValueError(
            "Missing columns: "
            f"{missing_columns}"
        )


    actual = df[
        "actual_label"
    ]


    scores = df[
        "match_score"
    ]


    # ========================================================
    # Test thresholds
    # ========================================================

    rows = []


    for threshold in range(
        20,
        91,
        5
    ):

        predicted = (
            scores >= threshold
        ).astype(int)


        accuracy = accuracy_score(
            actual,
            predicted
        )


        precision = precision_score(
            actual,
            predicted,
            zero_division=0
        )


        recall = recall_score(
            actual,
            predicted,
            zero_division=0
        )


        f1 = f1_score(
            actual,
            predicted,
            zero_division=0
        )


        rows.append({

            "threshold": threshold,

            "accuracy": round(
                accuracy * 100,
                2
            ),

            "precision": round(
                precision * 100,
                2
            ),

            "recall": round(
                recall * 100,
                2
            ),

            "f1_score": round(
                f1 * 100,
                2
            )
        })


    results = pd.DataFrame(
        rows
    )


    # ========================================================
    # Print complete table
    # ========================================================

    print()

    print(
        results.to_string(
            index=False
        )
    )


    # ========================================================
    # Find maximum F1
    # ========================================================

    maximum_f1 = results[
        "f1_score"
    ].max()


    best_rows = results[
        results["f1_score"]
        == maximum_f1
    ].copy()


    # ========================================================
    # If multiple thresholds have same F1,
    # choose the middle threshold.
    # ========================================================

    best_threshold = int(
        best_rows[
            "threshold"
        ].median()
    )


    recommended_row = results[
        results["threshold"]
        == best_threshold
    ].iloc[0]


    # ========================================================
    # Print best result
    # ========================================================

    print()
    print("=" * 75)
    print("BEST THRESHOLD ANALYSIS")
    print("=" * 75)


    print()

    print(
        "Maximum F1 Score : "
        f"{maximum_f1:.2f}%"
    )


    print()

    print(
        "Thresholds with maximum F1:"
    )


    print(
        ", ".join(
            str(int(x))
            for x in best_rows[
                "threshold"
            ]
        )
        + "%"
    )


    print()

    print(
        "Recommended Threshold : "
        f"{best_threshold}%"
    )


    print()

    print(
        f"Accuracy  : "
        f"{recommended_row['accuracy']:.2f}%"
    )


    print(
        f"Precision : "
        f"{recommended_row['precision']:.2f}%"
    )


    print(
        f"Recall    : "
        f"{recommended_row['recall']:.2f}%"
    )


    print(
        f"F1 Score  : "
        f"{recommended_row['f1_score']:.2f}%"
    )


    print()
    print("=" * 75)


    # ========================================================
    # Interpretation
    # ========================================================

    print()
    print("INTERPRETATION")
    print("-" * 75)


    if maximum_f1 == 100:

        print(
            "The synthetic evaluation dataset is "
            "perfectly separated at one or more "
            "tested thresholds."
        )

        print()

        print(
            "This does NOT mean the system has "
            "100% real-world hiring accuracy."
        )

        print()

        print(
            "The result should be reported as "
            "100% on this synthetic benchmark "
            "only."
        )

    else:

        print(
            "The evaluation dataset contains "
            "classification errors at the "
            "tested thresholds."
        )


    print()
    print("=" * 75)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    find_best_threshold()
