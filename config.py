# config.py
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

MODE = os.getenv("ENVIRONMENT", "dev").lower()

BACKEND_URL = os.getenv(f"BACKEND_URL_{MODE.upper()}")
FRONTEND_URL = os.getenv(f"FRONTEND_URL_{MODE.upper()}")
GOOGLE_CLIENT_ID = os.getenv(f"GOOGLE_CLIENT_ID_{MODE.upper()}")
GOOGLE_CLIENT_SECRET = os.getenv(f"GOOGLE_CLIENT_SECRET_{MODE.upper()}")
SECRET_KEY = os.getenv("SECRET_KEY")

def configure_app(app):
    app.secret_key = SECRET_KEY
    app.config.update({
        "SESSION_COOKIE_NAME": "talingual_session",
        "SESSION_COOKIE_HTTPONLY": True,
        "SESSION_COOKIE_SAMESITE": "None" if MODE == "prod" else "Lax",
        "SESSION_COOKIE_SECURE": MODE == "prod",
        "PERMANENT_SESSION_LIFETIME": timedelta(days=30)
    })

    print(f"[CONFIG] Mode: {MODE}, Backend: {BACKEND_URL}, Frontend: {FRONTEND_URL}")
