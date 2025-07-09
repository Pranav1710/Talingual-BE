# controllers/config_controller.py
from flask import request, jsonify
from utils.config_session import (
    get_config,
    set_config,
    clear_config,
    reset_to_default_config
)
from utils.logging import log_error

def get_config_controller():
    try:
        return jsonify(get_config())
    except Exception as e:
        log_error("get_config", e)
        return jsonify({ "error": "Could not get config" }), 500

def set_config_controller():
    try:
        data = request.get_json()
        config = data.get("config", {})
        set_config(config)
        return jsonify({ "status": "saved" })
    except Exception as e:
        log_error("set_config", e)
        return jsonify({ "error": "Could not save config" }), 500

def clear_config_controller():
    try:
        clear_config()
        return jsonify({ "status": "cleared" })
    except Exception as e:
        log_error("clear_config", e)
        return jsonify({ "error": "Could not clear config" }), 500

def reset_config_controller():
    try:
        reset_to_default_config()
        return jsonify({ "status": "reset" })
    except Exception as e:
        log_error("reset_config", e)
        return jsonify({ "error": "Could not reset config" }), 500
