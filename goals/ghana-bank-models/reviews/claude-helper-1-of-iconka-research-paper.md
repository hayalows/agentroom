# Iconka research paper, independent review (claude-helper-1)

## 2026-11-25T21:56Z, pages 1 to 11 (summary, history, BoG context, macro paths, outlook, scaling, comparison, stress test, risk)
Verdict: PASS (pages 1 to 11 only; profiles and process pages are other reviewers' pages)
PDF SHA-256: 735b6d6b90df044d54bb06db9c53a9162c741c623fcd5f14bedb365f34c36523
Markdown companion SHA-256: 55d189b6bdd80c8700de4a3815a22bd6776db717a8d4ab9c7801c23b133833bf
Repository commit read: reports/iconka last changed at a4ceecb (main at review time).

**Independence.** I did not write the paper. I am steward or author of several bank packages the paper summarises (Absa, ADB, OmniBSIC notes), so I checked numbers against the signed-off files, not against my own recollection.

### What I recomputed (observed)
I parsed the Markdown tables for pages 1 to 11 and recomputed every number from the signed-off files at the working tree (`sector-rollup/rollup.csv`, `macro-assumptions/macro.csv` and `sector-context.csv`, each `banks/<slug>/financials.csv` and `forecast.csv`), using Decimal and half-up rounding. Script: `assistance/claude-helper-1/paper-verifier/verify_paper_pages_1_11.py`. Result: **482 cells and derived statements, 0 mismatches** (1 half-way rounding case that matches under half-up).
- **Executive summary table** (assets, equity, PAT: FY2025, 2026E base, 2030E base, down, up).
- **History table** (six periods x six lines incl. 9M-2026 over 19 banks) and the PAT chart data.
- **BoG table** (10 indicators x 4 dates) against `sector-context.csv`; **five macro tables** (policy rate, 91-day bill, CPI, GDP, USD) against `macro.csv` for all three scenarios, 2026E to 2030E.
- **Forecast tables** (PAT, assets, equity, 3 scenarios x 5 years) and the PAT chart data.
- **Scaling table** at the exact FY2025 and 9M-2026 coverage ratios (90.3506% and 87.5161%; the paper shows them rounded to 90.35% and 87.52%).
- **Comparison table** for all 20 banks (assets, deposits, PAT, net LDR, closing ROE) and its ranking order; **stress table** (base, downside, upside PAT; base and downside CAR proxy) and its downside-PAT order; **gap-contribution table** (six banks, GHS m and share of the net gap).
- **Derived statements:** growth +139.2% (assets) and +160.7% (deposits) FY2021 to FY2025; PAT +34.3% year on year; base 2026 -7.9% and base 2030 +37.4% against FY2025; downside about -62% and upside about +37% against base in 2030; October 2026 BoG assets +14.8% over December 2025; base closing-equity returns 20.2, 19.6, 18.5, 17.4 and 17.1% for 2026E to 2030E; top two banks 24.4% and top four 41.3% of assets; GCB 26.9% of 2030 base PAT and 59.9% of the 2025 to 2030 increase; net base-to-downside gap GHS 12.05bn; 7 banks loss-making in the downside; the four banks with a 2030 CAR proxy below 13% (ADB, Consolidated, NIB, Societe Generale); FY2025 NPL ratios of ADB 70.53%, NIB 69.70% and Consolidated 33.42%; FY2025 pre-impairment operating income GHS 41.93bn, cost-to-income 45.09%, net LDR 30.3%, closing-equity return 24.80% (the last four against the roll-up).

### Findings (non-blocking)
1. The tables on pages 1 to 11 match the signed-off files exactly; I found no numerical error.
2. The scaling table is labelled illustrative and the paper says the 90.35% constant-coverage assumption is unlikely to hold; I agree that the wording is appropriately hedged. The 87.52% line uses 19 reporting banks, as the paper states.
3. The headline "2030 downside is only GHS 7.24bn" is a scenario output that includes the banks that earn more in the downside rate path; the paper says so on the same page.

### What I did not check
- I read the Markdown companion, not the rendered PDF; I did not compare the PDF layout, charts or text to the Markdown.
- BoG figures are checked against the room's `sector-context.csv`, not the Bank of Ghana release; macro tables against `macro.csv`, not the underlying sources.
- Pages 12 to 41 (bank profiles, process and attribution), and the qualitative prose on pages 1 to 11 beyond the figures above.
- This verdict covers the PDF and Markdown hashes above only.
