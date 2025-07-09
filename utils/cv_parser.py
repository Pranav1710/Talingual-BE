# utils/cv_parser.py

import fitz  # PyMuPDF
import docx
import re

def extract_text_from_file(file) -> str:
    """
    Determines the file type and extracts raw text content from PDF, DOCX, or TXT.
    Returns clean text while preserving all original content. No language assumptions.
    """
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        return extract_from_pdf(file)

    elif filename.endswith(".docx"):
        return extract_from_docx(file)

    elif filename.endswith(".txt"):
        return file.read().decode("utf-8", errors="ignore").strip()

    else:
        raise ValueError("Unsupported file type. Accepted formats: PDF, DOCX, TXT.")

def extract_from_pdf(file) -> str:
    """
    Uses PyMuPDF to extract text from all pages of the uploaded PDF.
    Returns clean text without modifying content.
    """
    file.stream.seek(0)
    doc = fitz.open(stream=file.read(), filetype="pdf")
    full_text = ""

    for page in doc:
        full_text += page.get_text()

    return full_text

def extract_from_docx(file) -> str:
    """
    Extracts text from DOCX files using python-docx.
    Returns joined paragraph text as a single string.
    """
    file.stream.seek(0)
    doc = docx.Document(file)
    full_text = "\n".join([para.text for para in doc.paragraphs])
    return full_text

def clean_text(text: str) -> str:
    """
    Applies minimal cleanup without touching content meaning:
    - Removes excessive whitespace
    - Removes common page markers
    """
    text = re.sub(r"\s{2,}", " ", text)               # Collapse multiple spaces
    text = re.sub(r"\n{2,}", "\n", text)              # Collapse multiple newlines
    text = re.sub(r"(?i)page \d+ of \d+", "", text)   # Remove 'Page X of Y'
    return text.strip()
