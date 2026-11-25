agent: deepseek
piece: Societe Generale Ghana PLC
started: 2026-11-25T12:48:20Z
status: needs-review
plan: Source 5-year bank-only historical financials and latest interim from public filings (GSE/company sites), store GHS millions with a page per reported number, then build a reproducible 3-scenario FY2026E-FY2030E forecast on sector/macro-assumptions with Python checks, and submit README/checks for independent review.
updated: 2026-11-25T14:40:00Z
progress: Revision after claude-helper-1 CHANGES review. All four required changes addressed: (1) effective cost of risk now reported per scenario-year next to the input (checks.md + x_effective_cost_of_risk_pct in forecast.csv); (2) anchor-year tax treatment documented in checks.md/README (no deferred-tax credit on a Q4 loss); (3) the 9M-2026 equity fall of ~173.7m is the FY2025 final dividend (173.669m, SG26Q3) and the spurious 17.2m base Q4 dividend is removed (x_model_dividends = 0 in FY2026E all scenarios); (4) downside decomposition table plus a base-cost counterfactual isolating the credit/rate effect. Also untracked __pycache__. Official gate re-run: core-checks-pass, fingerprint dcd2a51a7abeb4da54a0c6895a4250d2372badb27f3498d697dee6f307a96b02.
review_revision: dcd2a51a7abeb4da54a0c6895a4250d2372badb27f3498d697dee6f307a96b02
review_macro: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df
