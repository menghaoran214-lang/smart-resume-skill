"""Refresh the repository stats image that the README embeds.

The scheduled workflow runs this script; it writes assets/stats.svg from the
live GitHub API and commits the result. Failures keep the previous image
instead of breaking the README.
"""

import argparse
import json
import os
from pathlib import Path
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
SVG = ROOT / "assets/stats.svg"


def fetch(repo):
    request = urllib.request.Request(f"https://api.github.com/repos/{repo}")
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("User-Agent", "smart-resume-stats")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def build_svg(data):
    stars = data.get("stargazers_count", 0)
    forks = data.get("forks_count", 0)
    issues = data.get("open_issues_count", 0)
    parts = [("Stars", stars, "#0ea5e9"), ("Forks", forks, "#a855f7"), ("Issues", issues, "#22c55e")]
    x = 12
    pieces = []
    for label, value, color in parts:
        text = f"{label}: {value}"
        width = 22 + len(text) * 9
        pieces.append(
            f'<rect x="{x}" y="4" width="{width}" height="26" rx="6" fill="{color}"/>'
            f'<text x="{x + 11}" y="22" font-family="DejaVu Sans,Verdana,sans-serif" '
            f'font-size="14" fill="#ffffff">{text}</text>')
        x += width + 8
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{x}" height="34" '
            f'viewBox="0 0 {x} 34" role="img" aria-label="repository stats">'
            + "".join(pieces) + "</svg>")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default="menghaoran214-lang/smart-resume-skill")
    arguments = parser.parse_args()
    try:
        svg = build_svg(fetch(arguments.repo))
    except Exception as error:
        print(f"Keeping previous stats image: {error}")
        if not SVG.is_file():
            SVG.parent.mkdir(parents=True, exist_ok=True)
            SVG.write_text(build_svg({"stargazers_count": "-", "forks_count": "-",
                                      "open_issues_count": "-"}), encoding="utf-8")
        return 0
    SVG.parent.mkdir(parents=True, exist_ok=True)
    SVG.write_text(svg, encoding="utf-8")
    print(f"Updated {SVG.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
