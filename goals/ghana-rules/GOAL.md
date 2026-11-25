# Goal: a big leap for Ghana Rules

## Goal
Take Ghana Rules (`hayalows/research`, folder `ghana-rules-engine/`) from a promising research prototype to a clear, defensible leap in usefulness for Ghanaian law, not another incremental retrieval tweak. Decide what the leap is, prove it with evidence, then build the first slice of it.

## What exists today (starting facts, to be re-verified by each agent)
Source: the README, `V7-RESEARCH.md`, the descriptions of PRs 70, 72 and 79 in `hayalows/research`, and `benchmarks/results/benchmark_report.json`. Anything not re-checked in the repo is **unverified**.
- **Rule engine:** bitemporal, defeasible, three-valued reasoner with traces, SMT trace verification and an honest-abstention design. The only rule packs described are for **traffic** law.
- **Corpus:** 1,014 curated records, plus 3,763 Parliament catalogue records that are explicitly not admitted as current law, plus a national DSpace sweep. Full-text bodies exist for about 955 documents (per PR 72).
- **Search/answer engine (V8.2 to V11):** retrieval and research leads. Provision-text answers are gated off by default. In PR 72, the V9 hybrid reaches about 34/46 top-1 out of sample and 230/309 on the expanded set. PR 79 adds a shared scope gate (13/50 to 47/50 out-of-domain negatives blocked) with no ranking regression.
- **Verification:** the benchmarks are "AI-constructed automated checks (NOT human-verified legal benchmarks)".
- **Process:** several parallel version PRs are open at once (V8.1, V9, V11 scope gate), which suggests fragmentation.
- Stated roadmap targets that are **not** achieved: 10,000 documents, 1,000 answer records, 100 domains, 500 independently reviewed questions.

## Phase 1: Assess and propose (read-only)
Each agent works alone first, then they converge. No edits to `research` in this phase.
1. Each agent independently audits the engine, corpus, web app, benchmarks and open PRs, and writes findings to its own board file. Cover: what is real vs. claimed, the biggest gaps, and what a user in Ghana (lawyer, business owner, student, civil servant) would find most valuable.
2. Each agent proposes **up to 3 candidate "big leaps"**, each with: the user value, the evidence it is feasible from this repo, the main risk, a rough effort estimate and how we would measure success.
3. Agents read each other's proposals, challenge them in `reviews/`, and merge them into one **ranked shortlist of at most 3**. Disagreements stay visible and are not smoothed over.
4. The lead writes the shortlist to `HUMAN.md` and **waits for the human to choose**.

Ideas to consider (not a mandate, and agents should add better ones):
- Executable rule packs for high-demand domains beyond traffic (for example tax and VAT, employment, tenancy, company registration), with date-aware amendment lineage.
- Provision-level, source-verified answers (turning leads into cited text) with a strict admission contract and legal-review gate.
- A consolidated "law as of date" view built from amendment and commencement lineage.
- An independent, human-verified benchmark, so quality claims stop resting on AI-built checks.
- Consolidating the version branches into one trustworthy release line.

## Phase 2: Build the first slice (only after the human chooses in `HUMAN.md`)
- Work on branches in `hayalows/research` named `room/<agent>/<topic>`, and open **draft PRs**. Never push to `main`.
- Reuse the room's review rule: every task is reviewed by a different agent before it is marked ready.
- Report measured before/after results using the repo's existing benchmarks, plus any new ones, with the commands that were run.

## Done means
- [ ] Phase 1: three independent audits, a ranked shortlist of at most 3 leaps with evidence, and the human's choice recorded.
- [ ] Phase 2: a working first slice of the chosen leap, merged into a draft PR with tests that run, and a before/after measurement.
- [ ] Every claim in the final summary is labelled observed, inferred or unknown, and nothing is presented as legal advice.
- [ ] The final summary in `STATUS.md` lists what was verified, what was not, and the next 3 steps.

## Constraints (hard)
- **Not legal advice.** The engine verifies inference, not legal interpretation. Do not claim legal accuracy that no qualified reviewer has confirmed.
- Never present a bill, report or catalogue record as enacted law. Follow the admission contract in `V7-RESEARCH.md`.
- No invented statutes, section numbers, case holdings, figures or sources. If a source is missing, abstain and say so.
- Respect source restrictions and copyright. Do not bypass authentication or scrape against a site's terms.
- Do not deploy, change production, make paid API calls, send messages, or turn on scheduled jobs.
- Do not touch `main`, or other people's open PR branches, in `research`. Preserve other workspaces (`investment-intelligence-lab/`, `learning-room/`).
- Follow `research/AGENTS.md`: use a task branch and a reviewable PR for meaningful changes.

## Output
- Phase 1: `goals/ghana-rules/work/phase1/` (audits, proposals, shortlist).
- Phase 2: draft PRs in `hayalows/research`, with a summary in `goals/ghana-rules/work/phase2/`.
