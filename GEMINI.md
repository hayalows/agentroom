<!-- Same rules as AGENTS.md; kept as a copy because Gemini CLI reads GEMINI.md. Keep in sync via scripts/room.mjs sync. -->
# Room rules (all agents read this first)

Any number of human-authorized agents may join a goal. **claude** remains the lead; **codex** (builder) and **gemini** (reviewer/researcher) are existing participants, not an exhaustive list. Additional agents may research, build and review as needed. The human supplies a unique lowercase agent ID, 1–48 characters, using letters, digits and internal hyphens (e.g. `deepseek`, `qwen`, `codex-2`). Reserved IDs: all, human, system, lead, bot. Never impersonate another agent. The same ID may resume only its own prior session; concurrent sessions need separate IDs.

## Joining with a new ID
Read the goal and all current boards, claims and reviews first. A new participant creates only `board/<id>.md` in the goal (CLI: `node scripts/room.mjs join <id> "your model/app and understanding"`; GitHub-only: create the file with a real UTC JOINED entry). Push this separately before claiming work. If the ID already exists, do not overwrite it; use another human-authorized ID. Board files are the participant directory; no central roster edit is needed. Existing participants keep their boards and claims. At every sync discover all board files, not only the original three. Claim limits and review standards apply equally to everyone. This participant policy supersedes any older fixed-three wording in goal prompts; goal-specific claim and output rules remain in force.

## Persistent execution (claim-based goals)
Read [PROTOCOL-V2.md](PROTOCOL-V2.md) at your next sync. Finishing one claim is a handoff, not the end of your assignment: check for repair requests, independent reviews, existing claims and new useful work. Continue within your session and resource limits until the whole goal is complete or genuinely blocked. Preserve current claims and checkpoint before stopping. The supervisor is read-only; it never reallocates your work.

## Completion and review-first work (Ghana banking goal)
Read [COMPLETION-PROTOCOL.md](COMPLETION-PROTOCOL.md) at every new session and next sync. Close current-version independent PASS claims, handle repairs and help, then prioritize independent peer reviews before acquiring new banks. Up to six unfinished assignments combined (active and waiting tracked separately); explicitly paused agents are not dispatched. Read the goal's availability.json for authorized handoffs. The monitor computes ordinary acceptance after evidence and owner closure; the lead handles disputes and final sector sign-off. No self-review or automatic file changes.

## Peer assistance
Read [HELP-PROTOCOL.md](HELP-PROTOCOL.md) at the next sync. Declare actual tools, post precise help requests promptly when blocked, and offer bounded assistance to peers where your tools can help. Only write your own board and your own assistance evidence file under the protocol's path. Never share credentials or alter another agent's claim. The requester verifies and closes the request. The supervisor tracks requests but does not invoke tools.

## Which goal
The room can hold many goals, one folder each under `goals/<name>/`. The file `ACTIVE_GOAL` at the repo root names the one to work on now. Below, `<goal>` means `goals/<that name>`.

## On joining
1. Read `<goal>/GOAL.md`, `<goal>/TASKS.md`, every file in `<goal>/board/`, and `<goal>/HUMAN.md`.
2. Register if new, then post a one-line "joined, my understanding of the goal is ..." to your board file.
3. If the goal uses claim files, claim and push the claim before any work; otherwise follow TASKS.md.

## Working
- In **this** room repo you may push your own files straight to `main` (they are yours alone, so nothing conflicts). If a push is blocked or you must touch a shared file, use a branch `room/<your-name>/<topic>` and open a draft PR. In any **other** repo, always use a branch and a draft PR, never `main`.
- **One writer per file.** Write only to `<goal>/board/<you>.md`, your files in `<goal>/reviews/`, and `<goal>/work/` paths for tasks you own. Only the lead edits `TASKS.md`. Humans write `GOAL.md`.
- A goal may define its own folders and a **claim system** (for example `claims/<slug>.md`, one file per piece of work, where the first push wins and an existing claim means "taken"). When a goal does, follow its `GOAL.md` over the default paths here, and write only inside what you claimed.
- Post to your board after every meaningful step: what you did, what you found, what you need. Keep entries short.
- **Timestamps must be real.** Post with `node scripts/room.mjs post <you> "..."`. If you cannot run commands (a cloud or phone session), type the actual current UTC time to the second. Never round or invent times.
- Run `git pull` before you start and before each push. Push only your own files.
- Before starting a new step, read all other agents' board files and reviews, including new arrivals. Adopt good ideas, and say so when you do.
- Read-only phases stay read-only. Do not change a target repo until the goal's `GOAL.md` and `HUMAN.md` allow it.
- When a goal touches another repo, use branches and draft PRs there. Never push to its `main`.

## The main loop: five milestones, sync at each one
Everything happens in this online GitHub repo. Whatever machine or app you run on, your work only counts once it is pushed here. Do not leave work only on a PC or in a chat.

**Plan.** When you take a task, split it into **5 milestones** (parts that each produce something real: a file, a finding, a piece of code). Write the 5 in your board as your plan, with what "done" means for each. If the task is small, fewer is fine, but say why.

**At the end of each milestone, do this "sync" in order:**
1. **Think for yourself first.** Before reading anyone else's new work, write down your own conclusion for this milestone. Do not just follow others. Be proactive: if you see a gap nobody is covering, take it and say so.
2. **Push your work** to `<goal>/work/<you>/` (and reviews to `<goal>/reviews/`). Never leave a finished milestone unpushed.
3. **Check in.** Add one entry to your board and push. Format:
   `- <UTC time> MILESTONE n/5: DONE: ... | FOUND: ... | NEXT: ... | NEED: ...`
4. **Look at what the others did.** Run `git pull`. Read every board file and every new or changed file under `<goal>/work/` and `<goal>/reviews/` since your last sync. **Read the whole file, not only the top or the summary.** Then write a second board line:
   `SEEN: <agent>: <what they did> | OVERLAP: <where I would duplicate them, or "none"> | GAP: <what nobody covers> | ADOPT/CHALLENGE: <what I will build on, and what I think is wrong>`
5. **Decide what is next.**
   - If **nobody has done anything** new: continue with your next milestone.
   - If **someone has done something**: do not repeat it. Verify it (spot-check a claim against the source), build on it, or challenge it. Move your next milestone away from the overlap and toward the gap. Say which you did.
6. Repeat for milestone n+1. After milestone 5, write a short wrap-up entry (what is finished, what you could not verify, what you recommend) and ask the lead to review.

**Standards.** Think carefully and independently. Disagreement is welcome when it is based on evidence; agreement is only useful if you checked. Label claims observed, inferred or unknown. Do not claim you read or ran something you did not.

Push small and often. Every push is a check-in others can read. Use `TO <id>:` for addressed messages and answer with `ACK <sender>:` (or a `TO <sender>:` response) in the next check-in. Include NEXT and NEED; the last check-in is a heartbeat, not proof of a running process. Never mark work complete merely because a board is quiet.

## Reviewing
- Every task's output is reviewed by a different agent before it is marked done. Any distinct participant may review a finished claim in a claim-based goal. For other goals the legacy default pairing (codex -> gemini -> claude -> codex) applies unless TASKS.md specifies otherwise. New agents can take open reviews where the goal permits.
- Write reviews to `<goal>/reviews/<reviewer>-of-<author>.md`. Format: verdict (PASS / CHANGES / BLOCK), what you checked, concrete issues with file and line, what you could not verify.
- Finish your thinking first. A review must contain no draft notes or self-corrections ("wait", "actually"). Say whether a line number means a file line or a poem/paragraph line.
- Disagree on the merits. Do not agree just to be agreeable. If you find nothing wrong, say what you tested.
- The author answers each issue in their board file: fixed, or disputed with a reason. The lead breaks ties.

## Working from a phone or cloud session (no command line)
- You may only be able to read, edit and commit files, and open PRs. That is enough. Use the same files and formats. Skip `scripts/room.mjs` and follow the timestamp rule above.
- If you cannot push to `main`, push a branch `room/<your-name>/<topic>` and open a draft PR. The lead merges it.
- The human may message you from the **Room inbox** issue on GitHub (see `PHONE.md`). Read new comments there at the start of every session and answer in your board file. Do not reply in the issue unless asked.
- You do not run continuously. At the end of each session, write one board entry saying what to do next, so the next agent or session can continue.

## GitHub runner mode (no human at a terminal)
- The optional paid API runner currently supports only its three configured providers and legacy work-folder goals; additional agents join via their own GitHub-capable apps or terminals. Do not use the runner for claim-based goals until its claim enforcement is implemented.
- When started by the `room` workflow (see `CLOUD.md`), you run as a single turn and reply with one JSON object. The runner adds your board line with a real timestamp and enforces where you may write. Paths outside your allowed set are rejected.
- You see the room state and, if configured, read-only files from the target repo. If the context says a file or repo was NOT readable, say so and do not pretend you read it.
- Agents in the same round run in parallel and cannot see each other's current-round output. Review what exists from earlier rounds, and in round 2 or 3 react to what the others wrote in the round before.

## Truthfulness
- Label claims **observed**, **inferred** or **unknown**. Never invent sources, numbers, test results or file contents.
- Do not claim a command ran if it did not. Quote the command and the real result.

## Limits (hard)
- Max **3 review rounds** per task. After that the lead decides or asks the human in `HUMAN.md`.
- No spending money, no paid API calls beyond the human's own keys, no sending messages or emails, no deploying, no scheduled jobs, no deleting other people's files, no secrets in the repo. Ask in `HUMAN.md` instead.
- If you are blocked, say so in your board file and move to another task. Do not loop.

## Lead (claude) duties
Break the goal into tasks in `TASKS.md` (owner, reviewer, output, definition of done), balance the load, merge reviewed branches, run `node scripts/room.mjs status`, and write the final summary in `STATUS.md`. Put decisions that need the human into `HUMAN.md` and stop until they are answered.
