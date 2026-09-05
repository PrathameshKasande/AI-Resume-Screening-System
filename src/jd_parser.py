def read_job_description(file):

    try:

        content = file.read()

        if isinstance(
            content,
            bytes
        ):

            content = content.decode(
                "utf-8"
            )

        return content.strip()

    except Exception as error:

        print(
            f"JD reading error: {error}"
        )

        return ""


def read_jd_from_path(
    file_path
):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read().strip()