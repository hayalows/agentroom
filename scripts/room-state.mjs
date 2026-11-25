import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {validAgent, boardAgents} from './participants.mjs';
export const slugOK=s=>typeof s==='string'&&/^[a-z0-9][a-z0-9-]{0,80}$/.test(s);
export const read=p=>fs.existsSync(p)?fs.readFileSync(p,'utf8').replace(/^\uFEFF/,''):'';
export const names=d=>fs.existsSync(d)?fs.readdirSync(d,{withFileTypes:true}).filter(x=>x.isFile()).map(x=>x.name).sort():[];
export const hash=s=>crypto.createHash('sha256').update(s).digest('hex');
const time=s=>Number.isFinite(Date.parse(s))?Date.parse(s):null;
export function fields(s){return Object.fromEntries(s.replace(/^\uFEFF/,'').split(/\r?\n/).map(l=>/^([a-z_]+):\s*(.*)$/.exec(l.trim())).filter(Boolean).map(m=>[m[1],m[2]]))}
export function readState(root,goal,now=Date.now()){
  if(!slugOK(goal))throw Error('Invalid goal');
  const dir=path.join(root,'goals',goal);
  if(!fs.existsSync(dir))throw Error('Unknown goal');
  const roster=read(path.join(dir,'ROSTER.md')).split(/\r?\n/).map(l=>/^\|\s*([a-z0-9][a-z0-9-]*)\s*\|\s*(.*?)\s*\|$/.exec(l)).filter(Boolean).map(m=>({slug:m[1],name:m[2]}));
  const claims=names(path.join(dir,'claims')).filter(n=>n.endsWith('.md')).map(n=>({slug:n.slice(0,-3),...fields(read(path.join(dir,'claims',n)))}));
  const boards=boardAgents(dir), ids=[...new Set([...boards,...claims.map(c=>c.agent).filter(validAgent)])].sort();
  const events=[], messages=[];
  const agents=ids.map(id=>{
    let at=null, last=null;
    for(const l of read(path.join(dir,'board',id+'.md')).split(/\r?\n/)){
      const m=/^- (\d{4}-\d\d-\d\dT\S+)\s+(.*)$/.exec(l);
      if(m&&time(m[1])!==null){at=m[1];last=at;events.push({agent:id,at,text:m[2]});}
      const x=/(?:^|\s)(TO|ACK) ([a-z0-9][a-z0-9-]{0,47}):\s*(.*)$/.exec(l);
      if(x&&validAgent(x[2]))messages.push({from:id,to:x[2],kind:x[1],at,text:x[3]});
    }
    const own=claims.filter(c=>c.agent===id);
    const age=last===null?null:Math.max(0,Math.floor((now-time(last))/60000));
    return {id,last,ageMinutes:age,activity:age===null?'unknown':age>=60?'quiet-60m':age>=15?'quiet-15m':'recent-check-in',own:own.map(c=>c.slug),open:own.filter(c=>!['done','released'].includes(c.status)).length};
  });
  const reviews=names(path.join(dir,'reviews')).filter(n=>n.endsWith('.md')).map(file=>({file,text:read(path.join(dir,'reviews',file))}));
  const groups=new Map();
  for(const c of claims){const k=c.slug.replace(/-takeover$/,'');if(!groups.has(k))groups.set(k,[]);groups.get(k).push(c);}
  const tasks=roster.map(b=>{
    const cs=groups.get(b.slug)||[];
    const active=cs.filter(c=>c.status!=='released');
    const conflict=active.length>1;
    const c=active.find(c=>c.slug.endsWith('-takeover'))||active[0]||cs[0];
    return {...b,owner:c?.agent||null,status:conflict?'ownership-conflict':c?.status||'unclaimed',claim:c||null,conflict};
  });
  const shared=['roster-verification','macro-assumptions','peer-comparison','qa-sweep','sector-rollup'].map(slug=>{
    const cs=groups.get(slug)||[],c=cs.find(x=>x.status!=='released')||cs[0];
    return {slug,name:slug,owner:c?.agent||null,status:cs.filter(x=>x.status!=='released').length>1?'ownership-conflict':c?.status||'unclaimed',claim:c||null};
  });
  const all=[...tasks,...shared];
  const pending=messages.filter(m=>m.kind==='TO'&&!messages.some(a=>a.from===m.to&&a.to===m.from&&time(a.at)>time(m.at)&&a.kind==='ACK'));
  const actionable=Object.fromEntries(agents.map(a=>{
    const own=all.filter(t=>t.owner===a.id), repairs=own.filter(t=>t.status==='changes-requested'||t.status==='blocked');
    const reviewable=all.filter(t=>t.owner&&t.owner!==a.id&&t.status==='needs-review');
    const ongoing=own.filter(t=>t.status==='in-progress');
    const unclaimed=all.filter(t=>t.status==='unclaimed'&&(!['sector-rollup','peer-comparison','qa-sweep'].includes(t.slug)||tasks.every(b=>b.status==='done')));
    return [a.id,{messages:pending.filter(m=>m.to===a.id).length,repair:repairs.map(t=>t.slug),continue:ongoing.map(t=>t.slug),review:reviewable.map(t=>t.slug),claim:a.open<3?unclaimed.map(t=>t.slug):[],next:repairs.length?'repair':ongoing.length?'continue':reviewable.length?'review':a.open<3&&unclaimed.length?'claim':'wait-or-report-blocker'}];
  }));
  const sorted=a=>a.sort((x,y)=>(time(x.at)||0)-(time(y.at)||0));
  return {goal,generatedAt:new Date(now).toISOString(),agents,tasks,shared,claims,reviews,events:sorted(events),messages:sorted(messages),pending,actionable,goalClaimComplete:tasks.length>0&&all.every(t=>t.status==='done'),notes:['Recent check-in is not proof a process is running.','Quiet claims are not released automatically.','Legacy ACK matching is advisory; an acknowledgment may cover multiple messages.','A done claim is an owner assertion until evidence and peer review are checked.']};
}
