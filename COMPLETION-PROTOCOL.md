# Bank completion and review-first work policy

This replaces the previous open-claim limit and per-bank lead confirmation step for the Ghana banking goal. It does not change MODEL-SPEC.md, source requirements, independent review, ownership, or the existing financial quality bar.

## Priorities at each sync
Finish the current small milestone and push it. Read latest main, all boards, current claims, reviews and help requests. Read the supervisor queue (node scripts/supervisor.mjs --json or the latest Room status workflow summary).
1. ACK and act on addressed messages; verify delivered assistance.
2. Close your own verified submissions; repair real blocking findings, or explicitly report blockers. If you are the lead, resolve escalated review disputes.
3. Offer needed peer assistance and review another owner's eligible bank before claiming additional work. A reviewer does not claim a bank and may not approve their own model. Post REVIEW-START <slug> on your own board before reviewing; sync first to avoid duplicate effort. Another reviewer may take over a quiet review after 20 minutes; never overwrite another review.
4. Continue existing active work. If no repair, closure, peer review or assistance needs you and capacity exists, claim an unclaimed bank. When waiting for others, work on useful eligible tasks instead of ending the session.

Three active building/repair claims at a time, plus at most three submitted claims waiting on others before taking another new claim. Clean submitted models no longer occupy an active building slot. A requested repair occupies an active slot until resubmitted; if repairs push you above the active limit, repair before taking new claims. Submitted claims remain owned by the author. Reviews and bounded help never count as bank claims. No new claims are suggested while actionable repairs, closures, reviews or assistance are waiting. These limits are advisory coordination rules for GitHub-only workers, not a server-side lock. Released claims still follow the existing ownership/takeover process.

## Model closure
A complete bank needs the core gate, a distinct registered reviewer's current-version PASS, no unresolved CHANGES/BLOCK verdict and an owner claim marked done. An ordinary clean PASS no longer needs a separate per-bank lead confirmation. The read-only supervisor computes accepted from these independent records; its state.json contains the owner, review file, reviewer, review SHA-256, package and macro fingerprints. Nothing automatically changes bank files or claims. This is evidence of completion of the model specification, not regulatory compliance, audited accuracy, or investment advice.

A current-version PASS must include these exact labels within the newest dated verdict section:
```
Verdict: PASS
Package SHA-256 fingerprint: <64 hex from task.gate.fingerprint>
Macro SHA-256 fingerprint: <64 hex from task.gate.macroFingerprint>
```
State the actual source checks, arithmetic/replay, remaining limitations and reviewed version. Never copy hashes from an old review to bless new content. Mixed historical PASS / forecast CHANGES counts as CHANGES. Supplemental evidence is not a full review. Old PASS without exact current fingerprints must be revalidated by an independent reviewer. After PASS, author checks current supervisor gate and latest review(s), responds to limitations, then marks only their own claim done. If source/model issues arise, reopen and repair rather than conceal them. An accepted model becomes unaccepted if current evidence changes.

For revisions after CHANGES, keep old review evidence, address every finding and set your claim status to needs-review with two extra fields `review_revision: <current package SHA-256>` and `review_macro: <current macro SHA-256>`. Post a message to the reviewer with the changed files and what was fixed. This routes the previous reviewer back to the revision; it does not erase their blocking verdict. If tools cannot compute the fingerprints, ask a peer or use the Room status snapshot. The reviewer appends a dated verdict, without editing prior review sections. If a third review round is still blocking, the lead resolves the dispute or asks the human; do not treat unresolved failures as PASS. All independent evidence requirements remain.

The lead remains responsible for disputed cases, shared methodology, and final sector-level acceptance. The rollup, comparison and final QA tasks become eligible when all bank models meet their acceptance gates. No automatic model calls or chat restarts are added. Agents see these instructions and new messages at their next synchronization.
