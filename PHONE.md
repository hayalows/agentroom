# Running the room from your phone

No laptop needed. Each agent has a cloud version that works on this GitHub repo and pushes its results back. The repo is the meeting place. Product names and limits change, so check each one's current setup page.

| Agent | Where to open it | Needs |
| --- | --- | --- |
| claude | Claude Code on the web (claude.ai/code), or the Claude mobile app | GitHub connected to your Claude account |
| codex | Codex in ChatGPT (chatgpt.com/codex), or the ChatGPT mobile app | GitHub connected to your ChatGPT account |
| gemini | Jules (jules.google), or the Gemini app if its GitHub connection allows edits | GitHub connected to Jules |

You connect GitHub once in each app, and choose the `hayalows/agentroom` repo. That step is yours. An agent cannot do it for you.

## How a round works
1. Write what you want in the **Room inbox** issue on GitHub (a comment), or in `goals/<goal>/HUMAN.md`.
2. Open each agent's app and paste its message card below.
3. Each agent reads the rules and the others' notes, does its task, pushes, and writes what to do next on its board.
4. On the GitHub mobile app, read `goals/<goal>/STATUS.md` or the board files. Answer questions in the inbox.

Agents only act when you message them. They do not run on their own. To get the next round, send the same card again ("continue").

## Message cards (copy and paste)

**Claude**
> Repo: hayalows/agentroom. Read AGENTS.md, then act as "claude" (lead). Read the active goal in ACTIVE_GOAL, its GOAL.md, TASKS.md, all board files, HUMAN.md, and the newest comments on the Room inbox issue. Do your open tasks, update TASKS.md, review others' work, and put anything needing me into HUMAN.md. Use a branch room/claude/<topic> and open a draft PR if you cannot push to main.

**Codex**
> Repo: hayalows/agentroom. Read AGENTS.md, then act as "codex" (builder). Read the active goal in ACTIVE_GOAL, its GOAL.md, TASKS.md, all board files, HUMAN.md, and the newest comments on the Room inbox issue. Claim and do your open tasks, write to your own board file only, and review gemini's work. Use a branch room/codex/<topic> and open a draft PR.

**Gemini**
> Repo: hayalows/agentroom. Read AGENTS.md, then act as "gemini" (reviewer and researcher). Read the active goal in ACTIVE_GOAL, its GOAL.md, TASKS.md, all board files, HUMAN.md, and the newest comments on the Room inbox issue. Do your open tasks, write to your own board file only, and review claude's work. Use a branch room/gemini/<topic> and open a draft PR.

**Continue** (any agent)
> Continue as <your name>. git pull first. Read every board entry written since your last one, answer any review of your work, then do the next open task. End with a board note saying what is next.

## Changing the goal from your phone
Edit `ACTIVE_GOAL` on GitHub to the name of a folder under `goals/`. The next round of every agent follows it.

## Limits
- Agents do not talk live. They coordinate by leaving notes in the repo, one round at a time.
- Cloud agents may not run `node scripts/room.mjs`. The rules cover that.
- Spending, deploys and messages stay off-limits for all agents (see AGENTS.md).
