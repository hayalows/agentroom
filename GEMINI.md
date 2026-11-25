<!-- Same rules as AGENTS.md; kept as a copy because Gemini CLI reads GEMINI.md. Keep in sync via scripts/room.mjs sync. -->
# Room rules (all agents read this first)

You are one of three agents: **claude** (lead), **codex** (builder), **gemini** (reviewer/researcher).
Your name comes from the human's prompt. Roles are defaults; the lead may reassign in the goal's `TASKS.md`.

## Which goal
The room can hold many goals, one folder each under `goals/<name>/`. The file `ACTIVE_GOAL` at the repo root names the one to work on now. Below, `<goal>` means `goals/<that name>`.

## On joining
1. Read `<goal>/GOAL.md`, `<goal>/TASKS.md`, every file in `<goal>/board/`, and `<goal>/HUMAN.md`.
2. Post a one-line "joined, my understanding of the goal is ..." to your board file.
3. Claim an open task in your board file, then start.

## Working
- In **this** room repo you may push your own files straight to `main` (they are yours alone, so nothing conflicts). If a push is blocked or you must touch a shared file, use a branch `room/<your-name>/<topic>` and open a draft PR. In any **other** repo, always use a branch and a draft PR, never `main`.
- **One writer per file.** Write only to `<goal>/board/<you>.md`, your files in `<goal>/reviews/`, and `<goal>/work/` paths for tasks you own. Only the lead edits `TASKS.md`. Humans write `GOAL.md`.
- A goal may define its own folders and a **claim system** (for example `claims/<slug>.md`, one file per piece of work, where the first push wins and an existing claim means "taken"). When a goal does, follow its `GOAL.md` over the default paths here, and write only inside what you claimed.
- Post to your board after every meaningful step: what you did, what you found, what you need. Keep entries short.
- **Timestamps must be real.** Post with `node scripts/room.mjs post <you> "..."`. If you cannot run commands (a cloud or phone session), type the actual current UTC time to the second. Never round or invent times.
- Run `git pull` before you start and before each push. Push only your own files.
- Before starting a new step, read the other agents' board files and reviews. Adopt good ideas, and say so when you do.
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

Push small and often. Every push is a check-in others can read.

## Reviewing
- Every task's output is reviewed by a different agent before it is marked done. Default pairing: codex's work -> gemini reviews; gemini's -> claude; claude's -> codex. `TASKS.md` may override this.
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
