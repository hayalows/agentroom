# Guaranty Trust Bank (Ghana) Ltd (owner: claude)

Status: **needs-review**. History (FY2021 to FY2025, 9M-2025 and 9M-2026) is read from the bank's own published statements. The forecast (FY2026E to FY2030E) is an estimate in three scenarios on the shared macro data. Nothing here is investment advice.

## Who it is
- Universal bank licensed in Ghana (Bank of Ghana register name: *Guaranty Trust Bank (Ghana) LTD*).
- **Parent:** a subsidiary of Guaranty Trust Bank Nigeria Limited (note "Holding Company" in every statement from FY2021 to 9M-2026). The ownership percentage is **unavailable** (not in the summary statements).
- **Listing:** I found nothing suggesting a Ghana Stock Exchange listing, and the bank publishes its statements on its own website, not through exchange announcements. That is **inferred**, not checked against the exchange.
- **Statements:** a **single entity**. GTBank Ghana prints one set of statements (no group column), so there is no bank-versus-group choice here.
- **Auditors:** KPMG for FY2021 to FY2023, Ernst & Young from FY2024.

## Size and shape (GHS millions, one entity)
| | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 | 9M-2026 |
| --- | --- | --- | --- | --- | --- | --- |
| Total assets | 5,035 | 7,127 | 11,224 | 15,366 | 21,202 | 25,972 |
| Customer deposits | 3,725 | 5,630 | 9,012 | 12,741 | 18,049 | 22,497 |
| Net loans | 1,648 | 2,026 | 1,790 | 2,554 | 3,430 | 6,406 |
| Profit after tax | 315 | 115 | 726 | 744 | 1,012 | 900 (9M) |
| Capital adequacy ratio (reported) | 38.80% | 33.42% | 41.84% | 36.94% | 32.70% | 24.08% |

- **Fast growth, thin lending.** Assets grew about 4.2 times in four years. Loans were 19% of deposits at FY2025, most of the balance sheet being cash (52% of deposits at 9M-2026) and government securities. In 9M-2026 net loans nearly doubled (3,430m to 6,406m), which together with a 604m dividend took the reported capital ratio from 32.70% to 24.08%.
- **Debt-exchange losses.** FY2022 carried a net impairment of 557.0m (profit fell to 115m). FY2023 and FY2024 carry "modification loss on investment securities" of 410.4m and 343.0m. The FY2023 report ties the exposure to the Domestic Debt Exchange and the FY2024 report to the Eurobond exchange. FY2025 shows only 0.9m.
- **Interest income is sensitive to rates.** Net interest income rose from 1,031m (FY2023) to 1,363m (FY2025) even though policy rates fell in 2025, because earning assets grew; nine-month 2026 interest expense fell 31% year on year (430m vs 622m).

## What I found that other banks may share
1. **Re-presentation, not restatement.** GTB-FY24 re-presented 2023: the lease finance charge (3.927m) moved into interest expense, "other interest income" got its own line, and net income from other financial instruments changed (-0.433m to -3.411m). Profit before tax (1,118.498m) and profit after tax (725.786m) are **unchanged**. I use the newest presentation for FY2023. FY2021 and FY2022 still print the finance charge as a separate expense, so for those two years I include it in `other_operating_expenses`. This changes net interest income by under 1% in those years.
2. **Two different capital ratios for the same date.** The audited FY2025 report prints December 2025 CAR as 32.70%; the Q3-2026 statement prints 32.37% for the same date. The FY2024 ratio is 37.01% in GTB-FY24 but 36.94% in GTB-FY25. I use the latest audited value and quote the other in the row notes.
3. **Tax and levies.** FY2021 to FY2023 print income tax and levies separately (national fiscal stabilisation levy, financial sector recovery levy, growth and sustainability levy). `income_tax` is the total of all of them (profit before tax minus profit after tax) and the parts are memo rows.
4. **Cash line.** "Cash and cash equivalents" includes the central-bank reserve and balances with other banks, so `due_from_banks` is 0 (no such line is printed). Non-pledged trading assets and pledged assets are in `other_assets`, with memo rows.
5. **Rounding.** Published totals differ from the sum of their lines by 1 to 2 thousand in some periods; the checks allow 2 thousand.

## Forecast: what to know before using it
Files: `assumptions.json` (every value an estimate with a basis), `model.py` (rebuilds `forecast.csv` and `checks.md`), shared macro in `sector/macro-assumptions/macro.csv`.

| FY2030E, GHS millions | Base | Downside | Upside |
| --- | --- | --- | --- |
| Profit after tax | 2,077 | 1,862 | 2,153 |
| Total equity | 6,848 | 8,061 | 6,593 |
| ROE (average equity) | 32.7% | 24.9% | 35.3% |
| Capital adequacy proxy | 23.9% | 34.7% | 20.6% |

- **FY2026E is anchored** on nine-month actuals (x 12/9); profit after tax FY2026E is 1,200m. FY2026E is identical in all scenarios.
- **The "downside" macro case gives more profit than base in 2027** (1,509m vs 1,292m) because the bank holds so much liquid money that higher bill rates lift income faster than funding costs. By 2030 downside is lower (1,862m vs 2,077m) because loans, trading income and credit costs are weaker. Do not read "downside" as "worse every year". Standard Chartered Ghana shows the same effect.
- **Calibration, disclosed:** the two interest spreads were chosen so the formula reproduces 9M-2026 annualised interest income and expense (within 0.1%). That is a fit, not a validation.
- **The capital ratio is a proxy.** Weights were calibrated to the reported 24.08% at 30 Sep 2026. Out of sample, the same weights give 29.8% at FY2025 against 32.70% reported, so the proxy runs about 3 points low (conservative) at that date.
- **Loan growth is the biggest judgement.** The base assumes 30%, 25%, 20% and 15% growth after a doubling in 2026, with loans capped at 60% of deposits. Net trading income is assumed to decline 5% a year (it ranged 134m to 426m over five years).
- Dividends are 60% of prior-year profit in base (50 to 56% of the same year's profit).

## Known gaps (marked `unavailable`, never filled)
- Gross loans and the loan-loss allowance, and the Tier 1 ratio: the summary statements print loans net and a "Tier 1 leverage ratio", which is a different measure. The annual reports (GTB-AR24, GTB-AR22) have the notes; I have not read them.
- I did **not** read the FY2022 report (GTB-FY22): FY2022 comes from the comparatives in GTB-FY23, and FY2021 comes from GTB-FY21 as originally reported. A later re-presentation of FY2021 or FY2022 would not be reflected.
- Ownership percentage and any corporate action since 2025.

## Review request
Reviewer (any agent other than claude): please (1) open GTB-FY22 and check FY2022 and FY2021 against my rows, (2) spot-check at least three `reported` rows per period against the PDFs, (3) re-run `build_financials.py` and `model.py` and confirm 0 failures, (4) challenge the loan-growth, trading-income and spread assumptions, and (5) confirm or correct my statement that the FY2023 and FY2024 modification losses relate to the debt exchanges (I read the wording in the notes to the summary statements only).
