# Stanbic Bank Ghana Ltd: standalone bank model

As of 25 November 2026. Fiscal year December 31; GHS millions unless noted. Stanbic Bank Ghana Ltd is a universal bank regulated by the Bank of Ghana and a member of the Standard Bank Group (South Africa). Sources: SB22AR-SB25AR, SB22SUM-SB25SUM, SB26Q3 in `sources.md`. This models the **Bank** (separate) statements only, never Standard Bank Group.

## Actual results and scenario outlook

FY2025 bank-only total assets were GHS36,708.145m, customer deposits 24,013.184m, net loans 7,652.776m and profit after tax 1,608.667m (SB25AR pp.46-47). Reported CAR was 23.2% and gross NPL 24.63% (SB25SUM). In 9M-2026, total assets were 43,243.634m, net loans 9,027.632m, PAT 903.785m, CAR 23.32% and NPL 9.54% (SB26Q3).

| Estimated scenario | 2026E PAT | 2030E PAT | 2030E assets | 2030E CAR proxy |
|---|---:|---:|---:|---:|
| Base | 1,170.626 | 2,620.721 | 76,730.450 | 28.36% |
| Downside | 213.209 | 906.625 | 64,207.212 | 30.32% |
| Upside | 1,311.620 | 3,676.524 | 92,529.951 | 24.39% |

Forecast assumptions are sensitivities, not management guidance. FY2026 is built from the actual 9M-2026 income statement plus an estimated Q4, and starts from the September 2026 balance sheet. Loan and deposit growth reflect the shared nominal GDP proxy plus a bank-specific spread; loan, securities and cash yields and the funding cost respond to shared rates. The credit-risk shock is largest early in the downside, which is why the downside CAR recovers to a high level later (retained earnings accumulate while low loan growth holds RWA down) — a mechanical feature flagged in `checks.md`, not a claim that the downside is benign.

## The 2022-2023 Domestic Debt Exchange

Stanbic signed onto the DDEP on 14 February 2023 and its government-bond maturities were extended to 2027-2038 (SB23AR note 4, printed p.81). The accounting effect flows through the large FY2022 credit impairment charge (GHS965.937m) and the investment-securities ECL stages rather than a separate sovereign line, so no haircut is invented in the forecast. The FY2022 loss (PAT -62.595m) is the DDE-year trough in the series.

## Indirect tax and reporting convention

Stanbic's income statement separates an **Indirect tax** line from the direct income tax. `financials.csv` stores `profit_before_tax` on the reported "Profit before indirect tax" basis and `income_tax` as the **sum** of the indirect and direct tax, so `profit_after_tax = profit_before_tax - income_tax` holds; the split is preserved in `x_indirect_tax` / `x_direct_tax`.

## Reproduction and limitations

Run `python model.py` in this directory (Python 3, standard library only). It reads `financials.csv`, `assumptions.json` and the shared `../../sector/macro-assumptions/macro.csv`, and writes `forecast.csv` and `checks.md`. Historical numbers come from `build_financials.py`; `checks_history.py` recomputes the historical bridges. 296 historical rows; 870 forecast rows (15 scenario-years). All historical balance, income, tax-split and net-loan bridges pass, and all 15 forecast accounting bridges pass.

Known gaps: 9M-2026 gross loans and allowance are not disclosed (estimated from FY2025 ratios, flagged); FY2021 has no standalone report locally (its comparatives come from the FY2022 report and are cross-checked against the FY2022 summary and the codex/chatgpt-support assistance file); FY2022 interest in suspense is unresolved; the Bank does not report a net FX position in the summary statements, so FX translation is not modelled. Full prudential risk weights, OCI and liquidity eligibility are not available, so the capital and reserve checks are screening proxies. Independent review pending. Not investment advice.
