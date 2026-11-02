[简体中文](README.md) · [繁體中文](README.zh-TW.md) · [English](README.en.md)

# Smart Resume Skill

**A JD screenshot + existing materials → a tailored resume with traceable claims.**

Version **0.1.0** · Python **3.10+** · License **0BSD**

An installable Agent Skill. The host agent reads the job description, consults
authorized materials and tailors content. Local scripts validate the input,
create an A4 PDF and editable HTML, and write a separate private review record.
There is no bundled model, memory service, OCR service or standalone chat app.

## Preview

[`examples/demo.json`](examples/demo.json) contains entirely fictional Chinese
data. Run the demo commands below to generate actual PDF and HTML files.
Every demo page carries a notice prohibiting application use. The sparse
example illustrates structure, not a real candidate's complete two-page history.
See [acceptance](docs/ACCEPTANCE.md) and [task scope](docs/TASKS.md).

## Install and quick start

Extract the ZIP and enter the `smart-resume` directory containing `SKILL.md`.

```text
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/install.py --target "$HOME/.codex/skills/smart-resume"
```

macOS/Linux:

```sh
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/install.py --target "$HOME/.codex/skills/smart-resume"
```

Use your host's supported skills directory if different. The target must not
exist. The installer copies allowlisted project files, excludes personal
artifacts, and refuses to overwrite an existing version. It does not install
dependencies into your host agent's Python environment; continue to use the
interpreter where you installed the requirements.
Have the agent rediscover skills. Where discovery is unsupported, read
`SKILL.md` directly and report that this is not native installation. Manual
installation may copy the clean project folder into a supported skills directory.

In the following commands, `python` means the virtual environment interpreter:

```text
python scripts/resume.py validate examples/demo.json --demo
python scripts/resume.py render examples/demo.json --demo --out output/demo
```

Outputs: `resume.pdf`, `resume.html`, private `review.json`. Existing output
directories are preserved; choose a new directory for another run.
Windows font discovery prefers SimSun. Elsewhere provide a ReportLab-supported
TrueType font covering all output characters with `--font /path/to/font.ttf`
or `SMART_RESUME_FONT`. Missing glyphs cause an error. System fonts are not
redistributed. The default demo needs Chinese glyph coverage.

## Use with a real candidate

Tell your agent:

> Use $smart-resume to tailor my resume to this JD screenshot. First read relevant
> materials and memory you are authorized to access. If history is insufficient,
> ask for my old resume first, then ask about remaining missing items one at a
> time. Use only the exact JD title as my target role. Default to two A4 pages,
> deliver PDF and an editable version, inspect every page, and invent nothing.

Read existing materials before requesting them again. If necessary, request
the old resume first. Ask whether to provide or omit a photo; never require it.
Confirm remembered claims, resolve conflicting facts, and do not access
unauthorized accounts or other people's information. Ask about unreadable
screenshots instead of guessing the job title. Vision is supplied by the host.

Keep real data in a private directory outside this repository:

```text
python scripts/resume.py init --out ../private-resume/resume.json
python scripts/resume.py validate ../private-resume/resume.json
python scripts/resume.py render ../private-resume/resume.json --out ../private-resume/delivery
```

The incomplete intake intentionally fails validation until completed.
`document_supported` means a document supports a claim; `user_confirmed` means
the candidate confirmed it. Neither means independent third-party verification.
Pending, inferred and contradicted claims cannot be selected for the resume.
Scripts validate structure and source eligibility; they cannot determine truth
or assess job fit.

## Delivery and layout acceptance

Default: two A4 pages, 10.5 pt body. Ask about one page if content is insufficient;
never pad history. Overflow fails rather than shrinking or truncating text.
Photos may be omitted or embedded from private PNG/JPEG files with no network
loading. PDF text is selectable. HTML supports click-to-edit and browser Save
As. JSON is the content source for regeneration. **The editable format is HTML;
DOCX is not included.** HTML edits do not automatically update PDF.

Generated `review.json` starts factual, PDF visual and HTML review as `pending`.
Inspect every PDF page image and compare text with sources before recording
acceptance. HTML and PDF use separate layout engines; HTML printing is not PDF
verification. Send only the resume to employers; keep source and gap records private.

## Structure

```text
smart-resume/
├── SKILL.md                 Agent entry point
├── README*.md               Three language homepages
├── assets/                  Intake and HTML templates
├── examples/demo.json       Fictional fixture
├── references/workflow.md   Evidence and acceptance contract
├── scripts/                 Render, install, package
├── tests/                   Behavioral tests
├── docs/                    Scope and acceptance
└── .github/                 Checks and PR template
```

## Usage example

Give the scripts a completed private file and receive the three artifacts:

```text
python scripts/resume.py validate ../private-resume/resume.json
python scripts/resume.py render ../private-resume/resume.json --out ../private-resume/delivery
```

Output: `delivery/resume.pdf` (two A4 pages), `delivery/resume.html`
(editable) and `delivery/review.json` (layout and fact review record).
Missing or conflicting information fails the scripts instead of being
invented.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). Agent rules are in [AGENTS.md](AGENTS.md).

## License

Released under the 0BSD license in [LICENSE](LICENSE).

## Development and packaging

```text
python -m unittest discover -s tests -v
python scripts/package.py --out dist/smart-resume-0.1.0.zip
```

Packaging uses a fixed allowlist and prints SHA-256. Personal inputs, photos,
`.venv` and outputs are excluded. An allowlist cannot recognize personal data
inserted into an allowed file; review the diff before publishing.
CI is configured for Windows/Linux; configuration is not evidence of a remote run.
Read [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md).

## FAQ and privacy

- **No history access?** Only relevant materials actually authorized by the host can be used.
- **Can a screenshot alone finish a resume?** Candidate history is still required.
- **Font failure?** Supply a supported TrueType font with full coverage; complex shaping needs separate validation.
- **Can examples be public?** These examples are fictional. Never add real contact details, photos or resumes.
- **Automatic applications or GitHub pushes?** Neither is authorized by this skill.
- **Will installation activate it automatically?** Discovery and triggering depend on the host; confirm there.

See [LICENSE](LICENSE). All three READMEs describe 0.1.0 and must be updated together.
