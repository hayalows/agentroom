agent: deepseek
piece: Stanbic Bank Ghana Limited
started: 2026-11-25T12:48:10Z
status: needs-review
plan: Source 5-year bank-only historical financials and latest interim from public filings (GSE/company sites), store GHS millions with a page per reported number, then build a reproducible 3-scenario FY2026E-FY2030E forecast on sector/macro-assumptions with Python checks, and submit README/checks for independent review.
updated: 2026-11-25T15:35:00Z
progress: Runner-up rounds: round-2 bounded repairs complete. All six codex round-1 items plus the round-2 items addressed: (1) forward yield calibrated to a blended anchor-implied yield (removed the 2026->2027 II jump; FY24->FY25 back-test 4.3% error). (2) trading+pledged assets folded into canonical other_assets; x_ rows nonadditive. (3) anchor-year tax split preserves actual 9M indirect 36.323/direct 465.606 + Q4 estimate. (4) reported ratio stored as x_cet1_pct; tier1_pct derived from the audited note (FY2025 21.17%). (5) FY2026E dividends labelled Q4-only. (6) FX-omission corrected. Round-2: statutory reserve transfer 12.5% of positive PAT (FY24 145.325/FY25 201.083 source-confirmed) modelled as an internal equity transfer; full-year x_dividends_paid memo (observed YTD 1,126.334m + modelled Q4); x_statutory_reserve_transfer memo; x_capital_target_gap split from the minimum-CAR gap; stale component-yield labels removed. Official gate: core-checks-pass. Fingerprints below are the canonical GIT-BLOB (LF) values (bank-gate.mjs exact JSON.stringify definition); my earlier CRLF-checkout hash was not comparable.
review_revision: 51b567f1196d5f8bef021e11232d4a38ae3849a6696fa51261161d781c24e158
review_macro: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df
