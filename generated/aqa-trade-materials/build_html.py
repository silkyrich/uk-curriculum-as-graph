"""
build_html.py — Build a self-contained HTML presentation from curriculum_unit.json

Features:
  - All slide types rendered as HTML
  - Harris Clapham (or custom) colour scheme from meta.color_scheme
  - Keyboard navigation (← → Space), slide counter, progress bar
  - Speaker notes panel (toggle with N key) — teacher notes inline
  - Progressive diagram overlays (slide type: diagram_sequence)
  - External resource links clickable
  - Print-friendly (Ctrl+P prints each slide)
  - Self-contained: images embedded as base64 or referenced by relative path

Usage:
    python3 build_html.py <curriculum_unit.json> [output.html] [--embed-images]
"""

import json
import sys
import os
import base64
from pathlib import Path
from html import escape


# ── Colour schemes ─────────────────────────────────────────────────────────────

SCHEMES = {
    "harris_clapham": {
        "bg":             "#FFFFFF",
        "title_bar":      "#009FA3",
        "title_text":     "#FFFFFF",
        "body_text":      "#2B576B",
        "accent":         "#121F47",
        "accent_light":   "#009FA3",
        "section_bg":     "#121F47",
        "section_text":   "#009FA3",
        "callout_bg":     "#E0F7F7",
        "callout_border": "#009FA3",
        "error_bg":       "#FEE2E2",
        "error_text":     "#7F1D1D",
        "success_bg":     "#D1FAE5",
        "success_text":   "#065F46",
        "subtle_bg":      "#F4FBFB",
        "muted":          "#656565",
        "ao1":            "#06B6D4",
        "ao2":            "#10B981",
        "ao3":            "#F59E0B",
        "ao4":            "#EF4444",
    },
    "economics": {
        "bg":             "#FFFFFF",
        "title_bar":      "#1B2A4A",
        "title_text":     "#FFFFFF",
        "body_text":      "#1B2A4A",
        "accent":         "#F59E0B",
        "accent_light":   "#FEF3C7",
        "section_bg":     "#1B2A4A",
        "section_text":   "#F59E0B",
        "callout_bg":     "#FEF3C7",
        "callout_border": "#F59E0B",
        "error_bg":       "#FEE2E2",
        "error_text":     "#7F1D1D",
        "success_bg":     "#D1FAE5",
        "success_text":   "#065F46",
        "subtle_bg":      "#F8FAFC",
        "muted":          "#64748B",
        "ao1":            "#06B6D4",
        "ao2":            "#10B981",
        "ao3":            "#F59E0B",
        "ao4":            "#EF4444",
    },
}


def img_src(path: str, base_dir: Path, embed: bool) -> str:
    """Return an img src — base64 data URI if embed=True, else relative path."""
    full = base_dir / path
    if not full.exists():
        return ""
    if embed:
        mime = "image/png" if str(path).endswith(".png") else "image/jpeg"
        data = base64.b64encode(full.read_bytes()).decode()
        return f"data:{mime};base64,{data}"
    return path


def ao_badge(ao: str, c: dict) -> str:
    colour = c.get(f"ao{ao[-1].lower()}", c["accent"])
    return f'<span class="ao-badge" style="background:{colour}">{escape(ao)}</span>'


def render_bullets(bullets: list, c: dict, base_font: int = 18) -> str:
    if not bullets:
        return ""
    items = []
    for b in bullets:
        if isinstance(b, str):
            text, level, highlight, ao_tag = b, 1, False, None
        else:
            text = b.get("text", "")
            level = b.get("level", 1)
            highlight = b.get("highlight", False)
            ao_tag = b.get("ao_tag")

        indent = (level - 1) * 20
        font_size = max(base_font - (level - 1) * 2, 12)
        colour = c["accent"] if highlight else c["body_text"]
        weight = "600" if highlight else "400"

        badge = ao_badge(ao_tag, c) if ao_tag else ""
        items.append(
            f'<li style="margin-left:{indent}px;font-size:{font_size}px;'
            f'color:{colour};font-weight:{weight};margin-bottom:6px">'
            f'{badge}{escape(text)}</li>'
        )
    return f'<ul style="list-style:none;padding:0;margin:0">{"".join(items)}</ul>'


def render_speaker_notes(notes: str) -> str:
    if not notes:
        return ""
    paragraphs = notes.strip().split("\n")
    html_lines = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            html_lines.append("<br>")
        elif p.startswith("─"):
            html_lines.append('<hr style="border-color:#334155;margin:8px 0">')
        else:
            html_lines.append(f'<p style="margin:4px 0">{escape(p)}</p>')
    return "\n".join(html_lines)


# ── Slide renderers ────────────────────────────────────────────────────────────

def slide_title(data: dict, c: dict, base_dir: Path, embed: bool) -> str:
    bg_img = data.get("background_image", "")
    overlay = ""
    bg_style = f"background:{c['bg']}"
    if bg_img:
        src = img_src(bg_img, base_dir, embed)
        if src:
            bg_style = f"background:url('{src}') center/cover"
            overlay = f'<div style="position:absolute;inset:0;background:{c["section_bg"]};opacity:0.75"></div>'

    tag_line = escape(data.get("tag_line", ""))
    subtitle = escape(data.get("subtitle", ""))

    return f'''
<div class="slide-inner" style="{bg_style};position:relative">
  {overlay}
  <div style="position:relative;z-index:1;display:flex;flex-direction:column;justify-content:center;height:100%;padding:60px 70px">
    <div style="width:60px;height:5px;background:{c['title_bar']};margin-bottom:30px"></div>
    <h1 style="font-size:42px;font-weight:700;color:{c['section_bg'] if not bg_img else '#fff'};line-height:1.2;margin:0 0 16px 0">{escape(data.get('title',''))}</h1>
    {f'<p style="font-size:22px;color:{c["title_bar"]};font-style:italic;margin:0 0 12px 0">{subtitle}</p>' if subtitle else ''}
    {f'<p style="font-size:14px;color:{c["muted"]};margin:0">{tag_line}</p>' if tag_line else ''}
  </div>
</div>'''


def slide_section_header(data: dict, c: dict, **_) -> str:
    num = escape(data.get("section_number", ""))
    title = escape(data.get("section_title", ""))
    sub = escape(data.get("subtitle", ""))
    return f'''
<div class="slide-inner" style="background:{c['section_bg']};display:flex;flex-direction:column;justify-content:center;padding:60px 70px">
  {f'<p style="font-size:16px;color:{c["title_bar"]};font-weight:600;margin:0 0 12px 0;letter-spacing:2px;text-transform:uppercase">{num}</p>' if num else ''}
  <div style="width:80px;height:4px;background:{c['title_bar']};margin-bottom:24px"></div>
  <h2 style="font-size:44px;font-weight:700;color:{c['section_text']};margin:0 0 16px 0;line-height:1.2">{title}</h2>
  {f'<p style="font-size:18px;color:{c["muted"]};font-style:italic;margin:0">{sub}</p>' if sub else ''}
</div>'''


def slide_content(data: dict, c: dict, base_dir: Path, embed: bool) -> str:
    image = data.get("image", "")
    bullets = data.get("bullets", [])
    callout = data.get("callout", "")
    subtitle = data.get("subtitle", "")

    img_html = ""
    if image:
        src = img_src(image, base_dir, embed)
        if src:
            img_html = f'<div style="flex:0 0 42%;padding-left:24px"><img src="{src}" style="width:100%;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.12)"></div>'

    callout_html = ""
    if callout:
        callout_html = f'''
<div style="margin-top:16px;padding:12px 16px;background:{c['callout_bg']};
     border-left:4px solid {c['callout_border']};border-radius:4px;
     font-size:14px;color:{c['body_text']};font-style:italic">
  {escape(callout)}
</div>'''

    content_width = "58%" if img_html else "100%"
    return f'''
<div class="slide-inner" style="background:{c['bg']}">
  <div class="title-bar" style="background:{c['title_bar']};padding:16px 36px">
    <h2 style="margin:0;font-size:26px;font-weight:700;color:{c['title_text']}">{escape(data.get('title',''))}</h2>
    {f'<p style="margin:4px 0 0;font-size:14px;color:rgba(255,255,255,0.8);font-style:italic">{escape(subtitle)}</p>' if subtitle else ''}
  </div>
  <div style="display:flex;padding:24px 36px;flex:1;align-items:flex-start">
    <div style="flex:1;width:{content_width}">
      {render_bullets(bullets, c)}
      {callout_html}
    </div>
    {img_html}
  </div>
</div>'''


def slide_two_column(data: dict, c: dict, base_dir: Path, embed: bool) -> str:
    left = data.get("left", {})
    right = data.get("right", {})

    def col_html(col: dict) -> str:
        heading = col.get("heading", "")
        bullets = col.get("bullets", col.get("content", []))
        image = col.get("image", "")
        h = f'<p style="font-size:15px;font-weight:600;color:{c["title_bar"]};margin:0 0 10px;text-transform:uppercase;letter-spacing:1px">{escape(heading)}</p>' if heading else ""
        img_h = ""
        if image:
            src = img_src(image, base_dir, embed)
            if src:
                img_h = f'<img src="{src}" style="width:100%;border-radius:6px;margin-top:12px">'
        return h + render_bullets(bullets, c, 16) + img_h

    return f'''
<div class="slide-inner" style="background:{c['bg']}">
  <div class="title-bar" style="background:{c['title_bar']};padding:16px 36px">
    <h2 style="margin:0;font-size:26px;font-weight:700;color:{c['title_text']}">{escape(data.get('title',''))}</h2>
  </div>
  <div style="display:flex;padding:24px 36px;flex:1;gap:24px">
    <div style="flex:1;padding-right:16px;border-right:2px solid {c['title_bar']}">{col_html(left)}</div>
    <div style="flex:1;padding-left:8px">{col_html(right)}</div>
  </div>
</div>'''


def slide_diagram(data: dict, c: dict, base_dir: Path, embed: bool) -> str:
    image = data.get("image", "")
    steps = data.get("diagram_steps", [])
    description = data.get("diagram_description", "")
    annotation = data.get("annotation_notes", "")

    img_html = ""
    if image:
        src = img_src(image, base_dir, embed)
        if src:
            img_html = f'<img src="{src}" style="max-width:100%;max-height:340px;border-radius:6px;box-shadow:0 2px 12px rgba(0,0,0,0.1)">'

    steps_html = ""
    if steps:
        step_items = "".join(
            f'<li style="margin-bottom:6px;font-size:14px;color:{c["body_text"]}">'
            f'<strong style="color:{c["title_bar"]}">Step {i+1}:</strong> {escape(s)}</li>'
            for i, s in enumerate(steps)
        )
        steps_html = f'<ol style="padding-left:20px;margin:0">{step_items}</ol>'

    ann_html = ""
    if annotation:
        ann_html = f'''
<div style="margin-top:12px;padding:10px 14px;background:{c['error_bg']};
     border-radius:4px;font-size:13px;color:{c['error_text']}">
  ⚠ {escape(annotation)}
</div>'''

    desc_html = ""
    if description and not image:
        desc_html = f'''
<div style="padding:12px 16px;background:{c['subtle_bg']};border-left:4px solid {c['accent']};
     border-radius:4px;font-size:14px;color:{c['body_text']};font-style:italic;margin-bottom:16px">
  {escape(description)}
</div>'''

    layout = "flex-direction:row;gap:24px" if img_html and steps_html else "flex-direction:column"
    return f'''
<div class="slide-inner" style="background:{c['bg']}">
  <div class="title-bar" style="background:{c['title_bar']};padding:16px 36px">
    <h2 style="margin:0;font-size:26px;font-weight:700;color:{c['title_text']}">{escape(data.get('title',''))}</h2>
  </div>
  <div style="display:flex;{layout};padding:20px 36px;flex:1;align-items:flex-start">
    <div style="flex:{'0 0 60%' if steps_html else '1'};text-align:center">{desc_html}{img_html}{ann_html}</div>
    {f'<div style="flex:1">{steps_html}</div>' if steps_html else ''}
  </div>
</div>'''


def slide_diagram_sequence(data: dict, c: dict, base_dir: Path, embed: bool) -> str:
    """Progressive diagram build — each step is a separate overlaid image, revealed in sequence."""
    steps = data.get("steps", [])  # list of {image, label, notes}
    if not steps:
        return slide_diagram(data, c, base_dir, embed)

    step_divs = []
    for i, step in enumerate(steps):
        src = img_src(step.get("image", ""), base_dir, embed) if step.get("image") else ""
        label = escape(step.get("label", f"Step {i+1}"))
        visibility = "visible" if i == 0 else "hidden"
        opacity = "1" if i == 0 else "0"
        img_tag = f'<img src="{src}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:contain">' if src else f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:18px;color:{c["muted"]}">[{label} — image pending]</div>'
        step_divs.append(
            f'<div class="diagram-step" data-step="{i}" '
            f'style="position:absolute;inset:0;visibility:{visibility};opacity:{opacity};transition:opacity 0.3s">'
            f'{img_tag}</div>'
        )

    step_labels = "".join(
        f'<span class="step-dot" data-step="{i}" '
        f'style="display:inline-block;width:10px;height:10px;border-radius:50%;'
        f'background:{"" + c["title_bar"] if i == 0 else c["muted"]};margin:0 4px;cursor:pointer"></span>'
        for i in range(len(steps))
    )

    slide_id = data.get("slide_id", "seq").replace("-", "_")
    return f'''
<div class="slide-inner" style="background:{c['bg']}">
  <div class="title-bar" style="background:{c['title_bar']};padding:12px 36px">
    <h2 style="margin:0;font-size:24px;font-weight:700;color:{c['title_text']}">{escape(data.get('title',''))}</h2>
  </div>
  <div style="flex:1;position:relative;margin:12px 36px">
    {"".join(step_divs)}
  </div>
  <div style="text-align:center;padding:8px;background:{c['subtle_bg']}">
    <button onclick="prevStep('{slide_id}')" style="margin-right:12px;padding:4px 12px;background:{c['title_bar']};color:white;border:none;border-radius:4px;cursor:pointer">◀ Back</button>
    {step_labels}
    <button onclick="nextStep('{slide_id}')" style="margin-left:12px;padding:4px 12px;background:{c['title_bar']};color:white;border:none;border-radius:4px;cursor:pointer">Next ▶</button>
  </div>
</div>
<script>
window.diagramState = window.diagramState || {{}};
window.diagramState['{slide_id}'] = 0;
function showStep(id, n) {{
  var steps = document.querySelectorAll('[data-step]');
  document.querySelectorAll('.diagram-step').forEach(function(el) {{
    el.style.visibility = 'hidden'; el.style.opacity = '0';
  }});
  var target = document.querySelector('.diagram-step[data-step="' + n + '"]');
  if (target) {{ target.style.visibility = 'visible'; target.style.opacity = '1'; }}
  window.diagramState[id] = n;
}}
function nextStep(id) {{
  var cur = window.diagramState[id] || 0;
  var total = {len(steps)};
  showStep(id, Math.min(cur + 1, total - 1));
}}
function prevStep(id) {{
  var cur = window.diagramState[id] || 0;
  showStep(id, Math.max(cur - 1, 0));
}}
</script>'''


def slide_worked_example(data: dict, c: dict, **_) -> str:
    steps = data.get("steps", [])
    exam_tip = data.get("exam_tip", "")

    step_items = []
    for s in steps:
        if isinstance(s, str):
            step_items.append(f'<li style="margin-bottom:8px;font-size:17px;color:{c["body_text"]}">{escape(s)}</li>')
        else:
            step_items.append(
                f'<li style="margin-bottom:8px;font-size:{18 - (s.get("level",1)-1)*2}px;'
                f'margin-left:{(s.get("level",1)-1)*20}px;color:{c["body_text"]}">'
                f'{escape(s.get("text",""))}</li>'
            )

    tip_html = ""
    if exam_tip:
        tip_html = f'''
<div style="margin-top:16px;padding:12px 16px;background:{c['callout_bg']};
     border-left:4px solid {c['callout_border']};border-radius:4px">
  <strong style="font-size:14px;color:{c['body_text']}">Exam tip:</strong>
  <span style="font-size:14px;color:{c['body_text']}"> {escape(exam_tip)}</span>
</div>'''

    return f'''
<div class="slide-inner" style="background:{c['bg']}">
  <div class="title-bar" style="background:{c['title_bar']};padding:16px 36px">
    <h2 style="margin:0;font-size:26px;font-weight:700;color:{c['title_text']}">{escape(data.get('title',''))}</h2>
  </div>
  <div style="padding:20px 36px;flex:1">
    <ol style="padding-left:24px;margin:0">{"".join(step_items)}</ol>
    {tip_html}
  </div>
</div>'''


def slide_question(data: dict, c: dict, **_) -> str:
    marks = data.get("marks", "")
    ao_tags = data.get("ao_tags", [])
    question_text = data.get("question_text", "")
    hint = data.get("hint", "")
    time_guidance = data.get("time_guidance", "")

    badges = "".join(ao_badge(ao, c) for ao in ao_tags)
    hint_html = ""
    if hint:
        hint_html = f'''
<div style="margin-top:14px;padding:10px 14px;background:{c['callout_bg']};
     border-left:4px solid {c['callout_border']};border-radius:4px;font-size:14px;font-style:italic;color:{c['body_text']}">
  Hint: {escape(hint)}
</div>'''

    return f'''
<div class="slide-inner" style="background:{c['bg']}">
  <div class="title-bar" style="background:{c['title_bar']};padding:16px 36px;display:flex;justify-content:space-between;align-items:center">
    <h2 style="margin:0;font-size:26px;font-weight:700;color:{c['title_text']}">{escape(data.get('title','Practice Question'))}</h2>
    <div>
      {badges}
      {f'<span style="background:{c["accent"]};color:white;padding:4px 12px;border-radius:20px;font-weight:700;font-size:15px;margin-left:8px">[{marks} marks]</span>' if marks else ''}
    </div>
  </div>
  <div style="padding:24px 36px;flex:1">
    <div style="padding:20px 24px;background:{c['subtle_bg']};border:2px solid {c['body_text']};border-radius:6px;font-size:18px;line-height:1.6;color:{c['body_text']}">
      {escape(question_text)}
    </div>
    {f'<p style="font-size:13px;color:{c["muted"]};margin-top:8px;font-style:italic">Suggested time: {escape(time_guidance)}</p>' if time_guidance else ''}
    {hint_html}
  </div>
</div>'''


def slide_examiner_tip(data: dict, c: dict, **_) -> str:
    error = data.get("common_error", "")
    correction = data.get("correction", "")
    quote = data.get("examiner_quote", "")
    source = data.get("source", "")

    return f'''
<div class="slide-inner" style="background:{c['bg']}">
  <div class="title-bar" style="background:{c['title_bar']};padding:16px 36px">
    <h2 style="margin:0;font-size:26px;font-weight:700;color:{c['title_text']}">{escape(data.get('title','Common Exam Error'))}</h2>
  </div>
  <div style="padding:20px 36px;flex:1;display:flex;flex-direction:column;gap:14px">
    <div style="padding:14px 18px;background:{c['error_bg']};border-left:5px solid #DC2626;border-radius:4px">
      <div style="font-size:12px;font-weight:700;color:{c['error_text']};text-transform:uppercase;letter-spacing:1px;margin-bottom:6px">✗ Common error</div>
      <div style="font-size:16px;color:{c['error_text']}">{escape(error)}</div>
    </div>
    <div style="padding:14px 18px;background:{c['success_bg']};border-left:5px solid #059669;border-radius:4px">
      <div style="font-size:12px;font-weight:700;color:{c['success_text']};text-transform:uppercase;letter-spacing:1px;margin-bottom:6px">✓ Correct approach</div>
      <div style="font-size:16px;color:{c['success_text']}">{escape(correction)}</div>
    </div>
    {f'''<div style="padding:12px 16px;background:{c['subtle_bg']};border-radius:4px;font-size:14px;font-style:italic;color:{c['muted']}">
      Examiner report: &ldquo;{escape(quote)}&rdquo;{f' <em>— {escape(source)}</em>' if source else ''}
    </div>''' if quote else ''}
  </div>
</div>'''


def slide_summary(data: dict, c: dict, **_) -> str:
    key_points = data.get("key_points", [])
    next_steps = data.get("next_steps", "")
    return f'''
<div class="slide-inner" style="background:{c['bg']}">
  <div class="title-bar" style="background:{c['title_bar']};padding:16px 36px">
    <h2 style="margin:0;font-size:26px;font-weight:700;color:{c['title_text']}">{escape(data.get('title','Summary'))}</h2>
  </div>
  <div style="padding:20px 36px;flex:1">{render_bullets(key_points, c)}</div>
  {f'<div style="background:{c["section_bg"]};padding:14px 36px"><p style="margin:0;font-size:16px;color:{c["title_bar"]}">Next: {escape(next_steps)}</p></div>' if next_steps else ''}
</div>'''


RENDERERS = {
    "title":            slide_title,
    "section_header":   slide_section_header,
    "content":          slide_content,
    "two_column":       slide_two_column,
    "diagram":          slide_diagram,
    "diagram_sequence": slide_diagram_sequence,
    "worked_example":   slide_worked_example,
    "question":         slide_question,
    "examiner_tip":     slide_examiner_tip,
    "summary":          slide_summary,
}


# ── HTML shell ─────────────────────────────────────────────────────────────────

def build_html(unit_path: str, output_path: str = None, embed_images: bool = False):
    unit_path = Path(unit_path)
    base_dir = unit_path.parent

    with open(unit_path) as f:
        unit = json.load(f)

    meta = unit.get("meta", {})
    scheme_name = meta.get("color_scheme", "economics")
    c = SCHEMES.get(scheme_name, SCHEMES["economics"])

    # Flatten slides from sections (same logic as build_all.py)
    sections = unit.get("sections", [])
    if sections:
        slides = []
        for section in sections:
            for sl in section.get("slides", []):
                slide = dict(sl)
                slide["_speaker_notes"] = sl.get("speaker_notes", "")
                slides.append(slide)
    else:
        # Fallback: deck.json format
        slides = unit.get("slides", [])
        for sl in slides:
            sl["_speaker_notes"] = sl.get("speaker_notes", "")

    total = len(slides)
    title = meta.get("title", "Presentation")
    subject = meta.get("subject", "")

    # Logo
    logo_path = meta.get("logo_path", "")
    logo_src = img_src(logo_path, base_dir, embed_images) if logo_path else ""
    logo_html = f'<img src="{logo_src}" style="height:32px;opacity:0.9" alt="logo">' if logo_src else ""

    # Render all slides
    slide_htmls = []
    for i, slide in enumerate(slides):
        slide_type = slide.get("type", "content")
        renderer = RENDERERS.get(slide_type, slide_content)
        try:
            kwargs = {"data": slide, "c": c, "base_dir": base_dir, "embed": embed_images}
            inner = renderer(**{k: v for k, v in kwargs.items()
                               if k in renderer.__code__.co_varnames})
        except Exception as e:
            inner = f'<div style="padding:40px;color:red">[Slide {i+1} render error: {e}]</div>'

        notes = render_speaker_notes(slide.get("_speaker_notes", ""))
        slide_htmls.append(f'''
<div class="slide" id="slide-{i+1}" data-index="{i}">
  <div class="slide-content">{inner}</div>
  <div class="notes-panel">
    <div class="notes-header">Speaker Notes — Slide {i+1} of {total}</div>
    <div class="notes-body">{notes or "<p style='color:#64748b;font-style:italic'>No notes for this slide.</p>"}</div>
  </div>
</div>''')

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title)} — {escape(subject)}</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
          background: #0f172a; overflow: hidden; }}

  #deck {{ width: 100vw; height: 100vh; position: relative; }}

  .slide {{
    position: absolute; inset: 0; display: none;
    flex-direction: column; width: 100%; height: 100%;
  }}
  .slide.active {{ display: flex; }}

  .slide-content {{
    flex: 1; display: flex; flex-direction: column;
    overflow: hidden; position: relative;
  }}

  .slide-inner {{
    display: flex; flex-direction: column; width: 100%; height: 100%;
  }}

  .title-bar {{ flex: 0 0 auto; }}

  /* Notes panel */
  .notes-panel {{
    display: none; flex: 0 0 220px; background: #1e293b;
    border-top: 2px solid #334155; overflow-y: auto;
    padding: 0;
  }}
  .notes-header {{
    background: #0f172a; color: #94a3b8; font-size: 11px;
    font-weight: 600; text-transform: uppercase; letter-spacing: 1px;
    padding: 6px 16px;
  }}
  .notes-body {{
    padding: 12px 16px; font-size: 13px; color: #cbd5e1; line-height: 1.5;
  }}
  body.notes-visible .notes-panel {{ display: block; }}
  body.notes-visible .slide-content {{ flex: 1; min-height: 0; }}

  /* Controls bar */
  #controls {{
    position: fixed; bottom: 0; left: 0; right: 0; z-index: 100;
    background: rgba(15,23,42,0.95); padding: 8px 24px;
    display: flex; align-items: center; gap: 16px;
    font-size: 13px; color: #94a3b8;
  }}
  #controls button {{
    background: {c['title_bar']}; color: white; border: none;
    padding: 5px 14px; border-radius: 4px; cursor: pointer; font-size: 13px;
  }}
  #controls button:hover {{ opacity: 0.85; }}
  #progress {{ flex: 1; height: 3px; background: #334155; border-radius: 2px; }}
  #progress-bar {{ height: 100%; background: {c['title_bar']}; border-radius: 2px; transition: width 0.2s; }}

  /* AO badges */
  .ao-badge {{
    display: inline-block; padding: 2px 7px; border-radius: 10px;
    font-size: 11px; font-weight: 700; color: white; margin-right: 5px;
    vertical-align: middle;
  }}

  /* Logo */
  #logo-overlay {{
    position: fixed; bottom: 44px; right: 16px; z-index: 99; opacity: 0.85;
  }}

  @media print {{
    body {{ background: white; overflow: auto; }}
    #controls, #logo-overlay {{ display: none; }}
    .slide {{ position: relative; display: flex !important; page-break-after: always;
               width: 100vw; height: 100vh; }}
    .notes-panel {{ display: none !important; }}
  }}
</style>
</head>
<body>

<div id="deck">
  {"".join(slide_htmls)}
</div>

{f'<div id="logo-overlay">{logo_html}</div>' if logo_html else ''}

<div id="controls">
  <button onclick="navigate(-1)">◀</button>
  <span id="counter">1 / {total}</span>
  <div id="progress"><div id="progress-bar" style="width:{100/total:.1f}%"></div></div>
  <button onclick="navigate(1)">▶</button>
  <button onclick="toggleNotes()" title="Toggle speaker notes (N)">Notes</button>
  <span style="font-size:11px;color:#475569">← → navigate | N notes | F fullscreen | P print</span>
</div>

<script>
var current = 0;
var total = {total};
var slides = document.querySelectorAll('.slide');

function show(n) {{
  slides[current].classList.remove('active');
  current = Math.max(0, Math.min(n, total - 1));
  slides[current].classList.add('active');
  document.getElementById('counter').textContent = (current + 1) + ' / ' + total;
  document.getElementById('progress-bar').style.width = ((current + 1) / total * 100) + '%';
  window.location.hash = 'slide-' + (current + 1);
}}

function navigate(dir) {{ show(current + dir); }}

function toggleNotes() {{ document.body.classList.toggle('notes-visible'); }}

document.addEventListener('keydown', function(e) {{
  if (e.key === 'ArrowRight' || e.key === ' ') {{ e.preventDefault(); navigate(1); }}
  if (e.key === 'ArrowLeft') {{ e.preventDefault(); navigate(-1); }}
  if (e.key === 'n' || e.key === 'N') toggleNotes();
  if (e.key === 'f' || e.key === 'F') {{
    if (!document.fullscreenElement) document.documentElement.requestFullscreen();
    else document.exitFullscreen();
  }}
  if (e.key === 'Home') show(0);
  if (e.key === 'End') show(total - 1);
}});

// Jump to hash on load
(function() {{
  var hash = window.location.hash.replace('#slide-', '');
  var n = parseInt(hash);
  if (!isNaN(n) && n >= 1 && n <= total) show(n - 1);
  else show(0);
}})();
</script>
</body>
</html>'''

    if output_path is None:
        safe_title = meta.get("title", "deck").replace(" ", "_").replace("/", "-")
        output_path = base_dir / f"{safe_title}.html"

    with open(output_path, "w") as f:
        f.write(html)

    size_kb = Path(output_path).stat().st_size // 1024
    print(f"HTML deck written: {output_path} ({total} slides, {size_kb}KB)")
    return str(output_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 build_html.py <curriculum_unit.json> [output.html] [--embed-images]")
        sys.exit(1)
    inp = sys.argv[1]
    out = next((a for a in sys.argv[2:] if not a.startswith("--")), None)
    embed = "--embed-images" in sys.argv
    build_html(inp, out, embed)
