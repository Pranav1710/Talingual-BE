# utils/config_session.py
import os, json
from flask import session

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/default_cv_config.json")

def load_default_config():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError("Missing default_cv_config.json")

    if os.path.getsize(CONFIG_PATH) == 0:
        raise ValueError("default_cv_config.json is empty")

    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def get_config():
    try:
        return session.get("resume_default_config", load_default_config())
    except Exception as e:
        print("[GET CONFIG ERROR]", str(e))
        return {}  # fallback to empty config (optional)

def set_config(config: dict):
    session["resume_default_config"] = config

def clear_config():
    session.pop("resume_default_config", None)

def reset_to_default_config():
    session["resume_default_config"] = load_default_config()
