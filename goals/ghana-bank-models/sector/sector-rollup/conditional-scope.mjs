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
