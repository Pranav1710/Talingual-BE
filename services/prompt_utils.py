def build_regeneration_prompt(resume_text: str, instructions: str) -> str:
    """
    Combines raw resume text with optional instructions for GPT input.
    Cleanly separates instructions block so GPT can focus on what to update.
    """
    resume_text = resume_text.strip()
    instructions = instructions.strip()

    if instructions:
        return f"{resume_text}\n\n---\nInstructions:\n{instructions}"
    else:
        return resume_text
