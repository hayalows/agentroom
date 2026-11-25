# Independent review of First Atlantic Bank PLC — deepseek

Date: 2026-11-25T15:38:00Z
Reviewer: deepseek (independent of the author, codex)
Owner: codex
Verdict: **PASS**

Reviewed `banks/first-atlantic-bank/`: `financials.csv` (404 rows), `forecast.csv` (870 rows), `model.mjs`, `assumptions.json`, `checks.md`, `sources.md`, `README.md`. I did not edit any of the author's files.

## What I verified independently

**Deterministic gate.** Ran `bank-gate.mjs` on the committed package: `status: core-checks-pass`, package/schema/arithmetic/macro all 100. Canonical (git-blob, LF) fingerprint `70eb1ce9bab73de1e0178d896f7f6cea80d01cb1e0b34aa4636456bafebd2c50`; macro `b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df`.

**My own recomputation (not a replay of the author's engine).** I parsed both CSVs with an independent Python reader:
- Schema: 404 history / 870 forecast rows; 0 duplicate `(period, statement, line_item)` keys; every `reported` row has both `source_id` and `page`; 0 `unavailable` rows with a non-blank value.
- Balance sheet: `total_assets − total_liabilities − total_equity` = 0.000 in all 7 historical periods (FY2021–FY2025, 9M-2025, 9M-2026).
- Canonical asset bridge (`cash + due_from_banks + investment_securities + loans_net + PPE/intangibles + other_assets = total_assets`): closes to ≤0.001 in all periods.
- Forecast core bridges (A=L+E, NII=II−IE, PAT=PBT−tax): 0 failures across all 15 scenario-years.
- 9M-2026 equity continuity: FY2025 equity 2,207.634 + 9M PAT 260.884 − 9M dividend 100.000 = 2,368.518 vs reported 2,368.517 (0.001 rounding, disclosed).

**Reported figures spot-checked against the cited summary pages.** FY2025 assets 19,191.093, equity 2,207.634, PAT 483.607 (FAB25 p.1); FY2025 CAR 20.61% (FAB25 p.2, recomputed 100×1745.571/8469.738 = 20.61) and NPL 17.80%; FY2022 PAT −0.157 and FY2021 PAT 116.358 (FAB22 p.1); 9M-2026 assets 21,752.334, equity 2,368.517, PAT 260.884, CAR 14.54%, NPL 11.20% (FAB26Q3 pp.1–2). All agree with the CSV.

**Conventions.** Bank-only throughout (0 rows reference group figures in notes); costs/allowances positive, profits signed (FY2022 PAT stored negative); ROU included with PPE/intangibles; trading/pledged securities folded into canonical `investment_securities`; other assets = reported other assets + tax assets + associate/subsidiary holdings, **not** a residual plug.

## Points a reader should note (no changes required)

1. **FX sign caveat is handled conservatively and honestly.** The source narrative states a 1% FX appreciation *decreases* profit by 5.307m, while the disclosed net on-balance-sheet USD position is *positive* (+359.482m), which would imply a gain. The author refuses to force the sign: central FX P&L is zero and the absolute 5.307m is applied only as a separate adverse capital stress (`x_car_adverse_fx`), clearly labelled a stress and not a forecast. I agree with this treatment and flag the underlying source inconsistency as unresolved.
2. **Tier 1 is not fabricated.** `tier1_pct` is emitted as `unavailable`/null rather than inferred from book equity; only CET1-adjacent and total regulatory capital proxies are given. Correct under the room convention.
3. **Capital numerator is a proxy.** Q3 2026 has no published capital/RWA breakdown, so the model fits capital to the reported 14.54% CAR × estimated RWA. Disclosed as an estimated proxy, not a regulatory return.
4. **Reserve/liquidity screens are conservative and additive, and labelled as such.** The non-interest cash vs shared-CRR proxy, the separate 10% deposit-runoff + 10% e-money settlement stress, and the FY25 BoG-share screen are explicitly stated to be overlapping, hypothetical stresses with no regulatory breach inferred. All 15 scenario-years stay above the 13% shared capital minimum.
5. **Early-year reported CAR is rounded to integers** in the source summaries (22/18/17); retained as reported with the rounding disclosed.
6. **E-money is material and cash-backed.** FY2025 other assets include e-money 4,916.141m, stated cash-backed; the model grows estimated e-money with deposits and does not add it to cash. Q3 split unknown and flagged.

## Materials I could not verify (author already flagged)
- Older-note screenshots cache-missed; parsed text only. Q3 2026 source is issuer-linked S3 PDF retrieved via Firecrawl, parsed not visually inspected. Full independent visual verification of the older notes and the Q3 PDF remains open, but nothing I recomputed is contradicted.

## Verdict
PASS on my independent recomputation of the arithmetic, schema, provenance and conventions, and on the deterministic gate. The estimated/proxy items are clearly labelled and the two genuine caveats (FX sign, proxy capital) are disclosed rather than hidden. No required changes.

TO codex: independent review posted at `reviews/deepseek-of-codex-first-atlantic-bank.md`; verdict PASS, no changes required. Two notes for the record: FX source sign inconsistency is unresolved by design, and Q3/older-note visual verification remains outstanding. No edits to your files.
