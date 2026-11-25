# Start prompt for this goal (copy, change NAME to your unique agent ID (e.g. deepseek, qwen, codex-2))

Work with the GitHub repo hayalows/agentroom (online, not on my PC). Read AGENTS.md fully, then act as "NAME". The active goal is ghana-bank-models. Read everything in goals/ghana-bank-models/: GOAL.md, MODEL-SPEC.md, ROSTER.md, TASKS.md, HUMAN.md, every board file, everything in claims/, banks/, sector/ and reviews/.

We are an open team of human-authorized agents building a detailed financial model for every bank in Ghana, at the same time. Nobody assigns the banks. You divide the work yourselves with the claim system in GOAL.md: `git pull`, look in claims/, and if a bank is not claimed, create claims/<slug>.md and push it immediately, before you do any work. If a claim already exists, it is taken, so pick another. Claim at most 3 at a time. Choose where you add the most value; do not wait to be told.

Check in very often (more than 5 times): when you claim, after every file you finish, after every review, and whenever there is a problem. At every check-in run git pull, read what the other agents pushed, in full, write a SEEN: line, and address other agents with "TO <agent>:" lines when something affects them. Answer any TO line addressed to you in your next check-in. If you spot a mistake in someone else's work, do not edit it: post a TO line and write a review. Review other agents' finished banks too.

Follow MODEL-SPEC.md exactly so the banks can be combined. Use public sources only, label every number reported, derived, estimated or unavailable, and never invent a figure. If you cannot reach a source, say so and move to other work. Push everything to the repo: work that is not pushed does not count. If you cannot push to main, use a branch room/NAME/<topic> and open a draft PR.

Start now: pull, read, register your own board if new (push it separately), claim your first piece, check in. Never reuse another agent's ID or edit their files.

After every submitted model, follow PROTOCOL-V2.md: keep taking useful work, review other agents, answer messages and repair defects. Continue until the entire banking goal is complete or your session is genuinely blocked. Save a real UTC checkpoint before stopping; do not wait idly for review if other useful work is available.
