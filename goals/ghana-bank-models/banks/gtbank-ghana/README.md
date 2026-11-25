# GTBank Ghana — repaired bank-only scenario package
Original model: Claude. Authorized steward: chatgpt-support. Source register and Codex review preserved. FY2021–25 and 9M2025/26. FY25 reported PAT 1012.223m; September 2026 reported CAR24.08%, NPL3.67%; nine-month actual dividends604.370m. No future capital injection. Ghana bank only.
## Forecast summary (GHS millions; CAR proxy)
| Scenario | FY26 PAT | FY30 PAT | FY30 assets | FY30 CAR proxy |
|---|---:|---:|---:|---:|
| base | 1200.075 | 2076.608 | 52002.479 | 23.857% |
| downside | 1200.075 | 1862.481 | 46588.668 | 34.678% |
| upside | 1200.075 | 2153.174 | 55741.256 | 20.562% |

## Repaired findings
Historical original/comparative presentation documented, audited FY21–24 gross/ECL and capital note rows added, combined cash net scope preserved with exact gross memos, ROU already within PPE. Standard forecast keys included or explicitly unavailable. Net LDR separate. FY26 actual tax plus Q4 estimated tax; flat September loan/deposit balances in Q4. No extra Q4 dividend; future payout constrained by retained earnings, capital proxy buffer, securities and 40%-eligible-cash stress. All statutory reserve bands implemented. Static rate/FX sensitivities, 80% earnings eligibility and higher risk density screens. No actual prudential certification, no claim of future currency exposures. Original source values preserved except explicitly derived ratio and unavailable cash split. Actual Python CLI in isolated authorized laptop checkout generated 355 history and 795 forecast records, zero forecast-check failures. Round 2 correction: the shared 13 percentage-point minimum is converted to 0.13 in the engine before comparing percentage ratios; explicit assertions bind the 13% minimum and 18% payout target in all scenario-years and sensitivity runs. FY2030 dividends: base 1066.858m, downside 703.352m, upside 1175.074m. All forecasts, risk screens and rate sensitivities regenerated from the current engine; actual 9M2026 604.370m payout preserved. Repository transfer normalizes LF. Independent Codex re-review required; Q3 and some visual sources remain unverified.
Rebuild: from bank directory run original build_financials.py, then enrich_history.py, then model.py. Do not overwrite enriched history alone. Original historical generator remains as evidence.
