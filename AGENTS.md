# Project development

Scope: this Smart Resume project only.

- Keep real candidate materials outside the repository. Examples/tests must be
  synthetic; do not fetch the user's history while developing the public skill.
- Keep all three README versions aligned, including language links, commands,
  version and limitations. Do not imply model/OCR automation in the Python CLI.
- Run `python -m unittest discover -s tests -v` for behavior changes.
- Keep SKILL.md focused on agent behavior; put input details in references.
- Check the `scripts/package.py` allowlist when adding distribution files.
- Do not shrink resume body text or silently discard overflowing content.
- Never change pending review states to passed without performing the review.
- No GitHub creation, push, public upload or application submission without
  explicit user authorization. Do not alter global agent settings.
