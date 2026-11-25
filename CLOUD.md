> **Optional.** You do not need this. The simple way (no API keys) is in PHONE.md: each model works in its own app and checks in to the repo. This file describes an extra, automatic runner that uses paid API keys.

# Run the room entirely on GitHub

No PC, no command line. A GitHub Actions workflow runs Claude, Codex (OpenAI) and Gemini **in parallel** as jobs. Each reads the whole room, does its role, and commits its findings to this repo. You message them from the GitHub app or website.

## One-time setup (about 10 minutes, you do this, I cannot)
1. **Get API keys.** Chat subscriptions (Claude, ChatGPT, Gemini) are *not* API access. You need API keys, billed per use. Set a monthly spend limit in each console.
   - Anthropic: console.anthropic.com
   - OpenAI: platform.openai.com
   - Google: aistudio.google.com (Gemini API key)
2. **Add them as repository secrets:** GitHub > `hayalows/agentroom` > Settings > Secrets and variables > Actions > New repository secret.
   - `ANTHROPIC_API_KEY`
   - `OPENAI_API_KEY`
   - `GEMINI_API_KEY`
   - Optional: `RESEARCH_READ_TOKEN`. A fine-grained personal access token with **read-only** `Contents` access to `hayalows/research` only. Without it, agents cannot read the research repo and will say so.
   Never paste keys into chat, issues or files.
3. **Optional model names** (Settings > Secrets and variables > Actions > Variables): `CLAUDE_MODEL`, `OPENAI_MODEL`, `GEMINI_MODEL`. Defaults are in `scripts/agent.mjs` and may need updating to the model names your accounts offer.
4. Settings > Actions > General > Workflow permissions: choose **Read and write permissions**.

An agent whose key is missing is skipped. The others still run.

## Scope limitation
The optional API runner is limited to its three configured providers and legacy work-folder goals. For claim-based goals (including ghana-bank-models), use GitHub-capable apps/terminals following the goal START.md; they can register any unique participant ID without API keys. The runner does not implement claim acquisition or bank-folder writes.

## How to use it
**From the GitHub app or site (works on a phone):** comment on the issue titled **Room inbox**:

    /room Find the three biggest gaps in the engine and propose one big leap.

Options go before the instruction:

    /room rounds=3 agents=claude,gemini goal=ghana-rules Review each other's proposals.

| Option | Meaning | Default |
| --- | --- | --- |
| `rounds` | 1 to 3. In each round all agents run at the same time; the next round sees what the others wrote | 2 |
| `agents` | `all`, or a list like `claude,gemini` | all |
| `goal` | A folder under `goals/` | the one in `ACTIVE_GOAL` |

Only comments from the repo owner trigger a run. You can also use Actions > room > Run workflow.

When the run finishes, a summary comment appears on the Room inbox with each agent's report and any questions for you. The full output is in `goals/<goal>/` (board, reviews, work).

## What the agents can and cannot do here
- Each is a single turn per round: it reads the room (and the target repo, if configured) and writes files. It cannot run code or ask questions mid-turn.
- The runner enforces where each agent may write: its own `work/<agent>/`, its own `reviews/`, and an appended line on its own board. Claude can also edit `TASKS.md` and append to `HUMAN.md`. Writes anywhere else are rejected and logged.
- The target repo (`goals/<goal>/target.json`) is **read-only**. Agents propose changes as files in `work/`. Nothing is pushed to `research`.
- Rounds cost API money. Rough size: each agent call can read around 100k characters and writes up to about 7k tokens. Start with `rounds=1` and watch your usage.

## Safety
- Owner-only trigger, no scheduled runs, no deploys, no messages sent anywhere except the Room inbox comment.
- Repo contents are given to the models as data. Their output is limited by the path rules above.
- Keys are only available to the workflow, never written to files.
