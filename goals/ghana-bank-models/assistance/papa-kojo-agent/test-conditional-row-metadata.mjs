// Independent narrow regression for scoped diagnostics. Run from any cwd with Node.
// Synthetic repo only; actual rollup/peer generators from this checkout; no production output writes.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync,spawnSync} from 'node:child_process';
const goalDir=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'agentroom-row-metadata-'));
const root=path.join(tmp,'input'),out=path.join(tmp,'output'),goal=path.join(root,'goals','ghana-bank-models');
const write=(p,s)=>{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,s)};
const git=(...args)=>execFileSync('git',args,{cwd:root,stdio:'pipe',encoding:'utf8'});
const commit=()=>{git('add','.');git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','fixture')};
const tasks=[{slug:'alpha',acceptance:'accepted',status:'done',owner:'owner',reviewStage:'fixture',completionEvidence:{packageFingerprint:'p',macroFingerprint:'m',reviewSha256:'r',reviewer:'reviewer'},gate:{fingerprint:'p',macroFingerprint:'m'}},{slug:'umb',acceptance:'in-progress',status:'needs-review',owner:'owner2',reviewStage:'fixture',gate:{fingerprint:'q',macroFingerprint:'m'}}];
const items=['total_assets','customer_deposits','loans_and_advances_net','total_equity','profit_after_tax','net_interest_income','fee_commission_income','fee_commission_expense','net_trading_income','other_operating_income','staff_costs','depreciation_amortisation','other_operating_expenses','car_pct','npl_pct','loans_and_advances_gross'];
const results=[];
try{
 fs.mkdirSync(root,{recursive:true});git('init','-q');git('config','core.autocrlf','false');
 write(path.join(root,'scripts','completion.mjs'),'export async function evaluateRoom(){return {tasks:'+JSON.stringify(tasks)+'}}\n');
 const actual=fs.readFileSync(path.resolve(goalDir,'../../scripts/bank-gate.mjs'),'utf8');
 write(path.join(root,'scripts','bank-gate.mjs'),actual.slice(actual.indexOf('export function csv('),actual.indexOf('const required=')));
 for(const t of tasks){
  const v=t.slug==='alpha'?10:300,h=['bank,period,statement,line_item,value,status'],f=['bank,scenario,period,statement,line_item,value,status'];
  for(const y of ['FY2021','FY2022','FY2023','FY2024','FY2025','9M-2026'])for(const k of items)h.push([t.slug,y,'fixture',k,v,'reported'].join(','));
  for(const s of ['base','downside','upside'])for(let y=2026;y<=2030;y++)for(const k of items)f.push([t.slug,s,'FY'+y+'E','fixture',k,v,'estimated'].join(','));
  write(path.join(goal,'banks',t.slug,'financials.csv'),h.join('\n')+'\n');
  write(path.join(goal,'banks',t.slug,'forecast.csv'),f.join('\n')+'\n');
 }
 write(path.join(goal,'review-resolutions','umb.md'),'Scope: conditional (FY2025 annual and 2026 interim statements unavailable)\n');
 write(path.join(goal,'sector','macro-assumptions','sector-context.csv'),'indicator,2025-12,2026-09\ntotal_assets,100,100\ntotal_deposits,100,100\n');commit();
 const roll=path.join(goalDir,'sector','sector-rollup','rollup.mjs'),peer=path.join(goalDir,'sector','peer-comparison','compare.mjs');
 const run=(script,args)=>spawnSync(process.execPath,[script,...args],{encoding:'utf8'});
 const parse=(file)=>{const text=fs.readFileSync(file,'utf8');const [head,...rows]=text.trim().split('\n').map(l=>l.split(',').map(s=>s.replace(/^"|"$/g,'')));return rows.map(r=>Object.fromEntries(head.map((k,i)=>[k,r[i]])))};
 const f=path.join(goal,'banks','umb','forecast.csv'),original=fs.readFileSync(f,'utf8'),needle='umb,base,FY2030E,fixture,profit_after_tax,300,estimated';
 for(const [name,replacement] of [['valid',needle],['invalid forecast status','umb,base,FY2030E,fixture,profit_after_tax,999,reported'],['foreign bank attribution','foreign-bank,base,FY2030E,fixture,profit_after_tax,999,estimated']]){
  write(f,original.replace(needle,replacement));if(name!=='valid')commit();
  fs.rmSync(out,{recursive:true,force:true});
  const a=run(roll,['--input-root',root,'--output-dir',out]),b=run(peer,['--input-root',root,'--output',path.join(out,'comparison.csv'),'--report',path.join(out,'comparison.md')]);
  if(a.status!==0||b.status!==0)throw Error('generator execution failed: '+a.stderr+' '+b.stderr);
  const manifest=JSON.parse(fs.readFileSync(path.join(out,'manifest.json'),'utf8')),peerResult=JSON.parse(b.stdout);
  const rollRow=parse(path.join(out,'provisional.csv')).find(r=>r.bank==='umb'&&r.period_or_scenario==='base|FY2030E'&&r.item==='profit_after_tax');
  const peerRow=parse(path.join(out,'conditional-comparison.csv')).find(r=>r.bank==='umb');
  const expected=name==='valid'?300:null;
  const observed=[rollRow.value===''?null:Number(rollRow.value),peerRow.pat_base_2030_m===''?null:Number(peerRow.pat_base_2030_m)];
  const ordinary=manifest.accepted===1&&manifest.totals.total_assets.value===10&&peerResult.accepted===1&&peerResult.totals.assets_2025_m.total===10;
  const diagnostic=name==='valid'||(manifest.diagnosticErrors.some(x=>x.bank==='umb')&&peerResult.conditionalErrors.some(x=>x.bank==='umb'));
  results.push({name,expected,observed,ordinary,diagnostic,pass:ordinary&&diagnostic&&observed.every(v=>v===expected)});
 }
 console.log(JSON.stringify(results,null,2));if(results.some(r=>!r.pass))process.exitCode=1;
}finally{fs.rmSync(tmp,{recursive:true,force:true})}
