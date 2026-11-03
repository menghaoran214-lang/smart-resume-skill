# Acceptance

## 0.3.0 discussion alignment - 2026-11-03

Local Windows verification: 8 repository tests and 33 skill tests passed.
Six corrected styles in three languages produced 18 single-page PDF previews;
PDF contact sheets were visually inspected for layout, glyphs and clipping.
The suite also checks two-page output for every style/language combination.
Native ego-browser checked 42 gallery/resume viewport observations (1440/390 px):
no horizontal overflow, clipped text or failed images; growth filtering passed.
HTML screenshot review remains pending because the browser window was minimized.
Do not inherit 0.2.0 visual attestations for changed artifacts. New review records
retain pending categories until the respective review is performed.

The new private library lifecycle and feedback are executable and tested.
The 100-point rubric is an agent review instruction, not an automatic score.
No real application outcomes were collected or claimed. Public contributions
are PR-based; there is no unattended template crawler or self-training model.
GitHub synchronization and remote CI must be reported separately.

## Current release: 0.2.0 - 2026-11-03

Local verification on Windows with the bundled Python 3.13 runtime, ReportLab,
pypdf, Poppler and native ego-browser. The existing implementation was inspected
before extending it. The initial local verification did not create a GitHub
repository, push changes, upload samples or install globally. `sources/` was not modified.
The user's follow-up authorizes synchronization to the existing
`menghaoran214-lang/smart-resume-skill` repository. Repository visibility stays
unchanged; only synthetic preview PDFs and their contact sheet are included.

| Check | Observed result |
| --- | --- |
| Skill creator quick validator | Passed |
| Repository suite | 8 tests passed |
| Skill suite | 30 tests passed, including 18 style/language rendering combinations |
| Native make | Not available in this PowerShell environment; both commands in `make test` ran directly |
| Real preview PDFs | 18 final single-page A4 previews: six layouts in Simplified Chinese, Traditional Chinese and English |
| Two-page support | All six layouts in all three languages rendered and passed text/layout checks in the suite |
| PDF text and dimensions | Every selected claim and exact intention found; A4 and page counts passed |
| Layout integrity | Recorded text boxes remain in bounds and do not overlap |
| PDF visual inspection | All 18 final pages viewed in three six-style PDF contact sheets; no clipping, overlap or missing glyphs observed |
| HTML visual inspection | All 18 desktop pages viewed in three six-style browser screenshot contact sheets |
| Browser checks | 45 final gallery/filter/resume observations; all three languages at 1440 and 390 px; no horizontal overflow or clipped text |
| Real gallery assets | PDF-generated PNGs loaded; six cards per gallery; filter selected only the requested style |
| Personal profiles | Save, list, reload, rendered token reuse, contrast rejection, unsafe fields and no-overwrite behavior passed |
| Overflow behavior | All six layouts refuse oversized text without leaving a partial delivery |
| Acceptance gate | Pending/failed reviews and changed PDF/input fail; demo previews never become application-ready |
| Final preview acceptance | 18/18 accepted as synthetic previews; every `application_ready` value remains false |
| Standalone archive | Extracted archive installed into a fresh local validation directory; installed gallery generated all six PDF/HTML pairs |
| Distribution | Allowlist, deterministic ZIP bytes and no-overwrite tests passed |
| Three READMEs | Regenerated from templates/data; language links and generation tests passed |

The final gallery uses `--compact` to combine every fictional section into one
page without dropping text or shrinking fonts. The original two-page input
contract is unchanged. Preview PNGs come from the actual PDFs, not mockups.
The saved `demo-input.json` is the exact input used for each gallery.

Files next to this engineering project under `delivery/`:

- `smart-resume-0.2.0.zip`: installable skill archive.
- `smart-resume-engineering-0.2.0.zip`: local source engineering project.
- `smart-resume-gallery-0.2.0/`: Simplified Chinese gallery, PDFs, HTML, images and review records.
- `smart-resume-gallery-en-0.2.0/` and `smart-resume-gallery-zh-TW-0.2.0/`: English and Traditional Chinese galleries.
- `smart-resume-browser-qa-0.2.0-final.json`: final browser observations.
- `smart-resume-quality-0.2.0.json`: detailed acceptance checks for all 18 previews.

Limitations: matching is a transparent keyword heuristic, not an assessment of
candidate fit. Personal profiles customize a base layout's accent and spacing;
they do not implement arbitrary new renderer code. PDF and HTML use separate
layout engines. Browser Save As, HTML-to-PDF synchronization, remote CI and
host-wide skill discovery were not tested or claimed. Font licenses are not
bundled; non-Windows CJK generation may need `--font`. Gallery generation requires
Poppler, while ordinary PDF rendering does not. The prior temporary-directory
stall was avoided by running tests with a workspace-local TEMP/TMP.

## Historical 0.1.0 verification

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
