#!/usr/bin/env node
// One agent turn, run by GitHub Actions (or locally). No dependencies, Node 20+.
//   node scripts/agent.mjs <claude|codex|gemini>
// Env: GOAL, INSTRUCTION, ROUND, TOTAL_ROUNDS
//      ANTHROPIC_API_KEY / OPENAI_API_KEY / GEMINI_API_KEY (one per agent)
//      CLAUDE_MODEL / OPENAI_MODEL / GEMINI_MODEL (optional overrides)
//      TARGET_TOKEN (optional, read-only token for the goal's target repo)
//      MOCK=1 (fake model, for testing, no network, no cost)
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const NL = String.fromCharCode(10);
const AGENTS = ['claude', 'codex', 'gemini'];
const agent = process.argv[2];
if (!AGENTS.includes(agent)) {
  console.error('usage: agent.mjs <claude|codex|gemini>');
  process.exit(1);
}
const read = (p) => (fs.existsSync(p) ? fs.readFileSync(p, 'utf8') : '');
const clip = (s, n) => (s.length > n ? s.slice(0, n) + NL + '[...truncated ' + (s.length - n) + ' chars]' : s);
const goal = (process.env.GOAL || read(path.join(root, 'ACTIVE_GOAL'))).trim();
const round = Number(process.env.ROUND || 1);
const totalRounds = Number(process.env.TOTAL_ROUNDS || 1);
const instruction = (process.env.INSTRUCTION || 'Continue the active goal.').slice(0, 1500);
const MOCK = process.env.MOCK === '1';

if (!/^[a-z0-9][a-z0-9-]*$/.test(goal) || !fs.existsSync(path.join(root, 'goals', goal))) {
  console.error('bad or missing goal: ' + goal);
  process.exit(1);
}
const gdir = path.join(root, 'goals', goal);

const PROVIDERS = {
  claude: { key: 'ANTHROPIC_API_KEY', model: process.env.CLAUDE_MODEL || 'claude-sonnet-5-5' },
  codex: { key: 'OPENAI_API_KEY', model: process.env.OPENAI_MODEL || 'gpt-5' },
  gemini: { key: 'GEMINI_API_KEY', model: process.env.GEMINI_MODEL || 'gemini-2.5-pro' },
};
const prov = PROVIDERS[agent];
if (!MOCK && !process.env[prov.key]) {
  console.log('SKIP ' + agent + ': secret ' + prov.key + ' is not set. Nothing written.');
  process.exit(0);
}

// ---------- model calls ----------
async function http(url, init) {
  let last;
  for (let i = 0; i < 4; i++) {
    try {
      const r = await fetch(url, init);
      if (r.ok) return await r.json();
      last = r.status + ' ' + (await r.text()).slice(0, 300);
      if (r.status !== 429 && r.status < 500) break;
    } catch (e) {
      last = String(e);
    }
    await new Promise((res) => setTimeout(res, 2000 * (i + 1)));
  }
  throw new Error('API call failed: ' + last);
}

async function callModel(system, user, maxTokens) {
  if (MOCK) return mock(user);
  const key = process.env[prov.key];
  if (agent === 'claude') {
    const d = await http('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'x-api-key': key, 'anthropic-version': '2023-06-01' },
      body: JSON.stringify({ model: prov.model, max_tokens: maxTokens, system, messages: [{ role: 'user', content: user }] }),
    });
    return (d.content || []).map((c) => c.text || '').join('');
  }
  if (agent === 'codex') {
    const d = await http('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: { 'content-type': 'application/json', authorization: 'Bearer ' + key },
      body: JSON.stringify({
        model: prov.model,
        max_completion_tokens: maxTokens,
        response_format: { type: 'json_object' },
        messages: [{ role: 'system', content: system }, { role: 'user', content: user }],
      }),
    });
    return d.choices[0].message.content || '';
  }
  const d = await http('https://generativelanguage.googleapis.com/v1beta/models/' + prov.model + ':generateContent', {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'x-goog-api-key': key },
    body: JSON.stringify({
      systemInstruction: { parts: [{ text: system }] },
      contents: [{ role: 'user', parts: [{ text: user }] }],
      generationConfig: { maxOutputTokens: maxTokens, responseMimeType: 'application/json' },
    }),
  });
  return ((d.candidates || [{}])[0].content || { parts: [] }).parts.map((p) => p.text || '').join('');
}

function parseJson(text) {
  const a = text.indexOf('{');
  const b = text.lastIndexOf('}');
  if (a < 0 || b < a) throw new Error('model did not return JSON: ' + text.slice(0, 200));
  return JSON.parse(text.slice(a, b + 1));
}

function mock(user) {
  if (user.includes('LIST_FILES_STEP')) return JSON.stringify({ paths: [] });
  return JSON.stringify({
    board_entry: 'MOCK ' + agent + ' round ' + round + ': read the room, wrote one note. QUESTION for human: is the mock test OK?',
    files: [
      { path: 'goals/' + goal + '/work/' + agent + '/note-r' + round + '.md', mode: 'write', content: '# Note by ' + agent + NL + 'Round ' + round + NL },
      { path: 'AGENTS.md', mode: 'write', content: 'HACKED' },
      { path: 'goals/' + goal + '/board/' + (agent === 'claude' ? 'gemini' : 'claude') + '.md', mode: 'append', content: 'impersonation' },
    ],
  });
}

// ---------- write rules (enforced here, not by trust) ----------
function allowed(rel, mode) {
  const p = rel.replace(/\\/g, '/');
  if (p.includes('..') || p.startsWith('/') || !p.startsWith('goals/' + goal + '/')) return false;
  const sub = p.slice(('goals/' + goal + '/').length);
  if (sub === 'board/' + agent + '.md') return mode === 'append';
  if (new RegExp('^reviews/' + agent + '-of-(claude|codex|gemini)\\.md$').test(sub)) return true;
  if (sub.startsWith('work/' + agent + '/') && /\.(md|json|txt|csv|py|js|mjs|tsv)$/.test(sub)) return true;
  if (agent === 'claude' && sub === 'TASKS.md') return true;
  if (agent === 'claude' && sub === 'HUMAN.md') return mode === 'append';
  return false;
}

// ---------- context ----------
function listFiles(dir, base = dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((e) => {
    const full = path.join(dir, e.name);
    return e.isDirectory() ? listFiles(full, base) : [path.relative(base, full).replace(/\\/g, '/')];
  });
}

function roomContext() {
  let c = '';
  c += '## GOAL.md' + NL + clip(read(path.join(gdir, 'GOAL.md')), 14000) + NL;
  c += '## TASKS.md' + NL + clip(read(path.join(gdir, 'TASKS.md')), 6000) + NL;
  c += '## HUMAN.md' + NL + clip(read(path.join(gdir, 'HUMAN.md')), 4000) + NL;
  for (const a of AGENTS) c += '## board/' + a + '.md' + NL + clip(read(path.join(gdir, 'board', a + '.md')), 8000) + NL;
  for (const f of listFiles(path.join(gdir, 'reviews')).filter((f) => f.endsWith('.md'))) {
    c += '## reviews/' + f + NL + clip(read(path.join(gdir, 'reviews', f)), 6000) + NL;
  }
  for (const f of listFiles(path.join(gdir, 'work')).filter((f) => /\.(md|json|txt|csv|py|js|mjs|tsv)$/.test(f))) {
    c += '## work/' + f + NL + clip(read(path.join(gdir, 'work', f)), 9000) + NL;
  }
  return clip(c, 110000);
}

// ---------- target repo (read-only) ----------
async function targetContext(system) {
  const cfgPath = path.join(gdir, 'target.json');
  if (!fs.existsSync(cfgPath)) return 'No target repo for this goal.';
  const cfg = JSON.parse(read(cfgPath));
  const token = process.env.TARGET_TOKEN;
  if (MOCK) return 'MOCK: target repo skipped.';
  if (!token) return 'Target repo ' + cfg.repo + ' NOT readable: TARGET_TOKEN secret is not set. Do not claim to have read it.';
  const gh = (u) => http('https://api.github.com/' + u, { headers: { authorization: 'Bearer ' + token, accept: 'application/vnd.github+json', 'user-agent': 'agentroom' } });
  const tree = await gh('repos/' + cfg.repo + '/git/trees/' + (cfg.ref || 'HEAD') + '?recursive=1');
  const inc = cfg.include || [''];
  const exc = cfg.exclude || [];
  const files = tree.tree.filter((t) => t.type === 'blob' && inc.some((i) => t.path.startsWith(i)) && !exc.some((x) => t.path.startsWith(x)) && t.size < 400000);
  const listing = files.slice(0, 2500).map((t) => t.path + ' (' + t.size + ')').join(NL);
  const ask = 'LIST_FILES_STEP. Goal: ' + goal + '. Instruction: ' + instruction + NL + 'From this list of files in ' + cfg.repo + ', choose up to ' + (cfg.max_files || 8) + ' files most useful for your next step. Reply JSON only: {"paths":["..."]}' + NL + listing;
  const reply = parseJson(await callModel(system, ask, 800));
  const chosen = (reply.paths || []).filter((p) => files.some((f) => f.path === p)).slice(0, cfg.max_files || 8);
  let out = 'Target repo ' + cfg.repo + ' (read-only). ' + files.length + ' files in scope; you chose ' + chosen.length + ':' + NL;
  for (const p of chosen) {
    const j = await gh('repos/' + cfg.repo + '/contents/' + p.split('/').map(encodeURIComponent).join('/') + '?ref=' + (cfg.ref || 'HEAD'));
    out += NL + '### ' + p + NL + clip(Buffer.from(j.content || '', 'base64').toString('utf8'), 30000) + NL;
  }
  return clip(out, 90000);
}

// ---------- main ----------
const rules = read(path.join(root, 'AGENTS.md'));
const role = { claude: 'lead / planner / integrator', codex: 'builder', gemini: 'reviewer / researcher' }[agent];
const system =
  'You are "' + agent + '", the ' + role + ' in a three-agent room (claude, codex, gemini) that collaborates only through files in a GitHub repo. ' +
  'You are running as one automated turn: you cannot ask questions mid-turn and you cannot run commands. Read the context, do the most useful next step for your role, ' +
  'and answer with ONE JSON object and nothing else.' + NL + NL + '# ROOM RULES' + NL + rules;

const target = await targetContext(system);
const user =
  'Round ' + round + ' of ' + totalRounds + '. Goal folder: goals/' + goal + '. Human instruction: ' + instruction + NL + NL +
  '# ROOM STATE' + NL + roomContext() + NL + NL + '# TARGET REPO' + NL + target + NL + NL +
  '# YOUR OUTPUT' + NL +
  'Return JSON: {"board_entry": "<=1200 chars: what you did, found, need; label claims observed/inferred/unknown; start any human question with QUESTION:", ' +
  '"files": [{"path": "...", "mode": "write" | "append", "content": "..."}]}.' + NL +
  'You may write ONLY: goals/' + goal + '/work/' + agent + '/<file> (write), goals/' + goal + '/reviews/' + agent + '-of-<other>.md (write), ' +
  (agent === 'claude' ? 'goals/' + goal + '/TASKS.md (write), goals/' + goal + '/HUMAN.md (append). ' : '') +
  'Do NOT write your board file; the runner appends board_entry with a real timestamp. Max 6 files, 40000 chars each. ' +
  'Never invent sources, numbers or file contents. Review other agents\' newest work when it exists; disagree on the merits. ' +
  'If you changed something in response to a review, say so in board_entry.';

const text = await callModel(system, user, 7000);
const out = parseJson(text);

let wrote = 0;
const rejected = [];
for (const f of (out.files || []).slice(0, 6)) {
  const mode = f.mode === 'append' ? 'append' : 'write';
  if (typeof f.path !== 'string' || typeof f.content !== 'string' || !allowed(f.path, mode)) {
    rejected.push(String(f.path));
    continue;
  }
  const abs = path.join(root, f.path);
  fs.mkdirSync(path.dirname(abs), { recursive: true });
  const body = f.content.slice(0, 40000);
  if (mode === 'append') fs.appendFileSync(abs, NL + body + NL);
  else fs.writeFileSync(abs, body);
  wrote++;
}
const entry = String(out.board_entry || '(no entry)').replace(/\s+/g, ' ').slice(0, 1200);
fs.appendFileSync(path.join(gdir, 'board', agent + '.md'), '- ' + new Date().toISOString() + ' [round ' + round + '/' + totalRounds + '] ' + entry + (rejected.length ? ' (runner rejected paths: ' + rejected.join(', ') + ')' : '') + NL);
console.log(agent + ': wrote ' + wrote + ' file(s), rejected ' + rejected.length + ', board updated.');
