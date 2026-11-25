# UMB: new primary interim source recovery and source-gap log

Date: 2026-11-25T19:03:28.706Z. Named source-only assistance; Codex owns the canonical model. No canonical model files modified.

## Newly recovered source documents
- UMB25Q1: https://ghanaiantimes.com.gh/wp-content/uploads/2025/12/UMB-2025-Q1-Unaudited-Financials.pdf (Ghanaian Times public attachment 213324, uploaded 31 Dec 2025 18:41:45, 1 physical page).
- UMB25H1: https://ghanaiantimes.com.gh/wp-content/uploads/2025/12/UMB-2025-Unaudited-Financials-June-Q2-.pdf (attachment 213328, uploaded 31 Dec 2025 18:57:50, 1 physical page).
- Both are issuer-authored standalone bank unaudited summaries, full GHS units, with 2024 comparative columns. Firecrawl secondary HTTP200 and independently indexed web PDF text agree. Web page screenshot attempts cache-missed, no new visual confirmation claimed. PDF metadata says Draft 5/6, but page face says unaudited and has director signature labels; retain publication provenance and verify visual if used in owner package.

Source-mapped financials-q1-h1-2024-2025.csv (15b3b544) contains 172 rows across Q1-2024/25 and H1-2024/25, 43 per period including unavailable rows and nonadditive memos. Reported values in GHS millions at six decimals, exact unit conversion. Source-positive impairment expense is actually a reversal as corroborated by cash-flow sign; canonical expense negative. PPE includes ROU + intangibles. Net LDR derived, not gross. All 32 full-GHS arithmetic identities (NII, TOI, PBT, PAT, assets component sum, liabilities component sum, equity component sum, total BS) reconcile to zero. No 2025 year-end or 2026 figures inferred from these documents.

## What the 2025 trajectory tells us (GHS millions)
| Quarter end | Q1 | H1 | 9M |
|---|---:|---:|---:|
| Assets | 5731.661097 | 7685.610630 | 11820.440581 |
| Deposits | 5338.063292 | 6330.261694 | 8554.600075 |
| Securities | 1682.101381 | 2900.126377 | 6547.185433 |
| Borrowings | 0.000000 | 922.274889 | 2343.813978 |
| Equity | 21.116505 | 61.884227 | 476.200814 |
| Reported CAR | -13.74% | -11.60% | 6.46% (conditional on share-deposit approval) |
| NPL | 59.26% | 52.40% | 45.89% |

Quarter flows calculated by subtracting preceding YTD statement (not annualizing):
| Actual quarter | NII | PBT | Impairment reversal | PBT before reversal | PAT |
|---|---:|---:|---:|---:|---:|
| Q1 | 28.914773 | 44.611378 | 32.357824 | 12.253554 | 33.458533 |
| Q2 | 78.459411 | 54.356963 | 38.911816 | 15.445147 | 40.767723 |
| Q3 | 50.257291 | 161.840861 | 134.563218 | 27.277643 | 150.069658 |

9M PAT224.296m includes impairment reversal205.833m; Q3 alone produced 150.070m PAT and 134.563m reversal, so extrapolating the Q3 profit mechanically would be inappropriate. H1 to 9M deposits +35.14%, securities +125.76%, borrowings +154.13%; equity includes 264.247m deposit for shares. Q3 pretax income excluding reversal was only 27.278m. Existing owner conservative conditional 2025E base Q4 PAT7.262m and FY25 base PAT231.558m already does not extrapolate recoveries. B&FT June3 2026 rounded secondary FY25 PAT267.2m implies Q4 PAT42.904m, not a reported quarter in our dataset. Do not backfill.

## Source-gap investigation
Public WordPress attachment inventory, queried via Firecrawl secondary, returned exactly five UMB PDFs: FY23, FY24, 2025 Q1, H1, 9M. Query https://ghanaiantimes.com.gh/wp-json/wp/v2/media?search=UMB&mime_type=application%2Fpdf&per_page=100&_fields=id,date,title,source_url,mime_type . Exact Universal Merchant Bank search and financial statement search after 2026-05-01 both returned empty. This strengthens the finding of no later PDF in that newspaper inventory, not proof no public filing exists elsewhere.
Issuer newsroom lists 2025 ANNUAL REPORT; the known /docs/UMB%202025_26%20ANNUAL%20REPORT.pdf frontend target remains documented broken; Firecrawl map independently finds only that same target (not a recovered file). The Banker Database FY2025 index is not an accessible public filing.
Finex Insights/Graphic November10 report indicates FY25 auditor reporting milestone May29 2026, corroborates existence but no source bytes: https://www.finexinsights.com/post/ghana-s-2025-banking-audit-calendar-calbank-leads-as-march-reporting-rush-dominates ; https://www.graphic.com.gh/business/business-news/2025-banking-audit-calendar-calbank-leads-as-march-reporting-rush-dominates.html .
B&FT June3 article https://thebftonline.com/article/leadership-matters-more-than-the-balance-sheet-the-case-of-universal-merchant-bank repeats rounded FY25 PAT267.2m/equity551.3m/deposits10.4bn/NPL52.32% and Q1 2026 PAT81m; secondary context only. Official PwC Ghana Banking Survey 2026 landing links https://www.pwc.com/gh/en/assets/pdf/ghana-banking-survey-2026.pdf (28.5MB), but Firecrawl and web could not retrieve the report this session. No new FY25/FY26 primary values recovered.
Recommend owner consider optional Q1/H1 data as a source supplement and keep existing exact conditional package unchanged while awaiting independent reviews unless lead requests revision. No scope waiver.
