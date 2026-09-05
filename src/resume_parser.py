#adds candidate-name extraction
import re
import pymupdf


def extract_text_from_pdf(file):

    try:

        document = fitz.open(
            stream=file.read(),
            filetype="pdf"
        )

        text = ""

        for page in document:
            text += page.get_text()

        document.close()

        return text.strip()

    except Exception as error:

        print(
            f"PDF extraction error: {error}"
        )

        return ""


def extract_candidate_name(text):

    if not text:
        return "Unknown Candidate"

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    # Usually the candidate name appears near the top.
    for line in lines[:10]:

        cleaned = line.strip()

        if (
            len(cleaned.split()) >= 2
            and len(cleaned.split()) <= 5
            and not any(
                word in cleaned.lower()
                for word in [
                    "resume",
                    "curriculum",
                    "linkedin",
                    "github",
                    "email",
                    "phone",
                    "engineer",
                    "developer"
                ]
            )
        ):

            if re.match(
                r"^[A-Za-z .'-]+$",
                cleaned
            ):

                return cleaned

    return "Unknown Candidate"


def extract_resume_data(file):

    text = extract_text_from_pdf(file)

    candidate_name = extract_candidate_name(
        text
    )

    return {
        "text": text,
        "candidate_name": candidate_name
    }