"""Template library: classification, lifecycle, evidence and delivery records."""

import argparse
from datetime import date, datetime, timezone
import json
from pathlib import Path
import re
import sys

import styles


ROOT = Path(__file__).resolve().parents[1]
LIBRARY_ROOT = Path.home() / ".smart-resume" / "library"
STATUSES = {"candidate", "promoted", "deprecated"}
MINIMUM_SAMPLE = 30


def require(condition, message):
    if not condition:
        raise ValueError(message)


def template_root(root=None):
    return Path(root) if root is not None else LIBRARY_ROOT


def template_path(template_id, root=None):
    require(re.fullmatch(r"[a-z0-9][a-z0-9-]{0,47}", template_id), "Invalid template id")
    return template_root(root) / "templates" / template_id / "template.json"


def save_template(template_id, style, role_family, channel, seniority="any", source="", notes="", root=None):
    require(style in styles.STYLES, "Unknown style")
    require(role_family in styles.ROLE_FAMILIES, "Unknown role family")
    require(channel in styles.CHANNELS, "Unknown channel")
    require(seniority in {"any", "junior", "mid", "senior", "lead"}, "Unknown seniority")
    path = template_path(template_id, root)
    require(not path.exists(), "Template exists; choose a new id to preserve it")
    record = {
        "schema_version": 1, "id": template_id, "style": style, "role_family": role_family,
        "channel": channel, "seniority": seniority, "status": "candidate",
        "evidence": {"structure": "unverified", "technical": "unverified", "delivery": "no_data"},
        "source": source or "local practice", "notes": notes,
        "created_at": datetime.now(timezone.utc).isoformat(), "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    return record


def load_template(template_id, root=None):
    path = template_path(template_id, root)
    require(path.is_file(), "Unknown template")
    record = json.loads(path.read_text(encoding="utf-8"))
    require(record["status"] in STATUSES, "Invalid template status")
    return record


def list_templates(role_family=None, channel=None, status=None, root=None, seniority=None):
    directory = template_root(root) / "templates"
    records = []
    if directory.is_dir():
        for path in sorted(directory.glob("*/template.json")):
            try:
                record = json.loads(path.read_text(encoding="utf-8"))
            except (ValueError, OSError):
                continue
            if role_family and record["role_family"] != role_family:
                continue
            if channel and record["channel"] != channel:
                continue
            if status and record["status"] != status:
                continue
            if seniority and record["seniority"] not in {"any", seniority}:
                continue
            records.append(record)
    return records


def set_status(template_id, status, root=None, reason=""):
    require(status in STATUSES, "Invalid status")
    path = template_path(template_id, root)
    require(path.is_file(), "Unknown template")
    record = json.loads(path.read_text(encoding="utf-8"))
    if status == "promoted":
        require(record["evidence"]["structure"] == "quality_checked",
                "Structure quality must be checked before promotion")
        require(record["evidence"]["technical"] == "quality_checked",
                "Technical quality must be checked before promotion")
    if status == "deprecated":
        require(reason.strip(), "A deprecation reason is required")
    record["status"] = status
    record["notes"] = f"{record['notes']}\n{reason}".strip()
    record["updated_at"] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    return record


def record_evidence(template_id, kind, value, root=None, note=""):
    require(kind in {"structure", "technical"}, "Only structure and technical quality are checked by this skill")
    require(value in {"quality_checked", "failed", "unverified"}, "Invalid evidence value")
    path = template_path(template_id, root)
    require(path.is_file(), "Unknown template")
    record = json.loads(path.read_text(encoding="utf-8"))
    record["evidence"][kind] = value
    if value != "quality_checked" and record["status"] == "promoted":
        record["status"] = "candidate"
    if note:
        record["notes"] = f"{record['notes']}\n{note}".strip()
    record["updated_at"] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    return record


def log_use(template_id, root=None, when="", channel=None, applied=0, reply=0, interview=0, offer=0, note=""):
    path = template_path(template_id, root)
    require(path.is_file(), "Unknown template")
    for name, value in (("applied", applied), ("reply", reply), ("interview", interview), ("offer", offer)):
        require(isinstance(value, int) and value >= 0, f"{name} must be a non-negative count")
    require(applied >= reply >= interview >= offer, "Counts must not increase along the funnel")
    date.fromisoformat(when or date.today().isoformat())
    require(channel is None or channel in styles.CHANNELS, "Unknown channel")
    record = json.loads(path.read_text(encoding="utf-8"))
    entry = {
        "date": when or date.today().isoformat(),
        "channel": channel or record["channel"],
        "applied": applied, "reply": reply, "interview": interview, "offer": offer,
        "note": note, "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    log_path = path.parent / "uses.jsonl"
    with log_path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def read_uses(template_id, root=None):
    path = template_path(template_id, root).parent / "uses.jsonl"
    if not path.is_file():
        return []
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            entries.append(json.loads(line))
    return entries


def report(template_id, root=None):
    record = load_template(template_id, root)
    entries = read_uses(template_id, root)
    applied = sum(entry["applied"] for entry in entries)
    interview = sum(entry["interview"] for entry in entries)
    offer = sum(entry["offer"] for entry in entries)
    result = {
        "id": template_id, "status": record["status"], "style": record["style"],
        "role_family": record["role_family"], "channel": record["channel"],
        "evidence": record["evidence"], "applications": applied,
        "interviews": interview, "offers": offer,
        "invitation_rate": None, "evidence_level": "no_data",
        "caveats": [
            "Interview numbers come from one candidate's own submissions.",
            "A template is not proven to cause the outcome; role fit, company and timing also matter.",
            "Templates without real delivery data are never labelled as high pass rate.",
        ],
    }
    if applied >= MINIMUM_SAMPLE:
        result["invitation_rate"] = round(interview / applied * 100, 1)
        result["evidence_level"] = "delivery_sample"
    elif applied:
        result["evidence_level"] = "insufficient_sample"
        result["caveats"].append(
            f"Only {applied} recorded applications; a rate is shown from {MINIMUM_SAMPLE} samples.")
    return result


def built_in(language="zh-CN"):
    """Public library entries derived from the style catalog."""
    entries = []
    for style_id, style in styles.STYLES.items():
        for family in style["role_families"]:
            for channel in style["channels"]:
                entries.append({
                    "id": f"builtin:{style_id}:{family}:{channel}", "style": style_id,
                    "role_family": family, "channel": channel, "status": "builtin",
                    "ats": style["ats"], "name": style["names"][language],
                    "evidence": {"structure": "unverified", "technical": "unverified",
                                 "delivery": "no_data"},
                })
    return entries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)
    listing = subcommands.add_parser("list")
    listing.add_argument("--role-family", choices=sorted(styles.ROLE_FAMILIES))
    listing.add_argument("--channel", choices=sorted(styles.CHANNELS))
    listing.add_argument("--status", choices=sorted(STATUSES))
    listing.add_argument("--seniority", choices=["junior", "mid", "senior", "lead"])
    listing.add_argument("--root", type=Path)
    listing.add_argument("--language", default="zh-CN")
    saving = subcommands.add_parser("save")
    saving.add_argument("id")
    saving.add_argument("--style", required=True, choices=sorted(styles.STYLES))
    saving.add_argument("--role-family", required=True, choices=sorted(styles.ROLE_FAMILIES))
    saving.add_argument("--channel", required=True, choices=sorted(styles.CHANNELS))
    saving.add_argument("--seniority", default="any", choices=["any", "junior", "mid", "senior", "lead"])
    saving.add_argument("--source", default="")
    saving.add_argument("--notes", default="")
    saving.add_argument("--root", type=Path)
    evidence = subcommands.add_parser("evidence")
    evidence.add_argument("id")
    evidence.add_argument("kind", choices=["structure", "technical"])
    evidence.add_argument("value", choices=["quality_checked", "failed", "unverified"])
    evidence.add_argument("--note", default="")
    evidence.add_argument("--root", type=Path)
    promoting = subcommands.add_parser("promote")
    promoting.add_argument("id")
    promoting.add_argument("--root", type=Path)
    deprecating = subcommands.add_parser("deprecate")
    deprecating.add_argument("id")
    deprecating.add_argument("--reason", required=True)
    deprecating.add_argument("--root", type=Path)
    logging = subcommands.add_parser("log")
    logging.add_argument("id")
    logging.add_argument("--applied", type=int, default=0)
    logging.add_argument("--reply", type=int, default=0)
    logging.add_argument("--interview", type=int, default=0)
    logging.add_argument("--offer", type=int, default=0)
    logging.add_argument("--channel")
    logging.add_argument("--date")
    logging.add_argument("--note", default="")
    logging.add_argument("--root", type=Path)
    reporting = subcommands.add_parser("report")
    reporting.add_argument("id")
    reporting.add_argument("--root", type=Path)
    arguments = parser.parse_args()
    try:
        if arguments.command == "list":
            builtin = [item for item in built_in(arguments.language)
                       if (not arguments.role_family or item["role_family"] == arguments.role_family)
                       and (not arguments.channel or item["channel"] == arguments.channel)]
            payload = {"builtin": builtin,
                       "personal": list_templates(arguments.role_family, arguments.channel,
                                                 arguments.status, arguments.root, arguments.seniority)}
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        elif arguments.command == "save":
            print(json.dumps(save_template(arguments.id, arguments.style, arguments.role_family,
                                           arguments.channel, arguments.seniority, arguments.source,
                                           arguments.notes, arguments.root), ensure_ascii=False, indent=2))
        elif arguments.command == "evidence":
            print(json.dumps(record_evidence(arguments.id, arguments.kind, arguments.value,
                                             arguments.root, arguments.note), ensure_ascii=False, indent=2))
        elif arguments.command == "promote":
            print(json.dumps(set_status(arguments.id, "promoted", arguments.root), ensure_ascii=False, indent=2))
        elif arguments.command == "deprecate":
            print(json.dumps(set_status(arguments.id, "deprecated", arguments.root, arguments.reason),
                             ensure_ascii=False, indent=2))
        elif arguments.command == "log":
            print(json.dumps(log_use(arguments.id, arguments.root, arguments.date or "",
                                     arguments.channel, arguments.applied, arguments.reply,
                                     arguments.interview, arguments.offer, arguments.note),
                             ensure_ascii=False, indent=2))
        else:
            print(json.dumps(report(arguments.id, arguments.root), ensure_ascii=False, indent=2))
    except (ValueError, OSError, TypeError, KeyError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
