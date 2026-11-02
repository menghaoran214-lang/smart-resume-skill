# Project development

Scope: this Smart Resume repository only.

- The READMEs are generated products. Edit `templates/` and `data/project.json`,
  then run `python scripts/render_readme.py`. Never edit `README*.md` by hand.
- The skill itself lives in `skills/smart-resume/`. Keep it minimal: SKILL.md,
  scripts, references, assets, examples.
- Keep real candidate materials outside the repository. Examples and tests must
  be synthetic; do not fetch the user's history while developing the skill.
- Do not imply model or OCR automation in the Python CLI; the host agent does
  screenshot reading and tailoring.
- Run `make test` (repository tests plus skill tests) for behavior changes.
- Check the `skills/smart-resume/scripts/package.py` allowlist when adding files.
- Do not shrink resume body text or silently discard overflowing content.
- Never change pending review states to passed without performing the review.
- No GitHub creation, push, public upload or application submission without
  explicit user authorization. Do not alter global agent settings.
