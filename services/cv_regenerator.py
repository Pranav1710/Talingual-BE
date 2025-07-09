# services/cv_regenerator.py

import openai
from utils.cv_parser import extract_text_from_file
from services.section_prompt_builder import get_section_prompt
from services.prompt_utils import build_regeneration_prompt

def regenerate_section(file, section: str, instructions: str, config: dict) -> str:
    """
    Regenerates a single section of the CV using GPT-4 based on custom instructions.
    Returns only the regenerated section HTML (no styling or logo).
    """
    # 1. Extract resume text (untouched)
    resume_text = extract_text_from_file(file)

    # 2. Build scoped prompts
    system_prompt = get_section_prompt(section)
    user_prompt = build_regeneration_prompt(resume_text, instructions)

    # 3. Call GPT-4
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0.4,
        messages=[
            { "role": "system", "content": system_prompt },
            { "role": "user", "content": user_prompt }
        ]
    )

    return response["choices"][0]["message"]["content"]
