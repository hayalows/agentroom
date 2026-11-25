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
