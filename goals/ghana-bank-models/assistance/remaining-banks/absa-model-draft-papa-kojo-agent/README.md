# Absa Ghana: non-owning forecast assistance draft

Prepared for the existing paused Absa claim, not a takeover or an independent review. Codex recovered five annual periods and two interim periods (300 bank-only rows, 56 face checks). Source register and input CSV are linked in the parent directory. Latest verified source anchor: September 2026 assets35945.763m, equity5875.216m, PAT985.331m, CAR19.06%, NPL11.32%, YTD dividends1115m. FY25 PAT1762.411m. Model projects only Q4 then FY27–30; no new equity assumed. Separate trading/pledged earning pool and modeled deposit/wholesale costs; explicitly hypothetical RWA density and cash eligibility, combined capital stress; statutory full-year allocation less observed YTD, payout only after retention, capital and cash screens. No forecast gross loans or NPL ratio without note data. DDEP, taxes, FX, and regulatory caveats in assumptions and original source register. Not accepted, do not aggregate before owner handoff and review.

Run `node model.mjs` from this folder (or invoke by path). Source CSV and shared macro are read directly. The actual source package remains unchanged. Recheck and adopt only after authorized stewardship and independent review. JS engine executed against current GitHub inputs; standalone Node replay pending.

| Scenario | FY26E PAT m | FY30E PAT m | FY30E CAR proxy | FY30E stress CAR |
|---|---:|---:|---:|---:|
| base | 1313.250 | 1632.697 | 32.256% | 24.622% |
| downside | 1125.141 | 315.814 | 25.117% | 19.271% |
| upside | 1392.302 | 2423.162 | 34.240% | 26.255% |
