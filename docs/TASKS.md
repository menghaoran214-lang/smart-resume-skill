# Smart Resume task scope

Current outcome: an inspectable local Smart Resume engineering project and
installable 0.3.0 archive, extending the existing implementation. The follow-up
request authorizes updating the existing `menghaoran214-lang/smart-resume-skill`
repository, including clear usage, release differences and synthetic PDF samples.
Do not create another repository or change the existing repository's visibility.

| Requirement | Implementation |
| --- | --- |
| Installable skill | `skills/smart-resume/SKILL.md` plus `scripts/install.py` |
| Six real styles | ats, executive, growth, creative, technical, classic; independent STYLE.md and shared catalog |
| Discussion alignment | Role/channel/seniority classification, reuse-before-research, private lifecycle and feedback |
| Evidence boundaries | Separate structure quality, technical quality and actual delivery outcomes; internal rubric is not a hiring model |
| Real preview gallery | `scripts/gallery.py`; all preview PNGs originate from generated PDFs |
| Automatic template matching | Role/context keyword ranking, explicit overrides, reasons and conservative fallback |
| Personal style persistence | Validated profile.json and STYLE.md in a user-chosen private directory |
| Quality acceptance | `scripts/quality.py`; hashes, text, A4, bounds and explicit review attestations |
| Common skill layout | Skill body under `skills/`, repository files at the root |
| Three-language navigation | Generated README.md, README.zh-TW.md, README.en.md with centered HTML language links |
| Generated README | `scripts/render_readme.py` over `templates/` and `data/project.json`, automatic table of contents |
| First screen | Centered banner, badge row, one-line purpose, who it is for, install |
| Navigation | Explicit stable anchors and independently collapsible installation sublinks |
| JD screenshot workflow | Host vision procedure in SKILL.md |
| Reuse authorized history | Host memory/material inventory, then old resume if insufficient |
| Ask missing items individually | Intake order and photo provide/omit decision |
| Single intention | Exact jd.title equality validation |
| Truth and sources | Claim eligibility, source ledger, private gap handling |
| PDF + editable output | ReportLab PDF and editable HTML from common JSON |
| Default two A4 pages | Two-page intake, one-page support, overflow refusal |
| Basic tests | Skill suite plus repository README suite |
| Privacy | Synthetic examples, private inputs outside the repo, allowlisted package |
| GitHub readiness | AGENTS, CONTRIBUTING, LICENSE, CHANGELOG, CI, scheduled workflow, PR template, issue templates and security reporting |

Outside this delivery: building the Repo Standards Skill, actual applications,
public hosting, automatic memory or OCR services, DOCX export, global
installation without a chosen target, or a real candidate resume.
