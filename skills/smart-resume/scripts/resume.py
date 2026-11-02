"""Validate evidence eligibility and render private resume artifacts."""

import argparse
import base64
import html
import json
import os
from pathlib import Path
from string import Template
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = {
    "zh-CN": ("求职意向", "虚构示例 · 不可投递", "点击正文可编辑；保存请使用浏览器“另存为”。修改 HTML 不会同步 PDF，请修改 JSON 后重新生成。"),
    "zh-TW": ("求職意向", "虛構範例 · 不可投遞", "點擊正文可編輯；請使用瀏覽器「另存新檔」。修改 HTML 不會同步 PDF，請修改 JSON 後重新產生。"),
    "en": ("Target role", "FICTIONAL DEMO · NOT FOR APPLICATION", "Click text to edit; use your browser's Save As to retain changes. HTML edits do not update PDF; update JSON and regenerate."),
}
STATUSES = {"document_supported", "user_confirmed", "pending", "inferred", "contradicted"}
SOURCE_KINDS = {"document", "user_statement", "memory", "synthetic"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text(value):
    return isinstance(value, str) and bool(value.strip())


def indexed(items, label):
    require(isinstance(items, list), f"{label} must be an array")
    result = {}
    for item in items:
        require(isinstance(item, dict) and text(item.get("id")), f"{label}: missing id")
        require(item["id"] not in result, f"{label}: duplicate id {item['id']}")
        result[item["id"]] = item
    return result


def validate(data, demo=False):
    require(isinstance(data, dict), "Input must be an object")
    fields = {"schema_version", "language", "demo", "jd", "intention", "candidate", "sources", "claims", "pages"}
    require(set(data) == fields, "Top-level fields must match the input template")
    require(type(data["schema_version"]) is int and data["schema_version"] == 1, "Unsupported schema")
    require(data["language"] in LANGUAGES, "Unsupported language")
    require(type(data["demo"]) is bool, "demo must be boolean")
    require(not data["demo"] or demo, "Fictional data requires --demo")
    require(not demo or data["demo"], "--demo requires a demo input")
    job = data["jd"]
    require(isinstance(job, dict) and all(text(job.get(key)) for key in ("title", "company", "source")), "JD title, company and source required")
    require(text(data["intention"]) and data["intention"] == job["title"], "Intention must exactly match the single JD title")
    sources = indexed(data["sources"], "sources")
    for source in sources.values():
        require(source.get("kind") in SOURCE_KINDS and text(source.get("locator")), "Invalid source")
        require(source["kind"] != "synthetic" or data["demo"], "Synthetic source forbidden in real resumes")
    claims = indexed(data["claims"], "claims")
    for claim in claims.values():
        require(text(claim.get("text")) and claim.get("status") in STATUSES, "Invalid claim text/status")
        refs = claim.get("source_ids")
        require(isinstance(refs, list) and all(isinstance(ref, str) and ref in sources for ref in refs), "Unknown claim source")
    candidate = data["candidate"]
    require(isinstance(candidate, dict), "candidate must be an object")
    require(text(candidate.get("name")), "Name claim required")
    require(isinstance(candidate.get("contacts"), list) and candidate["contacts"], "At least one confirmed contact required")
    require(candidate.get("photo_preference") in {"omit", "provided"}, "Choose photo preference")
    require((candidate.get("photo_preference") == "provided" and text(candidate.get("photo"))) or
            (candidate.get("photo_preference") == "omit" and candidate.get("photo") is None), "Photo preference and path disagree")
    selected = [candidate["name"]] + candidate["contacts"]
    pages = data["pages"]
    require(isinstance(pages, list) and 1 <= len(pages) <= 2, "Use one or two pages")
    for page in pages:
        require(isinstance(page, list) and page, "Empty page")
        for section in page:
            require(isinstance(section, dict) and text(section.get("title")), "Section title required")
            refs = section.get("claim_ids")
            require(isinstance(refs, list) and refs, "Empty section")
            selected.extend(refs)
    for claim_id in selected:
        require(isinstance(claim_id, str) and claim_id in claims, "Unknown selected claim")
        claim = claims[claim_id]
        require(claim["status"] in {"document_supported", "user_confirmed"}, f"Unverified selected claim: {claim_id}")
        kinds = {sources[ref]["kind"] for ref in claim["source_ids"]}
        required_kind = "document" if claim["status"] == "document_supported" else "user_statement"
        require(required_kind in kinds or (data["demo"] and "synthetic" in kinds), f"No supporting source for {claim_id}")
    return claims, list(dict.fromkeys(selected))


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def photo_data(data, input_dir):
    if data["candidate"]["photo_preference"] == "omit":
        return None
    from reportlab.lib.utils import ImageReader
    photo = Path(data["candidate"]["photo"])
    require(not photo.is_absolute(), "Photo path must be relative to private input directory")
    photo = (input_dir / photo).resolve()
    require(photo.is_relative_to(input_dir.resolve()), "Photo must stay inside private input directory")
    require(photo.suffix.lower() in {".png", ".jpg", ".jpeg"}, "Use PNG or JPEG photo")
    require(photo.stat().st_size <= 10_000_000, "Photo exceeds 10 MB")
    image = ImageReader(str(photo))
    image.getSize()
    mime = "image/png" if photo.suffix.lower() == ".png" else "image/jpeg"
    return image, f"data:{mime};base64,{base64.b64encode(photo.read_bytes()).decode('ascii')}"


def render_html(data, claims, photo):
    label, demo_notice, editing_note = LANGUAGES[data["language"]]
    name = claims[data["candidate"]["name"]]["text"]
    blocks = []
    for number, sections in enumerate(data["pages"], 1):
        content = []
        if data["demo"]:
            content.append(f'<p class="demo">{html.escape(demo_notice)}</p>')
        if photo and number == 1:
            content.append(f'<img class="photo" alt="" src="{photo[1]}">')
        content.append(f"<h1>{html.escape(name)}</h1>")
        content.append(f'<p class="meta">{html.escape(label)}：{html.escape(data["intention"])}</p>')
        if number == 1:
            contact = " | ".join(claims[claim_id]["text"] for claim_id in data["candidate"]["contacts"])
            content.append(f'<p class="meta">{html.escape(contact)}</p>')
        for section in sections:
            content.append(f'<section><h2>{html.escape(section["title"])}</h2>')
            content.extend(f'<p>{html.escape(claims[claim_id]["text"])}</p>' for claim_id in section["claim_ids"])
            content.append("</section>")
        content.append(f"<footer>{number} / {len(data['pages'])}</footer>")
        blocks.append('<article class="page" contenteditable="true">' + "\n".join(content) + "</article>")
    return Template((ROOT / "assets/resume.html").read_text(encoding="utf-8")).substitute(
        language=data["language"], name=html.escape(name), intention=html.escape(data["intention"]),
        editing_note=html.escape(editing_note), pages="\n".join(blocks))


def register_font(font_path, all_text):
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    candidates = [font_path] if font_path else [
        os.environ.get("SMART_RESUME_FONT"),
        "C:/Windows/Fonts/simsun.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]
    errors = []
    for candidate in filter(None, candidates):
        try:
            font = TTFont("ResumeFont", str(candidate))
            unsupported = {ord(char) for char in all_text if not char.isspace()} - set(font.face.charToGlyph)
            require(not unsupported, f"Font lacks characters: {sorted(unsupported)[:5]}")
            pdfmetrics.registerFont(font)
            return "ResumeFont"
        except Exception as error:
            errors.append(f"{candidate}: {error}")
    raise ValueError("No usable font. Pass --font with a licensed TrueType font covering all text. " + "; ".join(errors))


def render_pdf(data, claims, photo, path, font_path):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.platypus import Paragraph
    label, demo_notice, _ = LANGUAGES[data["language"]]
    visible = [claims[data["candidate"]["name"]]["text"], label, data["intention"]]
    visible.extend(claims[claim_id]["text"] for claim_id in data["candidate"]["contacts"])
    for page in data["pages"]:
        for section in page:
            visible.append(section["title"])
            visible.extend(claims[claim_id]["text"] for claim_id in section["claim_ids"])
    all_text = " ".join(visible) + (demo_notice if data["demo"] else "") + "0123456789/: |"
    font_name = register_font(font_path, all_text)
    page_width, page_height = A4
    margin = 18 * mm
    body_width = page_width - margin * 2
    styles = {
        "body": ParagraphStyle("body", fontName=font_name, fontSize=10.5, leading=16, textColor=colors.HexColor("#182b3c"), wordWrap="CJK"),
        "title": ParagraphStyle("title", fontName=font_name, fontSize=24, leading=30, textColor=colors.HexColor("#182b3c"), wordWrap="CJK"),
        "heading": ParagraphStyle("heading", fontName=font_name, fontSize=13, leading=19, textColor=colors.HexColor("#244d68"), wordWrap="CJK"),
    }
    canvas = Canvas(str(path), pagesize=A4)
    canvas.setTitle("Smart Resume Demo" if data["demo"] else "Resume")
    measurements = []
    for number, sections in enumerate(data["pages"], 1):
        cursor = page_height - margin

        def draw(value, style="body", gap=8, width=body_width):
            nonlocal cursor
            paragraph = Paragraph(html.escape(value), styles[style])
            _, height = paragraph.wrap(width, page_height)
            require(cursor - height >= margin + 15, f"Page {number} overflows; shorten or move content")
            paragraph.drawOn(canvas, margin, cursor - height)
            cursor -= height + gap

        if data["demo"]:
            draw(demo_notice)
        header_width = body_width - 34 * mm if photo and number == 1 else body_width
        header_top = cursor
        if photo and number == 1:
            canvas.drawImage(photo[0], page_width - margin - 25 * mm, header_top - 32 * mm,
                             25 * mm, 32 * mm, preserveAspectRatio=True, anchor="c", mask="auto")
        draw(claims[data["candidate"]["name"]]["text"], "title", width=header_width)
        draw(f"{label}: {data['intention']}", width=header_width)
        if number == 1:
            draw(" | ".join(claims[claim_id]["text"] for claim_id in data["candidate"]["contacts"]), width=header_width)
        if photo and number == 1:
            cursor = min(cursor, header_top - 34 * mm)
        for section in sections:
            cursor -= 10
            draw(section["title"], "heading")
            for claim_id in section["claim_ids"]:
                draw(claims[claim_id]["text"])
        canvas.setFont(font_name, 9)
        canvas.drawRightString(page_width - margin, margin - 7, f"{number} / {len(data['pages'])}")
        measurements.append({"page": number, "content_bottom_pt": round(cursor + 8, 2)})
        canvas.showPage()
    canvas.save()
    return measurements


def render(data, input_dir, out, font_path=None, demo=False):
    claims, selected = validate(data, demo)
    out = Path(out).resolve()
    require(not out.exists(), "Output directory exists; choose a new directory to preserve previous files")
    out.parent.mkdir(parents=True, exist_ok=True)
    photo = photo_data(data, Path(input_dir))
    with tempfile.TemporaryDirectory(prefix=".resume-", dir=out.parent) as temporary:
        staging = Path(temporary)
        measurements = render_pdf(data, claims, photo, staging / "resume.pdf", font_path)
        (staging / "resume.html").write_text(render_html(data, claims, photo), encoding="utf-8")
        report = {
            "schema_version": 1, "demo": data["demo"], "page_count": len(data["pages"]),
            "page_size": "A4", "body_font_pt": 10.5, "selected_claim_ids": selected,
            "omitted_claim_ids": sorted(set(claims) - set(selected)), "measurements": measurements,
            "visual_review": "pending", "factual_review": "pending", "html_review": "pending",
            "note": "Structural validation is not factual verification or visual acceptance.",
        }
        (staging / "review.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        out.mkdir()
        for artifact in staging.iterdir():
            artifact.replace(out / artifact.name)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)
    init = subcommands.add_parser("init")
    init.add_argument("--out", type=Path, required=True)
    for command in ("validate", "render"):
        subparser = subcommands.add_parser(command)
        subparser.add_argument("input", type=Path)
        subparser.add_argument("--demo", action="store_true")
        if command == "render":
            subparser.add_argument("--out", type=Path, required=True)
            subparser.add_argument("--font", type=Path)
    arguments = parser.parse_args()
    try:
        if arguments.command == "init":
            arguments.out.parent.mkdir(parents=True, exist_ok=True)
            with arguments.out.open("x", encoding="utf-8") as stream:
                stream.write((ROOT / "assets/intake.json").read_text(encoding="utf-8"))
            print("Created incomplete private intake. Fill and verify before rendering.")
        elif arguments.command == "validate":
            _, selected = validate(load(arguments.input), arguments.demo)
            print(f"Structure and evidence eligibility passed: {len(selected)} selected claims. Factual review still required.")
        else:
            report = render(load(arguments.input), arguments.input.resolve().parent, arguments.out, arguments.font, arguments.demo)
            print(f"Generated {report['page_count']} A4 pages, editable HTML and private review record. Visual review pending.")
    except (ValueError, OSError, TypeError, KeyError, ImportError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
