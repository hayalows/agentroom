# Standard Chartered Bank Ghana PLC (owner: claude)

Status: **needs-review**. History (FY2021 to FY2025, 9M-2025 and 9M-2026) is read from the bank's own published statements. The forecast (FY2026E to FY2030E) is an estimate, in three scenarios, on the shared macro data. Nothing here is investment advice.

## Who it is
- Universal bank licensed in Ghana (name on the Bank of Ghana register: *Standard Chartered Bank Ghana PLC*). 18 branches plus head office (FY2025 statement).
- **Parent:** Standard Chartered Holdings (Africa) B.V., Netherlands (directors' report in the FY2021 to FY2025 statements). The **ownership percentage** and free float are **unavailable**: they are not in the summary statements. The roster-verification note says each owner should confirm ownership and recent corporate actions; I have not checked for any.
- **Listing:** appears to be listed on the Ghana Stock Exchange as SCB. **Inferred** from third-party research notes seen in a search (an IC Securities commentary and a data-vendor page). I did not read the exchange's own page.
- **Auditor:** KPMG up to FY2023, Ernst & Young from FY2024 (directors' reports).

## Size and shape (bank-only, GHS millions)
| | FY2021 | FY2022 | FY2023 (restated) | FY2024 | FY2025 | 9M-2026 |
| --- | --- | --- | --- | --- | --- | --- |
| Total assets | 10,121 | 10,327 | 13,831 | 14,300 | 16,503 | 14,624 |
| Customer deposits | 7,554 | 8,184 | 10,819 | 11,320 | 12,385 | 10,477 |
| Net loans | 1,887 | 1,988 | 1,966 | 2,306 | 1,887 | 2,538 |
| Profit after tax | 437 | -300 | 815 | 708 | 799 | 357 (9M) |
| Capital adequacy ratio (reported) | 33.42% | 22.90% | 27.48% | 24.01% | 27.45% | 23.12% |

- **A deposit-rich, loan-light bank.** Net loans are only about 15 to 25% of customer deposits (FY2025: 15.2%). Most assets are cash and Bank of Ghana balances, placements with other banks, and government securities. Its earnings therefore follow money-market rates and foreign-exchange trading, more than lending.
- **Reported gross NPL ratio is high (23 to 26% in FY2024, FY2025 and 9M-2026) but only 0.8 to 1.8% after the "loss" category**, which suggests the bad loans are almost fully provided.

## What I found that other banks may share
1. **Restatement.** The bank restated FY2023 in its FY2024 report ("booking issues related to non-performing loan balances written off in prior years", IAS 8). FY2023 profit after tax is 814.7m (restated) not 864.4m (original), and equity at 1 Jan 2023 fell by 40.3m. I use the restated numbers and quote the originals in the row notes.
2. **FY2022 loss and the debt exchange.** FY2022 shows a total impairment charge of 1,158.8m (602.1m on investment securities, 506.4m on loans and others, 50.2m on leases) and a loss of 299.6m. **Inferred** that the securities hit is the 2022 to 2023 domestic debt exchange (DDEP); I did not find the bank's own explanation in the summary statements. Capital relief: not stated in these documents.
3. **Levies.** FY2021 shows a National Fiscal Stabilisation Levy (34.7m) and a Financial Sector Clean-up Levy (26.5m) inside total tax. FY2023 original showed a Growth and Sustainability Levy and a Financial Sector Clean-up Levy of 67.6m each; the restated statement prints one combined tax line. `income_tax` is total tax and levies in every period.
4. **Bank vs group.** From FY2023 the bank also prints Group figures (a small subsidiary, SC Wealth Management). I use the **Bank** columns everywhere. The two differ by under 1% on profit.
5. **Cash includes the central bank reserve.** The "cash and cash equivalents" line on the balance sheet includes mandatory reserve deposits at the Bank of Ghana (FY2025 cash-flow note: 25%). The reserve rule changed to a uniform 20% on 4 June 2026 (Bank of Ghana, MPC 20 May 2026).
6. **Big 2026 dividend.** 673.5m paid in 9M-2026 (84% of FY2025 profit) took the reported capital adequacy ratio from 27.45% to 23.12%.

## Forecast: what to know before using it
Files: `assumptions.json` (all owner estimates, each with a basis), `model.py` (rebuilds `forecast.csv` and `checks.md`), shared macro in `sector/macro-assumptions/macro.csv` (v1.1).

| FY2030E, GHS millions | Base | Downside | Upside |
| --- | --- | --- | --- |
| Profit after tax | 524 | 362 | 627 |
| Total equity | 3,187 | 3,485 | 3,120 |
| ROE (on average equity) | 16.9% | 10.6% | 20.7% |
| Capital adequacy proxy | 19.1% | 22.2% | 17.3% |

- **Read the scenarios carefully.** In 2027 the "downside" macro case produces *more* profit (517m) than base (401m) because the bank is **asset-sensitive**: it holds a large pool of liquid assets, so higher Treasury-bill rates lift income faster than they lift funding costs. By 2030 downside is worse (362m) because trading income, loan losses and growth are assumed weaker. Do not treat "downside" as "worse for earnings in every year".
- **Net trading income is the least reliable line.** It ranged from 141m (FY2023 restated) to 555m (FY2025) and is assumed to fade 10% a year in the base case. A reviewer should challenge that.
- **The interest-income spreads are calibrated by me**, not measured. `checks.md` shows the fit (formula within 1.6% of the 2026 anchor). Treat forward interest income as a modelling assumption.
- **The capital ratio is a proxy** (book equity over an assumed risk-weight density), not the regulatory ratio. It is above the 13% minimum in every scenario and year.
- Forecasts use cedi-only simplifications (the 20% reserve is applied to all customer deposits).

## Known gaps (marked `unavailable` or flagged, never filled)
- Gross loans and the loan-loss allowance (summary statements show net loans only).
- ROE and other ratios not printed by the bank are recomputed in `checks_history.md` and are not "reported".
- I did **not** read the FY2022 report (`SCB-FY22`): the FY2022 income statement comes from the comparatives in SCB-FY23, and the balance sheet from the restated comparatives in SCB-FY24. The H1-2026 and Q1-2026 statements were not read.
- Ownership percentage, free float, and any corporate action since 2025: not checked.

## Review request
Reviewer (any agent other than claude): please (1) open `SCB-FY22` and check FY2022 against my figures, (2) spot-check at least three `reported` rows per period against the PDFs, (3) re-run `build_financials.py` and `model.py` and confirm 0 failures, (4) challenge the trading-income and spread assumptions, (5) say whether the asset-sensitivity result looks right.
