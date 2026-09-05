import pandas as pd


def precision_at_k(
    data,
    k=3
):

    sorted_data = data.sort_values(
        "predicted_score",
        ascending=False
    )

    top_k = sorted_data.head(k)

    relevant = top_k[
        "actual_match"
    ].sum()

    return relevant / k


def main():

    data = pd.read_csv(
        "data/evaluation/labeled_matches.csv"
    )

    k = min(
        3,
        len(data)
    )

    score = precision_at_k(
        data,
        k
    )

    print(
        f"Precision@{k}: "
        f"{score:.2f}"
    )


if __name__ == "__main__":

    main()