"""Check artifact integrity, selectable text and explicit review attestations."""

import argparse
from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path
import sys

import resume


CATEGORIES = ("visual_review", "factual_review", "html_review")


def compact(value):
    return "".join(value.split())


def inspect(delivery, data, demo=False):
    from pypdf import PdfReader
    delivery = Path(delivery)
    claims, selected = resume.validate(data, demo)
    report = resume.load(delivery / "review.json")
    checks = {}
    checks["artifact_integrity"] = all(
        report.get("artifact_sha256", {}).get(name) == hashlib.sha256((delivery / name).read_bytes()).hexdigest()
        for name in ("resume.pdf", "resume.html"))
    reader = PdfReader(delivery / "resume.pdf")
    checks["page_count"] = len(reader.pages) == len(data["pages"]) == report["page_count"]
    checks["a4"] = all(abs(float(page.mediabox.width) - 595.276) < 1 and
                       abs(float(page.mediabox.height) - 841.89) < 1 for page in reader.pages)
    extracted = [compact(page.extract_text() or "") for page in reader.pages]
    expected = [claims[claim_id]["text"] for claim_id in selected] + [data["intention"]]
    combined = "".join(extracted)
    checks["selected_text"] = all(compact(value) in combined for value in expected)
    checks["identity_first_page"] = all(compact(claims[claim_id]["text"]) in extracted[0]
                                       for claim_id in [data["candidate"]["name"]] + data["candidate"]["contacts"])
    checks["page_text"] = len(extracted) == len(data["pages"]) and all(
        compact(section["title"]) in extracted[index] and
        all(compact(claims[claim_id]["text"]) in extracted[index] for claim_id in section["claim_ids"])
        for index, sections in enumerate(data["pages"]) for section in sections
        if index < len(extracted))
    checks["no_replacement_glyph"] = "\ufffd" not in combined and "\x00" not in combined
    boxes = [box for page in report["measurements"] for box in page.get("boxes", [])]
    checks["layout_bounds"] = bool(boxes) and all(
        box["x"] >= 0 and box["top"] >= 0 and box["x"] + box["width"] <= 595.276 + 1
        and box["top"] + box["height"] <= 841.89 - 18 * 72 / 25.4 for box in boxes)
    checks["no_text_box_overlap"] = all(
        not (first["x"] + first["width"] > second["x"] + 1 and
             second["x"] + second["width"] > first["x"] + 1 and
             first["top"] + first["height"] > second["top"] + 1 and
             second["top"] + second["height"] > first["top"] + 1)
        for page in report["measurements"]
        for index, first in enumerate(page.get("boxes", []))
        for second in page.get("boxes", [])[index + 1:])
    checks["input_selection"] = report["selected_claim_ids"] == selected and report["demo"] == data["demo"]
    checks["input_integrity"] = report.get("input_sha256") == hashlib.sha256(
        json.dumps(data, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
    html_body = (delivery / "resume.html").read_text(encoding="utf-8")
    checks["html_selected_text"] = all(html.escape(value) in html_body for value in expected)
    reviews = {category: report.get(category, "pending") for category in CATEGORIES}
    attestations = report.get("attestations", {})
    reviewed = all(status == "passed" and attestations.get(category, {}).get("notes") and
                   attestations.get(category, {}).get("reviewer") for category, status in reviews.items())
    accepted = all(checks.values()) and bool(reviewed)
    return {
        "checks": checks, "reviews": reviews, "accepted": accepted,
        "application_ready": accepted and not data["demo"],
        "state": ("demo_preview_accepted" if data["demo"] else "candidate_delivery_accepted") if accepted else "review_required",
        "limitations": "Attestations require actual inspection. Text checks do not prove factual truth or pixel quality.",
    }


def record(delivery, category, status, reviewer, notes):
    if category not in CATEGORIES or status not in {"passed", "failed", "pending"}:
        raise ValueError("Invalid review category or status")
    if not reviewer or not reviewer.strip() or not notes or not notes.strip():
        raise ValueError("Reviewer and substantive notes required")
    path = Path(delivery) / "review.json"
    report = resume.load(path)
    for name in ("resume.pdf", "resume.html"):
        if report["artifact_sha256"][name] != hashlib.sha256((Path(delivery) / name).read_bytes()).hexdigest():
            raise ValueError("Artifacts changed; regenerate and review a new delivery")
    report[category] = status
    report.setdefault("attestations", {})[category] = {
        "reviewer": reviewer, "notes": notes, "time": datetime.now(timezone.utc).isoformat(),
    }
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("delivery", type=Path)
    parser.add_argument("input", type=Path)
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--record", choices=CATEGORIES)
    parser.add_argument("--status", choices=("passed", "failed", "pending"), default="pending")
    parser.add_argument("--reviewer")
    parser.add_argument("--notes")
    args = parser.parse_args()
    try:
        data = resume.load(args.input)
        result = inspect(args.delivery, data, args.demo)
        if args.record:
            if not all(result["checks"].values()):
                raise ValueError("Automatic checks failed; fix artifacts before recording acceptance")
            record(args.delivery, args.record, args.status, args.reviewer, args.notes)
            result = inspect(args.delivery, data, args.demo)
        (args.delivery / "quality.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["accepted"] else 1
    except (ValueError, OSError, KeyError, TypeError, ImportError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
