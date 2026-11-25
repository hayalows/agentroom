agent: claude
piece: qa-sweep
started: 2026-11-25T13:43:47Z
status: needs-review
plan: Automatic cross-bank validator (sector/qa-sweep/validate.py): checks every finished bank folder against MODEL-SPEC (files, columns, line items, status rules, identities, forecast scenarios, macro link, cross-bank conventions) and writes report.md.
updated: 2026-11-25T13:49:11Z
progress: v1 built and run on all banks: sector/qa-sweep/validate.py, report.md, report.json, README.md. Needs an independent review (re-run it; check for false positives).
updated: 2026-11-25T14:20:51Z
progress: v1.1 pushed after reviews by claude-helper-1 and codex: false SG FAIL fixed (suspense/adjustment rows), break bug removed, stronger forecast checks (line items, PAT bridge, asset sum, columns bank and unit), strict macro.csv rule. Re-review welcome.

steward: chatgpt-support
updated: 2026-11-25T17:39:20.328Z
progress: Accepted existing human-authorized QA handoff with returning lead's board acknowledgment; Gemini's round2 CHANGES remain binding. Correct forecast row truncation, takeover claim discovery, finite/status/column validation and stale report. Preserve old reviews, request independent Gemini re-review. No bank-package edits.

updated: 2026-11-25T17:43:47.975Z
progress: Pinned e73b4e6ee367d2f5e63a3465a0e3a57815917321; full QA run covers 23 folders, 2 FAIL/6 WARN overall, all 18 accepted banks have zero FAIL. Both FAIL concern Prudential FY23/24 gross-loan bridges; known write-off memo may not match validator naming rule, investigate before classifying as actual errors. Gemini fault injection fixed: duplicate/invalid line item continue, downstream later PAT corruption detected, only actually removed downside FY30 missing; takeover claim correctly assessed; finite numeric guards, malformed/missing headers, unavailable numeric rows, invalid status and wrong bank detected. Eight simultaneous faults + both missing-header cases and takeover/finite tests pass. No bank file edits. Pinned report not live; QA diagnostic not ordinary acceptance. Independent Gemini review requested.
