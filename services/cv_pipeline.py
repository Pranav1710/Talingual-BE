# services/cv_pipeline.py

import openai
from bs4 import BeautifulSoup
import time
from utils.cv_parser import extract_text_from_file
from utils.style_injector import inject_logo, inject_styles
from prompts.talingual_prompt import TALINGUAL_PROMPT

client = openai.OpenAI()  # ✅ instantiate client

def run_cv_pipeline(file, notes: str, config: dict) -> dict:
    resume_text = extract_text_from_file(file)
    system_prompt = TALINGUAL_PROMPT
    notes_block = f"\n\n---\nRecruiter Notes:\n{notes.strip()}" if notes.strip() else ""

    messages = [
        { "role": "system", "content": system_prompt },
        { "role": "user", "content": resume_text + notes_block }
    ]
    start = time.time()
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.2,
        messages=messages
    )
    print(f"GPT call took {time.time() - start:.2f} sec")
    raw_html = response.choices[0].message.content
    if config.get("showLogo", True):  # Default to True if not set
        html_with_logo = inject_logo(raw_html)
    else:
        html_with_logo = raw_html

    # ✅ Apply styles after logo (or directly on raw_html)
    styled_html = inject_styles(html_with_logo, config)

    # ✅ Extract structured sections
    # sections = extract_sections_from_html(raw_html)

    return {
        "html": styled_html,
        "sections": {
            "personal_information": "",
            "profile": "",
            "work_experience": "",
            "education": "",
            "additional_information": ""
        }
    }



def extract_sections_from_html(html: str) -> dict:
    """
    Extracts specific sections from GPT-generated HTML using their expected class names.
    Returns a dict with keys: profile, education, work_experience, additional_information.
    """
    soup = BeautifulSoup(html, "html.parser")

    sections = {
        "profile": "",
        "education": "",
        "work_experience": "",
        "additional_information": ""
    }

    # Profile = all profile-paragraph(s)
    profile_blocks = soup.find_all("p", class_=["profile-paragraph", "profile-paragraph-note"])
    if profile_blocks:
        sections["profile"] = "\n".join(str(p) for p in profile_blocks)

    # Education section
    edu = soup.find("div", class_="section education-section")
    if edu:
        sections["education"] = str(edu)

    # Work Experience section
    work = soup.find("div", class_="section work-section")
    if work:
        sections["work_experience"] = str(work)

    # Additional Information section
    add = soup.find("div", class_="section additional-section")
    if add:
        sections["additional_information"] = str(add)

    return sections
