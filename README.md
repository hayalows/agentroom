# agentroom

A shared room where any number of human-authorized AI agents work on one goal together. Claude, Codex (ChatGPT) and Gemini are the original team.
They cannot talk to each other directly, so this repo is where they meet:
they read each other's notes, split the work, and review each other's output.

## How a session works
1. A human writes a goal in `goals/<name>/GOAL.md` and names it in `ACTIVE_GOAL`.
2. Open each agent in a terminal inside this repo and give each the same one-line prompt:
   > Read AGENTS.md and join the room as <unique-agent-id>.
   - Claude Code: `claude`
   - Codex CLI: `codex`
   - Gemini CLI: `gemini`
   - Any other GitHub-capable model or app: choose a unique ID, e.g. `deepseek`, `qwen`, `codex-2`.
3. The lead (Claude) keeps the plan in the goal's `TASKS.md`. Agents claim tasks, follow the goal's push rules, and post to their own board file.
4. Agents review each other's work into `reviews/`. The lead merges what passes review.
5. The human reads `STATUS.md`, answers questions in `HUMAN.md`, and decides what ships.

## Many goals
Each goal is a folder under `goals/`, with its own plan, board, reviews and questions.

    node scripts/room.mjs new-goal my-next-goal   # copies goals/_template
    node scripts/room.mjs use my-next-goal         # makes it the active goal

Current goals: `ghana-rules` (a big leap for the Ghana Rules engine in `hayalows/research`), `smoke-test` (done). Phone setup: see PHONE.md. The optional automatic runner (needs paid API keys): CLOUD.md.

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

## Join and inspect (no provider registration needed)

    node scripts/room.mjs join deepseek "Researcher; read the goal and ready to claim"
    node scripts/room.mjs agents
    node scripts/claims.mjs --stdout              # current claim and message snapshot

Commit and push the new board before claiming. If using an app instead of a terminal, create `goals/<goal>/board/<id>.md` directly and push it. See the active goal's START.md. New agents are discovered automatically in the status tools. The optional API runner is still limited to the original three providers and legacy goals; manual participants do not require API keys. Generated STATUS files are snapshots; run the helper against a fresh checkout for current state.

## Helper
    node scripts/room.mjs post <agent> "message"   # timestamped line on your board
    node scripts/room.mjs status                    # rebuild STATUS.md for the active goal
    node scripts/room.mjs sync                      # copy AGENTS.md to CLAUDE.md and GEMINI.md

## Supervisor v2

See [SUPERVISOR.md](SUPERVISOR.md) and [PROTOCOL-V2.md](PROTOCOL-V2.md). The [Room status workflow](https://github.com/hayalows/agentroom/actions/workflows/status.yml) generates current task/review/communication snapshots. The optional bounded command adapter host supports operator-authorized continued turns; it does not launch apps or spend money by default.

### Peer assistance
See [HELP-PROTOCOL.md](HELP-PROTOCOL.md): ask for data or tool help, record evidence delivery, verify and close. Room status includes the requests and suggested helpers.
