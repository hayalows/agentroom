# Ghana bank financial models: lead summary (INTERIM)

Written by the lead (claude) on 2026-11-25 after returning from a usage pause. **This is an interim summary, not the final sign-off.** The goal is complete only when all 23 banks are accepted, the shared pieces are independently reviewed, and this file is refreshed. Nothing here is investment advice, a price target, or legal advice.

## 1. Where the goal stands (observed from a clean LF supervisor run)
- **18 of 23 bank models are accepted** (core gate passes, a distinct reviewer's current-version PASS, no unresolved blocking review, owner marked done): access-bank-ghana, adb, bank-of-africa-ghana, calbank, consolidated-bank-ghana, ecobank-ghana, fbnbank-ghana, fidelity-bank-ghana, first-atlantic-bank, first-national-bank-ghana, gcb, gtbank-ghana, nib, societe-generale-ghana, stanbic-bank-ghana, standard-chartered-ghana, uba-ghana, zenith-bank-ghana. (Stanbic closed after my lead decision authorised one bounded review round; see `review-resolutions/stanbic-bank-ghana.md`.)
- **5 are open:** absa-ghana and republic-bank-ghana (re-review of repairs), prudential-bank (re-review; the QA sweep also flags unexplained gross-loan bridge gaps there), omnibsic-bank and umb (still being built).
- Shared pieces: roster verification **done**; macro assumptions **done** (v1.1, reviewed); QA sweep, sector roll-up and peer comparison are built. The roll-up and peer comparison each have a Codex PASS on a pinned snapshot; my independent review of the peer comparison asks for two labelling fixes (ROE is not meaningful for NIB, whose equity was negative at FY2024; and its README is stale). The QA sweep is stewarded by chatgpt-support, with a tested patch from me in `assistance/claude/`.
- **Caveat on the roll-up snapshot:** the committed accepted-only roll-up (`sector/sector-rollup/rollup.md`, source commit 3f65697) counts **16** accepted banks. Two more (calbank, stanbic) have been accepted since. The numbers below are that snapshot and need a refresh by the roll-up steward before they are final.

## 2. What the accepted models show (snapshot of 16 banks; bank-only statements, GHS)
| Measure | FY2025 | Share of Bank of Ghana sector total |
| --- | --- | --- |
| Total assets | 311.4bn | about 70% of 446.9bn |
| Customer deposits | 233.0bn | about 72% of 325.3bn |
| Profit after tax | 10.1bn | n/a |

- **Profit path of the 16 banks:** 3.3bn (FY2021), **-4.5bn (FY2022, the domestic debt exchange year)**, 5.0bn (FY2023), 7.6bn (FY2024), 10.1bn (FY2025), 7.5bn in the first nine months of 2026 (15 banks reporting).
- **Banks hold far more deposits than loans.** Matched-bank net loans are 28.6% of deposits (FY2025). Earnings follow money-market rates and currency trading more than lending.
- **Return on equity** on closing equity is about 24% across the matched banks (FY2025). The Bank of Ghana's own sector figure is 30.8% for Dec 2025, but definitions differ (average vs closing equity), so the two are not directly comparable.
- **Wide spread between banks:** closing-equity ROE ranges from about 0.5% to 34%, and cost-to-income from about 26% to 86%. Several mid-size banks have thin profits and very high cost ratios.
- **Rates matter.** Shared macro (Bank of Ghana, Nov 2026): the policy rate was cut from 14% to 11% on 18 Nov 2026; inflation 5.5% (Oct 2026); the 91-day bill about 4.5%; a uniform 20% cedi cash reserve ratio since 4 June 2026; sector capital adequacy 18.5% and non-performing loans 13.1% (Oct 2026).
- **Forecast totals are scenarios, not predictions.** On the shared macro paths the accepted banks' combined base-case profit rises from about 9.8bn (FY2026E) to 15.1bn (FY2030E), while the downside falls to about 4.5bn and the upside reaches about 21.4bn. Banks with large liquid balances can earn *more* in the "downside" rate scenario in the early years (we saw this in at least Standard Chartered Ghana and GTBank Ghana), so "downside" does not mean lower profit in every year.

## 3. What was verified, and how
- **Arithmetic:** every accepted bank passes the automatic gate (balance sheet, net interest income and profit bridges for every period and every forecast scenario-year), and the protocol requires a distinct reviewer's current-version PASS for each. In the reviews I read, reviewers replayed the models and recomputed these bridges; I did not re-read every review for every bank.
- **Sources:** each bank's reported numbers carry a source and page. Reviewers spot-checked rows against the issuer's own filings; some also opened full annual-report notes. Spot-checking is **not** a full audit of every cell.
- **Review found real errors, and they were fixed.** Examples I saw first-hand: CalBank's first forecast overstated FY2026E interest income by 41% and interest expense by 168% and overstated its capital ratio by about 3 points; Standard Chartered restated FY2023 in a later report (profit 814.7m, not 864.4m); GTBank put balances held with other banks inside cash (found by Codex; the steward's repair then received an independent PASS, which I did not re-read line by line); several banks' forecasts initially did not add up to total assets.
- **Method:** one shared format (`MODEL-SPEC.md`), one shared macro file, a claim system (one owner per bank), at least one independent PASS per bank, and a round cap with a lead decision.

## 4. What is unavailable or uncertain (do not read these as facts)
- **Regulatory minimum paid-up capital (GHS 400m) is unconfirmed for 2026.** It comes from a 2017 notice; a 2026 search found no newer universal-bank rule, which is not proof. The 13% minimum capital ratio is confirmed from the Bank of Ghana's September 2026 report.
- **Macro history gaps:** inflation and Treasury-bill history for 2021 to 2024 and GDP for 2021 to 2022 are `unavailable` in the shared macro file. Forecast paths for FY2027E to FY2030E are the lead's estimates with reasoning in the file, not forecasts by the Bank of Ghana.
- **Capital ratios in forecasts are proxies,** calibrated to each bank's reported ratio at the latest date, not regulatory returns. Out-of-sample tests showed gaps of a few points in some banks.
- **Loan detail:** gross loans and loan-loss allowances are `unavailable` for several banks (summary statements print net loans only); some owners that read the annual-report notes filled them in; I did not check which.
- **Ownership percentages and listing status** are recorded bank by bank where a filing states them; otherwise they are marked unavailable or inferred.
- **Net trading income** is the least reliable line in many banks (it swung by multiples over five years). Forecasts assume fades chosen by each owner.
- **Calibration:** most interest spreads were chosen so the forecast matches nine-month 2026 actuals. That is a fit, not a validation, and every owner was asked to disclose it.

## 5. What remains
1. Finish and accept the five open banks (absa, omnibsic, umb, prudential, republic).
2. Independent review and refresh of the accepted-only sector roll-up (it must include calbank and stanbic) and of the peer comparison; review of the QA sweep.
3. Re-run the roll-up and peer comparison from a clean LF checkout once all 23 banks are accepted, and refresh this summary from those outputs.
4. Human sign-off. The room's agents verify arithmetic and sources; they are not lawyers, auditors or licensed advisers.

## 6. How to reproduce
Use a clean checkout with LF line endings (`git clone -c core.autocrlf=false`). Status: `node scripts/supervisor.mjs --json`. Bank models: `python model.py` (or `node model.mjs` for GCB) inside each `banks/<slug>/` folder. Roll-up: `node goals/ghana-bank-models/sector/sector-rollup/rollup.mjs --output-dir <path outside the repo>`. QA sweep: `python goals/ghana-bank-models/sector/qa-sweep/validate.py`.

## 7. Late-session update (claude, lead)
- **18 of 23 ordinary-accepted** at the last clean supervisor run. ADB was reopened after an independent source check found material omissions (cash and placement earnings, regulatory-capital numerator); ADB v2 is in re-review. Absa awaits Gemini's own exact re-review.
- **Three conditional banks** (policy: `review-resolutions/CONDITIONAL-POLICY.md`): prudential-bank (30 Sep 2026 statement unavailable: issuer site 502 and no mirror), omnibsic-bank (FY2021 annual unavailable), umb (FY2025 annual and 2026 interim unavailable). They will be counted and labelled separately and never inside an ordinary accepted total.
- Replays by the lead: Prudential and OmniBSIC `model.mjs` reproduce `forecast.csv` and `checks.md` byte for byte in an isolated copy.
- **Update 19:23Z:** Absa is now accepted (Gemini round-2 PASS plus two other exact PASS reviews). Ecobank was reopened by its owner for a six-period right-of-use asset repair and awaits a fresh independent review, so the ordinary count is still 18. ADB v2 and Prudential (conditional) are waiting for owner closure. OmniBSIC and UMB are conditional and cannot pass the five-annual-period gate by design; peer-comparison now emits a separate conditional file (lead round-3 PASS, 123 cells matched).
