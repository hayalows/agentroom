# GCB Bank PLC: standalone bank model

As of 25 November 2026. Fiscal year December 31; GHS millions unless indicated. GCB is a licensed universal bank listed on the Ghana Stock Exchange (GCB). The 2025 annual report note 37 describes government direct ownership of 21.36% and indirect ownership through SSNIT of 29.89%, total 51.25% (shareholder table rounds SSNIT to 29.88%). Sources: GCB25AGM, GSELIST, BOGREG in sources.md.

## Actual results and scenario outlook

FY2025 bank-only assets were GHS52,398.519m, deposits 41,048.267m, net loans 16,038.002m and profit after tax 2,043.968m (GCB25 pp.86,88). Reported CAR 18.02% and NPL 10.31% (GCB25SUM p.2), versus 14.6% and 4.8% in 9M-2026. September balance-sheet data are point-in-time; income data are cumulative.

| Estimated scenario | 2026E PAT | 2030E PAT | 2030E assets | 2030E CAR proxy |
|---|---:|---:|---:|---:|
| Base | 2,481.238 | 5,190.582 | 133,711.357 | 27.03% |
| Downside | 1,794.176 | 959.456 | 105,542.679 | 19.30% |
| Upside | 2,736.508 | 8,039.118 | 159,039.669 | 28.13% |

Forecast assumptions are sensitivities, not management guidance. Loan and deposit growth reflect shared nominal GDP proxies plus spreads; interest yields and funding costs respond to shared rates. FY2026 uses actual nine-month income plus estimated Q4, and begins from the September balance sheet. Capital and reserve checks are screening proxies. No modeled capital or liquidity shortfalls across 15 scenario-years at macro v1, but the downside 2026E CAR proxy of 14.38% is only 1.38 percentage points above the 13% shared minimum. The wide long-run range demonstrates sensitivity to credit risk, growth and funding.

DDEP: FY2024 investment derecognition loss of 297.212m includes DDEP bonds 42.807m and Eurobond-related losses 254.405m; no recurrence assumed (GCB25AGM p.159). FY2025 capital reported without expired DDEP relief. Tax levies are included within reported income tax (p.161); modeled blended tax 35%. FY2025 USD on-balance net exposure was USD56.853m (pp.143–144); translation is modeled from FY2027 using disclosed USD quantities as a proxy, not a prediction of FX positions.

## Reproduction and limitations

Run `node model.mjs` in this directory (Node 18+; built-in modules only). Reads financials.csv, assumptions.json and shared macro.csv; writes forecast.csv and the forecast section of checks.md. The pure engine was executed in cloud JS and the committed forecast was re-fetched and matched exactly. This is an alternative to the preferred Python implementation. 278 historical rows; 840 forecast rows. All available historical bridges and all 15 forecast bridges pass. Independent review pending.

Known gaps: interim gross loans/allowance and current FX positions not separately disclosed; opening 2021 equity/assets not sourced; historic CAR/reserve notices and bank-reported profitability ratio comparisons incomplete; some filing screenshots cache-missed (parsed text available). RWA, Tier 1, liquidity eligibility and full FX/OCI positions cannot be modeled precisely from available disclosures. Shared macro v1 regulatory paid-capital threshold has a verification caveat. See checks.md and sources.md. Not investment advice.
