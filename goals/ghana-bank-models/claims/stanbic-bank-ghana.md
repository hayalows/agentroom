agent: deepseek
piece: Stanbic Bank Ghana Limited
started: 2026-11-25T12:48:10Z
status: needs-review
plan: Source 5-year bank-only historical financials and latest interim from public filings (GSE/company sites), store GHS millions with a page per reported number, then build a reproducible 3-scenario FY2026E-FY2030E forecast on sector/macro-assumptions with Python checks, and submit README/checks for independent review.
updated: 2026-11-25T15:05:00Z
progress: Revision after codex CHANGES review (round 1). All six items addressed: (1) forward yield calibrated to a blended anchor-implied yield carried forward with policy-rate drift; removed the 2026->2027 interest-income jump of ~53% (base FY2027 II now 2,539.6m vs 4,034.3m before); added out-of-sample FY24->FY25 back-test (4.3% error) in checks.md. (2) trading + pledged assets folded into canonical other_assets; x_ rows are non-additive memos. (3) anchor-year tax split now preserves actual 9M indirect (36.323m)/direct (465.606m) and adds only a Q4 estimate; 82% net-to-gross documented as an estimated improvement. (4) reported summary ratio stored as x_cet1_pct; true tier1_pct derived from the audited capital note (FY2025 21.17%). (5) FY2026E dividends labelled Q4-only; no-transfer simplification disclosed; buffer gap reported. (6) FX-omission correction in sources.md. Official gate re-run: core-checks-pass. Note: core-check fingerprints are unaudited and independent source verification is still required.
review_revision: 2628443539e7dce48b6ac96917c0e9fc43a174fb6c2126db271b9c723b5c75bb
review_macro: 4cf8911a258f0c81a4a48e660b31b796de40e8327dca36d2bbdb16b59a2f7202
