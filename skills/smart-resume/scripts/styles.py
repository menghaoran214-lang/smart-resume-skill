"""Style catalog, transparent matching and private style profiles."""

import json
from pathlib import Path
import re
import tempfile


ROOT = Path(__file__).resolve().parents[1]
PROFILE_ROOT = Path.home() / ".smart-resume" / "styles"
CATALOG = json.loads((ROOT / "styles/catalog.json").read_text(encoding="utf-8"))
STYLES = {item["id"]: item for item in CATALOG["styles"]}
ROLE_FAMILIES = CATALOG["role_families"]
CHANNELS = CATALOG["channels"]


def check_profile(profile):
    if not isinstance(profile, dict) or set(profile) != {"schema_version", "name", "base", "accent", "spacing"}:
        raise ValueError("Profile must contain only schema_version, name, base, accent, spacing")
    if type(profile["schema_version"]) is not int or profile["schema_version"] != 1:
        raise ValueError("Unsupported profile version")
    if not isinstance(profile["name"], str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,47}", profile["name"]):
        raise ValueError("Profile name must be a lowercase slug of at most 48 characters")
    if profile["base"] not in STYLES:
        raise ValueError("Unknown base style")
    accent = profile["accent"]
    if not isinstance(accent, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", accent):
        raise ValueError("Accent must be a six-digit hex color")
    channels = [int(accent[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [value / 12.92 if value <= .04045 else ((value + .055) / 1.055) ** 2.4 for value in channels]
    luminance = sum(value * weight for value, weight in zip(linear, (.2126, .7152, .0722)))
    if 1.05 / (luminance + .05) < 4.5:
        raise ValueError("Accent needs at least 4.5:1 contrast against white")
    if profile["spacing"] not in {"regular", "airy"}:
        raise ValueError("Spacing must be regular or airy; body text is never reduced")
    return profile


def read_profile(path):
    return check_profile(json.loads(Path(path).expanduser().read_text(encoding="utf-8-sig")))


def save_profile(name, base, accent=None, spacing="regular", directory=None):
    profile = check_profile({
        "schema_version": 1, "name": name, "base": base,
        "accent": accent or STYLES[base]["accent"], "spacing": spacing,
    })
    directory = Path(directory) if directory is not None else PROFILE_ROOT
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / name
    if target.exists():
        raise ValueError("Profile exists; choose a new name to preserve it")
    with tempfile.TemporaryDirectory(prefix=".style-", dir=directory) as temporary:
        staging = Path(temporary) / name
        staging.mkdir()
        (staging / "profile.json").write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")
        (staging / "STYLE.md").write_text(
            f"# {name}\n\nBase: {base}\nAccent: {profile['accent']}\nSpacing: {spacing}\n\n"
            "These preferences contain no candidate facts. The base STYLE.md invariants still apply.\n"
            "Use profile.json with --profile; edit only validated tokens there.\n",
            encoding="utf-8")
        staging.rename(target)
    return target


def list_profiles(directory=None):
    directory = Path(directory) if directory is not None else PROFILE_ROOT
    profiles = []
    for path in sorted(directory.glob("*/profile.json")):
        try:
            profile = read_profile(path)
            profiles.append({"path": str(path.resolve()), **profile})
        except (ValueError, TypeError, OSError):
            continue
    return profiles


def match(data, context="", ats=False, channel=None):
    """Rank styles by role keyword hits, then by channel suitability."""
    if ats:
        return [{"id": "ats", "score": 100,
                 "reasons": ["Explicit ATS request; parsing compatibility is still not guaranteed."]}]
    title = str(data.get("jd", {}).get("title", ""))
    query = (title + " " + context).casefold()
    ranked = []
    for item in CATALOG["styles"]:
        hits = [keyword for keyword in item["keywords"] if
                (re.search(r"(?<![a-z0-9])" + re.escape(keyword) + r"(?![a-z0-9])", query)
                 if keyword.isascii() else keyword in query)]
        reasons = list(hits)
        score = sum(5 if keyword in {"analyst", "data", "ai", "运营", "運營"} else 10 for keyword in hits)
        if channel and channel in item["channels"]:
            score += 4
            reasons.append(f"Supports the {channel} channel")
        if item["id"] == "classic" and not hits:
            score += 1
            reasons.append("Conservative fallback")
        ranked.append({"id": item["id"], "score": score,
                       "reasons": reasons or ["No role keyword match"]})
    order = [item["id"] for item in CATALOG["styles"]]
    return sorted(ranked, key=lambda entry: (-entry["score"], order.index(entry["id"])))


def resolve(data, style=None, profile=None, context="", ats=False, channel=None):
    preferences = read_profile(profile) if profile else None
    recommendations = match(data, context, ats, channel)
    selected = style or (preferences["base"] if preferences else recommendations[0]["id"])
    if selected not in STYLES:
        raise ValueError(f"Unknown style: {selected}")
    if preferences and style and preferences["base"] != style:
        raise ValueError("Explicit style conflicts with profile base; choose one")
    if ats and selected != "ats":
        raise ValueError("--ats conflicts with the explicit style or saved profile")
    result = dict(STYLES[selected])
    result.update(accent=preferences["accent"] if preferences else result["accent"],
                  spacing=preferences["spacing"] if preferences else "regular")
    result["selection"] = "explicit" if style else "profile" if profile else "automatic"
    result["profile"] = preferences["name"] if preferences else None
    result["recommendations"] = recommendations[:3]
    return result


def describe(style_id, language="zh-CN"):
    """Return the catalog facts a user needs before choosing a layout."""
    style = STYLES[style_id]
    return {
        "id": style_id,
        "name": style["names"][language],
        "summary": style["summary"][language],
        "roles": [ROLE_FAMILIES[family][language] for family in style["role_families"]],
        "channels": [CHANNELS[channel][language] for channel in style["channels"]],
        "ats": style["ats"],
        "ats_note": style["ats_note"][language],
    }
