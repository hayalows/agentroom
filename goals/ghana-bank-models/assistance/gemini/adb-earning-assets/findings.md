# ADB: material earning-assets and primary-note evidence

2026-11-25 18:10 UTC, Papa Kojo Agent. Supplemental assistance, not a replacement owner package or a formal re-review. Preserve current accepted artifact until lead/owner coordinates revision. Model SHA256 a8c19745aedb75ebce51868c93272cdce13714ceb00c7f63bbfa551048edf503; macro SHA256 b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df.

## Primary evidence

ADB issuer annual report FY2025, [public SIC brokerage mirror](https://www.sicbrokerage.com/files/press_releases/PR-129_AGRICULTURAL_DEVELOPMENT_BANK_PLC_ANNUAL_REPORT_AND_FINANCIAL_STATEMENTS_31_DECEMBER_2025%282%29.pdf), also GSE filing cited in ADB sources.md. Indexed PDF text recovered; visual screenshot requests returned cache miss. Values below GHS million, reported GHS thousands divided by 1,000. Pages are printed page numbers, not viewer indexes. Owner should verify rendered page before replacing canonical data.

| Item | FY2025 | FY2024 | Source |
|---|---:|---:|---|
| Loan interest |562.031|691.103| Note 8, p113 |
| Govt security interest |1398.716|701.208| Note 8, p113 |
| Interbank placements interest |133.097|179.316| Note 8, p113 |
| Total interest income |2093.844|1571.627| Note 8, p113 |
| Customer deposits interest |599.998|753.485| Note 9, p113 |
| Interbank borrowing interest |0.431|0| Note 9, p113 |
| Long term borrowing interest |118.545|88.757| Note 9, p113 |
| Lease interest |4.624|6.204| Note 9, p113 |
| Total interest expense |723.598|848.446| Note 9, p113 |
| Cash in hand |484.966|519.449| Note 18, p117 |
| Bank of Ghana balance |5110.930|2170.801| Note 18, p117 |
| Included mandatory reserve |3306.666|1869.385| Note 18, p117 |
| Nostro |744.754|2603.989| Note 18, p117 |
| Treasury bills under 91 days |3561.795|1882.678| Note 18, p117 |
| Total cash |9902.445|7176.917| Note 18, p117 |
| Restricted cash |31.350|33.810| Note 19, p118 |
| T-bills in investment securities |2053.618|893.841| Note 20, p118 |
| Govt bonds |3006.360|2917.964| Note 20, p118 |
| Securities ECL |30.013|7.569| Note 20, p118 |
| Net investment securities |5029.965|3804.236| Note 20, p118 |
| Gross loans |3894.061|4225.264| Note 21, p121 |
| Loan ECL |1882.330|1650.737| Note 21, p121 |
| Net loans |2011.731|2574.527| Note 21, p121 |
| Regulatory CET1/Tier 1 capital |962.029|-260.363| Note 5.7.2, p102 (not p101) |
| Tier 2 capital |76.432|126.956| Note 5.7.2, p102 |
| Total regulatory capital |1038.461|-133.407| Note 5.7.2, p102 |
| Risk weighted assets |3821.530|4231.879| Note 5.7.2, p102 |
| CAR |27.17%|-3.15%| Note 5.7.2, p102 |

The three income components and four expense components tie exactly to historical totals. Cash components tie exactly. Gross minus ECL equals net in both years. Correct FY2025 gross LDR is 3894.061 / 13220.185 = 29.455%, not 15.217% net LDR; FY2024 gross LDR 35.076% vs 21.37% net LDR. FY2025 loan interest / average gross loans = 13.84%, versus 24.51% on average net loans. Historical actual effective rates on average combined govt securities plus short bills = 19.59%; placements/Nostro proxy 7.95% (not contractual yield). Customer deposit interest / average deposits = 4.75%; borrowing interest excluding leases / average borrowings = 8.86%. These are historical implied yields, not FY2026 estimates. Note 20 quotes FY25 T-bill 16.40%, bonds 9.18%; avoid double-counting govt interest already allocated to short bills.

Capital disclosure contradicts using book equity as actual regulatory numerator. FY25 regulatory capital is 41.91% of book equity; RWA 21.36% of total assets (book-equity-anchored model is an explicitly illustrative proxy, not a reported RWA). Use historical regulatory calibration and latest reported interim CAR, retain uncertainty on interim numerator/denominator and stress alternative RWA density/capital conversion. Note p122 regulatory NPL ratios FY25 70.53%, FY24 75.36% vs summary 75.26%; report disagreement, do not silently pick a number. FY25 gross NPL regulatory exposure vs accounting Stage 3 are different bases; avoid dividing regulatory gross NPL by IFRS accounting gross if definitions differ.

## Reproducible sensitivity

Script sensitivity.py committed 26c3947, tested on clean LF laptop checkout 18:09:39 UTC. Exact baseline replay (all 600 forecast rows). 45 scenario-year checks across all three weights, maximum residual in four independently recomputed balances/earnings bridges GHS0.002m or less. No canonical bank files changed.

Current owner engine includes interest on net loans and investment securities but zero earnings on the combined cash bucket. Since short bills are in cash separately from investment securities, this sensitivity retains all original owner assumptions, changes only incremental Q4 and forward short-bill interest, and recalculates equity and liquid assets through original iterative model. 2025 observed allocation: short bills / (cash minus mandatory reserves) = 54.001%; apply 0%, 50%, 100% of that share to estimated non-reserve cash, yield at scenario 91-day bill. No placements income added. 9M26 actuals frozen. 2026 macro rate is full-year proxy, not a distinct Q4 observation. This is not a proposed final forecast: 2026 short-bill mix is unavailable, and funding, loan yield, statutory reserve, gross balances, capital treatment and historical yield calibration also require attention.

| Scenario | Year | PAT owner | PAT half share | PAT historical share | CAR owner | CAR historical share |
|---|---|---:|---:|---:|---:|---:|
| base |2026E|276.071|304.412|323.514|26.678%|27.078%|
| base |2027E|-146.306|-28.033|57.694|23.104%|25.068%|
| base |2030E|-1008.973|-780.987|-538.831|2.884%|12.379%|
| downside |2030E|-1460.952|-1203.084|-915.610|-13.151%|2.453%|
| upside |2030E|-518.557|-318.805|-111.085|11.533%|17.924%|

The published 2027 base loss reverses under historical-share sensitivity. This is material. Even after incremental yield, FY2030E base CAR proxy remains below 13%, so no claim of solvency or guaranteed recovery. Reopen ADB jointly with existing ROU repair and re-review source mapping/forecast calibration rather than just change presentation. Source-specific note evidence can populate genuine FY24/25 previously unavailable rows and memo items; no guesses for 9M26 gross loans, ECL or capital breakdown.

Run from checkout: python -I goals/ghana-bank-models/assistance/gemini/adb-earning-assets/sensitivity.py goals/ghana-bank-models
