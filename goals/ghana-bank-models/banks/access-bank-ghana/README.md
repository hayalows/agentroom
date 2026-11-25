# Access Bank (Ghana) PLC: draft scenario model

Standalone Ghana bank; financial year ends 31 December; GHS millions. Historical statements cover FY2021–FY2025 and unaudited 9M-2026. See sources.md and checks-history.md for provenance and historical reconciliations. The bank is listed on the Ghana Stock Exchange; ownership needs an independently sourced current breakdown.

## Forecast

`model.py` generates FY2026E–FY2030E base, downside and upside estimates using `assumptions.json`, the historical CSV and the shared macro file. FY2026E preserves 9M-2026 reported income and estimates Q4; later income changes with balances and illustrative policy-rate and bill-rate sensitivity. Profit and capital figures are projections, not bank guidance.

Initial base PAT is GHS 483.4m in 2026E and GHS 597.3m in 2030E. Downside PAT is GHS 450.0m and 397.8m respectively. These values depend materially on assumed interest sensitivity, operating costs, impairment and loan growth. Both rates and growth use the shared macro scenarios, while actual investment repricing, FX exposure, dividend policy and new capital are simplified.

## Limitations for reviewers

- FY2025 annual report web copy's signed/final status remains unverified. More annual sources require visual checking; some FY2021/22 and interim fee splits remain unavailable. Some historic component groupings differ from forecast groupings and require careful alignment before sector aggregation.
- Net fees are projected because 9M-2026 does not split fees. Gross loans, allowance, eligible BoG reserves and Tier 1 capital are not forecast. NPL is an illustrative independent path; it is not used to derive credit losses.
- Forecast capital is an equity-to-assets proxy calibrated to the 9M-2026 reported CAR; it is not a prudential calculation. Cash includes balances that may not qualify as reserves, so no CRR compliance assertion is made. A negative investment residual indicates an infeasible forecast; no capital injection is assumed.
- FY2026 is based on observed 9M plus estimates. Future years use a simplified 50% rate-change sensitivity on earning/funding balances, not an asset-liability maturity model. The 35% tax rate and payout assumptions are estimates; no inferred regulatory or board decision should be attributed to them.
- `checks.md` and `checks-history.md` are preliminary; independent source spot checks and peer review are required before acceptance.
