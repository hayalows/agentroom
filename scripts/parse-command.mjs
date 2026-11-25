#!/usr/bin/env node
// Turns a "/room ..." comment or workflow inputs into outputs for the workflow.
// Comment form:  /room [goal=<slug>] [rounds=1-3] [agents=claude,codex,gemini] <instruction...>
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import crypto from 'node:crypto';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const NL = String.fromCharCode(10);
const ALL = ['claude', 'codex', 'gemini'];
const env = process.env;

let goal = '';
let rounds = '2';
let agents = 'all';
let instruction = '';

if (env.EVENT === 'issue_comment') {
  let text = (env.COMMENT_BODY || '').trim();
  text = text.replace(/^\/room\b/, '').trim();
  const words = text.split(/\s+/);
  const rest = [];
  let flags = true;
  for (const w of words) {
    const m = flags && /^(goal|rounds|agents)=(\S+)$/.exec(w);
    if (m) {
      if (m[1] === 'goal') goal = m[2];
      if (m[1] === 'rounds') rounds = m[2];
      if (m[1] === 'agents') agents = m[2];
    } else {
      flags = false;
      rest.push(w);
    }
  }
  instruction = rest.join(' ');
} else {
  goal = env.IN_GOAL || '';
  rounds = env.IN_ROUNDS || '2';
  agents = env.IN_AGENTS || 'all';
  instruction = env.IN_INSTRUCTION || '';
}

if (!goal) goal = fs.readFileSync(path.join(root, 'ACTIVE_GOAL'), 'utf8').trim();
if (!/^[a-z0-9][a-z0-9-]*$/.test(goal) || !fs.existsSync(path.join(root, 'goals', goal))) {
  console.error('unknown goal: ' + goal);
  process.exit(1);
}
rounds = String(Math.min(3, Math.max(1, parseInt(rounds, 10) || 2)));
const list = agents === 'all' ? ALL : agents.split(',').map((s) => s.trim()).filter((s) => ALL.includes(s));
if (!list.length) {
  console.error('no valid agents in: ' + agents);
  process.exit(1);
}
instruction = instruction.replace(/\s+/g, ' ').trim().slice(0, 1500) || 'Continue the active goal.';

const d = 'EOF_' + crypto.randomBytes(8).toString('hex');
const out =
  'goal=' + goal + NL + 'rounds=' + rounds + NL + 'agents=' + list.join(',') + NL +
  'start=' + new Date().toISOString() + NL +
  'instruction<<' + d + NL + instruction + NL + d + NL;
fs.appendFileSync(env.GITHUB_OUTPUT || '/dev/stdout', out);
