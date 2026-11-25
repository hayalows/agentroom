# Proposals by claude: candidate "big leaps" (task P1-D)

Based on `work/claude/audit-claude.md`. Evidence labels as in the audit. The other agents' audits were not yet in the repo when I wrote this, so these are my independent proposals.

## Leap A: One vertical, end to end ("answer, cite, abstain") (my top pick)
- **What:** pick one high-demand area (candidates from the repo's own 20 scenario domains: tenancy/housing lockout, employment/wages, pensions) and make Ghana Rules fully answer it: verified provision text for the governing Acts, an executable rule pack (using the existing bitemporal engine) for the main questions, and a cited answer with the effective date, or an abstention when evidence is missing.
- **User value:** the first time a citizen gets "your landlord cannot do this; here is the section and the date it applied" rather than a list of links. Bridges the two halves from audit section 4.
- **Evidence it is feasible:** the engine already evaluates date-aware rules with traces (README); the corpus has 364 legislative full texts (V11 report); an admission contract is already written (`V7-RESEARCH.md`).
- **Main risk:** legal correctness (inference verified, interpretation not) and reuse rights for quoted text. Needs a qualified reviewer for the encoding.
- **Effort (inferred):** medium. One vertical, perhaps 5 to 10 Acts and 30 to 60 questions.
- **Success metric:** on a gold set for that vertical (see Leap B), correct cited answer or correct abstention at an agreed rate, with zero wrong confident answers.

## Leap B: A human-verified gold benchmark (the foundation)
- **What:** 150 to 300 real-world questions with answers adjudicated by Ghanaian law students or lawyers, frozen before any tuning, scored blind. Replaces the developer-authored sets as the headline measure.
- **User value:** indirect, but it makes every other claim trustworthy and lets the answer gate be opened safely. Directly addresses the repo's own repeated caveat ("not lawyer-adjudicated").
- **Evidence:** the audit shows the headline gains come from developer-authored sets, while the broad set is flat (about 74% top-1).
- **Main risk:** needs people (reviewers), not code. Cost in time and possibly money.
- **Effort:** medium, mostly coordination. Questions can be drawn from the existing 100 and 309 sets.
- **Success metric:** two independent reviewers agree on at least 85% of labels; the frozen set is used for at least one real before/after comparison.

## Leap C: "Law as of date" consolidated view
- **What:** for a small set of core Acts, build amendment lineage so a user can ask "what did section X say on date D?", using the bitemporal model.
- **User value:** high for lawyers and businesses; fits the engine's strongest idea.
- **Evidence:** V11.2 already generates 64 relationship edges but explicitly "no authoritative amendment or repeal timeline is inferred" (observed). The engine is bitemporal (README).
- **Main risk:** hardest data work (finding every amendment and commencement date). Wrong dates would be worse than none.
- **Effort:** high.
- **Success metric:** for 5 Acts, 100% of tested dates match a lawyer-checked consolidated text.

## My ranking
1. **Leap A, using Leap B's gold set for its own vertical.** Build the gold set first for the chosen vertical (small: about 40 questions), then build the slice. This is the smallest step that changes what a user gets.
2. Leap B at full size, in parallel with human help.
3. Leap C after A shows the pipeline works.

## What I would not do
Another retrieval or ranking version. The audit shows found is already 303/309; the missing value is answers, not leads.
