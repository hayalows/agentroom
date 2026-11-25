# Agent Room supervisor v2

## Start here

- Open [Room status](https://github.com/hayalows/agentroom/actions/workflows/status.yml). The latest completed run has a task table, agent check-ins, messages and suggested next work. The downloadable room snapshot contains full JSON and an interactive local HTML viewer. No public deployment or write-back to workers' files.
- `node scripts/supervisor.mjs` prints the same view from a fresh checkout. `--json` returns structured data and exact bank/macro fingerprints. `--out /path/outside/repo` writes snapshot files. A snapshot is not a live connection.
- All agents use [PROTOCOL-V2.md](PROTOCOL-V2.md). Existing claims, boards and bank files stay intact. Review submissions aren't accepted automatically.

## Continuous execution: explicit opt-in

The room cannot remotely resume arbitrary ChatGPT, Claude or Gemini consumer chat sessions. A supported host CLI/API adapter is necessary. The generic command adapter host is included, but no provider is configured or launched by this change. Use a dedicated clean checkout of main, and independent authenticated worker apps/checkouts. Do not run two simultaneous sessions with the same ID or use another agent's credentials. Only one operator per room should run this local supervisor; its lock is local, not a distributed lease.

Create a private config outside Git, e.g.:
```json
{
  "authorized": false,
  "stateDir": "/absolute/path/room-state",
  "maxTurns": 12,
  "maxMinutes": 60,
  "turnTimeoutMinutes": 15,
  "pollSeconds": 30,
  "parallel": 3,
  "workers": [
    {"id":"codex","cwd":"/absolute/path/worker","argv":["/absolute/path/to/your-approved-adapter","{prompt}"]}
  ]
}
```
The example executable is a placeholder, not an installed provider command. The adapter must accept the prompt as a single argument, start/resume the registered worker, return when its turn ends and respect the existing no-spend/no-deploy/path rules. Configure authentication separately; never store secrets in config, prompts or logs. Provider-specific adapters must be tested for real authentication, permissions, process cancellation (including children) and costs. The runner only invokes explicitly configured commands without a shell; the executable itself remains a trusted boundary.

Dry run: `node scripts/worker-loop.mjs --config /absolute/path/config.json`. Inspect prompts and limits. When you have explicitly approved the actual adapters and resource limits, set authorized=true and add `--execute`. It runs only while the host process is alive, bounded by maxTurns/maxMinutes, per-turn timeout, concurrency and failure limits. It refreshes main before each batch and stops when no fresh checkpoint exists, the goal claims are complete or the budget is exhausted. It never auto-takes over claims. Restart manually to resume after a no-progress stop; verify no prior process is alive before removing a stale local lock. It logs dispatch/exit metadata only, not provider secrets or arbitrary model output. It does not enforce provider-level token billing or kill arbitrary detached descendants; the adapter must do that. Do not run it on a shared or dirty checkout.

## Quality and rollback

The evidence gate imports the exact Agent Team Architect v1.2 engine, with four binary mandatory checks. This is not a replacement for the existing bank model spec or independent review. Candidate and macro fingerprints change when inputs change. Human/lead confirms acceptance and adjudicates conflicting reviews. No historical score is invented, and no untrusted model code is executed in monitoring CI. To disable the execution host, stop the process; to disable automatic snapshots, disable the Room status workflow. The upgrade has no migration of active claims or model files.
