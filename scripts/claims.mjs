#!/usr/bin/env node
// Shows who claimed what in a goal, what is unclaimed, and each agent's last check-in.
// Usage: node scripts/claims.mjs [goal]      (default: ACTIVE_GOAL). Writes goals/<goal>/STATUS-BANKS.md
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { agentsFor, boardEvents } from './participants.mjs';
import { evaluateRoom } from './completion.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const NL = String.fromCharCode(10);
const read = (p) => (fs.existsSync(p) ? fs.readFileSync(p, 'utf8') : '');
const goal = (process.argv.slice(2).find(a => a !== '--stdout') || read(path.join(root, 'ACTIVE_GOAL'))).trim();
const gdir = path.join(root, 'goals', goal);
if (!/^[a-z0-9][a-z0-9-]*$/.test(goal) || !fs.existsSync(gdir)) {
  console.error('no such goal: ' + goal);
  process.exit(1);
}

const claimsDir = path.join(gdir, 'claims');
const claims = [];
for (const f of fs.existsSync(claimsDir) ? fs.readdirSync(claimsDir) : []) {
  if (!f.endsWith('.md')) continue;
  const o = { slug: f.replace(/\.md$/, '') };
  for (const line of read(path.join(claimsDir, f)).split(NL)) {
    const m = /^(\w+):\s*(.*)$/.exec(line.trim());
    if (m) o[m[1]] = m[2];
  }
  claims.push(o);
}

const roster = [];
for (const line of read(path.join(gdir, 'ROSTER.md')).split(NL)) {
  const m = /^\|\s*([a-z0-9-]+)\s*\|\s*(.+?)\s*\|$/.exec(line);
  if (m && m[1] !== 'Suggested' && !m[1].startsWith('---')) roster.push({ slug: m[1], name: m[2] });
}
const shared = ['roster-verification', 'macro-assumptions', 'sector-rollup', 'peer-comparison', 'qa-sweep'];

const taken = new Set(claims.map((c) => c.slug.replace(/-takeover$/, '')));
let md = '# Claims status: ' + goal + NL + NL + 'Generated ' + new Date().toISOString() + NL + NL;
md += '## Claimed' + NL + NL + '| Piece | Agent | Status | Started | Plan |' + NL + '| --- | --- | --- | --- | --- |' + NL;
for (const c of claims.sort((a, b) => a.slug.localeCompare(b.slug))) {
  md += '| ' + c.slug + ' | ' + (c.agent || '?') + ' | ' + (c.status || '?') + ' | ' + (c.started || '?') + ' | ' + (c.plan || '').slice(0, 90) + ' |' + NL;
}
if (!claims.length) md += '| (nothing claimed yet) | | | | |' + NL;

const open = roster.filter((b) => !taken.has(b.slug));
md += NL + '## Unclaimed banks (' + open.length + ' of ' + roster.length + ')' + NL + NL + (open.map((b) => '- ' + b.slug + ' (' + b.name + ')').join(NL) || '(none)') + NL;
const openShared = shared.filter((s) => !taken.has(s));
md += NL + '## Unclaimed shared pieces' + NL + NL + (openShared.map((s) => '- ' + s).join(NL) || '(none)') + NL;

const participants = agentsFor(gdir, claims.map(c => c.agent));
const evaluated=await evaluateRoom(root,goal);
md += NL + '## Load per agent (3 active / 3 submitted waiting)' + NL + NL;
for(const a of evaluated.agents)md += '- '+a.id+': '+a.activeClaims+' active, '+a.awaitingReview+' submitted waiting, '+a.accepted+' accepted; next: '+evaluated.actionable[a.id].next+NL;
md += NL + '## Last check-ins' + NL;
for (const a of participants) {
  const lines = read(path.join(gdir, 'board', a + '.md')).split(NL).filter((l) => /^- \d{4}-/.test(l));
  md += NL + '**' + a + '** (' + lines.length + ' check-ins)' + NL;
  md += (lines.slice(-3).map((l) => '- ' + l.slice(2).slice(0, 260)).join(NL) || '- (none)') + NL;
}
const toLines = boardEvents(gdir, participants).map(e => (e.time || 'undated') + ' ' + e.agent + ' -> ' + e.to + ': ' + e.text.slice(0,200));
md += NL + '## Messages between agents (TO lines)' + NL + NL + (toLines.slice(-12).map((l) => '- ' + l).join(NL) || '- (none yet)') + NL;
if (process.argv.includes('--stdout')) process.stdout.write(md);
else {
fs.writeFileSync(path.join(gdir, 'STATUS-BANKS.md'), md);
console.log('wrote goals/' + goal + '/STATUS-BANKS.md  (' + claims.length + ' claims, ' + open.length + ' banks unclaimed)');

}
