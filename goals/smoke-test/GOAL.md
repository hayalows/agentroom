# Goal: smoke test (prove two agents can collaborate through the room)

## Goal
A tiny, harmless test. Claude and Gemini each join, read each other's notes, produce one small file, and review the other's file. Nothing outside this repo is touched.

## Phases
1. Join: each agent posts a one-line join message to its own board file.
2. Make: Claude writes `work/claude-haiku.md` (a 3-line haiku about Ghana). Gemini writes `work/gemini-haiku.md` (a different 3-line haiku about Ghana).
3. Cross-read: each agent reads the other's board file and haiku, and quotes one thing from it in its own board.
4. Review: Gemini writes `reviews/gemini-of-claude.md`; Claude writes `reviews/claude-of-gemini.md`. Each gives a verdict (PASS / CHANGES), one strength and one concrete suggestion.
5. Respond: each author answers the review in their own board file (fixed, or disputed with a reason).

## Done means
- [ ] Both board files show a join message and a reference to the other agent's work.
- [ ] Both haikus exist.
- [ ] Both reviews exist with a verdict.
- [ ] Each author answered the review.

## Constraints (hard)
- Write only to your own files. No other repos, no deploys, no spending.
- Do not invent: if you could not read the other agent's file, say so.

## Output
- `goals/smoke-test/work/`, `goals/smoke-test/reviews/`, `goals/smoke-test/board/`
