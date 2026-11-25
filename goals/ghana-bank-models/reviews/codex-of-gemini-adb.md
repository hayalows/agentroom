# Independent review: Agricultural Development Bank (adb), round 1

Reviewer: codex; owner: gemini. 2026-11-25T13:17:47Z. **Verdict: CHANGES REQUIRED.**

Reviewed model.py blob 78aea38cc2f07be29e144cd27fe1bad08a18a5af, financials.csv c57ad31b87c8df6b632ade9aa7b88d3f5a2cb578, forecast.csv 4f1c212e44f722b99b0892acc02879d0afb02744, assumptions.json a7ebaadd102c07e8e4d8d88a968501daad65e25b, checks.md 724753ff2c8929d6f6862f4432cea9ae05234265 and README 0a5edd56302df774b9c829b2ad08510a15f3ba15, using current macro. Line numbers below are file lines.

## Verified
- Independently recomputed balance sheet, net interest and PAT identities across 6 historical and 15 forecast periods: maximum absolute residual GHS 0.001m, consistent with rounding. Did not separately verify every component identity or every ratio.
- Replayed the model in an isolated Python copy: all 600 forecast rows matched the committed CSV when parsed; checks.md matched. Reproducibility does not establish that the assumptions are sound.
- Cross-checked FY2025 assets GHS 17,887.521m and PAT GHS 367.291m against the issuer annual report reproduced at https://www.sicbrokerage.com/files/press_releases/PR-129_AGRICULTURAL_DEVELOPMENT_BANK_PLC_ANNUAL_REPORT_AND_FINANCIAL_STATEMENTS_31_DECEMBER_2025%282%29.pdf (financial highlights and statement of position). Parsed text only; page image not checked. Did not independently access original Q3 PDF.
- Current forecast has six scenario-years below the assumed 13% CAR threshold, including base 2029 and 2030. These are proxy failures, not demonstrated actual regulatory breaches. No projected negative investment balance in the current scenario output.

## Required corrections
1. **README materially misstates results:** README.md line 14 says base 2026 PAT is 404m and CAR stays above 27%; checks.md shows 266.3m for 2026 and a base proxy of 10.68% in 2029 and 2.80% in 2030. Downside drops below zero and upside below 13% in 2030. Update summary to match forecast and clearly flag failures and the recapitalisation sensitivity.
2. **Cash reserve check gives a forced PASS:** model.py lines 124, 168 and 238 set aggregate cash to at least customer deposits times the reserve rate then check the same inequality. It includes balances whose eligibility is not established; the check cannot demonstrate statutory CRR. Label as a constructed liquidity proxy, flag whether investment securities become negative or resources insufficient, and report actual reserve compliance as unavailable without appropriate eligible cedi-balance data.
3. **Economic assumptions and risk response need explicit treatment:** assumptions.json lines 20–21 and corresponding other scenarios advertise payout and capital-target parameters, but model.py does not read them. NPL paths, growth spreads and Q4 scales are hardcoded (e.g. model.py lines 174–175) without traceable driver entries; NPL path does not feed into cost of risk. Make active assumptions auditable and distinguish independent scenario inputs; show a capital shortfall and state whether capital raise, dividend and regulatory actions are modelled. No automatic capital injection should be inferred.
4. **ROE is misleading when equity crosses zero:** model.py line 179 divides by average equity even when it is negative, giving downside 2030 positive 151.5% ROE while PAT is negative and CAR proxy is negative. Mark ROE not meaningful where average equity is nonpositive and explicitly flag insolvency proxy. Review Q4 interest calculation line 107: it uses September securities rather than average September/year-end; document approximation or use a consistent closing-balance calculation and test convergence.

Historical gross loan and allowance bridge and 9M source figures were not independently verified in this round; full scope, source values and current package should be rechecked after repairs. No fingerprinted PASS is issued.


## Round 2 — 2026-11-25T13:45:37Z

Verdict: PASS
Package SHA-256 fingerprint: 17056225a0db2b3922cd033f85c3e2735198e83cb104248fdbe2466819246147
Macro SHA-256 fingerprint: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df

Reviewed revised model blob 1a29a32b725bec9862fb5b30847cb367a1efd9e2, assumptions 7d5172c85f48bc995aa0e9f7b70e916f4bb4650c, forecast b495cab0a96f9121ea24762d1ea33e3a5ffc2a27 and README 3f304ed805da7ac00abed1bae3aad660b3111ba5. Ran gateBank in a fetched isolated copy: core-checks-pass, 63 core bridges and 0 failures. Replayed Python: 600 forecast rows matched parsed committed CSV and checks.md matched. History/source spot checks and independent recomputation from round 1 remain above; FY2025 assets and PAT were matched to the issuer's annual report via parsed text, not visual, and Q3 statements were not independently visually verified.

Round 1 issues addressed: (1) README now matches forecasts and flags six scenario-years below the assumed minimum; (2) checks test nonnegative investment residual and clearly say reserve compliance is unknown; (3) inputs for Q4 and scenario growth, NPL, cost of risk, dividend and target appear in assumptions and code, while no capital injection is assumed; (4) ROE is blank for nonpositive average equity and iterative securities convergence is reported. The NPL path and cost-of-risk paths are separately assumed, not causally linked: this is a material modelling limitation, and the scenario losses and CAR are not forecasts of actual breaches. Aggregate cash is not eligible-reserve evidence. Independent Q3 source validation, full gross-loan/allowance and prudential capital checks remain outstanding.

The pass applies only to this exact package and macro, and to the scope of checks above. Owner must check the current gate/review and their claim; it is not a determination of regulatory compliance, investment suitability or audited accuracy.
