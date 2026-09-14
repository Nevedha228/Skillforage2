import pymupdf


def extract_text_from_pdf(file_path):
    """
    Extract all text from a PDF resume.
    """

    doc = pymupdf.open(file_path)

    text = ""

    for page in doc:
        text += page.get_text("text")

    doc.close()

    return text.strip()