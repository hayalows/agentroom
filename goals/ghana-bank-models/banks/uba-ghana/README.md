# United Bank for Africa (Ghana) Ltd (owner: claude-helper-1)

Status: **needs-review (round 1)**. History (FY2021 to FY2025, 9M-2025 and 9M-2026) is transcribed from the bank's own published statements. The forecast (FY2026E to FY2030E, three scenarios) is an estimate. Bank-only statements. Everything is in GHS millions unless a percent is shown.

## Who it is
- Owned **90.77% by United Bank for Africa Plc (Nigeria)**; stated capital 400m; no Ghana Stock Exchange listing found (unknown: not checked against the GSE list). No subsidiaries seen (unknown: no subsidiaries note read).
- Auditor and approval dates are in the statements; two printed audit dates look mistyped (checks_history.md section 6).

## Size and shape
| | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 | 9M-2026 |
| --- | --- | --- | --- | --- | --- | --- |
| Total assets | 5,373 | 6,210 | 7,921 | 9,848 | 11,542 | 12,559 |
| Customer deposits | 4,075 | 4,736 | 6,338 | 7,285 | 8,590 | 8,685 |
| Net loans | 1,033 | 1,545 | 1,142 | 1,114 | 1,277 | 1,693 |
| Profit after tax | 141.8 | 59.6 | 175.8 | 164.3 | 407.1 | 197.8 (9M) |
| Total equity | 1,133 | 1,191 | 1,367 | 1,491 | 1,896 | 1,791 |
| CAR (reported) | 22.8% | 20.2% | 15.0% | 17.25% | 26.11% | 16.7% |
| Gross NPL (reported) | 29.4% | 15.8% | 24.7% | 12.5% | 2.11% | 1.57% |

- **A securities bank.** Securities are about 57% of assets and loans only 13%; the loan-to-deposit ratio is under 20%. Earnings follow Treasury yields more than lending.
- **Credit clean-up in FY2025.** Stage 3 loans fell from 165m to 28m; the allowance fell from 203m to 63m; a 119m reversal of expected credit losses lifted FY2025 profit to 407m. Do not read 407m as a run rate.
- **Capital moves with dividends.** 305m was paid in 9M-2026; the CAR fell from 26.1% (FY2025) to 16.7%.

## Forecast, base case (estimates)
| | FY2026E | FY2027E | FY2030E |
| --- | --- | --- | --- |
| Net interest income | 540 | 680 | 950 |
| Profit after tax | 256 | 301 | 381 |
| ROE | 13.7% | 15.5% | 14.7% |
| CAR proxy (calibrated) | 17.3% | 17.4% | 16.5% |

FY2030E profit after tax: base 381, downside 361, upside 358. **The scenarios are not ordered the way the labels suggest** (full table in checks.md section 3). The shared macro file gives the downside higher policy and bill rates, and this bank earns mostly on securities, so higher rates raise its income. This is a feature of the shared macro file and the bank's balance sheet, not a bank-specific view. FY2026E is identical in all scenarios because nine months are reported.

## Method in short
- FY2026E = 9M-2026 x 12/9 for income and cost lines, plus an implied Q4 (reported as `x_q4_implied_*` rows). 9M-2026 tax was 41.3%; Q4 is taxed at 35%.
- From FY2027E: loans earn the 364-day bill + 6 points; securities earn a blend of bill and bond yields plus a **fitted haircut of -1.43 points**; funding cost is a solved ratio to the policy rate. **Both fitted constants match 9M-2026 by construction and are not validated** (checks.md section 2).
- Statutory reserve uses the full Act 930 s34 tiers. Dividends are a payout of prior-year profit, capped by distributable earnings and by a 15% CAR proxy target.
- CAR figures are **proxies**, calibrated to the reported 16.7%; regulatory CAR, Tier 1 and NPL are `unavailable` in the forecast.
- Sensitivities (checks.md 2b): a 1 point change in the securities haircut moves FY2030E base profit by about 75m (20%); a 41% tax rate lowers it by about 39m.

## Limits and unknowns
- Statement PDFs had no printed page numbers in the text I could read; rows cite SoCI/SoFP and AR pages (sources.md). **A visual check of the key pages was requested** (HELP uba-visual-fy25).
- No repricing schedule, deposit beta or net FX position was available.
- Unexplained: 59% jump in staff costs, property and equipment from 122m to 320m between June and September 2026, borrowings doubling to 1,691m, and the 9M-2026 tax rate.
- Absa Ghana, which I could not source, is still blocked; this claim is unrelated to it.

## Files
`sources.md`, `financials.csv` (341 rows), `forecast.csv` (671 rows), `assumptions.json`, `build_financials.py`, `model.py`, `checks_history.md`, `checks.md`.
