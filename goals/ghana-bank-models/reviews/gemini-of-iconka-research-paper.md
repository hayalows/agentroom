# Independent Review: `iconka` Supplementary Research Paper

- **Reviewer:** `gemini`
- **Author:** `iconka` (GPT-6.2)
- **Verdict:** **PASS**
- **Target artifacts:**
  - `goals/ghana-bank-models/reports/iconka/Ghana_Banking_Sector_Research_2026-2030.pdf` — 41 pages, 178,260 bytes, SHA-256 `735b6d6b90df044d54bb06db9c53a9162c741c623fcd5f14bedb365f34c36523` (commit `20a51ed7a5e8e04caefcdb2c2143f4ba6cc25504`)
  - `goals/ghana-bank-models/reports/iconka/Ghana_Banking_Sector_Research_2026-2030.md` — 1,355 lines, LF SHA-256 `55d189b6bdd80c8700de4a3815a22bd6776db717a8d4ab9c7801c23b133833bf` (commit `a4ceecb`)
  - `goals/ghana-bank-models/reports/iconka/build_report.py` — 405 lines (commit `6a0be00`)
- **Pinned inputs checked against:** Source pin `b728a09ffd52393f98b97c14298544c139d1921f`, published sector outputs `11dffc9111b208dc896e2db05f0e65c18aa09179`, sign-off commit `8d695a2`, all verified on clean `git -c core.autocrlf=false` detached worktrees.

## 1. Disclosure of Prior Involvement
Per `iconka.md` and room independence rules, `gemini` discloses prior authorship of four banks within Profiles 1–12 (`absa-ghana` reviewer, `adb` original owner, `calbank` original owner, `ecobank-ghana` original owner, `fidelity-bank-ghana` original owner) as well as prior reviews of `omnibsic-bank`, `umb`, `qa-sweep`, and `sector-rollup`. For this review of `iconka`'s synthesis paper, `gemini` checked exact transcription and arithmetic parity against the frozen signed-off pin `b728a09` / `11dffc9`; this does not constitute an independent re-audit of `gemini`'s own original bank models.

## 2. What Was Checked and Verified (0 Mismatches)
1. **Exact Artifact Hashes & PDF/Markdown Parity:**
   - Verified PDF SHA-256 `735b6d6b90df044d54bb06db9c53a9162c741c623fcd5f14bedb365f34c36523` and Markdown LF-normalized SHA-256 `55d189b6bdd80c8700de4a3815a22bd6776db717a8d4ab9c7801c23b133833bf`.
   - Extracted text across all 41 PDF pages via `pypdf` (`73,910` characters) and confirmed presence of key pins, sector totals, conditional closure labels, and all 23 bank headings. Inspected `build_report.py` lines 1–405 and confirmed PDF and Markdown are emitted from the same `story`/`markdown` structures.
2. **Bank Profiles 1–12 (`absa-ghana` to `gcb`) & All 23 Profiles (`financials.csv` and `forecast.csv` at `b728a09`):**
   - Independently recomputed every historical (`FY21`–`FY25`, `9M-2026`), 5-year forecast (`2026E`–`2030E`), and evidence-trail count (`historical rows`, `forecast rows`, `reported source_id` count) directly from raw bank CSVs.
   - **Result:** `1,403` cells checked across all 23 profiles (`732` cells in assigned Profiles 1–12), **0 mismatches**.
3. **Industry Context & Macro Tables (Sections 03–04):**
   - Verified Section 03 BoG indicator table (`40` cells) against `sector/macro-assumptions/sector-context.csv` at `b728a09`: **0 mismatches**.
   - Verified Section 04 macro tables (`75` cells) against `sector/macro-assumptions/macro.csv` at `b728a09`: **0 mismatches**.
4. **Research Operations Inventory & Attribution (Sections `RESEARCH OPERATIONS / 01` & `03`):**
   - Verified inventory counts against `b728a09` and `8d695a2`: `7,551` historical CSV rows, `19,493` forecast CSV rows, `131` reported source IDs, `65` review Markdown files at sign-off, `72` assistance files at sign-off, and `git rev-list --count` goal-path commits `1,036` (at `b728a09`) and `1,054` (at `8d695a2`): **0 mismatches**.
   - Verified all `23` rows of the ownership/steward/manifest-reviewer table against `claims/*.md` and `sector/peer-comparison/comparison.csv` at `11dffc9`: **0 mismatches**.
5. **Scope, Conditional Closures & Caveats:**
   - Verified 20 ordinary accepted banks and 3 conditional-closed banks (`omnibsic-bank`, `prudential-bank`, `umb`) are strictly separated everywhere, each conditional gap is stated accurately, UMB's PwC Q2 2026 numbers are labelled secondary, scenarios are framed as non-probabilistic model outputs, ADB's 70.53% NPL loss path and closing-equity vs. average-equity ROE definitions are explained, and Section 07 constant-coverage scaling (`90.35%` / `87.52%`) is explicitly labelled as Iconka's illustrative calculation not approved by the lead.
   - Confirmed no files under `banks/` or `sector/` were modified.

## 3. Minor Non-Blocking Note
- `build_report.py` line 18 defines `SIGN='8d695a28'` which is unused in the script; it has no effect on the generated PDF or Markdown.

## 4. What Could Not Be Verified
- Did not re-audit original bank PDF filings or visually render every PDF page image beyond `pypdf` 41-page text extraction and `build_report.py` source inspection.

## Round 2 (allocated by lead): 2026-11-25T22:01:30Z
- **Scope:**
  1. **(a) BoG industry context table (page 4 / Section 03) & macro anchors (page 5 / Section 04)** checked directly against the **original public Bank of Ghana releases** listed in `sector/macro-assumptions/SOURCES.md` (not only our CSVs).
  2. **(b) Qualitative prose on Bank Profiles 13–23 (pages 24–34)** checked against each bank's `README.md`, `sources.md`, `financials.csv`, `forecast.csv`, `claims/*.md`, and `CONDITIONAL-CLOSURES.md` / `summary.md`.
- **PDF & Markdown hashes unchanged:** PDF `735b6d6b90df044d54bb06db9c53a9162c741c623fcd5f14bedb365f34c36523`, Markdown LF `55d189b6bdd80c8700de4a3815a22bd6776db717a8d4ab9c7801c23b133833bf`.

### (a) Original BoG & MPC Public Release Verification (0 mismatches)
1. **BoG *Summary of Economic and Financial Data — November 2026* (`Summary-of-Economic-and-Financial-Data-November-2026-1.pdf`, 17-Nov-2026, 16 pages; fetched live, 1,201,990 bytes):**
   - **Page 13 (`9. Banking Sector Indicators`):** Verified all 4 columns (`2025:12`, `2026:04`, `2026:09`, `2026:10`) for Assets (`446.9`, `493.9`, `513.6`, `512.9`), Deposits (`325.3`, `365.5`, `372.9`, `369.8`), Gross Advances (`111.0`, `115.2`, `134.0`, `140.9`), CAR (`17.5`, `22.3`, `18.9`, `18.5`), NPL (`18.9`, `18.0`, `14.0`, `13.1`), NIM (`11.5`, `9.3`, `9.2`, `8.1`), ROE after tax (`30.8`, `22.4`, `23.2`, `19.0`), and Operational Cost / Gross Income (`48.8`, `52.0`, `53.3`, `54.8`) — **32/32 exact match**.
   - **Page 12 (`8b. Monetary Indicators`, `Nominal PSC (%)`):** Verified Private credit growth YoY (`19.2`, `28.7`, `34.0`, `37.2`) — **4/4 exact match**.
   - **Page 5 (`3a. Interest Rates`, `Average Lending Rate`):** Verified (`20.45`, `16.33`, `15.78`, `15.79`) — **4/4 exact match**.
2. **BoG *133rd MPC Press Release — 18 November 2026* (`MPC-Press-Release-November-2026.pdf`, 3 pages; fetched live, 206,515 bytes):**
   - Confirmed Page 3 decision: Monetary Policy Rate aligned from `14 percent to 11 percent`; Page 1: headline inflation rose to `5.5 percent` in October 2026; Page 2: 91-day Treasury bill declined to `4.6 percent` in October 2026 (`4.62%` in `Summary-of-Economic-and-Financial-Data-November-2026-1.pdf` p. 5).
3. **BoG Treasury Bill Auction Results (November 2026, `bog.gov.gh`):**
   - Confirmed Tender held 20 Nov 2026 (Issue Date 23 Nov 2026): 91-day Bill weighted average interest rate **`4.5193%`** (matches paper's `"approximately 4.52%"` in Section 04).

### (b) Prose on Bank Profiles 13–23 (pages 24–34, 0 mismatches)
- **Prior involvement disclosure for Profiles 13–23:** `gemini` did **not** originally build any bank in Profiles 13–23 (`gtbank-ghana`, `nib`, `omnibsic-bank`, `prudential-bank`, `republic-bank-ghana`, `societe-generale-ghana`, `stanbic-bank-ghana`, `standard-chartered-ghana`, `uba-ghana`, `umb`, `zenith-bank-ghana`); `gemini` did act as scoped reviewer on `omnibsic-bank` and `umb`.
- Verified qualitative claims, ownership/steward/reviewer attributions, conditional closure gaps, and cited ratios/amounts across all 11 profiles against each bank's `README.md`, `sources.md`, `financials.csv`, `forecast.csv`, `claims/*.md`, `CONDITIONAL-CLOSURES.md`, and `sector/summary.md` (`gtbank-ghana` CAR 24.08% / NPL 3.67% / 9M div 604.370m; `nib` negative opening FY25 equity / NPL 69.70% / downside CAR proxy 11.17%; `omnibsic-bank` FY21 gap / RWA density 22.58% & 38%/48% stress; `prudential-bank` Sep 2026 inaccessible / FY25 equity 60.863m, CAR -20.19%, NPL 57%, going-concern, 1.012bn shortfall, impairment reversal; `republic-bank-ghana` Republic Financial Holdings / DeepSeek->Codex; `societe-generale-ghana` 76.9% net LDR / downside CAR <13%; `stanbic-bank-ghana` Sep 2026 CAR 23.32% & NPL 9.54% vs 24.63% FY25; `standard-chartered-ghana` Claude->Codex / 9M tax & div; `uba-ghana` FY25 NPL 2.11% / upside<base 2030; `umb` Sep 2025 anchor / MoF recapitalisation unverified / PwC Q2 2026 secondary benchmark 16.684bn, 11.5375bn, 195.1m, 13.0%; `zenith-bank-ghana` unlisted Zenith Bank PLC subsidiary / bank-only). **0 mismatches**.

### Round 2 What Could Not Be Verified
- Did not re-fetch the earlier *Summary of Economic and Financial Data — September 2026* PDF separately (the November 17, 2026 release carries the full `2025:10`–`2026:10` series including `2026:09`), nor `S-BOG-MPR-SEP26` / `S-BOG-MPC-MAY26` in full during Round 2.

### Round 2 Verdict
- **PASS** (zero mismatches on all Round 2 checks; PDF and Markdown remain unchanged).

