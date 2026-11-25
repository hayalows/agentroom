# Absa Bank Ghana PLC: source register (owner: claude-helper-1)

Bank-only statements. Values in `financials.csv` are GHS millions (the issuer prints thousands). Costs positive; no reversal in this history except none observed.

## IMPORTANT: how this history was obtained (read first)
- **The owner could not open the Absa PDFs.** Absa's site refuses automated access to the owner's tools (shell proxy 403; fetch tool blocked by robots rules). The owner did not bypass this.
- The 300 history rows are the **independent transcription by agent `codex`** at `assistance/remaining-banks/absa-primary-source-pack-codex.csv` (with `.md` register), reporting visual checks of the official annual face pages and a text extraction of the Q3 2026 statement. `build_financials.py` copies those rows unchanged and re-runs the statement identities (0 failures, `checks_history.md`).
- **Therefore no row was re-read from the issuer's page by the owner.** Evidence of correctness is (a) codex's page visuals, (b) every statement identity and the 9M-2026 equity roll-forward tie, (c) FY2024 values agree between the FY2025 comparative column and the FY2024 trend. A reviewer should spot-check against the PDFs.

## Sources (official issuer PDFs, per codex's register)
| source_id | URL | pages used |
| --- | --- | --- |
| ABSA21 | https://www.absa.com.gh/content/dam/ghana/absa/pdf/annual-reports/annual-financial-statement-2021.pdf | printed 31-32 |
| ABSA22 | https://www.absa.com.gh/content/dam/ghana/absa/pdf/annual-reports/annual-financial-statement-2022.pdf | printed 31-32 |
| ABSA23 | https://www.absa.com.gh/content/dam/ghana/absa/pdf/annual-reports/financial-statement-2023.pdf | printed 36-37 |
| ABSA25 | https://www.absa.com.gh/content/dam/ghana/absa/pdf/annual-reports/financial-statement-2025.pdf | printed 59-60 (FY2025 and the FY2024 comparative) |
| ABSA26Q3 | https://www.absa.com.gh/content/dam/ghana/absa/pdf/annual-reports/q3-2026-for-period-ended-30-september.pdf | physical 1-2 (9M-2026 and the 9M-2025 comparative; text extraction only) |

Report index: https://www.absa.com.gh/reports/. The FY2024 integrated report is too large to open; FY2024 comes from the FY2025 comparative column.

## What is not available (and so not forecast)
- Annual CAR, gross loans, loan-loss allowance, risk-weighted assets, lease/PPE note and annual dividends are **not in the pack** (rows are `unavailable`, never zero). CAR (19.06%), NPL (11.32%), liquidity ratio and leverage ratio exist only for 9M-2025 and 9M-2026.
- Owner: 100% Absa Group Ltd per the FY2023 directors' report p.4 (codex's note); not confirmed against the current share register.

## Observations that shape the model (from the pack's notes, not re-read)
1. **FY2022 loss.** Impairment of 2,126.9m (domestic debt exchange) turned a pre-impairment profit into a loss of 429.2m. Not a run rate.
2. **9M-2026 dividend of 1,115m** (63% of FY2025 profit) is inside the 30 Sep 2026 equity; statutory reserve transfer 123.2m = 12.5% of 9M profit; credit-risk reserve transfer 68.2m.
3. **Interim equity roll.** FY2025 equity 5,973.1 + 985.3 PAT + 27.9 OCI + 3.9 other - 1,115 dividends = 5,875.2m (exact).
4. **Mapping choices.** `other_assets` contains trading assets (pledged 1,470.6m and unpledged 2,166.7m at Sep 2026), derivatives and tax assets; `other_liabilities` contains derivative liabilities and employee obligations; FY2023 `due_from_banks` is 0.000 as reported by the pack (possibly merged into cash; unknown).
5. **Regulatory events.** A Q3 2026 note mentions a sanction of 0.36m and a post-balance-sheet penalty of 16.1m (pack note); not modelled.
