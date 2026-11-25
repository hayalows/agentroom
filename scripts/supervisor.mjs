#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {readState,read,slugOK,peerReviewsFor} from './room-state.mjs';
import {gateBank} from './bank-gate.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const args=process.argv.slice(2), arg=k=>{const i=args.indexOf(k);return i<0?null:args[i+1]};
const goal=arg('--goal')||read(path.join(root,'ACTIVE_GOAL')).trim();
if(!slugOK(goal))throw Error('invalid goal');
const s=readState(root,goal);
for(const t of s.tasks.filter(t=>['needs-review','done','changes-requested'].includes(t.status))){
  t.gate=await gateBank(root,goal,t);
  const reviews=peerReviewsFor(s.reviews,t);
  t.peerReviews=reviews.map(r=>({file:r.file,reviewer:r.reviewer,verdict:r.verdict,bound:r.text.includes(t.gate.fingerprint)&&r.text.includes(t.gate.macroFingerprint)}));
  t.acceptance=t.status==='done'&&t.gate.status==='core-checks-pass'&&!t.repairRequested&&t.peerReviews.some(r=>r.verdict==='PASS'&&r.bound)?'eligible-for-lead-confirmation':'not-accepted';
}
s.goalReadyForLead=s.goalClaimComplete&&s.tasks.every(t=>t.acceptance==='eligible-for-lead-confirmation');
s.reviews=s.reviews.map(r=>({file:r.file}));
const md=[];
const safe=v=>String(v??'').replace(/\|/g,'\\|').replace(/[\r\n]/g,' ');
md.push('# Agent Room · '+s.goal,'Generated '+s.generatedAt,'','**'+s.agents.length+' recorded participants · '+s.tasks.filter(t=>t.owner).length+'/'+s.tasks.length+' banks claimed · '+s.tasks.filter(t=>t.status==='needs-review').length+' awaiting review · '+s.tasks.filter(t=>t.acceptance==='eligible-for-lead-confirmation').length+' eligible for lead confirmation**','','## Workers','| Agent | Last check-in (UTC) | Open claims | Suggested next |','|---|---|---:|---|');
for(const a of s.agents)md.push('| '+safe(a.id)+' | '+safe(a.last||'unknown')+' | '+a.open+' | '+s.actionable[a.id].next+' |');
md.push('','## Tasks','| Piece | Owner | Claim state | Core evidence gate | Acceptance |','|---|---|---|---|---|');
for(const t of [...s.tasks,...s.shared])md.push('| '+safe(t.name)+' | '+safe(t.owner||'—')+' | '+safe(t.status+(t.repairRequested?' (repair requested)':''))+' | '+safe(t.gate?.status||'not assessed')+' | '+safe(t.acceptance||'—')+' |');
md.push('','## Suggested next work');
for(const a of s.agents){const x=s.actionable[a.id];md.push('- **'+a.id+':** '+x.next+'; repair '+(x.repair.join(', ')||'none')+'; continue '+(x.continue.join(', ')||'none')+'; reviews '+(x.review.join(', ')||'none')+'; unacknowledged messages '+x.messages);}
md.push('','## Communication timeline');
for(const m of s.messages.slice(-40))md.push('- '+safe(m.at||'undated')+' **'+safe(m.from)+' → '+safe(m.to)+' ('+m.kind+'):** '+safe(m.text));
md.push('','## Evidence and limits',...s.notes.map(x=>'- '+x),'- Core checks do not establish correctness of reported data. No model code is executed by this read-only monitor.','- Goal ready for lead confirmation: '+s.goalReadyForLead);
const out=arg('--out');if(out){fs.mkdirSync(out,{recursive:true});fs.writeFileSync(path.join(out,'state.json'),JSON.stringify(s,null,2));fs.writeFileSync(path.join(out,'status.md'),md.join('\n')+'\n');}
process.stdout.write(args.includes('--json')?JSON.stringify(s,null,2)+'\n':md.join('\n')+'\n');
