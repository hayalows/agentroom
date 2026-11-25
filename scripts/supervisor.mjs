#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {read,slugOK} from './room-state.mjs';
import {evaluateRoom} from './completion.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const args=process.argv.slice(2), arg=k=>{const i=args.indexOf(k);return i<0?null:args[i+1]};
const goal=arg('--goal')||read(path.join(root,'ACTIVE_GOAL')).trim();
if(!slugOK(goal))throw Error('invalid goal');
const s=await evaluateRoom(root,goal);
s.reviews=s.reviews.map(r=>({file:r.file}));
const md=[];
const safe=v=>String(v??'').replace(/\|/g,'\\|').replace(/[\r\n]/g,' ');
md.push('# Agent Room · '+s.goal,'Generated '+s.generatedAt,'','**'+s.agents.length+' recorded participants · '+s.tasks.filter(t=>t.owner).length+'/'+s.tasks.length+' banks claimed · '+s.tasks.filter(t=>t.status==='needs-review').length+' awaiting review · '+s.tasks.filter(t=>t.acceptance==='accepted').length+' accepted**','','## Workers','| Agent | Last check-in (UTC) | Active / limit | Submitted waiting / limit | Accepted | Suggested next |','|---|---|---:|---:|---:|---|');
for(const a of s.agents)md.push('| '+safe(a.id)+' | '+safe(a.last||'unknown')+' | '+a.activeClaims+'/6 | '+a.awaitingReview+'/6 | '+a.accepted+' | '+s.actionable[a.id].next+' |');
md.push('','## Tasks','| Piece | Owner | Claim state | Core evidence gate | Next completion step | Acceptance |','|---|---|---|---|---|---|');
for(const t of [...s.tasks,...s.shared])md.push('| '+safe(t.name)+' | '+safe(t.owner||'—')+' | '+safe(t.status+(t.repairRequested?' (repair requested)':''))+' | '+safe(t.gate?.status||'not assessed')+' | '+safe(t.reviewStage||'—')+' | '+safe(t.acceptance||'—')+' |');
md.push('','## Suggested next work');
for(const a of s.agents){const x=s.actionable[a.id];md.push('- **'+a.id+':** '+x.next+'; handoffs '+(x.handoff.join(', ')||'none')+'; close '+(x.close.join(', ')||'none')+'; lead resolution '+(x.leadResolution.join(', ')||'none')+'; repair '+(x.repair.join(', ')||'none')+'; continue '+(x.continue.join(', ')||'none')+'; reviews '+(x.review.join(', ')||'none')+'; unacknowledged messages '+x.messages);}
md.push('','## Acceptance evidence');
for(const t of s.tasks.filter(t=>t.completionEvidence)){const x=t.completionEvidence;md.push('- **'+safe(t.slug)+'** '+safe(t.reviewStage)+'; owner '+safe(x.owner)+'; reviewer '+safe(x.reviewer)+'; review '+safe(x.reviewFile)+'; package '+safe(x.packageFingerprint)+'; macro '+safe(x.macroFingerprint)+'; review SHA-256 '+safe(x.reviewSha256));}
md.push('','## Requests for help','| Request | Bank/task | State | Suggested helper(s) | Need |','|---|---|---|---|---|');
for(const r of s.help.requests)md.push('| '+safe(r.key)+' | '+safe(r.task)+' | '+safe(r.phase)+' | '+safe(r.suggestedHelpers.join(', ')||'—')+' | '+safe(r.need)+' |');
if(!s.help.requests.length)md.push('No structured help requests recorded. A quiet board does not establish a blocker.');
md.push('','## Declared capabilities');
for(const a of s.agents)md.push('- '+safe(a.id)+': '+safe(s.help.capabilities[a.id].join(', ')||'not declared'));
for(const r of s.help.requests.filter(r=>r.status==='open')){md.push('- **'+safe(r.key)+'** tried: '+safe(r.tried)+'; next: '+safe(r.next));for(const h of r.responses)md.push('  - '+safe(h.agent)+' ('+safe(h.status)+'): '+safe(h.evidence));}
md.push('','## Communication timeline');
for(const m of s.messages.slice(-40))md.push('- '+safe(m.at||'undated')+' **'+safe(m.from)+' → '+safe(m.to)+' ('+m.kind+'):** '+safe(m.text));
md.push('','## Evidence and limits',...s.notes.map(x=>'- '+x),'- Core checks do not establish correctness of reported data. No model code is executed by this read-only monitor.','- Goal ready for lead confirmation: '+s.goalReadyForLead);
const out=arg('--out');if(out){fs.mkdirSync(out,{recursive:true});fs.writeFileSync(path.join(out,'state.json'),JSON.stringify(s,null,2));fs.writeFileSync(path.join(out,'status.md'),md.join('\n')+'\n');}
process.stdout.write(args.includes('--json')?JSON.stringify(s,null,2)+'\n':md.join('\n')+'\n');
