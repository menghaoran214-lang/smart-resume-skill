# Acceptance

Version: 0.1.0. Local implementation date: 2026-11-02.

Local checks performed on Windows on 2026-11-02, using the bundled Python 3.13
runtime, ReportLab and SimSun. No remote CI run is claimed.

## Results

| Check | Observed result |
| --- | --- |
| Skill creator quick validator | Passed: `Skill is valid!` |
| Behavioral suite | 19 tests passed |
| Chinese demo CLI | PDF, HTML and review record generated |
| PDF metadata | 2 pages; 595.276 x 841.89 pt, A4 |
| PDF text extraction | Every selected demo claim found with pypdf |
| PDF visual inspection | Both page images viewed; no missing glyphs, clipping or overlap |
| Demo composition | Intentionally sparse; substantial whitespace; not a finished candidate resume |
| HTML host browser | Opened successfully through native ego-browser |
| HTML editability | Both page articles reported contenteditable |
| HTML persistence | Edited DOM serialized to a local HTML copy; reopened text retained |
| Narrow layout | 390 px viewport; no horizontal overflow reported |
| HTML screenshot visual review | Pending: ego window was minimized and native screenshot capture failed |
| Browser Save As interaction | Not tested; persistence test used DOM serialization |
| Local fixture installation | Install succeeds; existing directory refused |
| ZIP | Allowlisted content, deterministic-byte test and no-overwrite test passed |

The Python tests include one-page output, embedded synthetic pixel image,
pending/memory/synthetic evidence rejection, exact job-title matching,
HTML escaping, missing fonts, overflowing content and output preservation.
Tests ran with temporary directories under a separate workspace validation
directory; the initial host temporary-directory attempt stalled and was stopped.
Installing beneath the source tree is intentionally refused.

The release archive is also extracted and exercised from a fresh isolated
installation before delivery. This checks the standalone package rather than
only the development directory.

## Required checks

- Skill frontmatter validator.
- Behavioral tests for evidence, rendering, install and package.
- Demo CLI generates PDF, HTML and a private review record.
- PDF metadata: two pages and A4; extracted text includes selected claims.
- Inspect every demo PDF page image for clipping, missing glyphs and overlap.
- Local isolated installation and archive extraction smoke test.
- Three-language links and distribution allowlist.

## Boundaries

The demo is fictional and intentionally sparse. Its evidence classification
does not represent a real person's verified career. Automatic eligibility
checks cannot establish truth or interpret JD fit.

HTML supports editing, but browser save/restore and visual QA must be reported
separately from PDF QA. No real application, remote CI, public repository,
GitHub push or host-wide native skill discovery is implied by local tests.
