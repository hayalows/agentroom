#!/usr/bin/env node
// Prints a markdown summary of what each agent posted since START (ISO time).
// Env: GOAL, START, RUN_URL
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { agentsFor } from './participants.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const NL = String.fromCharCode(10);
const goal = process.env.GOAL;
const start = process.env.START || '1970-01-01T00:00:00Z';
let md = '### Room round finished: `' + goal + '`' + NL + NL;
const questions = [];
for (const a of agentsFor(path.join(root, 'goals', goal))) {
  const f = path.join(root, 'goals', goal, 'board', a + '.md');
  const lines = fs.existsSync(f) ? fs.readFileSync(f, 'utf8').split(NL) : [];
  const fresh = lines.filter((l) => /^- \d{4}-/.test(l) && l.slice(2, 26) >= start.slice(0, 24));
  md += '**' + a + '**' + NL;
  if (!fresh.length) md += '- (no new post. Probably no API key set, or the agent was not selected.)' + NL;
  for (const l of fresh) {
    md += '- ' + l.slice(2).slice(0, 900) + NL;
    const q = /QUESTION:?(.*)/.exec(l);
    if (q) questions.push(a + ': ' + q[1].trim().slice(0, 300));
  }
  md += NL;
}
if (questions.length) md += '**Questions for you**' + NL + questions.map((q) => '- ' + q).join(NL) + NL + NL;
md += 'Files: `goals/' + goal + '/` (board, reviews, work). Reply with `/room <instruction>` to run another round.' + NL;
if (process.env.RUN_URL) md += NL + '[Workflow run](' + process.env.RUN_URL + ')' + NL;
process.stdout.write(md);
