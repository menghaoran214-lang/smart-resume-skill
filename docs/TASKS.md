# Smart Resume task scope

Requested outcome: an inspectable GitHub repository for the resume skill that
follows the agreed repository standard, before writing the separate Repo
Standards Skill.

| Requirement | Implementation |
| --- | --- |
| Installable skill | `skills/smart-resume/SKILL.md` plus `scripts/install.py` |
| Common skill layout | Skill body under `skills/`, repository files at the root |
| Three-language navigation | Generated README.md, README.zh-TW.md, README.en.md with a first-line switch |
| Generated README | `scripts/render_readme.py` over `templates/` and `data/project.json`, automatic table of contents |
| First screen | Centered banner, badge row, one-line purpose, who it is for, install |
| Dynamic content | `scripts/update_stats.py` and a scheduled workflow refreshing `assets/stats.svg` |
| JD screenshot workflow | Host vision procedure in SKILL.md |
| Reuse authorized history | Host memory/material inventory, then old resume if insufficient |
| Ask missing items individually | Intake order and photo provide/omit decision |
| Single intention | Exact jd.title equality validation |
| Truth and sources | Claim eligibility, source ledger, private gap handling |
| PDF + editable output | ReportLab PDF and editable HTML from common JSON |
| Default two A4 pages | Two-page intake, one-page support, overflow refusal |
| Basic tests | Skill suite plus repository README suite |
| Privacy | Synthetic examples, private inputs outside the repo, allowlisted package |
| GitHub readiness | AGENTS, CONTRIBUTING, LICENSE, CHANGELOG, CI, scheduled workflow, PR template |

Outside this delivery: building the Repo Standards Skill, actual applications,
public hosting, automatic memory or OCR services, DOCX export, global
installation without a chosen target, or a real candidate resume.
