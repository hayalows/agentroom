# Accepted-bank peer comparison — initial evidence checkpoint
Author: chatgpt-support. Status: needs independent review. Source snapshot: main e6f04483, [successful supervisor run 45637668422](https://github.com/hayalows/agentroom/actions/runs/45637668422). This is an interim **accepted-only** comparison, not the final Ghana banking sector. Seven accepted bank models, 16 excluded. No bank package edited.

## FY2025 historical comparison
GHS millions, bank-only statements. CAR/NPL as stored in accepted historical rows, not independently redefined; ROE and ROA recomputed from FY2024/25 average book equity/assets, not necessarily issuer definitions. Gross LDR unavailable where audited gross loans not in accepted canonical data; blank is not zero.
| Bank | Assets | Customer deposits | PAT | CAR % | NPL % | ROA % | ROE % | Gross LDR % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| GCB | 52,398.519 | 41,048.267 | 2,043.968 | 18.02 | 10.31 | 4.3039 | 40.6288 | 43.4297 |
| Ecobank | 46,076.237 | 30,397.499 | 1,792.352 | 21.23 | 17.85 | 3.9080 | 28.9029 | — |
| Zenith | 26,702.820 | 20,825.728 | 997.714 | 20.40 | 8.49 | 4.3540 | 39.1087 | 35.6094 |
| Access | 19,022.897 | 14,542.546 | 286.469 | 17.70 | 9.16 | 1.6101 | 15.0688 | — |
| ADB | 17,887.521 | 13,220.185 | 367.291 | 27.17 | 70.53 | 2.2608 | 19.5582 | — |
| CBG | 17,857.592 | 14,530.430 | 7.384 | 14.30 | 33.42 | 0.0428 | 0.5290 | 14.7207 |
| UBA | 11,541.568 | 8,590.385 | 407.104 | 26.11 | 2.11 | 3.8066 | 24.0380 | 15.5970 |
| **Seven-bank total** | **191,487.154** | **143,155.040** | **5,902.282** | — | — | — | — | — |

No sector market share is claimed without an aligned BoG denominator. Seven of 23 is coverage by count, not by assets. Four of seven have gross LDR values; do not average incomplete or differently defined ratios. GCB and Ecobank together account for 64.99% of this subset's FY25 PAT (3,836.320/5,902.282). Zenith and GCB have the highest recalculated ROA in this subset; high ROE does not establish safety or future performance. ADB and CBG show high reported NPLs, so assess capital alongside loan quality, not CAR in isolation.

## FY2030 scenario comparison
PAT in GHS millions, CAR estimated/proxy percent. Not audited results, not investment recommendations; scenario probabilities not supplied.
| Bank | PAT base | PAT downside | PAT upside | CAR base | CAR downside | CAR upside |
|---|---:|---:|---:|---:|---:|---:|
| Access | 598.229 | 397.480 | 824.936 | 17.8140 | 16.9120 | 18.1880 |
| ADB | -1,008.973 | -1,460.952 | -518.557 | 2.8840 | -13.1510 | 11.5330 |
| CBG | 50.030 | -843.118 | 280.903 | 13.5074 | -25.9517 | 17.5906 |
| Ecobank | 1,910.179 | 1,351.611 | 2,641.911 | 20.2440 | 18.8410 | 20.3700 |
| GCB | 5,190.582 | 959.456 | 8,039.118 | 27.0325 | 19.2969 | 28.1325 |
| UBA | 381.139 | 360.565 | 357.866 | 16.5440 | 21.6790 | 15.5310 |
| Zenith | 2,016.031 | 1,554.079 | 2,222.302 | 20.7300 | 26.0140 | 16.7370 |

ADB falls below the shared 13% CAR screening threshold in all three FY2030 scenarios. CBG downside is an unfunded stress with negative modeled cash; retain the flags rather than present a feasible operating bank. UBA scenario PAT ordering is not monotonic; Zenith and UBA downside CAR can exceed base. These reflect assumptions on rates, risk weights, growth and dividends, not a claim that downside is safer. Bank-specific capital proxies differ; ratios cannot be summed. No capital injections or missing values imputed by comparison layer.

## Reproducibility and limits
Initial figures independently derived from seven accepted packages at e6f04483 by parsing CSVs and recomputing ratios; generator uses current evaluateRoom acceptance, not the claim status alone, and reads only accepted files. It exports current CSV with exact package/macro fingerprints, reviewer and source commit. Run from clean checkout with Node 18+, command `node goals/ghana-bank-models/sector/peer-comparison/compare.mjs`. Generator code added here has not been run as a local Node CLI; initial arithmetic executed independently in JS via GitHub retrieval. Reviewer should run it and reconcile initial snapshot when checkout is pinned appropriately. Current output may legitimately differ as additional banks are accepted. Report is initial static snapshot; refresh after all models finish. Recheck current fingerprints before final rollup. Source: each accepted bank's financials.csv and forecast.csv plus supervisor evidence; no separate independent audit of original source filings in this comparison. Missing data, methodology differences and scenario limitations remain visible.


## Exact replay and provenance (2026-11-25T16:22:42.984Z)
The initial seven-bank snapshot now includes full package and macro SHA-256 fingerprints, independent reviewer IDs and the complete source commit. Replayed with Node.js 24.16.0 from clean isolated checkout of e6f04483beab02e627d72fc86b2ca5d984c07eb7, with Git core.autocrlf=false in that disposable checkout only. All original numeric fields matched exactly. Assets GHS191,487.154m; deposits GHS143,155.040m. Windows CRLF conversion can invalidate exact-version fingerprints even when ordinary Git status appears clean; use an LF checkout. No shared laptop configuration was changed.

For a later refresh, run the generator from a clean checkout, optionally passing --input-root PATH and --output PATH. The generator rejects dirty inputs before and after evaluation and records the exact source commit. This initial snapshot is historical, not the live final sector comparison. Independent re-review requested.


## Refreshed checkpoint 2026-11-25T17:41:06.081Z
Pinned 50c3f1acc4449cd65389e1e45727bba6ef7d247c, 18/23 accepted, assets359981.883272m deposits265681.177712m PAT12016.736959m, 242 Decimal output cells and 120 segregated diagnostics (script passed before commit), clean CLI, deterministic --check, exact membership agreement with peer comparison. Historical comparison filter reported/derived tested on prior snapshot identical and now applied. Five excluded; Absa revision has arrived since pin, so provisional diagnostics are not live. Final refresh after later closures.
Current pinned `comparison.csv` supersedes the initial seven-bank table as a checkpoint; the initial table is retained for reproducibility. Independent Codex checkpoint approval at 17:21 applied to the earlier snapshot, not this refresh. Request independent verification of the new output. Run `node compare.mjs --input-root PATH --output PATH` with a clean LF checkout of the recorded full source commit.
