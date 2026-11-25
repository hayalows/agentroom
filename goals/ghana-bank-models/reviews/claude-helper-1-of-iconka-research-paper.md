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

## Round 2, 2026-11-25T22:04Z (lead's 21:58Z allocation: (a) rendered PDF against the Markdown; (b) prose of bank profiles 1 to 12, pages 12 to 23)
Verdict (Round 2): **PASS, no CHANGES required.** Same artifacts: PDF SHA-256 735b6d6b90df044d54bb06db9c53a9162c741c623fcd5f14bedb365f34c36523, Markdown 55d189b6bdd80c8700de4a3815a22bd6776db717a8d4ab9c7801c23b133833bf. My earlier verdict and scope (pages 1 to 11 numbers) stand; this section adds the two checks. Authorship disclosure: I built or stewarded Absa, ADB (steward) and OmniBSIC and wrote ordinary reviews of other banks that the paper describes; I checked each claim against the files, not my memory.

### (a) Rendered PDF against Markdown (observed)
- **Text parity.** `pdftotext` of all 41 pages against the Markdown with links and table markup stripped: 10,255 Markdown tokens against 10,681 PDF tokens. The only tokens the PDF lacks are the two "Chart data" blocks (they are Markdown-only companions to the charts). The only extra PDF tokens are the running header and footer on each page, page numbers and chart axis ticks and labels. **No table cell, number or sentence differs.**
- **Charts.** Rendered pages 3 and 6 and compared with the tables beside them: the PAT bars (4.7, -5.9, 6.8, 10.5, 14.0; 2022 in red) and the three scenario lines (2026E to 2030E end points about 19.3, 7.2 and 26.5) match the tables and chart-data values.
- **Garbled characters.** I rendered pages 37 and 40 at 110 dpi and extracted their text. I found **no replacement symbols**. Page 37 shows em dashes in the empty "Final steward" cells and curly apostrophes; page 40 shows curly apostrophes. They are U+2014 and U+2019, which are in WinAnsi, and display correctly. I cannot reproduce the replacement symbols the lead saw; they may come from a viewer that substitutes its own font. **Non-blocking note:** the PDF uses standard Helvetica and Helvetica-Bold, not embedded. Standard viewers draw them correctly, but a viewer without Helvetica could substitute glyphs. Embedding a font in the next build would remove that risk. I did not test other viewers.
- **Layout.** Word boxes for all 41 pages stay inside the margins (max x 556 of 595 pt), no clipped text, no blank page, and no page is mostly empty.
- **Links.** 185 clickable link annotations against 185 Markdown links (151 distinct): none missing either way. All 103 repository links pinned to a 40-character commit resolve to an existing path at that commit (`git cat-file -e`); all 41 links to `main` resolve at current HEAD. I did not fetch the two bog.gov.gh URLs or the GitHub commit pages (no network access to them from here).

### (b) Prose of profiles 1 to 12 (Absa to GCB)
Machine checks (72, script `assistance/claude-helper-1/paper-verifier/check_profiles_1_12_evidence.py`): for each profile the paper's evidence-trail line against the claim files (original owner, steward), the manifest reviewer against `comparison.csv`, the historical row count against `financials.csv`, the forecast row count against `forecast.csv`, the count of reported-source IDs, and the stated reported CAR and NPL against `comparison.csv`. **Result: all match** (one flagged line, Absa NPL "n/a.", was my regex catching the sentence-final full stop; the value is blank in the CSV, so it matches).
Qualitative checks against each bank's README, sources.md, claim and reviews, all found consistent:
- Absa: Codex-recovered and transcribed history, Helper built the model, high net lending intensity (52.1%), FY2026E PAT below FY2025 on a larger balance sheet, calibrated reserve proxy and the 20% stress withholding dividends.
- Access: listed Ghana subsidiary; 9M2026 PAT 367.1m above FY2025 286.5m; signed or final status of one FY2025 web copy unverified.
- ADB: state-backed and listed; FY2023 loss and negative equity (-102.3m) then recovery; 70.53% gross NPL; corrected capital anchor.
- Bank of Africa: unlisted; September 2026 CAR 27.01% and NPL 17.89%; FY2022 qualified opinion on the omitted 80.883m impairment.
- CalBank: recapitalisation; Luna then Support as steward; ROU double count and early interest overstatement found by reviewers; downside above base from FY2027E.
- CBG: government-owned; FY2025 PAT 7.4m; H1-2026 assets 19,196.1m and PAT 59.6m; 2025 reserve waiver; cost-to-income about 85%.
- Ecobank: second-largest bank, ETI 68.93% and GSE-listed, ROU corrected across six periods, two uninvolved reviewers plus my PASS; FY2025 cost-to-income about 34% (third lowest of the 20).
- FBNBank: distinct from First National; FY2025 PAT 16.7m against 207.7m in FY2024; 9M2026 35.9m against 22.2m; no full IFRS notes in the summary.
- Fidelity: privately owned; Gemini origin and Codex stewardship; net loans 4.74bn to 6.33bn between FY2025 and September 2026; downside CAR above base because of the dividend suspension and slower growth.
- First Atlantic: listed 19 December 2025; mandatory BoG cash share 56.9% in FY2024 against 18.4% in FY2025.
- First National: FirstRand subsidiary; returned to profit after losses; retained deficit 309.925m; no further dividend or equity injection assumed.
- GCB: net loans 25.2bn; NPL 4.8% against 10.31%; CAR 14.6% against 18.02%.

**Optional wording points (no number is wrong; none blocks the PASS):**
1. CalBank: "the rate path benefits liquid assets" is narrower than the package. The checks say higher rates lift loan and securities income and the downside also carries a wider loan spread (+1.5 against +1.0 points). "Over six times" opening equity understates the ratio (217.3m to 1,528.4m is about 7.0 times).
2. Absa: the README's main limitation is that the owner could not open the issuer PDFs and no row was re-read by the owner; the profile says "independently transcribed" but not that. One clause would carry it.
3. First National: the loss history also includes FY2021 (-4.1m); the text names 2022 and 2023.

### Round 2, not checked
Prose on profiles 13 to 23 (Gemini's allocation); the BoG and macro pages against the original releases; the timeline and credits (pages 35 to 38), pages 7, 8, 11 interpretation and the GCB reading (lead's allocation); other PDF viewers; the two bog.gov.gh pages.
