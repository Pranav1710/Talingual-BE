# utils/style_injector.py

import os

def inject_logo(html, show_logo=True):
    """
    Injects the Talingual logo (base64) above the resume HTML if show_logo is True.
    """
    if not show_logo:
        return html

    try:
        logo_path = os.path.join("static", "logo_base64.txt")
        with open(logo_path, "r") as f:
            base64_data = f.read().strip()
            logo_img = f'<img class="resume-logo" src="{base64_data}" alt="Talingual Logo" />'
        return f"{logo_img}\n{html}"
    except Exception as e:
        print("[LOGO INJECTION ERROR]", e)
        return html


def inject_styles(html, config=None):
    """
    Wraps GPT-generated HTML with injected <style> for font, spacing, and layout.
    Styling is based on session config: fontFamily, fontSize, lineSpacing, logoSize.
    """
    config = config or {}

    font = config.get("fontFamily") or "Arial"
    font_px = config.get("fontSize", "13px").replace("px", "")
    logo_width = config.get("logoSize", "250px")
    line_height = config.get("lineSpacing") or 1.4

    try:
        px_val = float(font_px)
        preview_px = round(px_val * 1.333, 2)
        font_size = f"{preview_px}px"
    except:
        font_size = "17.33px"

    css = f"""
    .resume-preview {{
      font-family: {font}, sans-serif;
      font-size: {font_size};
      line-height: {line_height};
      color: #000;
      max-width: 800px;
      margin: 40px auto;
    }}

    .resume-preview .resume-logo {{
      width: {logo_width};
      display: block;
      margin-bottom: 16px;
    }}

    .resume-preview .info-field {{
      margin: 0 0 4px 0;
    }}

    .resume-preview .profile-paragraph {{
      margin: 12px 0 8px 0;
    }}
    .resume-preview .profile-paragraph-note {{
      margin: 0 0 14px 0;
    }}

    .resume-preview .section {{
      margin-top: 26px;
    }}
    .resume-preview .section h2 {{
      font-size: 15px;
      font-weight: bold;
      margin: 0 0 10px 0;
    }}

    .resume-preview .work-dates {{
      margin: 12px 0 2px 0;
      font-weight: normal;
    }}
    .resume-preview .work-title {{
      margin: 0 0 8px 0;
      font-weight: normal;
    }}
    .resume-preview .work-bullet-list,
    .resume-preview .edu-bullet-list {{
      margin: 0 0 8px 0;
      padding-left: 20px;
    }}
    .resume-preview .work-bullet,
    .resume-preview .edu-bullet {{
      margin-bottom: 5px;
    }}

    .resume-preview .edu-line-1 {{
      margin: 12px 0 4px 0;
    }}
    .resume-preview .edu-line-2 {{
      margin: 4px 0;
    }}

    .resume-preview .add-list {{
      padding-left: 20px;
      margin-top: 8px;
    }}
    .resume-preview .add-bullet {{
      margin-bottom: 5px;
    }}
    """

    return f"<style>{css}</style>\n<div class='resume-preview'>\n{html}\n</div>"
