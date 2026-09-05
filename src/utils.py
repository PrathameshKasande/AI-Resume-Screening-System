import os


def ensure_directory(
    directory
):

    if not os.path.exists(
        directory
    ):

        os.makedirs(directory)


def format_percentage(
    score
):

    return f"{score:.2f}%"