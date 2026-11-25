# Checks: CalBank PLC (`calbank`)

All historical and forecast checks dynamically computed by `model.py` from `financials.csv`, `assumptions.json`, and `sector/macro-assumptions/macro.csv`.

## 1. Historical Checks (recomputed from `financials.csv`)
| Period | BS Residual | NII Residual | TOI Residual | PBT Residual | PAT Residual | Max Abs Residual |
| --- | --- | --- | --- | --- | --- | --- |
| FY2021 | 0.000 | 0.000 | 0.000 | -0.000 | 0.000 | 0.000 |
| FY2022 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| FY2023 | 0.000 | -0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| FY2024 | 0.000 | 0.000 | 0.000 | 0.000 | -0.000 | 0.000 |
| FY2025 | 0.000 | -0.000 | -0.000 | -0.000 | 0.000 | 0.000 |
| 9M-2026 | 0.000 | -0.000 | 0.000 | -0.000 | 0.000 | 0.000 |
- Missing `source_id`/`page` on `reported` rows: **0**
- Non-blank `value` on `unavailable` rows: **0**
- Duplicate `(period, statement, line_item)` keys: **0**

## 2. Forecast Checks (`FY2026E–FY2030E`, recomputed)
| Scenario | Year | Max Residual | Iter Conv Residual | Inv Sec >= 0 | Est. CAR Proxy (%) | Min CAR (%) | CAR >= Min | Est. PAT (GHS m) | Est. ROE (%) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| base | FY2026E | 0.000 | 0.000000 | PASS | 18.88% | 13.00% | PASS | 427.2 | 24.5% |
| base | FY2027E | 0.000 | 0.000000 | PASS | 19.94% | 13.00% | PASS | 372.0 | 17.4% |
| base | FY2028E | 0.000 | 0.000000 | PASS | 20.04% | 13.00% | PASS | 380.5 | 15.3% |
| base | FY2029E | 0.000 | 0.000000 | PASS | 19.93% | 13.00% | PASS | 382.5 | 13.7% |
| base | FY2030E | 0.000 | 0.000000 | PASS | 19.76% | 13.00% | PASS | 416.4 | 13.4% |
| downside | FY2026E | 0.000 | 0.000000 | PASS | 19.15% | 13.00% | PASS | 425.8 | 24.5% |
| downside | FY2027E | 0.000 | 0.000000 | PASS | 21.16% | 13.00% | PASS | 491.1 | 22.3% |
| downside | FY2028E | 0.000 | 0.000000 | PASS | 22.63% | 13.00% | PASS | 564.9 | 20.9% |
| downside | FY2029E | 0.000 | 0.000000 | PASS | 23.32% | 13.00% | PASS | 517.0 | 16.2% |
| downside | FY2030E | 0.000 | 0.000000 | PASS | 23.66% | 13.00% | PASS | 503.1 | 13.8% |
| upside | FY2026E | 0.000 | 0.000000 | PASS | 18.75% | 13.00% | PASS | 427.5 | 24.5% |
| upside | FY2027E | 0.000 | 0.000000 | PASS | 19.34% | 13.00% | PASS | 326.7 | 15.4% |
| upside | FY2028E | 0.000 | 0.000000 | PASS | 18.96% | 13.00% | PASS | 333.5 | 13.9% |
| upside | FY2029E | 0.000 | 0.000000 | PASS | 18.52% | 13.00% | PASS | 366.3 | 13.7% |
| upside | FY2030E | 0.000 | 0.000000 | PASS | 18.02% | 13.00% | PASS | 411.9 | 13.9% |

## 3. Spot-checks & Caveats
- `CAL25` p. 65 (Bank 2025): `total_assets` = `11,899,483` GHS '000 (`11899.483` GHS m).
- `CAL25` p. 142 (Bank 2025, Note 26): `loans_and_advances_gross` = `1,290,234` GHS '000; `loan_loss_allowance` = `219,354` GHS '000.
- `CAL26Q3` p. 1–2 (Bank Sep-26): `profit_after_tax` = `321,670` GHS '000 (`321.67` GHS m); `customer_deposits` = `10,633,698` GHS '000 (`10633.698` GHS m).
- **CRR proxy caveat:** `cash_and_bog_balances` includes `due_from_banks` in summary statements; `cash_bog >= 20% * customer_deposits` is a liquidity proxy screen, not regulatory BoG cedi CRR compliance.
- **CAR caveat:** Forecast `car_pct` is a proxy calibrated to `9M-2026` reported `18.4%` CAR (`total_equity / (total_assets * RWA_density)`), not a prudential Tier 1+Tier 2 calculation.

## 4. Cost-of-funds calibration
Formula across scenarios: `max(1.5%, 0.7% + 0.18 x tbill_91d_pct)`, where the slope is 0.18 percentage points per one percentage-point bill-rate move. Funding is customer deposits + due to banks + borrowings; 9M cost is annualized by 4/3. These are derived bank-wide rates, not reported product pricing.
| Period | 91-day bill (%) | Annualized interest expense (GHS m) | Average funding (GHS m) | Observed cost (%) | Model fit (%) | Fit error (pp) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| FY2025 | 15.38 | 370.268 | 10670.087 | 3.470 | 3.468 | -0.002 |
| 9M-2026 annualized | 6.23 | 202.175 | 11152.078 | 1.813 | 1.821 | +0.009 |
- FY2025 bill rate is the 12-month mean in `macro.csv`. The 9M-2026 bill rate is the Jan-Sep monthly mean (6.23%) from Bank of Ghana November 2026 Summary, p.3.
- FY2026E adds Q4 only. Q4 uses an implied 91-day bill mean of 4.55%, a day-weighted policy rate of 12.57%, and investment-yield proxies of 9.447% (364-day bill) and 15.01% (10-year bond). These are Q4 run-rate proxies, not observed quarter-average yields. The 5.81% 91-day, 11.01% 364-day and 14.05% bond inputs in `macro.csv` are full-year estimates, so they are not applied directly to Q4.
- Related interest-income fit: base FY2026E is 879.963m versus the 9M-2026 annualized run rate of 884.093m (-0.5%). The base loan-yield rule is Q4 policy rate + 1.0 percentage point; this aggregate fit is a calibration guide, not an observed loan yield.

## 5. Scenario PAT ordering
| Year | Downside PAT | Base PAT | Upside PAT | Highest to lowest |
| --- | ---: | ---: | ---: | --- |
| FY2026E | 425.8 | 427.2 | 427.5 | upside > base > downside |
| FY2027E | 491.1 | 372.0 | 326.7 | downside > base > upside |
| FY2028E | 564.9 | 380.5 | 333.5 | downside > base > upside |
| FY2029E | 517.0 | 382.5 | 366.3 | downside > base > upside |
| FY2030E | 503.1 | 416.4 | 411.9 | downside > base > upside |
- From FY2027E, the downside macro path produces the highest modeled PAT because higher policy, T-bill and bond rates lift modeled loan and securities income faster than higher impairment and operating costs reduce profit. The downside loan spread is +1.5 percentage points versus +1.0 base and +0.5 upside; investment yields use a 50/50 blend of 364-day bills and 10-year bonds, with no maturity or repricing schedule. This ordering is sensitive to those assumptions and does not mean downside conditions are generally better for CalBank.

## 6. Presentation and source reconciliations
- FY2024 Bank retained earnings stored from CAL25 SoFP p.65 are (1,209.108)m. The Directors table p.22 shows (946.562)m excluding reserve transfers; CAL25 SoCE p.67 reconciles this as opening (1,202.955) + PAT 256.393 - statutory reserve transfer 64.098 - credit-risk reserve transfer 198.448 = closing (1,209.108).
- CAL25 p.122 reports Bank CAR of 18.87% (FY2025) and (7.22%) (FY2024). Group CAR is 19.80% and (6.38%); the p.14 narrative refers to Group. Historical rows retain the Bank series.
- Right-of-use assets are recast from `other_assets` to `property_equipment_intangibles` per MODEL-SPEC; the reclass changes no period total. Source values and formulas are in `financials.csv` and `sources.md`.
- CAL26Q3 Statement of Changes in Equity (physical PDF p.3; no printed page numbers) does not report a 9M-2026 dividend movement or amount. FY2026E `x_dividends_paid` is 0.000 because no Q4 payout is assumed; later payouts occur only when the full payout leaves positive retained earnings and post-payout CAR meets target.
