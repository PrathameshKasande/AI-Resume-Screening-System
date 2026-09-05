
"""
Evaluation metrics for the AI Resume Screening System.
"""

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


def calculate_metrics(
    actual_labels,
    predicted_labels
):

    accuracy = accuracy_score(
        actual_labels,
        predicted_labels
    )

    precision = precision_score(
        actual_labels,
        predicted_labels,
        zero_division=0
    )

    recall = recall_score(
        actual_labels,
        predicted_labels,
        zero_division=0
    )

    f1 = f1_score(
        actual_labels,
        predicted_labels,
        zero_division=0
    )

    matrix = confusion_matrix(
        actual_labels,
        predicted_labels,
        labels=[0, 1]
    )

    tn, fp, fn, tp = matrix.ravel()


    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp)
    }


def print_metrics(metrics):

    print()
    print("=" * 70)
    print(
        "AI RESUME SCREENING MODEL EVALUATION"
    )
    print("=" * 70)

    print(
        f"Accuracy       : "
        f"{metrics['accuracy'] * 100:.2f}%"
    )

    print(
        f"Precision      : "
        f"{metrics['precision'] * 100:.2f}%"
    )

    print(
        f"Recall         : "
        f"{metrics['recall'] * 100:.2f}%"
    )

    print(
        f"F1 Score       : "
        f"{metrics['f1'] * 100:.2f}%"
    )

    print()
    print("Confusion Matrix")
    print("-" * 40)

    print(
        f"True Negative  (TN) : "
        f"{metrics['tn']}"
    )

    print(
        f"False Positive (FP) : "
        f"{metrics['fp']}"
    )

    print(
        f"False Negative (FN) : "
        f"{metrics['fn']}"
    )

    print(
        f"True Positive  (TP) : "
        f"{metrics['tp']}"
    )

    print("=" * 70)