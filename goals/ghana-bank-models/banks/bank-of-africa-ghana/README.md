# Bank of Africa Ghana — initial complete scenario package

Bank-only; December year end; unlisted Ghana bank. Part of BANK OF AFRICA group; ultimate parent BMCE as described in issuer FY25 summary. FY2021–2025 and 9M2025/26 data; GHS millions. At September 2026 assets 4512.378m, PAT 50.242m, reported CAR 27.01%, NPL 17.89%. September 2026 impairment increased substantially; retain annualized observed cost of risk; actual GHS180m dividend already paid, no Q4 payment.

## Forecast
Model anchors FY2026E on nine-month actuals plus separately forecast Q4. All 15 scenario-years generated from common macro.csv, bank-specific observed calibration and explicitly estimated repricing and credit assumptions. No funding plug or further share injection. Regulatory CAR not projected as actual; book-equity/asset proxy and conservative positive-PAT eligibility stress shown in x_ rows. No projected gross loan, IFRS allowance or NPL path without sufficient inputs; net LDR labeled separately. Negative retained earnings or capital proxy gaps are model risk signals, not current bank insolvency.

| Scenario | FY2026E PAT | FY2030E PAT | FY2030E CAR proxy |
|---|---:|---:|---:|
| base | 73.782 | 153.763 | 25.113% |
| downside | 64.421 | 26.126 | 24.806% |
| upside | 80.023 | 255.972 | 25.137% |

## Limitations and review
Detailed full annual risk-note access remains incomplete, including actual maturity profile, contractual FX exposure, actual regulatory capital/RWA and cash reserve eligibility. Historical 2022 impairment is reported; exact DDEP allocation and relief need primary note, not assumed. See sources.md for source basis, conflicts and visual retrieval limits. All-in tax rate estimate; prior-year actual tax and levies preserved. Shared macro inputs are common scenario assumptions and not certification of bank-specific legal requirements. Source-page confirmation and independent code replay requested. Run `node banks/bank-of-africa-ghana/model.mjs` from goal directory or the absolute script path. Draft for independent review, not investment advice.
