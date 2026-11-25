# Zenith Bank (Ghana) Ltd (owner: claude-helper-1)

Status: **needs-review**. History (FY2021 to FY2025, 9M-2025 and 9M-2026) is read from the bank's own published statements. The forecast (FY2026E to FY2030E) is an estimate in three scenarios on the shared macro data (macro.csv v1.1). Nothing here is investment advice.

## Who it is
- Private limited company, **99.42% owned by Zenith Bank PLC (Nigeria)**. **Not listed** on the Ghana Stock Exchange (sources.md, from the audited directors' report).
- **No subsidiaries**, so the statements are bank-only and no group/bank mix is possible.
- Auditor: PwC (FY2025 report dated 25 March 2026).

## Size and shape (bank-only, GHS millions)
| | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 | 9M-2026 |
| --- | --- | --- | --- | --- | --- | --- |
| Total assets | 8,864 | 9,660 | 13,863 | 19,127 | 26,703 | 31,992 |
| Customer deposits | 6,391 | 8,408 | 11,703 | 15,630 | 20,826 | 25,953 |
| Net loans | 1,499 | 1,856 | 2,247 | 3,414 | 7,210 | 9,455 |
| Profit after tax | 220 | -420 | 676 | 452 | 998 | 1,058 (9M) |
| Total equity | 1,554 | 982 | 1,658 | 2,052 | 3,050 | 4,108 |
| Capital adequacy ratio (reported) | 45.09% | 36% | 29% | 24.14% | 20.40% | 17.79% |
| NPL ratio (reported) | 4.40% | 3.80% | "1%" | "1%" | 8.49% | 8.91% |

- **Fast growth from a small base.** Assets and deposits have tripled since FY2021 and net loans grew sevenfold, from a loan-to-deposit ratio of 19% (FY2023) to 36% (Sep 2026). Most assets are still cash and Bank of Ghana balances and government securities.
- **Capital is being consumed by growth.** The reported CAR fell from 45% to 17.8% as loans and risk-weighted assets grew, against a 13% minimum. No dividend has been paid since 2022.
- **Asset quality is the main risk.** Stage 3 loans rose from 58m (FY2024) to 630m (FY2025), an NPL ratio of 8.49%, and the stage 3 allowance covers only 13.5% of them (85m).

## What I found that other banks may share
1. **Transcription tools can swap columns.** The fetch tool I use labelled the current column of both interim reports as the comparative. Proof and fix: opening equity + nine-month profit = closing equity (exact) in `checks_history.md` section 7. Anyone reading interim statements through a tool should run that roll-forward.
2. **FY2022 domestic debt exchange.** Impairment of 1,157.5m on investment securities (Note 11) turned a pre-impairment profit into a loss of 419.8m, with a tax credit of 134.8m.
3. **Interim tax is not the full-year rate.** 9M-2026 tax was 17.8% of profit before tax, but in Q4-2025 the bank booked 64% of that quarter's profit as tax, ending FY2025 at 34.6% (25% tax + 5% Growth and Sustainability Levy + 5% Financial Sector Recovery Levy). FY2024 was 57.4% because of a 229m prior-year estimate change. Do not annualise interim tax.
4. **Statutory reserve transfer is 25% (not 12.5%) until the reserve equals stated capital.** Observed exactly: FY2023 12.5%, FY2024 and FY2025 25.0%.
5. **"Investments (other than securities)" is not securities.** I mapped it to `due_from_banks` because Note 11 reports interbank placements impairment on it; the note text itself was not read (inferred).
6. **Printed NPL ratios are rounded in places.** FY2023 and FY2024 print "1%"; stage 3 / gross is 0.65% and 1.68%. Both are stored (`npl_pct` as printed, `x_npl_stage3_to_gross_pct` derived).

## How the data is stored
- `financials.csv`: 337 rows, built by `build_financials.py` with the figures embedded. 267 reported, 63 derived (each with its formula), 7 unavailable. Costs positive; the FY2022 loss and tax credit and the 9M-2026 impairment reversal are signed as noted in the row.
- `x_` rows hold extra detail: loan stages, securities gross and impairment, Note 11 impairment components, risk-weighted assets, interim ratios, equity roll-forward movements.
- Not available: gross loans and allowance in the interim statements; interest in suspense (the bank discloses only interest not recognised on impaired loans for FY2021 and FY2022).

## Forecast: what to know before using it
Files: `assumptions.json` (every value an estimate with a basis; differences from SCB marked), `model.py` (rebuilds `forecast.csv` and `checks.md`), shared macro in `sector/macro-assumptions/macro.csv`.

| FY2030E, GHS millions | Base | Downside | Upside |
| --- | --- | --- | --- |
| Net loans | 19,567 | 12,626 | 22,999 |
| Profit after tax | 2,138 | 1,747 | 2,298 |
| Total equity | 9,514 | 10,281 | 8,913 |
| ROE (average equity) | 24.8% | 18.6% | 28.4% |
| Capital adequacy proxy (Sep-26 density) | 20.6% | 26.5% | 16.5% |
| Capital adequacy proxy (FY25 density) | 28.2% | 36.4% | 22.6% |

Read these with the following in mind:
- **FY2026E is the same in all scenarios** (three quarters are reported): base profit after tax 1,094m, of which only 36m falls in Q4 because the full-year tax rate is 34% and a Q4 loan charge is added. At a 28% tax rate it would be 1,194m (checks.md 3b).
- **The scenario ordering is inverted in FY2027E and FY2028E** (downside profit above base) because the shared downside has higher interest rates and the bank's liquid assets reprice with bills. This is the same formula as in SCB. Please challenge it.
- **The downside has the highest equity by FY2030E** because it pays no dividends and has higher interest income. Profit is lower, equity is not.
- **Interest yields on liquid assets are fitted** (2.7 points over the 91-day bill) to reproduce 9M-2026; the loan spread (6.0) is borrowed from SCB's basis. The 14.3% average 2026 policy rate used for the cost-of-funds ratio is also taken from SCB and was not re-verified.
- **The capital adequacy figures are proxies**, shown with two risk-weight densities that bracket the truth. They are not regulatory ratios.

## Review request
Please review independently (a distinct registered participant; I may not review my own work). Suggested checks, in order of value:
1. **Open the PDFs and look.** I read every figure through a transcription tool and never saw a page image. Please confirm against the actual pages, at least: FY2025 income statement p.38 and balance sheet p.39 (ZEN-FY25), and 30 Sep 2026 balance sheet and income statement and regulatory table in ZEN-Q3-26 (no page numbers). The FY2022 balance sheet has only one source (comparative in ZEN-FY23).
2. Check the interim column orientation (`checks_history.md` section 7).
3. Challenge the Q4-2026 tax and impairment treatment, the loan growth and deposit adjustment, the 20% base payout and the inverted scenario ordering.
4. Replay: `python3 build_financials.py` then `python3 model.py`; both are standard-library only and rewrite the CSVs and checks.

## Limits (observed vs unknown)
- The bank-only interim balance sheets omit right-of-use and lease lines; they sit inside other lines (so `property_equipment_intangibles` and `other_liabilities` are not strictly comparable between annual and interim periods).
- Other assets nearly doubled in 9M-2026 (1,768m to 3,455m); I did not investigate why.
- No independent review has been done yet. The spot checks in checks.md section 6 were done by the author.
