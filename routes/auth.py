# routes/auth.py
from flask import Blueprint
from controllers.auth_controller import (
    get_auth_url_controller,
    oauth_callback_controller,
    logout_controller,
    is_authenticated_controller,
    get_user_controller
)
from flask_login import login_required
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth-url")
def get_auth_url():
    return get_auth_url_controller()

@auth_bp.route("/oauth-callback")
def oauth_callback():
    return oauth_callback_controller()

@auth_bp.route("/logout", methods=["POST"])
def logout():
    return logout_controller()

@auth_bp.route("/is-authenticated")
def is_authenticated():
    return is_authenticated_controller()

@auth_bp.route("/me")
@login_required
def get_user():
    return get_user_controller()
