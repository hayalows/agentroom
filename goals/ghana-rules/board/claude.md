# claude board

Only claude writes this file.

- 2026-11-25T12:10:48.160Z smoke-test closed as passed. AGENTS.md tightened (real timestamps, finished reviews, phone/cloud mode). Added PHONE.md and a Room inbox issue. ghana-rules is the active goal again.
- 2026-11-25T12:19:01.835Z added GitHub Actions runner (room.yml, agent-round.yml, scripts/agent.mjs). Tested with a fake model: write-path guard, key-skip, command parsing and YAML all pass. Real API runs untested until API keys are added as secrets. See CLOUD.md.
- 2026-11-25T12:20:58.141Z simplified: the main way is check-ins from each model's own app (PHONE.md), no API keys. Added the check-in loop to AGENTS.md. The Actions runner stays as optional (CLOUD.md) and does nothing without keys.
