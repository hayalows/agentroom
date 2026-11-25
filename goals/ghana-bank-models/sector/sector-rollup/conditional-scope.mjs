// Lead policy: conditional markers override ordinary supervisor acceptance.
import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';

export function parseConditionalMarker(text) {
  if (!/\bconditional\b/i.test(text)) return null;
  const scope=text.match(/^Scope:\s*conditional\s*\(([^\r\n]+)\)\s*$/im);
  const label=text.match(/["“]conditional:\s*([^"”\r\n]+)["”]/i);
  return 'conditional: '+(scope?.[1]??label?.[1]??'source gap; see scope marker').trim();
}
export function partitionTasks(tasks,dir) {
  const markers={};
  for(const t of tasks) {
    const p=path.join(dir,'review-resolutions',t.slug+'.md');
    if(!fs.existsSync(p)) continue;
    const text=fs.readFileSync(p,'utf8'), label=parseConditionalMarker(text);
    if(label) markers[t.slug]={label,sha256:createHash('sha256').update(text).digest('hex')};
  }
  return {
    markers,
    accepted:tasks.filter(t=>t.acceptance==='accepted'&&!markers[t.slug]),
    excluded:tasks.filter(t=>t.acceptance!=='accepted'||markers[t.slug]),
    conditional:tasks.filter(t=>markers[t.slug])
  };
}

// Excluded data does not necessarily pass bank-gate; never attribute another bank's values or present actuals as estimates.
export function validateDiagnosticRows(rows,bank,history){
 const statuses=history?['reported','derived','estimated','unavailable']:['estimated','unavailable'];
 for(const r of rows){
  const tag=bank+' '+(r.period??'')+'/'+(r.line_item??'');
  if(r.bank!==bank||!r.period||!r.line_item)throw Error('invalid bank or row identity '+tag);
  if(!statuses.includes(r.status))throw Error('invalid '+(history?'history':'forecast')+' status '+tag);
  if(!history&&(!['base','downside','upside'].includes(r.scenario)||!/^FY202[6-9]E$|^FY2030E$/.test(r.period)))throw Error('invalid forecast period/scenario '+tag);
  if(typeof r.value!=='string'||(r.status==='unavailable'?r.value.trim()!=='':r.value.trim()===''||!Number.isFinite(Number(r.value))))throw Error('invalid value/status '+tag);
 }
 return rows;
}
