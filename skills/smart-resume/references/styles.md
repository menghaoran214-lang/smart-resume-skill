# Style library, matching and personal styles

The mechanism is inspired by the separation of invariant STYLE.md rules, demos,
gallery and personal styles in [Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar).
Reviewed on 2026-11-03: `styles/_template/STYLE.md`, `AGENTS.md` and
`plugin/skills/lemo-opuscar/SKILL.md`. These are original resume layouts, not
copies of its film styles or a dependency on its runtime.

Read `styles/<id>/STYLE.md` for the chosen style. The machine-readable catalog
drives both engines and the gallery. Invariants are not candidate facts.
Demo content lives separately under examples.

## Selection

Offer the user's saved styles first when they ask to choose. Run `styles` to
list built-ins and profiles. No saved style is silently made a global default.
Precedence: explicit `--style`, explicit `--profile`, automatic role matching.
Conflicting explicit style and profile base are rejected.

`match INPUT --context TEXT` ranks keywords from the exact JD title plus optional
host-supplied context. It prints matches and reasons; scores are rule counts, not
model confidence or hiring probabilities. No claim text is mined to choose a
style. No matches fall back to classic. `--ats` explicitly selects ATS; conflicts
with a different explicit style/profile fail. Company preference and candidate
choice override automatic recommendations. Do not imply an ATS compatibility
certification.

## Local commands (from skill directory)

```text
python scripts/resume.py styles
python scripts/resume.py match /private/resume.json --context "software engineer"
python scripts/resume.py render /private/resume.json --style technical --out /private/technical
python scripts/resume.py save-style my-green --base technical --accent "#155e52" --spacing airy
python scripts/resume.py render /private/resume.json --profile ~/.smart-resume/styles/my-green/profile.json --out /private/reused
python scripts/gallery.py --compact --out /private/gallery
```

Profiles contain only a slug, base ID, dark accent and spacing. Default location:
`~/.smart-resume/styles/<name>/{profile.json,STYLE.md}`. `--profiles-dir` supports
a user-chosen private location. Keep profiles outside the repository; never save
names, contacts, histories, source locators or rendered resumes there.
Existing profiles are never overwritten. Edit tokens in profile.json or save a
new name. Loading validates exact fields, values and 4.5:1 contrast on white.
No arbitrary CSS, scripts or file paths are executed from a profile.
The saved STYLE.md explains its base; renderers read only validated JSON.

## Gallery

`gallery.py` creates six actual PDF/HTML pairs from the same fictional input,
renders every PDF page to PNG using Poppler and links all pages in a local,
responsive gallery. Pass `--input` only for a synthetic `demo: true` fixture;
personal data is deliberately refused. `--pdftoppm` selects the Poppler binary.
It never downloads fonts, publishes files or opens network services.
`--compact` combines the fictional fixture's sections onto one page without
discarding claims or shrinking text. It fails on overflow. The exact gallery
fixture is saved as `demo-input.json` alongside the gallery for quality checking.

## Acceptance

`python scripts/quality.py DELIVERY INPUT --demo` verifies output hashes,
page count, A4, text completeness, glyph replacement characters and recorded
layout bounds. For a real input omit `--demo`. It does not inspect truth or pixels.
It returns nonzero until automatic checks AND visual/factual/HTML reviews pass.

After actually reviewing both formats and source facts, record each category:

```text
python scripts/quality.py DELIVERY INPUT --demo --record visual_review --status passed --reviewer agent --notes "Inspected every rendered page; no clipping or missing glyphs."
python scripts/quality.py DELIVERY INPUT --demo --record factual_review --status passed --reviewer agent --notes "Synthetic fixture; every selected claim matches the fixture; not a real applicant."
python scripts/quality.py DELIVERY INPUT --demo --record html_review --status passed --reviewer agent --notes "Checked desktop and 390 px viewport; all selected text present."
```

These records are attestations, not automatic proof of human review. Only record
what was actually inspected. Failed/pending categories block readiness. Changed
PDF or HTML hashes require regenerating and reviewing a new delivery directory.
`quality.json` distinguishes `demo_preview_accepted` from
`candidate_delivery_accepted`; a demo can never become application-ready.
