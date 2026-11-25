# agentroom

A shared room where Claude, Codex (ChatGPT) and Gemini work on one goal together.
They cannot talk to each other directly, so this repo is where they meet:
they read each other's notes, split the work, and review each other's output.

## How a session works
1. A human writes a goal in `goals/<name>/GOAL.md` and names it in `ACTIVE_GOAL`.
2. Open each agent in a terminal inside this repo and give each the same one-line prompt:
   > Read AGENTS.md and join the room as <claude|codex|gemini>.
   - Claude Code: `claude`
   - Codex CLI: `codex`
   - Gemini CLI: `gemini`
3. The lead (Claude) keeps the plan in the goal's `TASKS.md`. Agents claim tasks, work on their own branch, and post to their own board file.
4. Agents review each other's work into `reviews/`. The lead merges what passes review.
5. The human reads `STATUS.md`, answers questions in `HUMAN.md`, and decides what ships.

## Many goals
Each goal is a folder under `goals/`, with its own plan, board, reviews and questions.

    node scripts/room.mjs new-goal my-next-goal   # copies goals/_template
    node scripts/room.mjs use my-next-goal         # makes it the active goal

Current goals: `ghana-rules` (a big leap for the Ghana Rules engine in `hayalows/research`), `smoke-test` (done). Phone setup: see PHONE.md. Run it fully on GitHub (no PC): see CLOUD.md.

## Layout
| Path | Who writes | Purpose |
| --- | --- | --- |
| `ACTIVE_GOAL` | human | Name of the goal agents work on now |
| `goals/<g>/GOAL.md` | human | The goal and what "done" means |
| `goals/<g>/TASKS.md` | lead only | Plan, owners, reviewers, status |
| `goals/<g>/board/<agent>.md` | that agent only | Progress log, findings, questions to others |
| `goals/<g>/reviews/<reviewer>-of-<author>.md` | reviewer | Critique of another agent's work |
| `goals/<g>/work/` | agents | The actual deliverables |
| `goals/<g>/HUMAN.md` | human + agents | Questions needing a human, and answers |
| `goals/<g>/STATUS.md` | generated | One-page summary |

Rule that prevents conflicts: **each file has one writer.** Read anything, write only your own file.

## Helper
    node scripts/room.mjs post <agent> "message"   # timestamped line on your board
    node scripts/room.mjs status                    # rebuild STATUS.md for the active goal
    node scripts/room.mjs sync                      # copy AGENTS.md to CLAUDE.md and GEMINI.md
