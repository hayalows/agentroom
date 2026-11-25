# Financial completion bridge — 25 November 2026

UTC 2026-11-25T19:33:55.773Z. Source pin 70172b9ba758ba9559f99ed010088c0094c0deae. This is an arithmetic planning bridge, NOT a new full supervisor run or final published sector roll-up. Last lead verified 18 ordinary at 19:23:49Z; Absa in, Ecobank reopened. Current owner claims still need closure. Earlier 18-bank arithmetic cross-check c38767ca and Codex frozen 67ff7c9 cohort (Ecobank in, Absa out) are the starting point. Extracted actual current CSV values for Absa, Ecobank and ADB at this pin; Ecobank prior FY30 scenario values restored by documented round4 PAT deltas. All amounts GHS millions.

| Cohort | FY25 assets | FY25 deposits | FY25 PAT | 9M26 assets | 9M26 deposits | 9M26 PAT | FY30E base PAT | downside | upside |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Earlier 18 (Ecobank in, Absa out) |354359.375272|260829.060712|11904.035959|393258.877|288779.446|8589.583|17936.419|6560.068|24585.746|
| Absa addition |31529.847|19185.669|1762.411|35945.763|21185.474|985.331|1657.106|1360.823|1810.655|
| Earlier Ecobank subtraction |46076.237|30397.499|1792.352|53807.300|36100.191|1325.413|1910.179|1351.611|2641.911|
| 18 after swap (planning reconciliation) |339812.985272|249617.230712|11874.094959|375397.340|273864.729|8249.501|17683.346|6569.280|23754.490|
| Ecobank round4 addition |46076.237|30397.499|1792.352|53807.300|36100.191|1325.413|1910.075|1351.485|2641.818|
| 19 if Ecobank closes |385889.222272|280014.729712|13666.446959|429204.640|309964.920|9574.914|19593.421|7920.765|26396.308|
| ADB current addition |17887.521|13220.185|367.291|20277.994|15362.718|301.714|-308.243|-683.644|80.277|
| 20 if both close |403776.743272|293234.914712|14033.737959|449482.634|325327.638|9876.628|19285.178|7237.121|26476.585|

9M totals cover one fewer bank than each cohort (CBG reports H1 only in the model). No mix of H1 and 9M. FY25 and FY30 coverage 18/19/20 respectively. Forecasts are undiscounted scenario estimates, not guaranteed outcomes. Prudential, OmniBSIC and UMB excluded from every row, regardless of conditional closure. UMB's newer PwC secondary benchmark and stale-anchor warning should accompany any conditional output. This bridge does not replace clean LF same-pin regeneration, independent output verification or lead acceptance; use it as a numeric cross-check when those are completed.

Completion queue: Ecobank owner Gemini bind cdd36f76 and close (Codex and Support independent exact PASS); ADB lead completes eligible source check and verdict before steward closes; Prudential and OmniBSIC lead explicit conditional-only closure; UMB Gemini eligible scoped review with auxiliary hash, then lead conditional-only closure. Do not edit other agents' claims or record acceptance prematurely.
