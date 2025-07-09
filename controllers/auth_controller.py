# controllers/auth_controller.py

from flask import request, session, jsonify, redirect
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from utils.config_session import clear_config
from config import BACKEND_URL, FRONTEND_URL
import os, urllib.parse, json, requests, secrets
from flask_login import login_user
from models.user import User

# OAuth Scopes
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/userinfo.email"
]

# Utility to create OAuth Flow
def create_flow(redirect_uri):
    return Flow.from_client_secrets_file(
        "client_id.json",
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )

# Get Google OAuth Authorization URL with CSRF state
def get_auth_url_controller():
    oauth_redirect_uri = f"{BACKEND_URL}/api/auth/oauth-callback"

    flow = create_flow(oauth_redirect_uri)

    csrf_state = secrets.token_urlsafe(16)
    session["oauth_state"] = csrf_state

    auth_url, state = flow.authorization_url(
        access_type="offline",
        prompt="consent",
        include_granted_scopes=False,
        state=csrf_state
    )

    return jsonify({"auth_url": auth_url})

# OAuth Callback Handler
def oauth_callback_controller():
    try:
        code = request.args.get("code")
        state = request.args.get("state")

        # Validate CSRF state
        if state != session.get("oauth_state"):
            return redirect(f"{FRONTEND_URL}/auth-error?msg=Invalid+state+parameter")

        redirect_uri = f"{BACKEND_URL}/api/auth/oauth-callback"

        flow = create_flow(redirect_uri)
        flow.fetch_token(code=code)

        creds = flow.credentials
        if not creds or not creds.token:
            return redirect(f"{FRONTEND_URL}/auth-error?msg=Missing+access+token")

        userinfo_response = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {creds.token}"}
        )

        if userinfo_response.status_code != 200:
            return redirect(f"{FRONTEND_URL}/auth-error?msg=Failed+to+fetch+Google+userinfo")

        email = userinfo_response.json().get("email", "").strip().lower()
        if not email.endswith("@talingual.com"):
            return redirect(f"{FRONTEND_URL}/auth-error?msg=Access+denied+for+{email}")

        # Initialize session
        session.clear()
        session["google_token"] = json.loads(creds.to_json())
        session["email"] = email
        
        user = User(email)
        login_user(user)

        return redirect(FRONTEND_URL)

    except Exception as e:
        error_message = urllib.parse.quote(str(e))
        return redirect(f"{FRONTEND_URL}/internal-error?msg={error_message}")

# Logout Controller
def logout_controller():
    try:
        session.clear()
        return jsonify({"message": "Logged out successfully"})
    except Exception as e:
        print("[LOGOUT ERROR]", e)
        return jsonify({"error": "Logout failed", "details": str(e)}), 500

# Authenticated Status Check with token refresh attempt
def is_authenticated_controller():
    token_data = session.get("google_token")
    if not token_data:
        return jsonify({"authenticated": False})

    try:
        creds = Credentials.from_authorized_user_info(token_data)

        if creds.expired:
            if creds.refresh_token:
                try:
                    creds.refresh(Request())
                    session["google_token"] = json.loads(creds.to_json())
                except Exception as refresh_err:
                    print("[TOKEN REFRESH FAILED]", refresh_err)
                    session.pop("google_token", None)
                    return jsonify({"authenticated": False})
            else:
                print("[NO REFRESH TOKEN]")
                session.pop("google_token", None)
                return jsonify({"authenticated": False})

        return jsonify({"authenticated": not creds.expired})

    except Exception as e:
        print("[AUTH ERROR]", e)
        session.pop("google_token", None)
        return jsonify({"authenticated": False})

# Get Current User Info
def get_user_controller():
    token_data = session.get("google_token")
    email = session.get("email")

    is_authenticated = False
    if token_data:
        try:
            creds = Credentials.from_authorized_user_info(token_data)
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                session["google_token"] = json.loads(creds.to_json())
            is_authenticated = not creds.expired
        except Exception as e:
            print("[USER CHECK ERROR]", e)

    return jsonify({
        "email": email,
        "authenticated": is_authenticated
    })
