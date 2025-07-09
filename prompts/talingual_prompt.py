import json
import os

PROMPT_FILE = os.path.join(os.path.dirname(__file__), "talingual_system_prompt.json")

with open(PROMPT_FILE, "r", encoding="utf-8") as f:
    prompt_dict = json.load(f)

# Convert the entire prompt JSON into a clean string
TALINGUAL_PROMPT = json.dumps(prompt_dict, indent=2)
