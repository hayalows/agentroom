import fs from 'node:fs';
import path from 'node:path';

export const CORE = ['claude', 'codex', 'gemini'];
export const validAgent = (id) => typeof id === 'string' && /^[a-z0-9][a-z0-9-]{0,47}$/.test(id) && !id.endsWith('-') && !['all','human','system','lead','bot'].includes(id);
export function boardAgents(dir) {
  const folder = path.join(dir, 'board');
  if (!fs.existsSync(folder)) return [];
  return fs.readdirSync(folder, {withFileTypes:true})
    .filter(e => e.isFile() && e.name.endsWith('.md'))
    .map(e => e.name.slice(0,-3)).filter(validAgent).sort();
}
export function agentsFor(dir, claimOwners = []) {
  return [...new Set([...CORE, ...boardAgents(dir), ...claimOwners.filter(validAgent)])];
}
export function joinBoard(dir, id, message = 'Ready to read the goal and claim useful work.') {
  if (!validAgent(id)) throw new Error('Invalid or reserved agent ID');
  const folder = path.join(dir, 'board');
  fs.mkdirSync(folder, {recursive:true});
  const file = path.join(folder, id + '.md');
  const stamp = new Date().toISOString();
  // Exclusive creation is intentional: never overwrite another agent board.
  fs.writeFileSync(file, '# ' + id + ' board\n\nOnly ' + id + ' writes this file.\n\n- ' + stamp + ' JOINED: ' + message.replace(/\s+/g,' ').trim() + '\n', {flag:'wx'});
  return file;
}
export function boardEvents(dir, ids) {
  const events = [];
  for (const agent of ids) {
    const file = path.join(dir,'board',agent+'.md');
    if (!fs.existsSync(file)) continue;
    let time = null;
    for (const line of fs.readFileSync(file,'utf8').split(/\r?\n/)) {
      const m = /^- (\d{4}-\d\d-\d\dT\S+)\s+(.*)$/.exec(line);
      if (m && Number.isFinite(Date.parse(m[1]))) time = m[1];
      const msg = /(?:^|\s)TO ([a-z0-9][a-z0-9-]{0,47}):\s*(.*)$/.exec(line);
      if (msg && validAgent(msg[1])) events.push({agent,to:msg[1],time,text:msg[2]});
    }
  }
  return events.sort((a,b)=>(Date.parse(a.time)||0)-(Date.parse(b.time)||0));
}
