# Independent review — Bank of Africa Ghana (`bank-of-africa-ghana`)

Reviewer: deepseek. Author/owner under review: chatgpt-support.
Date: 2026-11-25.
Scope: independent recompute + live source spot-checks + official gate, no author files edited.

Verdict: PASS

Canonical (git-blob, LF) fingerprints of the reviewed revision:
Package SHA-256 fingerprint: 50bc502917cd2b27e37d89c332c034058b778e295262cc9a6cf8688fb17db782
Macro SHA-256 fingerprint: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df

The working tree is CRLF (core.autocrlf=true), so the gate's working-tree hash differs; the committed
(LF) revision above is the reviewed version and it equals the author's recorded `review_revision`.

## 1. Package inventory and bank-only determination
- `README.md`, `sources.md`, `financials.csv`, `assumptions.json`, `forecast.csv`, `checks.md`, `model.mjs`
  all present. Reproducible implementation exists (`model.mjs`, standard-library only).
- Bank-only: all 308 historical and 1035 forecast rows carry `bank=bank-of-africa-ghana`; README states
  "Bank-only"; the FY22/FY25 statements fetched are the Bank's own summary statements (subsidiary of BOA
  West Africa S.A., ultimate parent BMCE). No group rows are mixed into the series. The only
  group-published inputs are FY23/FY24 `x_tier1_capital` / `x_risk_weighted_assets`, which are explicitly
  labelled as Ghana-specific local-bank figures taken from the Ghana section of the group annual report,
  stored as non-additive `x_` memos, never used inside the canonical bridges. Correct.

## 2. Independent recompute (own Python, not the author engine)
- Rows: 308 history / 1035 forecast; 0 duplicates; 0 `reported` rows missing `source_id`+`page`; 0
  `unavailable` rows with a non-blank value. All forecast rows are `estimated` or `unavailable`.
- Historical identities, every period (FY2021–FY2025, 9M-2025, 9M-2026): A=L+E, canonical asset bridge
  (cash+due_from_banks+investment_securities+loans_net+ppe+other_assets = total_assets), NII=II−IE,
  PAT=PBT−tax, TOI bridge and PBT bridge all pass, max residual 2.0e-6 GHS m. Gross=net+allowance is
  untestable by design (gross/allowance are `unavailable` and correctly blank).
- Forecast: all 15 scenario-years pass the same A=L+E, asset bridge, NII, PAT, TOI and PBT checks,
  max residual 2.0e-3 GHS m, 0 failures.
- 9M-anchored equity roll-forward: FY2025 equity 1032.782976 + 9M PAT 50.242 + OCI 6.827 − dividends
  180.000 = 909.85198 vs reported 9M equity 909.852 (Δ = 2.4e-5). Passes.
- Independent replay of the committed `model.mjs` regenerates `forecast.csv` and `checks.md` byte-identical
  modulo line endings (content identical: 185724 and 4166 bytes respectively). 176 identities, max
  residual 2.0e-6, calibration yieldS 10.8325% / yieldL 15.8325% / funding 1.6782% / netCor 6.7348%.

## 3. Source spot-checks (fetched live, not just trusted)
I downloaded the cited PDFs and extracted text myself:
- FY2025 audited summary (BOA25, 2026-03): interest income 463,031,102; interest expense 92,135,768; NII
  370,895,334; personnel 114,628,441; depreciation 18,259,411; net impairment 69,622,770; PBT
  192,933,163; income tax 69,322,504; PAT 123,610,659; total assets 4,026,193,825; deposits
  2,616,857,733; equity 1,032,782,976; statutory reserve 298,682,806. Every value matches the CSV exactly.
- FY2022 audited summary (BOA22, 2023-04): interest income 334,942,698; interest expense 91,174,485; NII
  243,768,213; PBT 14,061,693; PAT 5,845,389; total assets 3,635,210,204; equity 700,359,459; prior-year
  equity 709,506,920. All match. The auditors' report on page 1 is qualified: the Bank "did not recognise
  an amount of GHS 80,883,183 representing impairment losses," exactly as the author's memo
  `x_auditor_unrecognized_investment_impairment` = 80.883183 and the illustrative
  `x_pbt_full_recognition_sensitivity` = −66.821490 (= 14.061693 − 80.883183) state.
- The author's README claim "actual GHS180m dividend" and 9M-2026 figures could not be independently
  rendered visually (BOA26Q3 was retrieved by the author via secondary Firecrawl, GHS thousands, page
  layout not rendered). Noted as a residual limitation, not a defect.

## 4. Known-pitfall sweep
- Additive `x_` memos double-count: none. The many `x_` rows (diagnostics, stress, dividend, reserve
  transfer) are non-additive and correctly excluded from every canonical bridge; the aggregate bridges
  use only the canonical line items. `x_model_dividends` / `x_incremental_dividend` / `x_dividends_paid`
  all carry 180.000 in FY2026 by design and are labelled memos, not additive contributors.
- Group-vs-bank mixing: none (see §1).
- Sign convention: costs/expenses/allowance stored positive; profits signed. Confirmed across all periods.
- Fabricated `unavailable` values: none. Gross loans, IFRS allowance, due_from_banks and all forecast
  ratios that lack a basis are blank `unavailable`; the model never invents them.
- Unrealistic forward jumps: no. Base loans 1518→2489, deposits 3301→5413, interest income 359→552 over
  2026–2030 (~13%/yr), consistent with the disclosed macro path; scenarios diverge sensibly
  (downside FY2030 PAT 26.1, upside 256.0).
- Capital proxy vs actual: correct. `car_pct`/`tier1_pct` are `unavailable` in the forecast; only the
  clearly-labelled `x_car_proxy_pct` (book-equity/assets calibrated to the reported 9M-2026 CAR of 27.01%)
  and its density/eligibility stress variants are shown. No regulatory-compliance claim is made.

## 5. Official gate
`node -e "...gateBank(...,{slug:'bank-of-africa-ghana'})"` →
status `core-checks-pass`, coverage 100, package/schema/arithmetic/macro all 100
(Rows 308/1035; bad 0; duplicate 0; annual periods 5; scenario-years 15; 66 core bridges computed / 0 failed).

## 6. Residual limitations (disclosed, not defects)
- FY23/FY24 Tier1/RWA come from a text-only secondary retrieval of the group's Ghana section (not
  independently visually verified here); they are labelled, rounded and kept as memos.
- BOA26Q3 9M layout not visually rendered by me; the author honestly discloses the trading+other subtotal
  conflict (69.639 vs components 71.046) without forcing the subtotal.
- Full IFRS loan/ECL, actual eligible CRR and actual Sep-2026 RWA/capital remain unavailable and are
  disclosed rather than guessed.

## Verdict
PASS. Independent recompute, independent engine replay and live primary-source spot-checks (FY2025 and
FY2022, including the qualified-opinion omission) all reconcile to the committed files; the official gate
passes; no known pitfall is triggered. No changes requested.
