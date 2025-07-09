# services/section_prompt_builder.py

import json
from prompts.talingual_prompt import TALINGUAL_PROMPT

def get_section_prompt(section: str) -> str:
    """
    Builds a system prompt for GPT-4 to regenerate a specific CV section.
    Includes tone, formatting, and section-specific rules.
    """

    style = TALINGUAL_PROMPT.get("style_guide", {})
    section_rules = TALINGUAL_PROMPT.get("output_structure", {}).get(section)

    if not section_rules:
        raise ValueError(f"Section '{section}' is not defined in output_structure.")

    section_label = section.replace("_", " ").title()

    return (
        f"Regenerate only the '{section_label}' section of the CV.\n\n"
        f"Tone: {style.get('tone')}\n"
        f"Language: {style.get('language')}\n"
        f"HTML Formatting Rules: {style.get('formatting')}\n\n"
        f"Section Rules:\n{json.dumps(section_rules, indent=2)}\n\n"
        "Do not modify or reformat other sections of the CV. "
        "Only return valid HTML for the requested section."
    )
