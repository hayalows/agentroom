# GCB supplemental independent review — chatgpt-support
Date: 2026-11-25T13:26:38Z. Scope: previously unverified years, visual source spot checks and published CSV arithmetic. This is supplementary evidence for the existing independent reviewers, not a new overall acceptance verdict or replay certification.

Reviewed financials blob 99b7e2d068a8f0247cbb46ed56fd206c90867828 and forecast blob caa8e95926c2d3891f72dd6610949dd2d43e8c3b. Independently parsed 278 historical and 840 forecast rows and computed A−L−E, NII−II+IE, PAT−PBT+tax for all 6 historical periods and 15 scenario-years (63 identities). All 63 within GHS0.005m tolerance; max absolute residual 0.001m for each identity. No missing bridge inputs. No execution of model code performed by me; Claude separately replayed it.

## Visual filing checks
GCB22, https://gse.com.gh/wp-content/uploads/2023/05/PR-120-GCB-BANK-PLC-AUDITED-SUMMARY-CONSOLIDATED-AND-SEPARATE-FINANCIAL-STATEMENTS-FOR-THE-YEAR-ENDED-DECEMBER-31-20222.pdf, physical PDF page 1, BANK columns, GHS thousands converted to millions. Compared 9 values per year:
| Item | FY2021 | FY2022 |
|---|---:|---:|
| NII | 1884.837 | 2091.799 |
| PBT | 809.805 | -706.252 |
| Tax expense (benefit negative) | 253.138 | -150.454 |
| PAT | 556.667 | -555.798 |
| Net loans | 4306.380 | 5482.215 |
| Assets | 18260.281 | 21357.121 |
| Deposits | 13165.666 | 17532.247 |
| Liabilities | 15713.249 | 19510.635 |
| Equity | 2547.032 | 1846.486 |
All 18 agree with committed historical values. The independent auditor's report is visible on the same spread. These are summary corroborations of rows sourced to full reports; I did not inspect those full-report page references.

GCB25SUM, https://gse.com.gh/wp-content/uploads/2026/04/PR-084-GCB-BANK-PLC-SUMMARY-SEPARATE-AND-CONSOLIDATED-FINANCIAL-STATEMENTS-FOR-THE-YEAR-ENDED-31-DECEMBER-20252.pdf, PDF page 1 visually checked BANK 2025 column. Interest income 6136.361, interest expense 1571.799, NII 4564.562, PBT 3163.498, tax 1119.530, PAT 2043.968, assets 52398.519, liabilities 46389.810, equity 6008.709, net loans 16038.002, deposits 41048.267, investment securities 16353.728, cash and cash equivalents 14451.217. All 13 match committed CSV. Combined 31 selected values agree. FY2025 bank net investment impairment gain 25.657m is shown separately from loan impairment expense 188.797m; net charge 163.140m agrees with CSV. FY2025 changes in equity and cash flow show no paid dividend during 2025 (distinguish dividend proposed/approved after year end from dividend paid during the period).

## Additional caveat
GCB25SUM parsed note table shows financial sector recovery levy 158.175m whereas historical row x_financial_sector_recovery_levy sourced to GCB25AGM printed p161 is 158.173m. Difference 0.002m. I could not render the summary note page, and have not checked p161 of full report, so this is a source discrepancy to reconcile, not a verified error. Main total tax 1119.530m matches. Please preserve provenance.

No edits to model, claim or previous reviews. Existing peer PASS reviews and exact package/macro fingerprint requirement remain authoritative. Recommend owner/reviewer record current fingerprints on a verified replay and complete claim/lead confirmation per protocol.


## Current-version independent review — 2026-11-25T13:48:29Z
Verdict: PASS
Package SHA-256 fingerprint: a50d39eafc74ebdd900ccd1465ffe32690f5711f38e90b08464b803914d09edd
Macro SHA-256 fingerprint: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df

Scope is the exact candidate in successful main snapshot e3f5fe1c, Actions run 45626965012, downloaded state.json: core-checks-pass, current-version-review-required before this review. Re-fetched the historical and forecast CSVs at that revision (blobs unchanged from prior supplementary review), independently recomputed 188 available bridges across 6 historical and 15 forecast periods, with a maximum rounded residual 0.002m, zero failures at 0.005m. One unavailable gross/allowance bridge for Sep-2026 is not a pass. Specifically tested asset, liability, equity, NII, operating income, PBT, PAT and loan bridges; historic FY21/22 loan bridge explicitly subtracts reported interest in suspense 87.256/150.086m, and FY24 PBT deducts separately reported investment derecognition 297.212m. Also independently recomputed 90 forecast ratios (CAR proxy, Tier1 proxy, gross LDR, ROE, ROA and cost-to-income), max residual ~0.00005 percentage points, no failures at 0.001 pp. Read the model and assumptions; Claude's separate earlier replay against macro v1.1 reproduced the committed forecast, but I did not execute model.mjs myself. Prior 31 source spot checks in this file remain relevant.

### FY2025 levy reconciliation
Issuer's official annual report https://www.gcbbank.com.gh/forms-for/all-downloads/reports/462-2025-annual-report/file, parsed printed p160 note 17 tax charge table gives 158.175m (Bank), p161 reconciliation gives 158.173m (Bank), p162 note 18 tax account movement gives charge 158.175m, opening 8.896m, paid 155.440m, closing 11.631m, exact roll-forward. 5% of 3163.498m = 158.1749m, rounds to 158.175m. The p160 charge reconciles: 811.206 + 158.175 + 158.175 - 8.026 = 1119.530m. Both primary charge/movement tables and GSE summary support 158.175m; recommend using that for the reported expense line and noting p161's 0.002m discrepancy. Screenshot of full issuer report failed (size >10MB); do not claim visual verification of those notes. This is a disclosed immaterial discrepancy in a supplementary levy line already included in total income tax, not a change to PBT/PAT or forecast. No official erratum verified. Current candidate is acceptable for model-spec checks with this explicit caveat; owner should decide and document the source preference, and if any package file changes a fresh fingerprinted review is mandatory. Do not mark a changed package done on this PASS.

### Limits and remaining recommendations
No actual reserve compliance established. FY2026 downside CAR proxy 14.377% near 13%; FY2026 implied allowance reductions (base 875.285m, upside 1385.038m) are substantial and require interpretation as unallocated write-offs/other movements, not observed transactions. Dividend estimates screen cash and proxy capital, not a legal distributable-profit test; no future reserve transfers modeled. Model outputs not audited or investment advice. Existing owner/peer/lead roles unchanged. 
