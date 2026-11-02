"""Render the three README files from templates and the project data file.

The rendered README is a product: templates hold the prose, this script owns
the generated parts (banner, badges, table of contents, skill tree, stats).
Rendering is idempotent, so CI can fail when a README is out of date.
"""

import argparse
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"
LANGUAGES = {
    "zh-CN": ("README.md", "README.zh-CN.template.md"),
    "zh-TW": ("README.zh-TW.md", "README.zh-TW.template.md"),
    "en": ("README.en.md", "README.en.template.md"),
}


def load_data():
    """Read the project data file, with PyYAML when available."""
    path = ROOT / "data/project.yaml"
    try:
        import yaml
    except ImportError:
        yaml = None
    if yaml is not None:
        with path.open(encoding="utf-8") as stream:
            return yaml.safe_load(stream)
    return parse_simple_yaml(path.read_text(encoding="utf-8"))


def parse_simple_yaml(text):
    """Minimal parser for the nested mapping and scalar lists used here."""
    root = {}
    stack = [(-1, root)]
    key = None
    for raw in text.splitlines():
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()
        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()
        container = stack[-1][1]
        if line.startswith("- "):
            value = parse_scalar(line[2:].strip())
            if isinstance(container.get(key), list):
                container[key].append(value)
            continue
        if ":" not in line:
            continue
        name, _, value = line.partition(":")
        name, value = name.strip(), value.strip()
        key = name
        if value:
            container[key] = parse_scalar(value)
        else:
            container[key] = {}
            stack.append((indent, container[key]))
    return root


def parse_scalar(value):
    value = value.strip().strip('"')
    if value.startswith("[") and value.endswith("]"):
        return [item.strip().strip('"') for item in value[1:-1].split(",") if item.strip()]
    return value


def github_slug(text):
    """Match GitHub's heading anchor rules."""
    slug = re.sub(r"[^\w\s-]", "", text.strip().lower())
    return re.sub(r"\s", "-", slug)


def build_toc(body, language):
    """Collect level-2 and level-3 headings into a nested, clickable list."""
    lines = []
    for line in body.splitlines():
        match = re.match(r"^(#{2,3})\s+(.+?)\s*$", line)
        if not match:
            continue
        depth, title = len(match.group(1)), match.group(2)
        title = re.sub(r"\s*\{[A-Z_]+\}\s*", "", title).strip()
        indent = "" if depth == 2 else "  "
        lines.append(f"{indent}- [{title}](#{github_slug(title)})")
    heading = {"zh-CN": "目录", "zh-TW": "目錄", "en": "Table of Contents"}[language]
    return f"## {heading}\n\n" + "\n".join(lines) + "\n"


def build_badges(data):
    images = []
    for badge in data["badges"]:
        label = str(badge["label"]).replace(" ", "%20")
        message = str(badge["message"]).replace(" ", "%20")
        images.append(
            f'<img src="https://img.shields.io/badge/{label}-{message}-{badge["color"]}.svg" '
            f'alt="{badge["label"]}: {badge["message"]}" height="20">')
    return " ".join(images)


def build_banner():
    return ('<p align="center">\n'
            '  <img src="assets/banner.png" alt="Smart Resume" width="820">\n'
            '</p>')


def build_skill_tree():
    skill_root = ROOT / "skills/smart-resume"
    rows = []
    paths = [path for path in sorted(skill_root.rglob("*"))
             if path.is_file() and "__pycache__" not in path.parts]
    for path in paths:
        if not path.is_file():
            continue
        parts = path.relative_to(skill_root).parts
        prefix = "│   " * (len(parts) - 1) + "├── "
        rows.append(f"{prefix}{parts[-1]}")
    return "```text\nsmart-resume/\n" + "\n".join(rows) + "\n```\n"


def build_stats_svg():
    path = ROOT / "assets/stats.svg"
    if not path.is_file():
        return ""
    return ('<p align="center">\n'
            '  <img src="assets/stats.svg" alt="repository stats" height="26">\n'
            '</p>')


def build_stats():
    """Report the latest local commit without failing when git is unavailable."""
    sha, stamp = "local", ""
    try:
        sha = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"],
                             capture_output=True, text=True, timeout=15).stdout.strip() or "local"
        stamp = subprocess.run(["git", "-C", str(ROOT), "log", "-1", "--format=%cs"],
                               capture_output=True, text=True, timeout=15).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    suffix = f" · {stamp}" if stamp else ""
    return f"- 最新提交 / latest commit：`{sha}`{suffix}\n- CI 状态：见仓库顶部 Actions 徽章\n"


def render(language, data):
    output_name, template_name = LANGUAGES[language]
    body = (TEMPLATES / template_name).read_text(encoding="utf-8")
    replacements = {
        "{{BANNER}}": build_banner(),
        "{{BADGES}}": build_badges(data),
        "{{LANG_SWITCH}}": " · ".join(
            f"[{link['text']}]({link['target']})" for link in data["links"]),
        "{{TAGLINE}}": data["tagline"][language],
        "{{WHAT}}": "\n".join(f"- {item}" for item in data["what"][language]),
        "{{AUDIENCE}}": data["audience"][language],
        "{{INSTALL}}": "\n".join(data["install"]),
        "{{DEMO}}": data["demo"][language],
        "{{SKILL_TREE}}": build_skill_tree(),
        "{{STATS}}": build_stats(),
        "{{STATS_SVG}}": build_stats_svg(),
    }
    for token, value in replacements.items():
        body = body.replace(token, value)
    body = body.replace("{{TOC}}", build_toc(body, language))
    if "{{" in body or "}}" in body:
        raise ValueError(f"Unresolved placeholder in {template_name}")
    return output_name, body


def render_all(data=None):
    data = data or load_data()
    return {name: body for name, body in (render(language, data) for language in LANGUAGES)}


def write(results, check=False):
    changed = []
    for name, body in results.items():
        target = ROOT / name
        current = target.read_text(encoding="utf-8") if target.is_file() else None
        if current == body:
            continue
        changed.append(name)
        if not check:
            target.write_text(body, encoding="utf-8")
    return changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail when a README is out of date")
    arguments = parser.parse_args()
    try:
        changed = write(render_all(), check=arguments.check)
    except (ValueError, OSError, KeyError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    if arguments.check and changed:
        print(f"Out of date: {', '.join(changed)}. Run scripts/render_readme.py.", file=sys.stderr)
        return 1
    print("Rendered: " + (", ".join(changed) if changed else "already up to date"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
