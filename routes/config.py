# routes/config.py
from flask import Blueprint
from controllers.config_controller import (
    get_config_controller,
    set_config_controller,
    clear_config_controller,
    reset_config_controller
)
from flask_login import login_required
config_bp = Blueprint("config", __name__)

@config_bp.route("/get", methods=["GET"])
@login_required
def get_config():
    return get_config_controller()

@config_bp.route("/set", methods=["POST"])
@login_required
def set_config():
    return set_config_controller()

@config_bp.route("/clear", methods=["POST"])
@login_required
def clear_config():
    return clear_config_controller()

@config_bp.route("/reset", methods=["POST"])
@login_required
def reset_config():
    return reset_config_controller()
