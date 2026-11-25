# Independent review — First National Bank Ghana (FirstRand) — deepseek of chatgpt-support
Date: 2026-11-25T16:05:00Z
Reviewer: deepseek (independent; did not modify owner files)
Owner: chatgpt-support
Verdict: PASS

Package SHA-256 fingerprint (bank-gate order, git-blob LF contents):
`c687b8541b2b001cb03c32a39bb629f416e903442f22ee9988f86269f3668a61`
Macro SHA-256 fingerprint:
`b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df`
Working-tree (CRLF) gate fingerprint: `4ec2cc32935e1a4d9a881fd4639a3a9ffdebb4ac4f7540d954fd1053376c87b3`
Gate status: `core-checks-pass` (package 100, schema 100, arithmetic 100, macro 100; coverage 100).

## Method
I did **not** trust the author's engine. I (a) re-parsed both CSVs with my own Python,
(b) recomputed every required bridge independently, (c) downloaded all four cited PDFs and
read the source pages myself, and (d) separately replayed the committed `model.mjs` in an
isolated copy of the folder and diffed its outputs byte-for-byte. I touched no owner file.

## 1. Bank-only (never group) — CONFIRMED
The statements are the bank's own ("First National Bank Ghana Ltd"), signed by the bank
chairman/CEO. `firstnationalbank.com.gh` FY2025 p3 names the bank as a subsidiary of
FirstRand EMA Holdings Proprietary Ltd (ultimate FirstRand Ltd, South Africa). This is the
FirstRand subsidiary, explicitly distinct from FBNBank Ghana / FirstBank: README, sources.md
and the entity note all say so, and no row is drawn from group accounts. Never mixes group
and bank rows. Line-item keys are drawn only from MODEL-SPEC.

## 2. Independent recomputation (own Python)
- **Rows / duplicates / provenance.** History 317 rows, forecast 1050 rows. Duplicate keys
  (period|statement|line_item): **0** in each. `reported` rows missing `source_id` or `page`:
  **0**. `unavailable` rows with a non-blank value: **0**. Forecast rows with a status outside
  {estimated, unavailable}: **0**.
- **Balance sheet A = L + E.** Exact (≤5e-4 GHS m) for all 7 history periods and all 15
  scenario-years. My residuals are 0.
- **Canonical asset bridge** (cash + due_from_banks + investment_securities +
  loans_net + ppe + other_assets = total_assets): exact every period. `due_from_banks` is
  blank (`unavailable`) and handled as 0 in the canonical aggregate only, not as an assertion
  it is zero — as documented.
- **Canonical operating-income bridge**
  (NII + fee_income − fee_expense + net_trading + other_operating = total_operating_income):
  exact. **PAT = PBT − tax**: exact. **NII = II − IE**: exact. **net = gross − allowance**:
  not computable because `loans_and_advances_gross`/`loan_loss_allowance` are correctly left
  `unavailable` for every period (see §4) — the model does *not* fake this identity.
- **9M-anchored roll-forward.** FY2025 equity 1003.049 + 9M-2026 PAT 48.823 = **1051.872**,
  which equals reported 9M-2026 equity exactly (delta 0.000). Retained earnings:
  −358.748 + 48.823 = −309.925 = reported. Stated capital 1297.557 unchanged; statutory
  reserve 64.240 unchanged. All three match the Q3 filing to the cedi-thousand.

## 3. Official gate + fingerprint
`gateBank(..., {slug:'first-national-bank-ghana'})` → `core-checks-pass`, all four checks
100. I recomputed the canonical fingerprint myself using the gate's exact definition
(`hash(JSON.stringify(files.map(f=>[f.name,hash(f.text)])))`) over
README.md, sources.md, financials.csv, assumptions.json, forecast.csv, checks.md **then**
model.mjs, from `git show HEAD:<path>` (LF) — because the tree is CRLF (`git ls-files --eol`
shows `i/lf w/crlf`). Result **c687b85…** — byte-identical to the fingerprint recorded in
codex's Round-2 PASS. The package has not changed since that accepted revision.

## 4. Source spot-checks (visual, primary PDFs — retrieved and read by me)
I downloaded all four URLs (HTTP 200, `application/pdf`) and extracted text with pymupdf:
- **FY2025** (`SummaryFinancialStatements_December2025.pdf`, p1): interest income 648,996;
  interest expense 295,187; NII 353,809; operating income 605,595; PBT 110,362; PAT 106,813;
  cash 1,991,898; loans 1,208,202; securities 1,840,039; total assets 6,484,459; deposits
  4,151,503; stated capital 1,297,557; accumulated losses (358,748); equity 1,003,049 → **all
  match the model**. p2 equity statement: proceeds 358,572; transfer to statutory reserve
  53,407 → matches sources.md and the memo. p3 notes: gross loans 1,382,443; NPL 168,848 =
  12.21%; CAR 34.08% → matches. Two levies 5,518 each + tax credit 7,487 → net tax 3,549 →
  matches the single reported `income_tax` 3,549 with PAT = 110,362 − 3,549 = 106,813.
- **FY2023** (`SummaryFinancialStatements_Dec2023.pdf`, p1): interest income 487,993; loans
  1,123,222; securities 1,022,222; total assets 3,711,201; equity 350,350; loss (2,569) →
  match. p2: gross loans 1,265,474; NPL 11.16%; CAR 19.18% → match (gross/allowance correctly
  **not** asserted as IFRS).
- **FY2022** (`Financialpublication_December2022.pdf`, p1): interest income 300,599; expense
  181,837; operating income 212,598; loss (340,464); total assets 3,068,390; equity 245,922;
  restricted BoG cash note 516,832 (2021:GHS212,907) → match. p2/p3 ratios: CAR 36.62% (2021),
  19.82% (2022); NPL 3.49%/7.09% → match.
- **Q3-2026** (`..._30_September_2026.pdf`, p1): 2026 column interest income 406,413;
  expense 175,039; NII 231,374; PAT 48,823; cash 2,292,736; loans 1,734,015; securities
  2,155,571; total assets 7,323,471; deposits 5,348,493; capital 1,297,557; reserve 64,240;
  accumulated losses (309,925); equity 1,051,872; non-pledged 208,015; pledged 84,511;
  derivative 610; deferred tax 40,165; tax 20,955 + 3,877 + 3,877 = 28,709 → **all match**.
  The 9M-2025 comparative (1,581,100 / 115,177 / 229,173 / 12,814 / 1,121,993 / 2,357,622 /
  6,099,653 / 4,147,496 / 943,556 / −364,834) also matches exactly. So 12 `reported` values
  across 4 filings were visually verified — well beyond the 3 required.

## 5. Pitfall scan
- **Additive `x_` double-count:** none. FY2025 `other_assets` 1,353,835 = non-pledged 205,753 +
  pledged 320,918 + derivative 50,831 + other assets 735,056 + current tax 1,102 + sub 10 +
  deferred tax 40,165 — i.e. the trading/derivative/deferred-tax rows are *components*, and
  the memos are labelled non-additive; the balance identity uses `other_assets` alone. Not
  double counted. The 9M-2026 memos reconcile the same way.
- **Group vs bank:** no mixing (bank-only; see §1).
- **Sign convention:** costs stored positive (interest expense, staff, D&A, opex, impairment,
  loan-loss allowance); profits signed (FY2021 −4.090, FY2022 −340.464, FY2023 −2.569, downside
  FY2030 −1.559). All identities use these signs correctly.
- **Fabricated `unavailable`:** none. Gross loans/allowance are left `unavailable` in every
  period where the summary does not disclose an IFRS allowance (the FY2021–25 gross figures are
  flagged "regulatory gross, not necessarily IFRS"). Forecast gross/ECL/NPL/CET1/liquid ratio
  are all blank, not guessed. The regulatory gross − net difference is explicitly labelled
  "not verified IFRS allowance", never presented as an allowance.
- **Unrealistic forward jumps:** nominal growth ~11–15%/yr on loans and deposits, consistent
  with shared nominal GDP (real ~5% + CPI ~6–8%) plus the ±scenario adjustments; base FY2026E
  loans rise only ~3.4% because FY2026 is Q4-anchored on 9M-2026 (t=0.25). No cliff jumps.
- **Capital proxy vs actual:** correctly presented as a **proxy**, not actual CAR.
  `x_car_proxy_pct` is book-equity/assets calibrated to the Sep-2026 reported CAR, and the
  review flags that CAR fell 34.08%→24.07% despite rising book equity (risk density/eligibility
  change). No actual RWA/capital numerator is inferred or fabricated.
- **Macro linkage:** assumptions.json points to `../../sector/macro-assumptions/macro.csv`
  (bank-local relative path) and model.mjs loads it; gate macro check passes with the canonical
  macro fingerprint b3c4412d…. FY2026E macro rows are sourced/estimated as documented.

## 6. Reproducibility (independent replay)
I copied financials.csv, assumptions.json, model.mjs + macro.csv into an isolated temp folder
and ran `node model.mjs`. Output: `{rows:1050, checks:176, maxResidual:1.14e-12}` and the
regenerated `forecast.csv` and `checks.md` were **byte-identical** (SHA-256, LF-normalised) to
the committed files (forecast 564ceda4…, checks f312c7b2…). The written checks.md claim
"History 317 rows; forecast 1050 rows; 176 accounting identities, max residual 1.137e-12" is
accurate.

## Verdict
**PASS.** Every required identity holds with zero residual, provenance and `unavailable`
handling are correct, the bank-only framing is consistent, all four filings I fetched agree
with the cited rows, no pitfall is present, and the package reproduces byte-for-byte. The
remaining gaps (no IFRS allowance note, no actual RWA/Tier-1/liquidity ratio, Q3 images) are
correctly left `unavailable` and documented rather than guessed — that is compliant, not a
defect. Fingerprint `c687b8541b2b001cb03c32a39bb629f416e903442f22ee9988f86269f3668a61`
(macro `b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df`). No changes
requested. No owner files were modified by this review.
