# Tasks: ghana-rules (lead edits only)

| ID | Task | Owner | Reviewer | Status | Output |
| --- | --- | --- | --- | --- | --- |
| P1-A | Audit engine, rule packs, tests, benchmarks. What is real vs claimed? Run the tests if you can. | codex | gemini | open | work/codex/audit-codex.md |
| P1-B | Audit corpus, acquisition ledger, admission contract, data gaps, copyright/source risks. | gemini | claude | open | work/gemini/audit-gemini.md |
| P1-C | Audit web search/answer engine (V8.2 to V11), open PRs 70/72/79, version fragmentation, user value. | claude | codex | in-review | work/claude/audit-claude.md |
| P1-D | Each agent proposes up to 3 candidate leaps (value, evidence, risk, effort, success metric). | all (claude done) | cross | claimed | work/<agent>/proposals-<agent>.md |
| P1-E | Cross-challenge all proposals in reviews/. | all | - | open | reviews/ |
| P1-F | Merge into a ranked shortlist of at most 3, then ask the human in HUMAN.md. | claude | codex + gemini | open | work/claude/shortlist.md |
| P2-* | Build the first slice of the chosen leap. Lead defines these after the human chooses. | tbd | tbd | blocked | - |

Status values: open, claimed, in-review, changes-requested, merged, blocked.
P1-A, P1-B and P1-C can run in parallel. P1-D starts once an agent finishes its own audit. P2 is blocked until HUMAN.md has a recorded choice.
