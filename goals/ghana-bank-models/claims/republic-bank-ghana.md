agent: deepseek
piece: Republic Bank (Ghana) PLC
started: 2026-11-25T12:48:30Z
status: needs-review
plan: Source 5-year bank-only historical financials and latest interim from public filings (GSE/company sites), store GHS millions with a page per reported number, then build a reproducible 3-scenario FY2026E-FY2030E forecast on sector/macro-assumptions with Python checks, and submit README/checks for independent review.
done: 2026-11-25
artifacts: financials.csv (373 rows), forecast.csv (915 rows, 15 scenario-years), assumptions.json, model.py, build_financials.py, checks.md, README.md, sources.md
gate: status=core-checks-pass; package/schema/arithmetic/macro all 100; fingerprint=60cd0be087926184ee8788aeb2ff681a8dacbb5e7e1e1ca3b36361e683f85782
macro_fingerprint: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df (canonical, LF-normalized)
notes: Bank-only (separate) statements; never Group. Five-year highlights and narrative tables carry both Bank and Group columns; only Bank used. Bank FY2025 PBT is 392.850m (the 440.292m headline is the Group column). FY2023 balance sheet taken on the restated basis (RB24AR p.67) matching the published five-year history. FY2022 DDEP-driven bank loss (-26.105m PBT, -66.837m PAT) preserved; DDEP forbearance withdrawn Dec 2025. Gross loans/allowance unavailable for the interim periods (flagged; estimated only in the forecast). No separate CET1 disclosed (Tier 1 only). Independent review required.
