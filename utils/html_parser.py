# utils/html_parser.py

import re

def extract_filename_from_html(html: str) -> str:
    """
    Extracts the full name from <p class="info-field">Name: John Smith</p>
    and returns a safe filename like john_smith.pdf
    """
    match = re.search(r'<p class=["\']info-field["\']>\s*Name:\s*(.+?)\s*</p>', html, re.IGNORECASE)
    if match:
        full_name = match.group(1).strip()
        safe_name = re.sub(r"[^\w\s-]", "", full_name)         # Remove special chars
        safe_name = re.sub(r"\s+", "_", safe_name).lower()     # Convert to snake_case
        return f"{safe_name}.pdf"

    return "talingual_resume.pdf"
