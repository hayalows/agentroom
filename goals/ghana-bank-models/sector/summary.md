# Ghana bank financial models: lead summary (FINAL DRAFT for human sign-off)

Written by the lead (claude), 2026-11-25. Source pin of the final reports: commit `b728a09ffd52393f98b97c14298544c139d1921f` (roll-up input fingerprint `b59a8526...`, macro `b3c4412d...`). Nothing here is investment advice, a price target, an audit or legal advice. **The goal is complete only when the human signs this off.**

## 1. Where the goal stands
- **23 of 23 licensed banks are closed.** **20 are ordinarily accepted** (core gate passes, distinct reviewers' exact-version PASS, no unresolved blocker, owner closed): absa-ghana, access-bank-ghana, adb, bank-of-africa-ghana, calbank, consolidated-bank-ghana, ecobank-ghana, fbnbank-ghana, fidelity-bank-ghana, first-atlantic-bank, first-national-bank-ghana, gcb, gtbank-ghana, nib, republic-bank-ghana, societe-generale-ghana, stanbic-bank-ghana, standard-chartered-ghana, uba-ghana, zenith-bank-ghana.
- **3 are conditional-closed**, each missing one primary filing that nobody could reach after documented retries (`review-resolutions/CONDITIONAL-CLOSURES.md`, policy in `CONDITIONAL-POLICY.md`). They are shown separately and never inside ordinary totals:
  - **prudential-bank:** 30 Sep 2026 bank-only statement unavailable (issuer site returned HTTP 502 to every agent and to the human; no mirror or news report found).
  - **omnibsic-bank:** FY2021 annual statement unavailable (four FY2021/22 archive URLs returned 404); four complete annual periods FY2022 to FY2025 plus 9M-2025 and 9M-2026.
  - **umb:** FY2025 annual and 2026 interim statements unavailable. FY2025 is a labelled estimated anchor, and the model is a September-2025-anchored counterfactual, not a current post-recapitalisation outlook. A secondary PwC Q2 2026 benchmark (assets GHS 16,684m, deposits GHS 11,537.5m, H1 pre-tax profit GHS 195.1m, CAR 13.0%) is kept as secondary evidence, not primary history.
- **Shared pieces:** roster verification done; macro assumptions v1.1 done; QA sweep v1.3 independently passed; peer comparison and sector roll-up generated once at the final pin from a clean LF checkout, with independent reviews posted (section 6).

## 2. What the 20 ordinary models show (bank-only statements, GHS)
| Measure | FY2025 | 9M-2026 (19 of 20 banks) |
| --- | --- | --- |
| Total assets | 403.8bn (about 90% of the Bank of Ghana sector total of 446.9bn) | 449.5bn (about 88% of 513.6bn) |
| Customer deposits | 293.2bn (about 90% of 325.3bn) | 325.3bn (about 87% of 372.9bn) |
| Net loans | 88.8bn | 114.5bn |
| Profit after tax | 14.0bn | 9.9bn |

- **Profit path (20 banks):** 4.7bn (FY2021), **-5.9bn (FY2022, domestic debt exchange)**, 6.8bn (FY2023), 10.5bn (FY2024), 14.0bn (FY2025). Total equity rose from 24.2bn (FY2021) to 56.6bn (FY2025).
- **Banks hold far more deposits than loans:** net loans are about 30% of deposits (matched banks, FY2025). Earnings follow money-market rates and currency trading more than lending.
- **Return on closing equity** is about 24.8% across the matched banks and cost-to-income about 45%. Individual banks range from about 0.5% (Consolidated Bank) to about 34% (GCB) on closing equity, and cost-to-income from about 26% to 86%. The Bank of Ghana's own sector ROE uses a different definition and is not directly comparable.
- **Rates matter:** shared macro (Bank of Ghana, Nov 2026): policy rate cut from 14% to 11% on 18 Nov 2026; inflation 5.5% (Oct 2026); 91-day bill about 4.5%; uniform 20% cedi cash reserve ratio since 4 June 2026; sector capital adequacy 18.5%.
- **Scenario totals are model outputs on shared macro paths, not predictions.** Combined profit after tax, GHS bn: base 12.9 (FY2026E) rising to 19.3 (FY2030E); downside 10.4 falling to 7.2; upside 13.6 rising to 26.5. In early years a "downside" rate case can raise profit for banks with large liquid balances.
- **Notable individual results:** ADB is loss-making by FY2030E in base (-308m) and downside (-684m, capital proxy about -4.5%) because of a reported non-performing loan ratio of 70.5% and an allowance already near 48% of gross loans. NIB's average-equity ROE is shown as not meaningful (equity was negative at FY2024); CalBank's carries a caution because equity rose more than 6x.

## 3. What was verified, and how
- **Arithmetic:** every ordinary bank passes the automatic gate (balance sheet, net interest income and profit bridges for every period and every forecast scenario-year) and has an independent reviewer's exact-version PASS. Reviewers replayed models in isolated copies and recomputed identities. QA at the final pin: 0 FAIL and 0 WARN across the 20 ordinary banks.
- **Sources:** each reported number carries a source and page. Reviewers spot-checked rows against the issuer's own filings (for example, I checked 14 ADB values against notes 8, 9 and 21 of its signed FY2025 report, all exact). Spot-checking is **not** a full audit of every cell.
- **Review caught real errors, fixed:** CalBank's first forecast overstated interest income by 41% and its capital ratio by about 3 points; ADB's first accepted version omitted all cash and placement earnings and used book equity as the capital numerator, so I reopened it and a corrected version was independently passed; several banks had right-of-use asset double counts or loan fields that did not tie.
- **Lead's own checks at the final pin:** peer-comparison 190 cells recomputed from raw bank files, 0 mismatches; replays of Prudential, OmniBSIC, UMB and ADB output files were byte-identical.

## 4. What is unavailable or uncertain (do not read as facts)
- The three conditional gaps above. 9M-2026 coverage is 19 of 20 ordinary banks (Consolidated Bank has only a first-half 2026 statement).
- **Regulatory minimum paid-up capital (GHS 400m)** is unconfirmed for 2026; the 13% minimum capital ratio is confirmed from the Bank of Ghana's September 2026 report.
- **Macro history gaps:** inflation and Treasury-bill history for 2021 to 2024 and GDP for 2021 to 2022 are unavailable in the shared macro file; FY2027E to FY2030E paths are the lead's estimates with reasoning, not Bank of Ghana forecasts.
- **Capital ratios in forecasts are proxies,** calibrated to each bank's latest reported ratio, not regulatory returns.
- **Loan detail:** gross loans and allowances are unavailable for several banks (summary statements print net loans only).
- **Net trading income** is the least reliable line; forecasts assume owner-chosen fades. **Calibration:** interest spreads were mostly fitted to nine-month 2026 actuals, which is a fit, not a validation.
- The roll-up is **partial coverage (about 90% of sector assets)**, bank-only against Bank of Ghana aggregates whose definitions may differ.

## 5. How to reproduce
Use a clean checkout with LF line endings (`git clone -c core.autocrlf=false`). Status: `node scripts/supervisor.mjs --json`. Bank models: `python model.py` (or `node model.mjs`) inside each `banks/<slug>/`. Roll-up: `node goals/ghana-bank-models/sector/sector-rollup/rollup.mjs --output-dir <path outside the repo>`; peer comparison: `node goals/ghana-bank-models/sector/peer-comparison/compare.mjs --output <path>`; QA: `python goals/ghana-bank-models/sector/qa-sweep/validate.py`.

## 6. Independent review of the final reports
Final roll-up: claude-helper-1 PASS and a second independent PASS (see `reviews/` for the roll-up review files). Final peer comparison: my round-4 PASS in `reviews/claude-of-chatgpt-support-peer-comparison.md`.

## 7. For the human
Please sign off or tell us what to change. Decisions only you can make: whether three labelled conditional banks are acceptable in the final report; and, if the Prudential site returns, to supply its Q3 2026 PDF so that bank can drop its conditional label.

## 8. Human sign-off
Signed off by the human in chat on 2026-11-25T21:13:42Z (recorded by the lead, claude). Scope of the sign-off: 20 ordinary banks plus 3 conditional-closed banks, each with its stated gap, as published at source pin b728a09ffd52393f98b97c14298544c139d1921f. The conditional banks are accepted as labelled exceptions. The agents verified arithmetic and spot-checked sources; this is not an audit, investment advice or legal advice. Any later change to a file under banks/ or sector/ voids the relevant closure and needs a fresh review.
