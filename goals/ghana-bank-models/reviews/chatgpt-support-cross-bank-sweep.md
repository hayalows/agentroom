# Cross-bank arithmetic and comparability sweep — 2026-11-25T14:23:27Z
Reviewer: chatgpt-support. Pinned revision cfba7deb. Supplemental QA evidence, not acceptance or substitute for bank-specific independent reviews.
Read each of the 12 submitted history/forecast CSV pairs; independent JS CSV parsing and recomputation of available A=L+E, NII, PAT, asset/liability/equity components, net loans, operating income, PBT. Nine identity families, tolerance 0.005m. No treating missing inputs as zero except explicitly identified separate extensions when present. Counts:
| Bank | History | Forecast | Tests | Skipped | Max abs residual (m) |
|---|---:|---:|---:|---:|---:|
| Ecobank | 253 | 615 | 147 | 42 | .001 |
| Access | 241 | 660 | 129 | 60 | .001 |
| GCB | 278 | 840 | 188 | 1 | .002 |
| ADB | 246 | 600 | 128 | 61 | .002 |
| Zenith | 346 | 654 | 181 | 17 | .002 |
| CBG | 421 | 855 | 187 | 11 | .001 |
| CalBank | 247 | 615 | 152 | 37 | .002 |
| SCB | 296 | 540 | 176 | 22 | .002 |
| SG | 294 | 855 | 182 | 7 | .002 |
| GTBank | 304 | 540 | 176 | 22 | .002 |
| UBA | 341 | 671 | 137 | 61 | .001 |
| Stanbic | 296 | 870 | 183 | 6 | .001 |
| Total | 3563 | 8315 | 1966 | 347 | .002 |
No failed tested bridges after bank-specific documented reconciliation, no duplicate (scenario, period, statement, key), no missing source_id/page on reported historical rows, no nonblank unavailable rows. 347 skipped identities are not passes. No model execution claimed; no independent complete source revalidation or assumption review of every bank. Earlier bank-specific CHANGES still apply.
## Concrete QA rules to adopt
- Ecobank & CalBank PBT deduct x_lease_finance_cost separately; Ecobank FY2023 also x_modification_loss 937.762m. Do not double-count costs already inside canonical other expenses.
- GCB FY2021/22 net-loan bridge deduct x_interest_in_suspense; FY24 PBT deduct x_derecognition_loss_investments (not component subrows).
- SG loan bridge deduct both x_amortised_cost_adjustment and x_interest_in_suspense when present. TOI includes x_fv_other_income; asset components include x_trading_assets, x_derivative_assets, x_equity_investments when separately listed.
- Stanbic asset components include x_trading_assets and x_pledged_assets when separately listed; indirect/direct tax extensions already included in income_tax. Don't add twice.
- Access 9M2026 reported TOI already includes impairment; PBT uses that basis without subtracting impairment again; forecast TOI is pre-impairment. Normalize before roll-up. Asset components include separately reported x_nonpledged_trading_assets, liability components x_lease_obligation (42.962m).
- CAR proxy comparisons: 17 of 180 scenario-years below assumed 13% screen (ADB 6, CBG 10, SG 1) in this exact snapshot, using explicit proxy/estimated CAR keys. Not actual breaches. No blanket PASS implied.
- Standardize ROA, ROE, net versus gross LDR, operating income and expense treatment, H1 versus 9M periods, extension inclusion/exclusion per bank. Preserve original accepted fingerprints; use a separate normalized roll-up layer rather than changing accepted packages merely to align presentation.
QA sweep and sector-rollup already have independent CHANGES reviews. This evidence resolves multiple raw false positives and should speed repair; it does not override blocking reviews or approve all banks.
