#!/usr/bin/env node
// Tiny helper for the room. No dependencies.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const AGENTS = ['claude', 'codex', 'gemini'];
const [cmd, ...args] = process.argv.slice(2);
const NL = String.fromCharCode(10);

const read = (p) => (fs.existsSync(p) ? fs.readFileSync(p, 'utf8') : '');

function post(agent, message) {
  if (!AGENTS.includes(agent) || !message) {
    console.error('usage: room.mjs post <claude|codex|gemini> "message"');
    process.exit(1);
  }
  const line = '- ' + new Date().toISOString() + ' ' + message + NL;
  fs.appendFileSync(path.join(root, 'board', agent + '.md'), line);
  console.log('posted to board/' + agent + '.md');
}

function status() {
  let out = '# Room status' + NL + NL + 'Generated ' + new Date().toISOString() + NL + NL;
  out += '## Goal' + NL + read(path.join(root, 'GOAL.md')) + NL;
  out += '## Tasks' + NL + read(path.join(root, 'TASKS.md')) + NL;
  for (const a of AGENTS) {
    const lines = read(path.join(root, 'board', a + '.md')).split(NL).filter((l) => l.startsWith('- '));
    out += NL + '## ' + a + ' (last 5 of ' + lines.length + ' posts)' + NL;
    out += (lines.slice(-5).join(NL) || '(no posts)') + NL;
  }
  const revDir = path.join(root, 'reviews');
  const revs = fs.existsSync(revDir) ? fs.readdirSync(revDir).filter((f) => f.endsWith('.md')) : [];
  out += NL + '## Reviews' + NL + (revs.map((r) => '- ' + r).join(NL) || '(none yet)') + NL;
  const human = read(path.join(root, 'HUMAN.md'));
  const open = human.split(NL).filter((l) => /^\s*[-*]/.test(l) && !/\[answered\]/i.test(l));
  out += NL + '## Open questions for the human' + NL + (open.join(NL) || '(none)') + NL;
  fs.writeFileSync(path.join(root, 'STATUS.md'), out);
  console.log('wrote STATUS.md');
}

function sync() {
  const src = read(path.join(root, 'AGENTS.md'));
  for (const [f, who] of [['CLAUDE.md', 'Claude Code'], ['GEMINI.md', 'Gemini CLI']]) {
    const head = '<!-- Same rules as AGENTS.md; kept as a copy because ' + who + ' reads ' + f + '. Keep in sync via scripts/room.mjs sync. -->' + NL;
    fs.writeFileSync(path.join(root, f), head + src);
  }
  console.log('synced CLAUDE.md and GEMINI.md from AGENTS.md');
}

if (cmd === 'post') post(args[0], args.slice(1).join(' '));
else if (cmd === 'status') status();
else if (cmd === 'sync') sync();
else console.error('commands: post, status, sync');
