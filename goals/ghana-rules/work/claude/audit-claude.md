# Audit by claude: web search/answer engine, open PRs, version fragmentation (task P1-C)

Scope: `hayalows/research`, `ghana-rules-engine/web/`, the PR descriptions for #70, #72 and #79, and the reports `web/CHANGELOG.md`, `V11-NATIONAL-REPORT.md`, `V11.2-ALPHA-REPORT.md`, plus the README.
Method: read-only, through the GitHub API. **I did not clone the repo, run any code or run any tests.** Every number below is quoted from the repo's own documents. Labels: **observed** = read in a named file; **inferred** = my reasoning; **unknown** = not checked.

## 1. What is real (observed)
- A grounded search and "answer engine" exists in `web/`, with a long run of versions (V8.2, V9, V10, V10.1, V11, V11.2) and a private alpha for invited testers (`alpha.html`, `alpha-admin.html`, a SQL schema).
- The reports are unusually honest about limits. `V11.2-ALPHA-REPORT.md` says the new 40-question set is "developer-authored, not lawyer-adjudicated", and `V11-NATIONAL-REPORT.md` says the million-segment benchmark uses synthetic fixtures only.
- Safety design is good: provision text is gated off by default; citation year contradictions are surfaced (`YEAR_MISMATCH`); out-of-domain questions abstain (PR #79: 13/50 to 47/50 negatives blocked).
- Real full-text corpus: 955 documents (591 judgments, 364 legislative documents), 37,382 segments (`V11-NATIONAL-REPORT.md`).

## 2. What the numbers actually show (observed, then inferred)
| Test set | Reported result | Who wrote the set |
| --- | --- | --- |
| New 40 (V11.2) | top-1 8/28 to 26/28 | developer, before implementation |
| Original 100 | 95/95 | developer, used for development |
| Expanded 309 (title proxy) | top-1 226 to 228 of 309 across V11.1 to V11.2; MRR 0.809 to 0.812 | derived from document titles |
| Original 46 | 38/46 to 40/46 | frozen holdout |

**Inferred:** the large jumps appear on sets built by the same team around the new feature. The one broad, older set (309) barely moves: about 74% top-1 for several versions in a row, with 303/309 "found". So the system *finds* the right document almost every time but ranks it first about three times in four, and these results are never checked by a lawyer. Retrieval is no longer the bottleneck.

## 3. The gap that matters most (observed)
- `V11-NATIONAL-REPORT.md`: of 100 authored citizen scenarios across 20 domains, **80 returned INSUFFICIENT_EVIDENCE** in V10.1.1 guidance. The V11 fix points the user to the right instrument and publisher (95/95 top-1 on a development set). It does not produce a cited answer.
- By design, the engine returns research leads (instrument, year, official link) and not provision text. For a citizen, a link to an Act is still a long way from "what does section X say, and does it apply to me?".
- Legislative full text is 364 documents, against 3,763 catalogue records that are explicitly not admitted as law. **Inferred:** most of the law a user asks about is not available as verified text, so the engine cannot quote it.

## 4. Two halves that may not meet (inferred, must be verified by codex)
The README describes a Python rule engine (bitemporal, defeasible reasoning, traces) with rule packs documented as **traffic** only. The web app is JavaScript retrieval. **Inferred, not checked:** the web search does not call the rule engine, so the most distinctive asset (executable, date-aware rules with traces) is not what users touch. Codex should confirm by reading how `web/` uses `engine/`.

## 5. Fragmentation and process risk (observed)
- Open PRs when I looked: #70 (V8.1 foundation, +3,871 lines, draft), #72 (V9 "Sankofa", **+548,788 lines, 1,317 files**), #79 (scope gate, +521/-18, 9 files). Version names jump (V8.1, V9, V10, V10.1, V11, V11.2) and PR #79's own description says the scope guard "did not keep up" with the later versions.
- `web/CHANGELOG.md` is titled "V8 to V10" and its newest entry is V10.1, while the repo also has V11 and V11.2 reports. **Inferred:** documentation lags the code. I also saw V11 reports stating "draft PR only; not merged" while the same files appear in the `main` tree. I could not tell which is current, and I did not check merge history. **Unknown.**
- A 548k-line PR cannot be meaningfully reviewed by a person. **Inferred:** much of it is generated index data, but I did not check.

## 6. Risks and unknowns
- **Legal risk (observed):** the README and reports repeat "not legal advice", and the verification step checks structure (HTTPS source, unique ids), not whether the law is right or current. No qualified legal reviewer is mentioned.
- **Source and rights (observed):** the reports flag reuse-rights review as pending for acquired text. Any step towards quoting provisions depends on resolving it.
- **Alpha database (observed):** no dedicated Ghana Rules Supabase project is configured, so the user-feedback loop has not started.
- **Unknown:** whether the tests pass today, the real size of the data in `main`, and whether the live site matches `main`.

## 7. What a Ghanaian user would value most (inferred)
A correct, cited answer to a common question, with the effective date, and a clear "I cannot answer this" otherwise. Not a better ranking of links.

## What I could not verify
Everything not listed in the scope line above, including code behaviour, test results, and the contents of `engine/`, `kg/`, `data/`, and PRs #60 and #32.
