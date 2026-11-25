# Goal: financial models for all the banks in Ghana

## Goal
Together, build a detailed, sourced, comparable financial model for **every licensed bank in Ghana**, and then a sector roll-up. Any number of human-authorized agents work **at the same time** (initial team: claude, codex, gemini). New participants register their unique board ID following AGENTS.md before claiming; existing claims and review requirements are unchanged. They divide the work **themselves** using the claim system below, check in often, and read each other's work so nobody duplicates anybody.

This is the first live test of the room, so the coordination matters as much as the models.

## What "a model" means
See `MODEL-SPEC.md` (the shared format). In short, for each bank: sourced historical financials (about 5 years), a transparent 5-year forecast with explicit assumptions and three scenarios, ratio checks, and a short written summary. Every number is either sourced to a public filing, derived by a stated formula, or marked estimated or unavailable. **Never guess a reported number.**

## The roster
`ROSTER.md` lists the banks (from the lead's memory, **unverified**). Verifying it against the Bank of Ghana's published list of licensed banks is the first shared piece of work. Use the verified list, not the starting one.

## How the agents divide the work (no one assigns it)
**Claims.** One file per piece of work: `claims/<slug>.md`.
1. `git pull`. Look in `claims/`. If `claims/<slug>.md` exists, **it is taken. Do not work on it.** Pick another.
2. If it does not exist, create it with the content below, commit and **push immediately** (before you do any work):
   ```
   agent: <you>
   piece: <bank or shared piece>
   started: <real UTC time>
   status: in-progress
   plan: <one or two lines: what you will deliver>
   ```
3. If your push is rejected, run `git pull --rebase`. If Git reports a conflict on that claim file, someone claimed it at the same moment and **you lost**. Abort (`git rebase --abort`), discard your claim commit (`git reset --hard origin/main`), and pick another piece. Make the claim its **own commit containing only the claim file**, so discarding it loses nothing. If your app cannot run these commands, just check whether the claim file on `main` names someone else, and if so, drop your attempt.
4. Only the claimer edits their own claim file (update `status:` to `in-progress`, `done`, `needs-review` or `released`). Update it at every check-in.
5. **Limit and review priority:** follow [COMPLETION-PROTOCOL.md](../../COMPLETION-PROTOCOL.md): at most **3 active building/repair claims** and no additional new claims when **3 submitted claims await review**. Submitted clean work remains owned but does not consume an active slot. Close passed models, handle repairs/help and review others before taking more banks.
6. **Stale claims:** if a claim shows no activity for 24 hours, anyone may post `TO <owner>: is <slug> still yours?` on their board. If there is no answer by the next sync, post `TAKING OVER <slug>` and create `claims/<slug>-takeover.md`.

**Slugs.** Banks use a short lowercase name, e.g. `absa-ghana`, `gcb`. Shared pieces use:
- `roster-verification`: check `ROSTER.md` against the Bank of Ghana list, report differences on your board (the lead updates the file).
- `macro-assumptions`: one shared set of macro drivers all bank forecasts use (policy rate, T-bill and bond yields, inflation, GHS exchange rate, GDP growth), with sources and three scenarios.
- `sector-rollup`: combine all banks' outputs into a sector view. Needs bank models to exist first.
- `peer-comparison`: ratios side by side with commentary.
- `qa-sweep`: independent checks across finished banks (balance sheets balance, totals add up, sources resolve).
Agents may propose other shared pieces by claiming them.

**Who does what is up to you.** Look at what is claimed, think about where you add the most, and take it. Do not wait to be told.

## Check-ins: regular, specific, addressed
This test needs **more than 5 check-ins each**. Read every board including new participants; acknowledge addressed messages at your next sync. Check in **at all of these moments**:
- right after you claim something (the claim push itself),
- after every file you finish (financials loaded, ratios checked, assumptions written, forecast built, summary written),
- after every review you write,
- whenever you hit a problem or a decision others should know about.

**At every check-in, sync** (this is the point of the test):
1. `git pull`. Read every other board file since your last sync, and open the files they pushed.
2. Write your check-in line, then a `SEEN:` line saying what the others did.
3. If something affects another agent, **address it**: `TO <agent>: ...` on your board. Examples: "TO gemini: your Absa loan figures for FY2023 differ from the annual report p.45, please recheck", "TO codex: macro-assumptions is done, please use it for your forecasts".
4. **Answer** every `TO <you>:` line addressed to you in your very next check-in.
5. If you see a mistake in someone's work, **do not edit their files**. Post a `TO` line and write `reviews/<you>-of-<them>.md`.

Format: `- <UTC time> CLAIM|DONE|REVIEW|PROBLEM <slug>: <what> | NEXT: <what> | NEED: <what>` followed by `SEEN: ...` and any `TO <agent>: ...`.

## Reviews
Every finished bank model is reviewed by a **different** agent before it counts. When a claim is marked `needs-review`, any other agent may pick it up: write `reviews/<you>-of-<owner>-<slug>.md` with verdict PASS / CHANGES / BLOCK. The reviewer must **recompute** at least: balance sheet balances, totals add up, two sourced numbers match the filing, forecast checks pass. The owner answers each issue in their board (fixed or disputed). Max 3 rounds, then the lead resolves the dispute. The author marks their own claim done after current-version independent PASS and passing core checks. Ordinary acceptance is computed without a second per-bank lead approval; unresolved issues cannot pass. See COMPLETION-PROTOCOL.md.

## Where the work goes
Because the work is by bank, this goal uses these folders instead of `work/<agent>/`. **Write only inside a folder you claimed** (plus your own board and reviews):
- `banks/<slug>/` for each bank
- `sector/<piece>/` for shared pieces (`macro-assumptions`, `sector-rollup`, etc.)

## Done means
- [ ] The roster is verified against the Bank of Ghana list, and every bank on it is either modelled or listed with a reason it was not.
- [ ] Every modelled bank has all the files in `MODEL-SPEC.md`, passes its checks, and has been reviewed by a different agent.
- [ ] One shared macro-assumptions set is used by every forecast.
- [ ] A sector roll-up and peer comparison exist, built only from finished banks.
- [ ] `STATUS-BANKS.md` (made by `node scripts/claims.mjs`) shows who did what, with no duplicate work.
- [ ] A final summary lists what is verified, what is unavailable, and what remains.

## Constraints (hard)
- **Not investment advice.** No buy/sell opinions, no price targets presented as advice. Do not place any trade.
- **Sourced numbers only.** If a figure is not in a public filing you can read, mark it `unavailable`. Do not invent or fill it from memory. If your app cannot reach the internet or a filing, say so on your board and do other work.
- Public sources only (company annual reports and financial statements, the Bank of Ghana, the Ghana Stock Exchange, regulators). Respect site terms. No logins, no bypassing access limits.
- Do not claim you read, ran or verified something you did not.
- No spending, no deploys, no messages to anyone outside the repo.
- Everything goes to this online repo. Work not pushed does not count.

## Output
`banks/`, `sector/`, `claims/`, `reviews/`, `board/`, and the final summary in `sector/summary.md`.
