# Response to review of stanbic-bank-ghana (author: deepseek) by codex — round 1

Date: 2026-11-25. Author: deepseek. Re: `reviews/codex-of-deepseek-stanbic-bank-ghana.md` (Verdict: CHANGES, reviewed financials `cf9b2e8a…`, forecast `9a441f28…`, model `a855355e…`).

I accept all six changes. Five are fully fixed and one is documented as a stated limitation; the model is rerun and the official `bank-gate.mjs` passes.

## Item 1 — Forward yield calibration. FIXED (blended anchor-implied yields; the 53% jump is gone).
Confirmed the defect: the old component-yield formula priced the large cash/BoG residual at the policy rate and produced base FY2027 interest income of 4,034.3m against an annualised 9M-2026 run rate of 2,633.0m (+53.2%). Replaced it with a **blended, anchor-implied yield carried forward for continuity**: `yield_t = income_{t-1} / mean earning assets_{t-2,t-1}`, drifted by the shared policy-rate ratio (rate_t / rate_{t-1}). Base FY2027 interest income is now 2,539.6m (−3.5% vs the run rate) and interest expense 372.6m (−1.1%). Out-of-sample back-test: the FY2024 implied earning-asset yield applied to FY2025 average earning assets predicts FY2025 interest income of 3,563.0m versus the actual 3,415.7m (4.3% error). `checks.md` "Forward-yield calibration diagnostics" documents this. The cash base still contains non-earning reserve balances, so the blended yield is a portfolio average, not an eligible-reserve rate — stated explicitly; inter-bank balances are not given a separate income line (also stated).

## Item 2 — Canonical asset composition. FIXED.
Non-pledged trading assets (9M-2026 3,107.390m; FY2025 3,783.127m) and pledged trading assets (9M-2026 997.908m; FY2025 1,084.220m) are now folded into the canonical `other_assets` line; `x_trading_assets` / `x_pledged_assets` remain as non-additive memos of the components already inside it. The asset-component bridge and `noncash()` were changed to count them once, so cross-bank aggregation will not understate asset lines. `checks_history.py` and `model.py` bridges re-pass.

## Item 3 — Anchor and tax split. FIXED (split) / DOCUMENTED (anchor).
- **Tax split:** the anchor year now preserves the ACTUAL 9M-2026 indirect tax (36.323m) and direct tax (465.606m) and adds only an estimated Q4 component; the annual indirect tax is never recomputed from full-year PBT. Downside FY2026E now shows indirect 36.323m (was 21.454m) and direct 465.606m (was 480.475m); total unchanged at 501.929m.
- **Anchor 82%:** documented in `assumptions.json` (`net_to_gross_pct`) and `model.py` as an explicit **estimated improvement** over the actual FY2025 77.93%, and it changes opening gross/RWA/capital and the Q4 allowance build — the sensitivity is stated. The allowance stock is explicitly the combined allowance-plus-interest-in-suspense deduction (gross minus net), stated in `financials.csv` notes and the README.
- **FX register claim:** the `sources.md` note that FX revaluation is "forecast" is corrected — the model does **not** model FX translation (no net FX position disclosed); the omission is stated consistently.

## Item 4 — CET1 vs Tier 1, and derived ratios. FIXED.
The reported summary ratio (which the disclosures label CET1) is now stored as `x_cet1_pct`. A true `tier1_pct` is derived from the audited capital-adequacy note where numerator and RWA are available: FY2022 12.28%, FY2023 16.65%, FY2024 16.00%, FY2025 21.17% (definitionally distinct from the rounded reported CET1 12.3/16.6/16.0/21.2). FY2021 and 9M-2026 have no audited Tier 1 numerator, so `tier1_pct` is `unavailable` there. Historical derived LDR, cost/income, ROE and ROA are now populated (closing-balance basis, with the basis stated).

## Item 5 — Dividend constraints and buffer gap. FIXED (label) / DOCUMENTED (simplification).
The FY2026E `x_model_dividends` row is labelled a **Q4-only** figure and is not comparable to a full-year payout (the observed nine-month equity already contains the year-to-date dividend). The model applies no Act 930 statutory-reserve transfer; this **no-transfer simplification is disclosed** in the assumptions/README. In the downside, FY2026E capital (19.60%) sits below the stated target (21%); `checks.md` reports the explicit buffer gap per scenario-year (`x_capital_shortfall` where the minimum is breached).

## Item 6 — Source scope / independent verification.
README ownership: Stanbic Bank Ghana Ltd is a subsidiary of Standard Bank Group (South Africa), GSE-listed, operating as an independent universal bank. I do not have the exact percent holding in the summary statements used, so it is not asserted. Independent spot-checks of FY2023–FY2026 and a Python replay are still required for final PASS; I cannot substitute for an independent reviewer.

## Verification
- `bank-gate.mjs` on `stanbic-bank-ghana`: **core-checks-pass**, package/schema/arithmetic/macro 100. 302 history + 870 forecast rows; 0 bad; 0 duplicate; 5 annual periods; 15 scenario-years; 63 core bridges, 0 failed.
- New package fingerprint: `2628443539e7dce48b6ac96917c0e9fc43a174fb6c2126db271b9c723b5c75bb`. Macro: `4cf8911a258f0c81a4a48e660b31b796de40e8327dca36d2bbdb16b59a2f7202` (v1.1).
- `model.py` rerun is deterministic (byte-identical forecast.csv).

Changed files: `banks/stanbic-bank-ghana/{build_financials.py,model.py,checks_history.py,assumptions.json,financials.csv,forecast.csv,checks.md,checks_history.md,README.md,sources.md}`.
