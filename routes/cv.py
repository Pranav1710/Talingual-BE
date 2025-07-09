# routes/cv.py

from flask import Blueprint
from controllers.cv_controller import (
    generate_cv_controller,
    regenerate_cv_section_controller,
    export_pdf_controller,
    export_docx_controller,
    export_to_google_docs_controller
)
from flask_login import login_required
cv_bp = Blueprint("cv", __name__)

@cv_bp.route("/generate", methods=["POST"])
@login_required
def generate_cv():
    return generate_cv_controller()

@cv_bp.route("/regenerate", methods=["POST"])
@login_required
def regenerate_cv_section():
    return regenerate_cv_section_controller()

@cv_bp.route("/export-pdf", methods=["POST"])
@login_required
def export_pdf():
    return export_pdf_controller()

@cv_bp.route("/export-docx", methods=["POST"])
@login_required
def export_docx():
    return export_docx_controller()

@cv_bp.route("/open-in-google-docs", methods=["POST"])
@login_required
def export_to_google_docs():
    return export_to_google_docs_controller()
