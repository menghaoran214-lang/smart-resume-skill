# Input and acceptance contract

## Private workflow

1. Inventory accessible conversation, references and memory. Record unavailable
   sources honestly. Do not copy all history into a resume.
2. Extract JD text from the image; read back uncertain title/requirements.
3. Read an existing resume before asking for new facts. Request it only if
   existing material is insufficient. Ask consequential missing details one at
   a time: conflicting employment dates, role/education, contact, photo preference.
4. Maintain the source ledger and classify each claim. Confirm memory-derived
   claims; retain both versions of a conflict in private notes until resolved.
5. Compare each requirement to supported claims. Mark direct match, transferable
   experience (interpretation), or gap. Do not present fit scoring as objective.
6. Draft one job intention exactly equal to JD title. Use existing role titles
   in experience entries. Prefer action + scope + supported result; a plain
   responsibility is better than an invented metric.
7. Build PDF/HTML, verify both, then deliver privately.

## JSON fields

`schema_version` is 1. Unknown top-level fields are rejected to catch misspellings.
`language`: `zh-CN`, `zh-TW`, `en`. This selects labels, not translation of claims.
`demo`: false for a real candidate. `jd`: title, company and source locator.
`intention`: the exact JD title. `candidate`: IDs of the `name` claim and
`contacts` claims; `photo_preference`: `omit` or `provided`.
`photo`: relative image path if provided (PNG/JPEG, stored with private JSON).
Omission is the default layout; ask the user before deciding the preference.
`pages` contains one or two pages, each an array of sections with `title` and
`claim_ids`. No empty pages, sections or claim references are permitted.

`sources` contains unique `id`, `kind` and `locator`.
Kinds: `document`, `user_statement`, `memory`, `synthetic`.
`claims` contains unique `id`, `text`, `status`, `source_ids`.
Statuses: `document_supported`, `user_confirmed`, `pending`, `inferred`,
`contradicted`. Every referenced claim must be supported. Document-supported
claims need a document source; user-confirmed claims need a user-statement
source. A memory source alone is insufficient. Add a separate source recording
the user's confirmation. Synthetic sources are accepted only in explicit demo
mode, with a visible notice on every page.

Unreferenced pending claims remain private and are reported as omitted.
Do not insert source IDs or gap notes into employer-facing files.
Do not put requirements into candidate claims without candidate evidence.
An evidence status is not proof that a document is accurate or an employer
independently verified a statement. The agent must read the source and check
semantic support; the validator checks structure and eligibility only.

## Acceptance record

The renderer writes page count, A4 dimensions, fixed body size, claim IDs,
omitted claims, and `visual_review: pending`, `factual_review: pending`,
`html_review: pending` into `review.json`. Change a review to `passed` only
after performing it; add `review_notes` with reviewer, date, findings and tools.

PDF checks: all pages A4; expected page count; no missing characters, clipped
photo, overlap, orphan headings or excessive blank area; readable at 100%;
all visible claims present in extracted text; one intention; correct dates
and contact; photo preference respected. Two pages are a default, not a reason
to fabricate or pad. If content does not fit, edit selected claims or move
sections. Never reduce font below the default just to get a green check.

HTML checks: view at desktop and narrow widths, edit a line, save a copy and
confirm the saved copy retains it. Print layout is secondary: the generated
PDF is the checked delivery format and uses an independent typesetting engine.
After editing HTML, regenerate PDF from updated JSON for a consistent pair.

## Limitations

The host agent performs screenshot recognition, research and tailoring; the
Python scripts do not call models, search memory, assess job fit, or verify
truth. Available memory/vision/connectors depend on the host environment.
The renderer can fail on unsupported fonts, scripts needing complex shaping,
or excessive content. Report these limitations and use an appropriate document
tool if needed. Do not claim a PDF export is visual acceptance.
