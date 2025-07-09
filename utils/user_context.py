# utils/user_context.py
from flask import session

def current_user():
    return {
        "email": session.get("user_email"),
        "domain": session.get("user_domain"),
        "is_authenticated": session.get("is_authenticated", False),
        "logged_in_at": session.get("logged_in_at")
    }
