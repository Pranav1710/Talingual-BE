import os, json
from flask import session

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "../config/default_cv_config.json")

def load_default_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def get_config():
    return session.get("resume_default_config", load_default_config())

def set_config(config):
    session["resume_default_config"] = config

def clear_config():
    session.pop("resume_default_config", None)

def reset_to_default_config():
    session["resume_default_config"] = load_default_config()
