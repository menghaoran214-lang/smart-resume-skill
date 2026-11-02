# Contributing

Use Python 3.10+ and install `skills/smart-resume/requirements.txt` into an
isolated environment. Run `make test` for the repository tests and the skill
tests. For a demo PDF, use the README commands and a locally licensed font
covering its characters.

The three READMEs are generated from `templates/` and `data/project.yaml`.
Change the source and run `python scripts/render_readme.py`; CI fails when a
README is out of date. Include a concrete behavior test for validation,
rendering or installation changes. Do not commit real resumes, photos, contact
details, secrets, output files or system fonts. Use fictional fixtures and
reserved example addresses. Review every distribution file before publishing;
the packaging allowlist is not a personal-data detector.

Use a focused PR with the behavior changed, validation performed and remaining
limitations. Do not claim remote CI or native installation based on local checks.
