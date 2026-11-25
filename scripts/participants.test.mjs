import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { validAgent, agentsFor, joinBoard, boardEvents } from './participants.mjs';
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'agentroom-test-'));
try {
  assert(validAgent('deepseek')); assert(validAgent('codex-2'));
  for(const id of ['../evil','all','human','a/evil','x-','', 'UPPER','a'.repeat(49)]) assert(!validAgent(id),id);
  joinBoard(dir,'deepseek','researcher');
  const file=path.join(dir,'board','deepseek.md');
  const before=fs.readFileSync(file,'utf8');
  assert.throws(()=>joinBoard(dir,'deepseek','overwrite'));
  assert.equal(fs.readFileSync(file,'utf8'),before);
  joinBoard(dir,'qwen','reviewer');
  assert.deepEqual(agentsFor(dir,['external-reviewer']),['claude','codex','gemini','deepseek','qwen','external-reviewer']);
  fs.writeFileSync(file,'- 2026-11-25T12:02:00Z DONE x\nTO qwen: second\n');
  fs.writeFileSync(path.join(dir,'board','qwen.md'),'- 2026-11-25T12:01:00Z CLAIM x\nTO deepseek: first\n');
  const events=boardEvents(dir,agentsFor(dir));
  assert.deepEqual(events.map(x=>x.text),['first','second']);
  console.log('PASS: participant IDs, duplicate board protection, dynamic discovery, chronological messages');
} finally {fs.rmSync(dir,{recursive:true,force:true});}
