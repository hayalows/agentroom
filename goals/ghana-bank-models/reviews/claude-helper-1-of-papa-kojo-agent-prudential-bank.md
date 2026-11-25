# Prudential Bank independent conditional review (claude-helper-1)

## 2026-11-25T18:31Z, conditional scope "9M-2026 unavailable", package 1919f9e6
Verdict: PASS
Scope: conditional (9M-2026 unavailable)
Package SHA-256 fingerprint: 1919f9e67abe7b9a4c0bee01ea80cb1629b137516d991bd25daca96202841384
Macro SHA-256 fingerprint: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df

**Scope of this PASS.** It applies only under the lead's scope decision (`review-resolutions/prudential-bank.md`): a model labelled "conditional: 9M-2026 unavailable", not a full-data acceptance. If the September 2026 statement becomes reachable, the owner must patch it in and the package needs a new review.

**Independence.** I claimed Prudential at the start and released the claim at 14:21Z without building or committing any bank file. Every file in `banks/prudential-bank/` is the work of papa-kojo-agent and codex. The lead named me as the second reviewer. I did not supply evidence for this package.

### What I checked (observed)
- **Gate:** `gateBank` returns `core-checks-pass` with the fingerprint above (238 history rows, 915 forecast rows, 5 annual periods, 15 scenario-years, 60 core bridges, 0 failed, 0 bad rows, 0 duplicates).
- **Replay:** copied the bank folder and the shared macro file to a scratch tree and ran `node model.mjs` (exit 0). `forecast.csv` and `checks.md` are byte-identical to the submitted files.
- **Independent identities:** from `forecast.csv` alone I recomputed net interest income, profit after tax and assets = liabilities + equity for all 15 scenario-years (45 checks). Largest residual 0.001m, none above 0.0025m.
- **The four scope conditions:**
  1. *FY2025 audited year-end is the last reported anchor:* the history holds FY2021 to FY2025 only and has no 9M-2026 row. Met.
  2. *FY2026E is labelled an estimate, not anchored on a 9M actual:* forecast rows carry status `estimated` and the note "Conditional full-year forecast from FY25 audited anchor; no 2026 interim actual". Met.
  3. *Recapitalisation is a labelled assumption or sensitivity with the amount from the issuer:* the README states conditional cash and capital recognition (100% base, 80% downside, 100% upside) and the checks rerun 20% debt-like funding, 20% non-cash contribution and tax stresses; the GHS 1,130m amount is sourced to the issuer's 9 October 2026 announcement (`PBL26CAP`). The Ministry of Finance is not cited in the file. Met on the issuer source.
  4. *README carries the label:* the README opens with "conditional: 9M-2026 unavailable". Met for the README. The roll-up and peer-comparison rows are outside this package; Prudential is not in the accepted-only roll-up yet, so that label must be added by their owners when the bank is accepted.
- **Arithmetic of selected history rows:** FY2025 profit before tax 107.908 less tax 75.955 gives profit after tax 31.953, matching `financials.csv` and `sources.md`.

### Findings
1. **Non-blocking, please answer:** a web search excerpt of the FY2025 summary (`PBL25SUM`) shows "107,908" and "110,429" next to the label "Profit/(loss) after tax". 107,908 equals the package's FY2025 profit before tax, so the 110,429 is probably the Group column, not an FY2024 comparative (the package has FY2024 profit before tax of -256.654). I could not read the page, so please confirm the column order in the owner's notes.
2. **Non-blocking:** FY2025 RWA (3,049.111m) is inferred from a stated auditor shortfall and the reported -20.19% CAR, not reported. It is labelled an inference in `sources.md`. Please keep that label in any roll-up use.
3. **Non-blocking:** with the recapitalisation, the base FY2026E profit after tax is -62.7m and the downside CAR proxy is deeply negative. These are labelled conditional stress results, not forecasts of an actual outcome.

### What I could not verify
- I did not read the Prudential PDFs. The site returns HTTP 502 to every tool I used, and the fetch tool refused the PDF host's robots file. History values are arithmetic-checked only against the owner's and codex's recorded figures, not against a page.
- I did not test the source URLs or check the Act or the Ministry of Finance statement.
- This verdict covers the exact fingerprint above and nothing else.
