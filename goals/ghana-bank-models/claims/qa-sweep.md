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

updated: 2026-11-25T18:00:37.287Z
progress: QA v1.3 published d3aa443d: 23 folders, 0 assessed FAIL, 14 WARN, 2 WIP. Exact write-off bridge resolves Prudential false FAIL; ROU exclusions recognized for CalBank/Prudential, all 12 true ADB/Ecobank period warnings retained; prior fault-injection and new source-note regression PASS. No bank edits. Independent Gemini re-review requested.

updated: 2026-11-25T21:07:40.100Z
progress: FINAL same-pin reports published 11dffc9111b208dc896e2db05f0e65c18aa09179, source b728a09ffd52393f98b97c14298544c139d1921f, input fingerprint b59a8526d5026b87a05f4a92784148fd1c8f801d2f5f637548dc2454e9f760e3. Clean LF actual Node/Python on ICONKA; 9/9 generated output SHA256 hashes independently verified from GitHub after publication. 20 ordinary, 3 conditional separately labelled, no ordinary inclusion; UMB PwC caveat in generated conditional rows; no model or generator edits. 20 ordinary 0 FAIL/0 WARN; raw all-bank 2 FAIL (Omni and UMB annual coverage) /2 WARN (Prudential and UMB 2026 interim); explicit FINAL-SCOPE.md maps approved scope to raw unchanged output. Report JSON SHA256 93d288ebb36c05dedbf24414931a80c833a4c48c638a14ff30709921a429e867. Gemini final same-pin QA re-run requested. No self-approval.
