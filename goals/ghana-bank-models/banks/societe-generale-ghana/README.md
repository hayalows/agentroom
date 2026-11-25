# Societe Generale Ghana PLC: standalone bank model

As of 25 November 2026. Fiscal year December 31; GHS millions unless noted. Societe Generale Ghana PLC (SGGH) is a universal bank listed on the Ghana Stock Exchange and regulated by the Bank of Ghana. It is a subsidiary of the Societe Generale Group (France) through its wholly owned holding SG Financial Services Holding, which holds 60.22% of the shares; the Social Security and National Insurance Trust holds 19.36% (SG25AR p.136). Sources: SG21AR-SG25AR, SG25FIN, SG26Q3, GSELIST, BOGREG in `sources.md`. This models the **Bank** (separate) statements only, never the Group.

## Actual results and scenario outlook

FY2025 bank-only total assets were GHS9,676.100m, customer deposits 5,843.183m, net loans 4,491.827m and profit after tax 397.001m (SG25AR pp.65-66). Reported CAR was 23.39% on the audited capital-adequacy basis and gross NPL 13.06% (SG25AR p.133, p.95). In 9M-2026, total assets were 11,078.375m, net loans 4,674.926m, PAT 150.003m, CAR 18.52% and NPL 13.98% (SG26Q3).

| Estimated scenario | 2026E PAT | 2030E PAT | 2030E assets | 2030E CAR proxy |
|---|---:|---:|---:|---:|
| Base | 192.956 | 430.171 | 18,524.687 | 18.07% |
| Downside | 38.552 | -343.615 | 14,437.864 | 10.65% |
| Upside | 232.442 | 829.102 | 23,581.244 | 19.13% |

Forecast assumptions are sensitivities, not management guidance. FY2026 is built from the actual 9M-2026 income statement plus an estimated Q4, and starts from the September 2026 balance sheet. Loan and deposit growth reflect the shared nominal GDP proxy plus a bank-specific spread; loan, securities and cash yields and the funding cost respond to shared rates. The downside path pushes the CAR proxy below the 13% shared minimum in FY2030E (a flagged shortfall of about GHS284m, not an assumed capital raise), while the base path holds a comfortable buffer.

Two disclosure points a reader should note. First, the downside is a **combined** cost-and-credit stress: the shared macro downside has higher inflation, and opex growth is CPI-plus-8pts, so a large part of the downside FY2030E loss is mechanical cost pass-through rather than credit losses. `checks.md` splits the two and, to isolate the growth-rate effect, recomputes downside FY2030E with **base** cost growth as a one-year marginal diagnostic (the FY2029 opening costs already embed cumulative downside opex, so it is not a full five-year base-cost path). Second, the scenario `cost_of_risk` is an input; the allowance-build floor lifts the **effective** charge above it in high-growth scenarios, so the upside's 0.80% input becomes a 2.04% effective rate in FY2030E. `checks.md` reports the effective rate next to the input for every scenario-year, and `forecast.csv` carries it as `x_effective_cost_of_risk_pct`. NPL is a scenario input held flat across all years (12% base, 16% downside, 11% upside), independent of the modelled cost of risk.

The model's anchor-year tax treatment: FY2026E retains the actual 9M-2026 tax charge and adds tax only on positive estimated Q4 profit; no deferred-tax credit is recognised for a Q4 loss, so a loss-making downside Q4 shows an effective rate above the 35% input. The observed 9M-2026 equity already reflects the FY2025 final dividend of GHS173.669m paid in 2026 (SG26Q3) — the unexplained 9M equity fall against 9M profit is that dividend — so no further Q4-2026 dividend is assumed, and `x_model_dividends` is zero in FY2026E for every scenario. The statutory reserve transfer is modelled explicitly (12.5% of positive PAT, source-confirmed FY2024 68.912m / FY2025 49.625m / 9M-2026 18.750m); it is an internal equity transfer, so total equity and regulatory capital are unaffected, but it caps distributable retained earnings for dividends. Reported capital ratios are CET1 (`x_cet1_pct`), not total Tier 1; no separate Tier 1 ratio is disclosed, so canonical `tier1_pct` is left unavailable.

## The 2022-2023 Domestic Debt Exchange

SG participated in the DDEP; its reviews describe limited impact on the Bank's profitability and an indirect third-party risk (SG22AR p.18, SG23AR p.23, SG24AR p.106). The accounting effect flows through the reported impairment charge and the capital notes rather than a separate DDEP line, so no sovereign haircut is invented in the forecast. Because the audited CAR note and the narrative quote different bases (audited 23.39% for FY2025 versus a narrative 17.5% excluding DDEP reliefs), the model uses the audited series and records the alternative; a reviewer should confirm the preferred basis.

## Reproduction and limitations

Run `python model.py` in this directory (Python 3, standard library only). It reads `financials.csv`, `assumptions.json` and the shared `../../sector/macro-assumptions/macro.csv`, and writes `forecast.csv` and `checks.md`. The historical numbers come from `build_financials.py` (re-runnable). 354 historical rows (FY2021-FY2025, 9M-2025 and 9M-2026); 915 forecast rows (15 scenario-years). All historical balance, income and net-loan bridges pass, and all 15 forecast accounting bridges pass.

Known gaps: 9M-2026 gross loans and allowance are not disclosed (estimated from FY2025 ratios, flagged); the Bank does not report a separate asset-side `due_from_banks` or a net FX position in the summary statements, so FX translation is not modelled; the historic reserve-notice timeline is owned by the shared macro work; the preferred CAR basis for peer comparison is open. Full prudential risk weights, OCI and liquidity eligibility are not available, so the capital and reserve checks are screening proxies. Independent review pending. Not investment advice.
