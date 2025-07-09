# services/exporter/google_drive_exporter.py

import json
import os
from flask import request, session
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

from services.exporter.docx_exporter import convert_html_to_docx
from utils.html_parser import extract_filename_from_html


from flask import session
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

def get_user_google_credentials():
    """
    Retrieves and refreshes Google credentials from session.
    """
    token_data = session.get("google_token")
    if not token_data:
        raise Exception("Google token missing or user not authenticated.")

    creds = Credentials.from_authorized_user_info(token_data)

    # Attempt to refresh if expired
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Update session with new token after refresh
        session["google_token"] = json.loads(creds.to_json())

    return creds



def upload_docx_to_drive(creds, docx_path, filename="Talingual Resume.docx"):
    """
    Uploads a DOCX to Google Drive and converts it to Google Docs format.
    Returns the Google Docs edit link.
    """
    service = build("drive", "v3", credentials=creds)

    file_metadata = {
        "name": filename,
        "mimeType": "application/vnd.google-apps.document"
    }

    media = MediaFileUpload(
        docx_path,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    uploaded = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    return f"https://docs.google.com/document/d/{uploaded['id']}/edit"


def export_to_google_docs():
    """
    Main Flask route handler for exporting to Google Docs.
    Uses session config, HTML, and Google credentials.
    """
    html = request.json.get("html", "")
    config = session.get("resume_default_config", {})
    creds = get_user_google_credentials()

    docx_path = convert_html_to_docx(html, config)
    filename = extract_filename_from_html(html).replace(".pdf", ".docx")

    link = upload_docx_to_drive(creds, docx_path, filename)
    return { "google_docs_url": link }
