#!/usr/bin/env node
// Tiny helper for the room. No dependencies.
// Usage:
//   node scripts/room.mjs post <claude|codex|gemini> "message"
//   node scripts/room.mjs status
//   node scripts/room.mjs sync
//   node scripts/room.mjs new-goal <slug>
//   node scripts/room.mjs use <slug>
// Add --goal <slug> to post/status to target a goal other than ACTIVE_GOAL.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const AGENTS = ['claude', 'codex', 'gemini'];
const NL = String.fromCharCode(10);
const read = (p) => (fs.existsSync(p) ? fs.readFileSync(p, 'utf8') : '');

let argv = process.argv.slice(2);
let goalFlag = null;
const gi = argv.indexOf('--goal');
if (gi !== -1) {
  goalFlag = argv[gi + 1];
  argv.splice(gi, 2);
}
const [cmd, ...args] = argv;

function goalName() {
  const name = goalFlag || read(path.join(root, 'ACTIVE_GOAL')).trim();
  if (!name || !/^[a-z0-9][a-z0-9-]*$/.test(name)) {
    console.error('no valid goal. set ACTIVE_GOAL or pass --goal <slug>');
    process.exit(1);
  }
  const dir = path.join(root, 'goals', name);
  if (!fs.existsSync(dir)) {
    console.error('goal folder not found: goals/' + name);
    process.exit(1);
  }
  return { name, dir };
}

function post(agent, message) {
  if (!AGENTS.includes(agent) || !message) {
    console.error('usage: room.mjs post <claude|codex|gemini> "message"');
    process.exit(1);
  }
  const { name, dir } = goalName();
  const line = '- ' + new Date().toISOString() + ' ' + message + NL;
  fs.appendFileSync(path.join(dir, 'board', agent + '.md'), line);
  console.log('posted to goals/' + name + '/board/' + agent + '.md');
}

function status() {
  const { name, dir } = goalName();
  let out = '# Room status: ' + name + NL + NL + 'Generated ' + new Date().toISOString() + NL + NL;
  out += read(path.join(dir, 'GOAL.md')) + NL;
  out += read(path.join(dir, 'TASKS.md')) + NL;
  for (const a of AGENTS) {
    const lines = read(path.join(dir, 'board', a + '.md')).split(NL).filter((l) => l.startsWith('- '));
    out += NL + '## ' + a + ' (last 5 of ' + lines.length + ' posts)' + NL;
    out += (lines.slice(-5).join(NL) || '(no posts)') + NL;
  }
  const revDir = path.join(dir, 'reviews');
  const revs = fs.existsSync(revDir) ? fs.readdirSync(revDir).filter((f) => f.endsWith('.md')) : [];
  out += NL + '## Reviews' + NL + (revs.map((r) => '- ' + r).join(NL) || '(none yet)') + NL;
  const human = read(path.join(dir, 'HUMAN.md'));
  const open = human.split(NL).filter((l) => /^\s*[-*]/.test(l) && !/\[answered\]/i.test(l));
  out += NL + '## Open questions for the human' + NL + (open.join(NL) || '(none)') + NL;
  fs.writeFileSync(path.join(dir, 'STATUS.md'), out);
  console.log('wrote goals/' + name + '/STATUS.md');
}

function sync() {
  const src = read(path.join(root, 'AGENTS.md'));
  for (const [f, who] of [['CLAUDE.md', 'Claude Code'], ['GEMINI.md', 'Gemini CLI']]) {
    const head = '<!-- Same rules as AGENTS.md; kept as a copy because ' + who + ' reads ' + f + '. Keep in sync via scripts/room.mjs sync. -->' + NL;
    fs.writeFileSync(path.join(root, f), head + src);
  }
  console.log('synced CLAUDE.md and GEMINI.md from AGENTS.md');
}

function newGoal(slug) {
  if (!slug || !/^[a-z0-9][a-z0-9-]*$/.test(slug)) {
    console.error('usage: room.mjs new-goal <lowercase-slug>');
    process.exit(1);
  }
  const dest = path.join(root, 'goals', slug);
  if (fs.existsSync(dest)) {
    console.error('goal already exists: goals/' + slug);
    process.exit(1);
  }
  fs.cpSync(path.join(root, 'goals', '_template'), dest, { recursive: true });
  console.log('created goals/' + slug + ' from template. Edit its GOAL.md, then: node scripts/room.mjs use ' + slug);
}

function use(slug) {
  if (!slug || !fs.existsSync(path.join(root, 'goals', slug))) {
    console.error('goal not found: goals/' + (slug || ''));
    process.exit(1);
  }
  fs.writeFileSync(path.join(root, 'ACTIVE_GOAL'), slug + NL);
  console.log('active goal is now ' + slug);
}

if (cmd === 'post') post(args[0], args.slice(1).join(' '));
else if (cmd === 'status') status();
else if (cmd === 'sync') sync();
else if (cmd === 'new-goal') newGoal(args[0]);
else if (cmd === 'use') use(args[0]);
else console.error('commands: post, status, sync, new-goal, use');
