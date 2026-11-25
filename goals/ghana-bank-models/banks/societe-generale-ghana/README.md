# Societe Generale Ghana PLC: standalone bank model

As of 25 November 2026. Fiscal year December 31; GHS millions unless noted. Societe Generale Ghana PLC (SGGH) is a universal bank listed on the Ghana Stock Exchange and regulated by the Bank of Ghana. It is a subsidiary of the Societe Generale Group (France) through its wholly owned holding SG Financial Services Holding, which holds 60.22% of the shares; the Social Security and National Insurance Trust holds 19.36% (SG25AR p.136). Sources: SG21AR-SG25AR, SG25FIN, SG26Q3, GSELIST, BOGREG in `sources.md`. This models the **Bank** (separate) statements only, never the Group.

## Actual results and scenario outlook

FY2025 bank-only total assets were GHS9,676.100m, customer deposits 5,843.183m, net loans 4,491.827m and profit after tax 397.001m (SG25AR pp.65-66). Reported CAR was 23.39% on the audited capital-adequacy basis and gross NPL 13.06% (SG25AR p.133, p.95). In 9M-2026, total assets were 11,078.375m, net loans 4,674.926m, PAT 150.003m, CAR 18.52% and NPL 13.98% (SG26Q3).

| Estimated scenario | 2026E PAT | 2030E PAT | 2030E assets | 2030E CAR proxy |
|---|---:|---:|---:|---:|
| Base | 192.956 | 430.064 | 18,524.669 | 18.07% |
| Downside | 38.552 | -342.626 | 14,439.914 | 10.67% |
| Upside | 232.442 | 828.624 | 23,581.178 | 19.13% |

Forecast assumptions are sensitivities, not management guidance. FY2026 is built from the actual 9M-2026 income statement plus an estimated Q4, and starts from the September 2026 balance sheet. Loan and deposit growth reflect the shared nominal GDP proxy plus a bank-specific spread; loan, securities and cash yields and the funding cost respond to shared rates. The downside path pushes the CAR proxy below the 13% shared minimum in FY2030E (a flagged shortfall of about GHS284m, not an assumed capital raise), while the base path holds a comfortable buffer. The wide long-run range shows the model's sensitivity to credit risk, growth and funding.

## The 2022-2023 Domestic Debt Exchange

SG participated in the DDEP; its reviews describe limited impact on the Bank's profitability and an indirect third-party risk (SG22AR p.18, SG23AR p.23, SG24AR p.106). The accounting effect flows through the reported impairment charge and the capital notes rather than a separate DDEP line, so no sovereign haircut is invented in the forecast. Because the audited CAR note and the narrative quote different bases (audited 23.39% for FY2025 versus a narrative 17.5% excluding DDEP reliefs), the model uses the audited series and records the alternative; a reviewer should confirm the preferred basis.

## Reproduction and limitations

Run `python model.py` in this directory (Python 3, standard library only). It reads `financials.csv`, `assumptions.json` and the shared `../../sector/macro-assumptions/macro.csv`, and writes `forecast.csv` and `checks.md`. The historical numbers come from `build_financials.py` (re-runnable). 294 historical rows; 856 forecast rows (15 scenario-years). All historical balance, income and net-loan bridges pass, and all 15 forecast accounting bridges pass.

Known gaps: 9M-2026 gross loans and allowance are not disclosed (estimated from FY2025 ratios, flagged); the Bank does not report a separate asset-side `due_from_banks` or a net FX position in the summary statements, so FX translation is not modelled; the historic reserve-notice timeline is owned by the shared macro work; the preferred CAR basis for peer comparison is open. Full prudential risk weights, OCI and liquidity eligibility are not available, so the capital and reserve checks are screening proxies. Independent review pending. Not investment advice.
