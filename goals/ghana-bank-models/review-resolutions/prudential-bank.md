# Lead scope decision: prudential-bank (source unavailable)

Lead: claude. Date: 2026-11-25. This is a scope decision under the round cap, not a review verdict, and it does not accept the model by itself.

## Situation
The only open finding is that Prudential's 30 Sep 2026 bank-only statement is missing. I tried to find it: prudentialbank.com.gh/ifs lists "FINANCIAL STATEMENT Q3 2026" but the site returns HTTP 502 to every agent and to the human (reported by the human, 2026-11-25). The Wayback Machine's newest copy of that page is 2026-07-18 (before the Q3 file existed), so the PDF's file name (`/pdfs/<epoch>_...`) is not discoverable. Searches (web and news) found no mirror, no press release and no news report of Prudential's 9M-2026 figures. The GH¢1.13bn Bloom Africa capital injection (October 2026) is confirmed by the issuer and the Ministry of Finance but without a post-event capital ratio.

## Decision
1. The 9M-2026 period is declared `unavailable` for Prudential after documented, bounded retries. Nothing may be invented to fill it.
2. The model may be accepted **as a conditional model** if (a) the FY2025 audited year-end is the last reported anchor, (b) FY2026E is labelled an estimate that is not anchored on a 9M actual, (c) the recapitalisation is shown as an explicit labelled assumption/sensitivity (amount from the issuer and Ministry of Finance only), and (d) the README and roll-up/peer-comparison rows carry the label "conditional: 9M-2026 unavailable".
3. The reviewer (chatgpt-support, round-2 BLOCK) is asked to re-issue its verdict at the current fingerprint under this scope: PASS-with-limitation if the four conditions hold, otherwise a specific CHANGES list. A second distinct independent PASS is needed as for every bank (claude-helper-1 or papa-kojo-agent).
4. If the PDF becomes reachable, the owner must patch in the real 9M-2026 and re-review; this scope decision then lapses.
