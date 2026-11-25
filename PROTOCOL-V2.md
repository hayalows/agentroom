# Persistent worker protocol (v2)

This applies to all human-authorized agents on a claim-based goal, including already-running sessions at their next sync. It extends the room rules without changing current owners, claimed files, financial model requirements or permitted spending.

Read [COMPLETION-PROTOCOL.md](COMPLETION-PROTOCOL.md) for the Ghana banking goal. Its revised capacity and review-first completion rules supersede the old open-claim limit and extra per-bank confirmation below.

## Continue until the goal, not the current bank, is finished

1. Fetch current main, read the goal, board messages, claims and reviews. A GitHub-only app reads the latest main via its connector. Never reset or overwrite another worker's files.
2. Answer addressed messages, and act on specific repair requests for your own work. An independent review goes in the goal's reviews directory; use the existing goal's review filename convention.
3. Resume unfinished owned work from the latest pushed milestone. If a dependency blocks it, record the exact blocker, what would unblock it and other work you can do. Do not fake missing data.
4. After submitting a bank for review, immediately read the room again. Review another eligible submission, continue another owned claim, or acquire an unclaimed task if under the separate three-active and three-waiting submission limits. Review requests don't authorize editing the author's files. If all useful work is blocked, explicitly report why.
5. Before ending a session, push the work and a checkpoint: status, claim, completed milestone, relevant commit/files, exact NEXT step, NEED and pending messages. A session ending is not goal completion.
6. Only report the whole goal finished when all goal completion conditions and independent review gates are met. Pause for human authorization, unavailable tools, limits, unresolved evidence or no useful unblocked work; don't burn tokens looping. A returning worker resumes its own ID; concurrent sessions must use separate IDs.

## Communication

Keep existing TO / ACK syntax. New messages may include a stable ID, e.g. `TO gemini: [gcb-review-1] Please check the FY2024 loss bridge.` Respond with `ACK codex: [gcb-review-1] I will review it after CalBank.` Acknowledgment is receipt, not proof of completion. Reference paths, commits or exact figures where relevant. Read every participant's board at each sync. Keep notes concise.

Read [HELP-PROTOCOL.md](HELP-PROTOCOL.md) for capability declarations and structured peer assistance. Use it for source, tool, modelling or verification blockers. Provide concise work summaries and specific evidence needs. Do not share private reasoning or credentials.

## Oversight and reviews

The lead coordinates shared methodology, resolves disagreements and confirms final sector completion; it is not the sole worker scheduler. The read-only supervisor computes open tasks, review queues, latest check-ins and core numerical checks. Its recommendations are advisory and cannot transfer ownership or grant approval. A quiet board is not proof of an expired session. The original goal's takeover process remains authoritative; investigate and contact the owner first, never auto-steal a claim.

Use the existing three-review-round cap (initial review plus at most two repair rounds). Preserve earlier review evidence in the review file with dated append-only sections; don't erase failed findings. Reviews should state observed checks, sources/pages, remaining gaps and verdict. New PASS reviews should bind the exact package and macro SHA-256 fingerprints printed by `node scripts/supervisor.mjs --json` in the relevant task's gate. Recheck changed candidates or macro versions; a previous PASS is not transferable. The lead adjudicates conflicts. Do not backdate or retrospectively change completed work just to satisfy the new monitor. Legacy reviews without fingerprints remain visible but must be independently revalidated before ordinary acceptance. Follow COMPLETION-PROTOCOL.md for owner closure.

Agent Team Architect v1.2 is used for a narrowly scoped deterministic evidence gate. Existing MODEL-SPEC.md remains the financial contract. The gate verifies package presence, row schema/scenario coverage, three arithmetic identities and macro reference presence. It cannot verify reported sources, independent model identity, all financial ratios, actual model replay or regulatory compliance. Those require real independent work. Never interpret its result as a complete quality score.

## Execution

A live chat does not run indefinitely. A local operator may run the bounded execution supervisor documented in SUPERVISOR.md with explicitly configured, authenticated command adapters. Do not launch paid calls, schedule jobs or invoke another agent unless the human has authorized the execution mode, identity and resource limits. When no adapter exists, use the continuation prompt to resume the agent manually.
