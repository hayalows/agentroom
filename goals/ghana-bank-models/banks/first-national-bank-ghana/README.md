# First National Bank Ghana — initial complete scenario package

Bank-only; December year end; unlisted Ghana bank. FirstRand group subsidiary, distinct from FBNBank Ghana. FY2021–2025 and 9M2025/26 data; GHS millions. At September 2026 assets 7323.471m, PAT 48.823m, reported CAR 24.07%, NPL 12.14%. Retained deficit remains GHS309.925m at September 2026; no dividend assumed in all scenarios, no further equity injection; preserve observed GHS358.572m FY2025 contribution only in history.

## Forecast
Model anchors FY2026E on nine-month actuals plus separately forecast Q4. All 15 scenario-years generated from common macro.csv, bank-specific observed calibration and explicitly estimated repricing and credit assumptions. No funding plug or further share injection. Regulatory CAR not projected as actual; book-equity/asset proxy and conservative positive-PAT eligibility stress shown in x_ rows. No projected gross loan, IFRS allowance or NPL path without sufficient inputs; net LDR labeled separately. Negative retained earnings or capital proxy gaps are model risk signals, not current bank insolvency.

| Scenario | FY2026E PAT | FY2030E PAT | FY2030E CAR proxy |
|---|---:|---:|---:|
| base | 72.998 | 204.201 | 23.599% |
| downside | 69.274 | -1.559 | 21.055% |
| upside | 74.843 | 333.641 | 23.964% |

## Limitations and review
Detailed full annual risk-note access remains incomplete, including actual maturity profile, contractual FX exposure, actual regulatory capital/RWA and cash reserve eligibility. Historical 2022 impairment is reported; exact DDEP allocation and relief need primary note, not assumed. See sources.md for source basis, conflicts and visual retrieval limits. All-in tax rate estimate; prior-year actual tax and levies preserved. Shared macro inputs are common scenario assumptions and not certification of bank-specific legal requirements. Source-page confirmation and independent code replay requested. Run `node banks/first-national-bank-ghana/model.mjs` from goal directory or the absolute script path. Draft for independent review, not investment advice.

## Round 2 review repairs
Traded and pledged asset memos separated from aggregate other assets; 50% earning-trading exposure sensitivity with recalibrated yield. No marginal trading interest assumed in central case. No additional dividend or equity contribution. Central scenario unchanged; historical ratios and dividend memo supplemented. Base FY2030 CAR proxy 23.599%; +20% density stress 19.666%; combined density and eligibility 18.187%. 40% eligible cash sensitivity gap GHS257.632m. See checks.md for full reruns and rate calibration diagnostic. Central dividends and alternative stress payout caps separate. Exact JS replay executed using same engine functions and input data; independent Node CLI review still required.
