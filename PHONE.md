# Running the room from your phone or any app

No PC needed. Each agent works in its own app, connected to this GitHub repo, and everything it does is pushed here. The repo is the meeting place and the memory.

| Agent | Where to open it | Needs |
| --- | --- | --- |
| claude | Claude Code on the web (claude.ai/code), the Claude app, or the Claude desktop app | GitHub connected to your Claude account |
| codex | Codex in ChatGPT (chatgpt.com/codex) or the ChatGPT app | GitHub connected to your ChatGPT account |
| gemini | Jules (jules.google), Antigravity, or the Gemini app if its GitHub link allows edits | GitHub connected |

Connect GitHub once in each app and choose `hayalows/agentroom`. That step is yours. Product names and limits change, so check each app's current setup page.

## How it works
1. You send the agent the card below.
2. The agent reads `AGENTS.md` and the goal, splits its task into 5 milestones, and works.
3. At the end of each milestone it pushes its work and a check-in, then reads what the other agents pushed, avoids duplicating them, and builds on or challenges their work.
4. You read progress in the GitHub app: `goals/<goal>/board/` (check-ins), `work/` (the work) and `reviews/`.

Agents act only when you message them, and they do not talk live. They coordinate by leaving work in the repo. To get more, send the **Continue** card.

## Message cards (copy and paste)

**Start (change NAME to claude, codex or gemini)**
> Work with the GitHub repo hayalows/agentroom (online, not on my PC). Read AGENTS.md fully, then act as "NAME". Read ACTIVE_GOAL and everything in that goal's folder: GOAL.md, TASKS.md, HUMAN.md, every board file, every review and every file under work/. Take your open tasks from TASKS.md. Split your work into 5 milestones, and follow the milestone-and-sync loop in AGENTS.md: at the end of each milestone push your work, check in, then read what the other agents pushed so you do not duplicate it and you advance it. Think independently and be proactive. Push everything to the repo. If you cannot push to main, use a branch room/NAME/<topic> and open a draft PR.

**Continue (any agent)**
> Continue as NAME in hayalows/agentroom. git pull first. Read every board entry, review and work file written by others since your last sync, in full. Then carry on with your next milestone using the loop in AGENTS.md, and push your work and check-in.

**Review**
> As NAME in hayalows/agentroom, review the newest work by the other agents in the active goal. Read it in full, verify claims against the sources, and write reviews/NAME-of-<author>.md. Disagree where the evidence says so. Push it.

## Changing the goal from your phone
Edit `ACTIVE_GOAL` on GitHub to the name of a folder under `goals/`.

## Limits
- Agents do not run on their own, and they do not see each other live. They see each other's pushed work at each milestone.
- If an app cannot push to this repo, it opens a branch and a draft PR. Merge those from the GitHub app.
- Spending, deploys and messages stay off-limits (see AGENTS.md).
