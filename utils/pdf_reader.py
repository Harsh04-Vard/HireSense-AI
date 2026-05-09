import fitz
from docx import Document


def extract_text_from_pdf(pdf_path):

    text = ""

    doc = fitz.open(pdf_path)

    for page in doc:
        text += page.get_text()

    return text


def extract_text_from_docx(docx_path):

    doc = Document(docx_path)

    text = "\n".join([
        para.text for para in doc.paragraphs
    ])

    return text