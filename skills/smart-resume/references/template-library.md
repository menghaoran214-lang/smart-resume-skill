# Template intelligence and feedback

Reuse before research. Read the JD, retrieve approved templates by role family,
channel and seniority, and inspect supported candidate evidence. Research only
when the existing library cannot resolve a specific requirement. Explain the
choice to the candidate; keyword ranking is a suggestion, not a hiring model.

## Three independent measures

1. Structure quality: JD relevance, supported achievements and readable hierarchy.
2. Technical quality: PDF text extraction, fonts, pagination, bounds and visual review.
3. Delivery outcomes: actual applications, replies, interviews and offers.

Never merge these into one hiring score. Say "quality checked" only for the
artifact reviewed. "Validated with actual delivery data" needs recorded real
applications and their context. No template is proven to cause an interview.
Synthetic examples have no delivery evidence.

## Internal 100-point editorial rubric

This is our own review framework, not an employer or ATS algorithm. Reviewers
must cite evidence and explain deductions; the CLI does not calculate it.

| Criterion | Points |
| --- | ---: |
| Match to the exact JD | 35 |
| Supported achievements and attribution | 25 |
| Factual consistency and source traceability | 15 |
| Content hierarchy and concise language | 10 |
| Parsing, pagination and font quality | 10 |
| Visual design | 5 |

Unsupported claims, incorrect contact information or failed technical acceptance
block delivery regardless of points. A score never predicts hiring probability.

## Private library

Store metadata by role family × channel × seniority outside the repository in
`~/.smart-resume/library`. Style preferences remain in `~/.smart-resume/styles`.
The library saves reusable classification and feedback, not a candidate resume.
Do not put personal details in notes; keep evidence files in private storage.

```text
python scripts/library.py list --role-family ops-growth --channel cn-platform
python scripts/library.py save shenzhen-growth --style growth --role-family ops-growth --channel cn-platform --seniority mid
python scripts/library.py evidence shenzhen-growth structure quality_checked --note "Private review reference"
python scripts/library.py evidence shenzhen-growth technical quality_checked --note "Private quality.json reference"
python scripts/library.py promote shenzhen-growth
python scripts/library.py log shenzhen-growth --applied 10 --reply 3 --interview 2 --offer 0
python scripts/library.py report shenzhen-growth
python scripts/library.py deprecate shenzhen-growth --reason "Parsing needs repair"
```

States: candidate → promoted only after both quality reviews; deprecated excludes
it from recommended reuse. Repair a deprecated template and review again before
promotion. A failed new check must downgrade it before further reuse. Do not
keep adding templates without reviewing poor or obsolete ones.
Feedback batches must describe distinct applications, not repeated cumulative
totals. The report suppresses rates below 30 applications as a display convention,
not a statistical proof. Outcome data remains user-reported.

## Research and public contributions

Four source channels guide research: university career centers (Harvard/MIT),
recruiting research (NACE), actual JD requirements (BOSS直聘/猎聘/LinkedIn),
and ATS diagnostics plus actual application feedback (for example Jobscan).
These are research starting points, not endorsements or claims that this library
has imported or verified their templates. Verify current original sources when used.

For Shenzhen and domestic platforms, use a Chinese font with complete glyphs,
one or two pages according to evidence, one exact job intention and confirmed
contact details. Ask about a candidate-supplied photo; never require a photo,
age, marital status or identity number by default. Follow the target employer's
actual requirements rather than assuming all domestic employers are alike.
Keep portfolio links readable; do not invent work examples.

Public evolution uses a reviewed GitHub PR: include a licensed, de-identified
STYLE.md, classification, synthetic input, real PDF previews and review evidence.
Never contribute paid templates, other people's resumes, personal feedback logs,
candidate records or unlicensed fonts. Do not upload without authorization.
Public library updates are reviewed contributions, not autonomous web scraping.
