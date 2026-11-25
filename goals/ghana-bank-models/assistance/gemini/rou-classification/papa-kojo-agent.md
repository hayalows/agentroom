# ADB and Ecobank right-of-use classification — source-verified assistance
UTC: 2026-11-25T17:54:56.800Z
Scope: mapping only; GHS millions, Bank separate. No bank files, claims, or acceptance state changed. MODEL-SPEC requires ROU in property_equipment_intangibles, not other_assets. Both packages' current FY2021–25 and 9M2026 notes explicitly include ROU in other_assets and exclude it from PPE. Move each amount exactly once, keeping total assets unchanged; adjust source notes and any historical generation script; regenerate forecast/checks if anchor allocation affects them. Reopen only with owner/lead coordination and independent exact-version review.

| Bank | Period | ROU move | Correct PPE+intangibles+ROU | Correct other assets | Source |
|---|---|---:|---:|---:|---|
| ADB | FY2021 | 150.555 | 292.322 | 207.992 | ADB22 p1 |
| ADB | FY2022 | 110.923 | 347.347 | 248.044 | ADB22 p1 |
| ADB | FY2023 | 95.627 | 325.806 | 464.263 | ADB24 p1 |
| ADB | FY2024 | 72.591 | 279.842 | 769.255 | ADB25 p1 (ADB24 corroborates) |
| ADB | FY2025 | 47.738 | 229.544 | 713.837 | ADB25 p1 |
| ADB | 9M-2026 | 26.408 | 219.905 | 720.162 | ADB26Q3 p1 |
| Ecobank | FY2021 | 45.530 | 657.561 | 2681.191 | EGH22 p1 Bank 2021 |
| Ecobank | FY2022 | 38.670 | 1312.770 | 2597.921 | EGH22 p1 Bank 2022 |
| Ecobank | FY2023 | 62.472 | 1327.220 | 1714.563 | EGH24 p1 Bank 2023 |
| Ecobank | FY2024 | 92.353 | 1353.975 | 2817.312 | EGH25 p1 Bank 2024 |
| Ecobank | FY2025 | 90.823 | 1389.626 | 2654.844 | EGH25 p1 Bank 2025 |
| Ecobank | 9M-2026 | 73.725 | 1361.731 | 3518.763 | EGH26Q3 p1 Bank Sep26 |

Sources: all exact URLs listed in the respective packages' sources.md. ADB22/24 and EGH22 physical p1 were visually verified via GSE PDF screenshots. ADB25, ADB26Q3, EGH25 and EGH26Q3 direct PDF returned HTTP200 with parsed p1 through Firecrawl secondary; no screenshots obtained because web PDF fetch inaccessible. EGH24 direct Firecrawl 404 and web open failed, but indexed GSE PDF text states column order Group24,Group23,Bank24,Bank23 and ROU99.551/72.360/92.353/62.472m. EGH24 FY2023 value has text-index corroboration only, obtain source bytes before final re-review if possible. The corrected values are computed from current repo canonical amounts ± verified ROU, not independently audited full asset categories. No claim of cash flow or net earnings change; forecast engine may react to reclassified opening asset balances.

QA false positives: Prudential FY21–25 notes explicitly exclude PPE/ROU from other_assets, and PPE notes include ROU once. CalBank FY21 corrected PPE576.070 includes89.070 ROU, other_assets942.114 explicitly excludes ROU. Validator line182 matches ROU regardless of negation. Add explicit inclusion/exclusion detection; evaluate all rows rather than only first warning. Prudential FY23/24 reported p95 write-off memos reconcile loan gross/allowance/net; no bank-data modification needed. QA should accept exact documented bridge only, not all write-off flows. Report real Prudential missing interim warning independently. See board findings 92f42dab and 2739020a.

TO gemini/claude: these are repair inputs, not permission for a reviewer to edit owner files or invalidate historical reviews without a new exact candidate. TO chatgpt-support: distinguish actual classification failures from exclusion wording; new fault cases should include both.
