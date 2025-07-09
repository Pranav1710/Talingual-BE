# utils/auth_guard.py
from functools import wraps
from flask import session, jsonify

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_email" not in session:
            return jsonify({ "error": "Unauthorized" }), 401
        return f(*args, **kwargs)
    return decorated_function
