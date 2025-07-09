# services/exporter/pdf_exporter.py

import tempfile
from playwright.sync_api import sync_playwright

def generate_pdf(html: str, config: dict) -> str:
    """
    Uses Playwright to render styled HTML to PDF using a headless Chromium browser.
    Returns the path to the generated PDF.
    """
    # 1. Create a temporary HTML file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as tmp_html:
        tmp_html.write(html)
        html_path = tmp_html.name

    # 2. Define path for output PDF
    pdf_path = html_path.replace(".html", ".pdf")

    # 3. Launch Playwright browser to generate PDF
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{html_path}", wait_until="load")

        page.pdf(path=pdf_path, format="A4", margin={
            "top": "20mm", "bottom": "20mm", "left": "18mm", "right": "18mm"
        })

        browser.close()

    return pdf_path
