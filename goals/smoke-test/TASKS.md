# Tasks: smoke-test (lead edits only)

| ID | Task | Owner | Reviewer | Status | Output |
| --- | --- | --- | --- | --- | --- |
| S1 | Join the room (post to your board) | claude, gemini | - | merged | board/ |
| S2 | Write a 3-line Ghana haiku | claude | gemini | merged (PASS) | work/claude-haiku.md |
| S3 | Write a different 3-line Ghana haiku | gemini | claude | merged (PASS) | work/gemini-haiku.md |
| S4 | Cross-read, then quote one thing from the other's work in your board | claude, gemini | - | merged | board/ |
| S5 | Review the other's haiku | claude, gemini | - | merged | reviews/ |
| S6 | Answer the review you received | claude: done. gemini: pending | - | open | board/ |

Codex is not part of this test.

Lead note: the room works end to end. Gemini still owes S6 (an answer to reviews/claude-of-gemini.md).
