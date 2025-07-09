# controllers/cv_controller.py
from flask import request, session, jsonify
from services.exporter.pdf_exporter import generate_pdf
from services.cv_regenerator import regenerate_section
from utils.html_parser import extract_filename_from_html
from io import BytesIO
from flask import send_file
from flask import request, session, jsonify
from services.cv_pipeline import run_cv_pipeline
from utils.logging import log_error
from utils.html_parser import extract_filename_from_html
from flask import send_file


def generate_cv_controller():
    """
    Handles POST /api/cv/generate
    Accepts: multipart/form-data with 'cv' (file) and optional 'notes' (string)
    Returns: full styled HTML + separated resume sections
    """
    try:
        UPLOAD_KEY = "cv"

        # 1. Validate file presence
        if UPLOAD_KEY not in request.files:
            return jsonify({ "error": f"Missing file. Expected '{UPLOAD_KEY}' in form-data." }), 400

        file = request.files[UPLOAD_KEY]
        notes = request.form.get("notes", "").strip()
        config = session.get("resume_default_config", {})

        # 2. Run GPT formatting pipeline
        result = run_cv_pipeline(file, notes, config)

        # 3. Return structured response
        return jsonify({
            "html": result["html"],
            "sections": result["sections"]
        })

    except Exception as e:
        log_error("generate_cv_controller", e)
        return jsonify({
            "error": "Resume formatting failed.",
            "details": str(e)
        }), 500


def export_pdf_controller():
    try:
        html = request.json.get("html", "")
        config = session.get("resume_default_config", {})

        path = generate_pdf(html, config)
        filename = extract_filename_from_html(html)

        return send_file(path, as_attachment=True, download_name=filename)

    except Exception as e:
        log_error("export_pdf_controller", e)
        return jsonify({ "error": "PDF export failed.", "details": str(e) }), 500


from services.exporter.docx_exporter import generate_docx

def export_docx_controller():
    """
    Handles POST /api/cv/export-docx
    Accepts: JSON with 'html'
    Returns: Downloadable DOCX file
    """
    try:
        return generate_docx()
    except Exception as e:
        log_error("export_docx_controller", e)
        return jsonify({ "error": "DOCX export failed.", "details": str(e) }), 500


from services.exporter.google_drive_exporter import export_to_google_docs

def export_to_google_docs_controller():
    """
    Handles POST /api/cv/open-in-google-docs
    Accepts: JSON with 'html'
    Returns: { "google_docs_url": "https://docs.google.com/..." }
    """
    try:
        return export_to_google_docs()
    except Exception as e:
        log_error("export_to_google_docs_controller", e)
        return jsonify({
            "error": "Google Docs export failed.",
            "details": str(e)
        }), 500



def regenerate_cv_section_controller():
    """
    Handles POST /api/cv/regenerate
    Accepts: {
        cv: (File),
        section: "profile" | "education" | "work_experience" | "additional_information",
        notes: string (optional),
        instructions: string (optional)
    }
    Returns: regenerated section HTML
    """
    try:

        file = request.files['cv']
        section = request.form.get("section", "").strip()
        instructions = request.form.get("instructions", "").strip()
        config = session.get("resume_default_config", {})

        if section not in {"profile", "education", "work_experience", "additional_information"}:
            return jsonify({ "error": f"Unsupported section: '{section}'" }), 400

        html = regenerate_section(file, section, instructions, config)

        return jsonify({ "html": html })

    except Exception as e:
        log_error("regenerate_cv_section_controller", e)
        return jsonify({
            "error": "Section regeneration failed.",
            "details": str(e)
        }), 500
