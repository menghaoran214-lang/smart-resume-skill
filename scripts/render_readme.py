"""Render the three README files from templates and the project data file.

The rendered README is a product: templates hold the prose, this script owns
the generated parts (banner, badges, table of contents and skill tree).
Rendering is idempotent, so CI can fail when a README is out of date.
"""

import argparse
import difflib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"
LANGUAGES = {
    "zh-CN": ("README.md", "README.zh-CN.template.md"),
    "zh-TW": ("README.zh-TW.md", "README.zh-TW.template.md"),
    "en": ("README.en.md", "README.en.template.md"),
}


def load_data():
    """Read the project data file. JSON keeps the toolchain dependency-free."""
    return json.loads((ROOT / "data/project.json").read_text(encoding="utf-8-sig"))


def build_toc(data, language):
    """Render a collapsible table of contents with explicit, stable anchors."""
    labels = {"zh-CN": "目录", "zh-TW": "目錄", "en": "Contents"}
    lines = [f"## {labels[language]}", ""]
    for section in data["sections"][language]:
        if section["anchor"] == "install":
            children = {
                "zh-CN": ("安装方式（点击展开）", "让 AI 帮你安装", "手动安装"),
                "zh-TW": ("安裝方式（點擊展開）", "讓 AI 幫你安裝", "手動安裝"),
                "en": ("Installation options (expand)", "Ask your AI to install", "Manual installation"),
            }[language]
            lines += [f"- [{section['title']}](#install)", "",
                      "  <details>", f"  <summary>{children[0]}</summary>", "",
                      f"  - [{children[1]}](#install-ai)",
                      f"  - [{children[2]}](#install-manual)", "", "  </details>", ""]
        else:
            lines.append(f"- [{section['title']}](#{section['anchor']})")
    lines.append("")
    return "\n".join(lines)


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
    """Draw the skill directory as a tree with platform-independent ordering."""
    skill_root = ROOT / "skills/smart-resume"
    lines = []

    def walk(directory, prefix):
        entries = sorted(directory.iterdir(),
                         key=lambda item: (item.name.lower(), item.name))
        directories = [item for item in entries if item.is_dir() and item.name != "__pycache__"]
        files = [item for item in entries if item.is_file() and item.name != "__pycache__"]
        for index, item in enumerate(directories + files):
            last = index == len(directories) + len(files) - 1
            connector = "└── " if last else "├── "
            if item.is_dir():
                lines.append(f"{prefix}{connector}{item.name}/")
                walk(item, prefix + ("    " if last else "│   "))
            else:
                lines.append(f"{prefix}{connector}{item.name}")

    lines.append("smart-resume/")
    walk(skill_root, "")
    return "```text\n" + "\n".join(lines) + "\n```\n"


def render(language, data):
    output_name, template_name = LANGUAGES[language]
    body = (TEMPLATES / template_name).read_text(encoding="utf-8")
    replacements = {
        "{{BANNER}}": build_banner(),
        "{{BADGES}}": build_badges(data),
        "{{TITLE}}": data["name"],
        "{{LANG_SWITCH}}": " · ".join(
            f'<a href="{link["target"]}">{link["text"]}</a>' for link in data["links"]),
        "{{TAGLINE}}": data["tagline"][language],
        "{{WHAT}}": "\n".join(f"- {item}" for item in data["what"][language]),
        "{{AUDIENCE}}": data["audience"][language],
        "{{INSTALL_PROMPT}}": data["install_prompt"][language],
        "{{INSTALL}}": "\n".join(data["install"]),
        "{{DEMO}}": data["demo"],
        "{{SKILL_TREE}}": build_skill_tree(),
        "{{TOC}}": build_toc(data, language),
    }
    for token, value in replacements.items():
        body = body.replace(token, value)
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
        if check and current is not None:
            diff = list(difflib.unified_diff(current.splitlines(), body.splitlines(),
                                             "committed", "generated", lineterm=""))[:40]
            print("\n".join(diff))
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
