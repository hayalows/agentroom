# UMB supplemental model review and 2026 applicability warning

UTC 2026-11-25T19:29:49.019Z. chatgpt-support; source-assistance contributor, NOT an eligible independent scoped verdict. No bank files edited; Codex owns the package. Source pin 872f8f3dcee07f9805f4126d66675417b25a9ce9; owner package 4e18d1fd69549708fbbca8a9ff36d1e3bad724d70ccfee63e05fe99dfac31357 / macro b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df / auxiliary anchor 8f320f384de4147e3ffa1ef344f07b08fcee2b9f7ead08559a73916f08c2adc2 (owner identifiers, not newly rehashed in this run).

## Recomputed from actual fetched CSVs
280 history rows (FY21–24, 9M24/25 only), 846 forecast rows, 165 separate FY25E anchor rows. Independently recomputed 267 checks: 14 per scenario-year across all 18 anchor/forecast cases (NII, operating income, PBT, PAT, assets composition, liability composition, equity composition, balance, equity roll, retained roll, reserve roll, RWA, CAR proxy, minimum capital shortfall), plus 5 recap overlay checks per FY26 scenario (minimum overlay, post-overlay CAR/equity/assets, 60% density overlay). 267/267 within tolerance (money 0.004m, percentage points 0.0002); maximum absolute residual across all numeric checks 0.0010716941 in native units. Used independent equations on rounded output, not owner check count. FY25 equity roll uses incremental Q4 PAT = estimated full year PAT minus actual 9M PAT. Native engine not newly replayed in this run; Helper and lead have independently reported exact scratch replay.

## Material new external benchmark, not primary history
Read Codex and Papa's separate PwC Q2 evidence files at the source pin. No new issuer filing or visual verification in this review. Earlier primary-source H1-25 supplement CSV independently read: assets 7685.610630m, deposits 6330.261694m, PBT 98.968341m, all agree to one decimal with PwC secondary table. PwC Q2 2026 assets 16684m, deposits 11537.5m, H1 PBT 195.1m, CAR 13%. Q2 precedes MoF's confirmed July recapitalisation; no post-event recognition or injection inferred. Source: https://www.pwc.com/gh/en/assets/pdf/quarterly-banking-league-2026.pdf ; secondary compilation, no verification warranty, Q3 notice wording inconsistency, Q2 cover/tables and H1 comparison corroborate period.

| FY26E case | Assets m | Deposits m | PBT m | CAR proxy % | Q2 assets excess vs FY26E | Q2 deposits excess vs FY26E | H2 PBT required to hit FY26E (m) |
|---|---:|---:|---:|---:|---:|---:|---:|
| base | 13493.803 | 9900.307 | 227.801 | 6.0411 | 23.64% | 16.54% | 32.701 |
| downside | 11929.312 | 8793.761 | 105.836 | 1.7465 | 39.86% | 31.20% | -89.264 |
| upside | 14371.115 | 10621.723 | 284.985 | 8.5730 | 16.09% | 8.62% | 89.885 |

H2 residuals are arithmetic only, not estimates or PAT. FY-end balances can decline, so this is not a proven annual forecast error. Under all three scenarios the secondary H1 scale already exceeds year-end projected scale. The original forecasts represent an old Sep25-anchored unquantified-capital counterfactual; cannot be represented as a current best estimate or regulatory forecast.

Papa's secondary table gives 40.3% RWA density and 19.67 assets/equity multiple: illustrative implied RWA 6723.652m, capital 874.07476m, equity 848.19522m; these are derived from rounded secondary values, not directly reported values. At a fixed implied RWA, a hypothetical 16% target would be about 201.710m above 13%; not a capital requirement or actual injection. Do not substitute this into the canonical forecast or add it to the July event.

## Recommendation for owner and lead
1. Keep the primary FY25 and FY26 rows unavailable. Do not insert secondary values as reported history.
2. Conditional closure only after eligible second independent scoped verdict and lead decision. Existing model is mechanically sound on these checks; source limitation is material to use.
3. Before final distribution put the Q2 comparison and explicit 'September 2025-anchored counterfactual, not current post-recapitalisation outlook' beside UMB in the conditional peer/sector report and summary. Link both external evidence files. If canonical README/model package changes, rehash and re-review; no silent change while eligible reviewer working. A separate sensitivity appendix can remain outside canonical history.
4. Exclude UMB from all ordinary accepted totals, even if completion machinery reports otherwise. Do not publish the old proxy as UMB's current CAR.
