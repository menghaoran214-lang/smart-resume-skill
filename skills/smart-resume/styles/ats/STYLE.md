# ATS Minimal · ATS 极简 · ATS 極簡

## Identity
A plain black single-column document with conventional section names and no
decorative rules. Intended for text extraction and conservative upload workflows.
Compatibility with every applicant tracking system is not guaranteed.

## Invariants
A4, 18 mm margins, 10.5 pt body, 16 pt leading, 24 pt name, 13 pt headings.
All content follows source reading order. No columns, rating bars, icons or
color-dependent meaning. Prefer no photo when the candidate has no preference.
Never remove a provided photo without discussing it with the candidate.

## Variation
Regular or airy spacing. A saved accent is accepted but black PDF text takes
priority in this style. User content and approved labels remain unchanged.

## Engine and acceptance
`scripts/resume.py`, layout `plain`; `assets/resume.html`, style `ats`.
Extract the PDF text and verify every selected claim, contact and exact title.
Check that a long URL wraps without disappearing. Demo data is separate.
