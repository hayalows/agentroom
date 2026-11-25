agent: claude
piece: qa-sweep
started: 2026-11-25T13:43:47Z
status: in-progress
plan: Automatic cross-bank validator (sector/qa-sweep/validate.py): checks every finished bank folder against MODEL-SPEC (files, columns, line items, status rules, identities, forecast scenarios, macro link, cross-bank conventions) and writes report.md.
updated: 2026-11-25T13:49:11Z
progress: v1 built and run on all banks: sector/qa-sweep/validate.py, report.md, report.json, README.md. Needs an independent review (re-run it; check for false positives).
updated: 2026-11-25T14:20:51Z
progress: v1.1 pushed after reviews by claude-helper-1 and codex: false SG FAIL fixed (suspense/adjustment rows), break bug removed, stronger forecast checks (line items, PAT bridge, asset sum, columns bank and unit), strict macro.csv rule. Re-review welcome.

steward: chatgpt-support
updated: 2026-11-25T17:39:20.328Z
progress: Accepted existing human-authorized QA handoff with returning lead's board acknowledgment; Gemini's round2 CHANGES remain binding. Correct forecast row truncation, takeover claim discovery, finite/status/column validation and stale report. Preserve old reviews, request independent Gemini re-review. No bank-package edits.
