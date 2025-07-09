# from flask import Flask
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os

# from config import configure_app
# from routes.auth import auth_bp
# from routes.cv import cv_bp
# from routes.config import config_bp
# from flask_login import LoginManager
# from models.user import User

# load_dotenv()

# app = Flask(__name__)
# configure_app(app)

# CORS(app, supports_credentials=True, expose_headers=["Content-Disposition"])

# # ✅ Setup Flask-Login
# login_manager = LoginManager()
# login_manager.init_app(app)

# # 🔑 This is REQUIRED:
# @login_manager.user_loader
# def load_user(user_id):
#     return User(user_id)  # Simple user loader from the session

# # ✅ Register blueprints
# app.register_blueprint(auth_bp, url_prefix="/api/auth")
# app.register_blueprint(cv_bp, url_prefix="/api/cv")
# app.register_blueprint(config_bp, url_prefix="/api/config")

# @app.route("/api/health")
# def health_check():
#     return {"status": "ok"}

# if __name__ == "__main__":
#     app.run(debug=True)

# prod

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from flask_login import LoginManager
import os

from config import configure_app
from routes.auth import auth_bp
from routes.cv import cv_bp
from routes.config import config_bp
from models.user import User

load_dotenv()

def create_app():
    app = Flask(__name__)
    configure_app(app)

    # Enable CORS — customize allowed origins in production
    CORS(app, supports_credentials=True, expose_headers=["Content-Disposition"])

    # Flask-Login setup
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(cv_bp, url_prefix="/api/cv")
    app.register_blueprint(config_bp, url_prefix="/api/config")

    @app.route("/api/health")
    def health_check():
        return {"status": "ok"}

    return app
