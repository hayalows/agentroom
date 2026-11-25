// Real Node/Git integration regression, synthetic data only. No production files modified.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync,spawnSync} from 'node:child_process';
const here=path.dirname(fileURLToPath(import.meta.url));
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'agentroom-scope-regression-'));
const root=path.join(tmp,'input'),out=path.join(tmp,'output'),goal=path.join(root,'goals','ghana-bank-models');
const write=(p,s)=>{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,s)};
const git=(...a)=>execFileSync('git',a,{cwd:root,stdio:'pipe',encoding:'utf8'});
const commit=()=>{git('add','.');git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','fixture')};
let n=0;
const test=(x,msg)=>{assert.ok(x,msg);n++};
const tasks=[['alpha','accepted',10],['beta','accepted',20],['prudential-bank','accepted',100],['omnibsic-bank','accepted',200],['umb','accepted',300],['pending','in-progress',400]].map(([slug,acceptance,value])=>({slug,acceptance,value,status:'done',reviewStage:'fixture',owner:'owner',completionEvidence:{packageFingerprint:'p-'+slug,macroFingerprint:'m',reviewSha256:'r',reviewer:'reviewer'},gate:{fingerprint:'p-'+slug,macroFingerprint:'m'}}));
const items=['total_assets','customer_deposits','loans_and_advances_net','total_equity','profit_after_tax','net_interest_income','fee_commission_income','fee_commission_expense','net_trading_income','other_operating_income','staff_costs','depreciation_amortisation','other_operating_expenses','car_pct','npl_pct','loans_and_advances_gross'];
try{
 fs.mkdirSync(root,{recursive:true});git('init','-q');git('config','core.autocrlf','false');
 write(path.join(root,'scripts','completion.mjs'),'export async function evaluateRoom(){return {tasks:'+JSON.stringify(tasks)+'}}\n');
 write(path.join(root,'scripts','bank-gate.mjs'),"export function csv(s){const [h,...rr]=s.trim().split('\\n').map(l=>l.split(','));return rr.map(r=>Object.fromEntries(h.map((k,i)=>[k,r[i]])))}\n");
 for(const t of tasks){
  const h=['period,line_item,value,status'],f=['scenario,period,line_item,value,status'];
  for(const yr of ['FY2021','FY2022','FY2023','FY2024','FY2025','9M-2026'])for(const i of items)h.push([yr,i,t.value,t.slug==='umb'&&yr==='FY2025'?'estimated':'reported'].join(','));
  for(const s of ['base','downside','upside'])for(let y=2026;y<=2030;y++)for(const i of items)f.push([s,'FY'+y+'E',i,t.value,'estimated'].join(','));
  write(path.join(goal,'banks',t.slug,'financials.csv'),h.join('\n')+'\n');write(path.join(goal,'banks',t.slug,'forecast.csv'),f.join('\n')+'\n');
 }
 const marker=(slug,s)=>write(path.join(goal,'review-resolutions',slug+'.md'),s);
 marker('prudential-bank','Separate label "conditional: 9M-2026 unavailable"\n');
 marker('omnibsic-bank','Scope: conditional (FY2021 annual statement unavailable)\n');
 marker('umb','Scope: conditional (FY2025 annual and 2026 interim statements unavailable)\n');
 write(path.join(goal,'sector','macro-assumptions','sector-context.csv'),'indicator,2025-12,2026-09\ntotal_assets,100,100\ntotal_deposits,100,100\n');
 commit();
 const roll=path.join(here,'rollup.mjs'),peer=path.resolve(here,'../peer-comparison/compare.mjs'),ra=['--input-root',root,'--output-dir',out],pa=['--input-root',root,'--output',path.join(out,'comparison.csv'),'--report',path.join(out,'comparison.md')];
 const run=(script,args)=>spawnSync(process.execPath,[script,...args],{encoding:'utf8'});
 const success=(script,args)=>{const r=run(script,args);test(r.status===0,r.stderr||r.stdout);return r};
 const read=f=>fs.readFileSync(path.join(out,f),'utf8');
 success(roll,ra);success(peer,pa);success(roll,[...ra,'--check']);
 const mf=JSON.parse(read('manifest.json')),original=read('manifest.json');
 test(mf.accepted===2&&mf.conditional===3&&mf.excluded===4,'partition');
 test(mf.totals.total_assets.value===30,'ordinary asset sum contaminated');
 test(mf.acceptedEvidence.every(e=>['alpha','beta'].includes(e.bank)),'ordinary evidence');
 test(!/prudential-bank|omnibsic-bank|"umb"/.test(read('comparison.csv')),'ordinary peer contamination');
 test(read('conditional-comparison.csv').includes('conditional: FY2025 annual and 2026 interim statements unavailable'),'conditional peer label');
 test(read('conditional-comparison.csv').split('\n').find(l=>l.startsWith('"umb"')).includes('"","",""'),'estimated history not blank');
 test(read('rollup.md').includes('conditional: 9M-2026 unavailable'),'conditional rollup label');
 const mutations=[
  m=>m.acceptedEvidence[0].reviewer='tampered',m=>m.acceptedEvidence[0].packageFingerprint='0'.repeat(64),m=>m.totals.total_assets.value=0,
  m=>m.schema=2,m=>m.conditionalMarkers.umb.label='bad',m=>m.diagnosticInputs.umb['financials.csv']='wrong',m=>m.outputHashes.extra='extra',
  m=>m.exclusions[0].stage='tampered',m=>m.scopeClassifierSha256='wrong'
 ];
 for(const mutate of mutations){const m=JSON.parse(original);mutate(m);write(path.join(out,'manifest.json'),JSON.stringify(m));const result=run(roll,[...ra,'--check']);test(result.status!==0&&result.stderr.includes('modified manifest field'),'manifest mutation not specifically rejected: '+result.stderr)}
 write(path.join(out,'manifest.json'),original);
 write(path.join(goal,'board','test.md'),'board-only change\n');commit();success(roll,[...ra,'--check']);
 marker('umb','Scope: conditional (FY2025 annual and 2026 interim statements unavailable)\nChanged evidence.\n');commit();
 const stale=run(roll,[...ra,'--check']);test(stale.status!==0&&stale.stderr.includes('STALE'),'marker change did not invalidate fingerprint');
 console.log('PASS: '+n+' conditional/manifest integration checks');
}finally{fs.rmSync(tmp,{recursive:true,force:true})}
