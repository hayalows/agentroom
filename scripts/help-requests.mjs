import {validAgent} from './participants.mjs';
const validId=s=>/^[a-z0-9][a-z0-9_-]{0,63}$/.test(s||'');
const capability=s=>/^[a-z][a-z0-9-]{0,39}$/.test(s||'');
const parseFields=s=>Object.fromEntries(s.split(/\s*\|\s*/).map(p=>/^([a-z]+)=(.+)$/.exec(p.trim())).filter(Boolean).map(m=>[m[1],m[2].trim()]));
// Untrusted board content advises workers; it never authorizes or executes tools.
export function helpState(events,agents,tasks){
  const byAgent=new Map(agents.map(a=>[a.id,a]));
  const owned=new Map(tasks.map(t=>[t.slug,t.owner]));
  const caps=new Map(),requests=new Map(),invalid=[];
  for(const e of events.slice().sort((a,b)=>Date.parse(a.at)-Date.parse(b.at)||a.order-b.order)){
    if(!byAgent.has(e.agent)||!Number.isFinite(Date.parse(e.at)))continue;
    const text=e.text.trim();let m;
    if((m=/^CAPABILITIES:\s*(.*)$/.exec(text))){
      caps.set(e.agent,[...new Set(m[1].split(',').map(x=>x.trim()).filter(capability))]);continue;
    }
    if((m=/^HELP \[([^\]]+)\]\s*\|\s*(.+)$/.exec(text))){
      const id=m[1],f=parseFields(m[2]),key=e.agent+'/'+id;
      if(!validId(id)||requests.has(key)||owned.get(f.task)!==e.agent||!capability(f.kind)||!f.need||!f.tried||!f.next||!(f.target==='any'||(validAgent(f.target)&&byAgent.has(f.target)&&f.target!==e.agent))){invalid.push({agent:e.agent,at:e.at,reason:'invalid, duplicate, or unowned request',id});continue;}
      requests.set(key,{key,id,requester:e.agent,task:f.task,kind:f.kind,target:f.target,need:f.need,tried:f.tried,next:f.next,at:e.at,status:'open',responses:[]});continue;
    }
    if((m=/^ASSIST \[([^\]]+)\]\s*\|\s*(.+)$/.exec(text))){
      const r=requests.get(m[1]),f=parseFields(m[2]);
      if(!r||r.status!=='open'||r.requester===e.agent||!['offered','delivered','blocked'].includes(f.status)||!f.evidence||(r.target!=='any'&&r.target!==e.agent)){invalid.push({agent:e.agent,at:e.at,reason:'invalid assist record',id:m[1]});continue;}
      r.responses.push({agent:e.agent,at:e.at,status:f.status,evidence:f.evidence});continue;
    }
    if((m=/^HELP-RESOLVED \[([^\]]+)\]\s*\|\s*(.+)$/.exec(text))){
      const r=requests.get(e.agent+'/'+m[1]),f=parseFields(m[2]);
      if(!r||r.status!=='open'||!f.evidence||!['resolved','withdrawn'].includes(f.status)){invalid.push({agent:e.agent,at:e.at,reason:'invalid closure',id:m[1]});continue;}
      r.status=f.status;r.closedAt=e.at;r.closure=f.evidence;
    }
  }
  const all=[...requests.values()];
  for(const r of all){
    const lastBy=new Map(r.responses.map(x=>[x.agent,x]));
    r.helpers=[...lastBy.values()];
    r.suggestedHelpers=agents.filter(a=>a.id!==r.requester&&(r.target==='any'?(caps.get(a.id)||[]).includes(r.kind):a.id===r.target)&&!lastBy.has(a.id)).sort((a,b)=>(a.ageMinutes??Infinity)-(b.ageMinutes??Infinity)||a.id.localeCompare(b.id)).map(a=>a.id);
    r.phase=r.status!=='open'?r.status:r.helpers.some(x=>x.status==='delivered')?'awaiting-requester-verification':r.helpers.some(x=>x.status==='offered')?'assistance-offered':'waiting-for-helper';
  }
  const queues=Object.fromEntries(agents.map(a=>[a.id,{
    requested:all.filter(r=>r.requester===a.id&&r.status==='open').map(r=>r.key),
    verify:all.filter(r=>r.requester===a.id&&r.status==='open'&&r.phase==='awaiting-requester-verification').map(r=>r.key),
    assist:all.filter(r=>r.status==='open'&&r.requester!==a.id&&(r.helpers.some(h=>h.agent===a.id&&h.status==='offered')||(r.phase==='waiting-for-helper'&&r.suggestedHelpers[0]===a.id))).map(r=>r.key)
  }]));
  return {capabilities:Object.fromEntries(agents.map(a=>[a.id,caps.get(a.id)||[]])),requests:all,queues,invalid};
}
