// Accepted-only peer comparison. Run node goals/ghana-bank-models/sector/peer-comparison/compare.mjs from a clean repository checkout.
// No bank files are modified. The exact-version supervisor is the eligibility gate.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';
const here=path.dirname(fileURLToPath(import.meta.url));
const args=process.argv.slice(2), options={};
for(let i=0;i<args.length;i+=2){if(!['--input-root','--output'].includes(args[i])||!args[i+1]||Object.hasOwn(options,args[i]))throw Error('Usage: compare.mjs [--input-root PATH] [--output PATH]');options[args[i]]=args[i+1];}
const root=path.resolve(options['--input-root']??path.resolve(here,'../../../..'));
const goal='ghana-bank-models',dir=path.join(root,'goals',goal);
const out=path.resolve(options['--output']??path.join(here,'comparison.csv'));
const clean=()=>{const changed=execFileSync('git',['status','--porcelain','--untracked-files=all'],{cwd:root,encoding:'utf8'}).trim();if(changed)throw Error('Input checkout must be entirely clean before comparison: '+changed.slice(0,400));};
clean();
const sha=execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim();
const {evaluateRoom}=await import(pathToFileURL(path.join(root,'scripts/completion.mjs')).href);
const {csv}=await import(pathToFileURL(path.join(root,'scripts/bank-gate.mjs')).href);
const state=await evaluateRoom(root,goal);
const num=r=>r&&r.value.trim()!==''&&r.status!=='unavailable'&&Number.isFinite(+r.value)?+r.value:null;
function values(rows,p,s){const result={};for(const r of rows.filter(r=>r.period===p&&(!s||r.scenario===s))){if(Object.hasOwn(result,r.line_item))throw Error('duplicate period/line: '+p+'/'+r.line_item);result[r.line_item]=!s&&!['reported','derived'].includes(r.status)?null:num(r)}return result;}
const ratio=(a,b)=>a!=null&&b!=null&&b>0?100*a/b:null,avg=(a,b)=>a!=null&&b!=null?(a+b)/2:null,car=x=>x.car_pct??x.x_car_proxy_pct??null;
const rows=[];
for(const t of state.tasks.filter(t=>t.acceptance==='accepted')){
 const bankdir=path.join(dir,'banks',t.slug);
 const h=csv(fs.readFileSync(path.join(bankdir,'financials.csv'),'utf8')),f=csv(fs.readFileSync(path.join(bankdir,'forecast.csv'),'utf8'));
 const p=values(h,'FY2024'),a=values(h,'FY2025'),b=values(f,'FY2030E','base'),d=values(f,'FY2030E','downside'),u=values(f,'FY2030E','upside');
 rows.push({bank:t.slug,assets_2025_m:a.total_assets,customer_deposits_2025_m:a.customer_deposits,pat_2025_m:a.profit_after_tax,reported_car_2025_pct:a.car_pct,reported_npl_2025_pct:a.npl_pct,roa_2025_pct:ratio(a.profit_after_tax,avg(p.total_assets,a.total_assets)),roe_2025_pct:ratio(a.profit_after_tax,avg(p.total_equity,a.total_equity)),gross_ldr_2025_pct:ratio(a.loans_and_advances_gross,a.customer_deposits),pat_base_2030_m:b.profit_after_tax,pat_downside_2030_m:d.profit_after_tax,pat_upside_2030_m:u.profit_after_tax,car_base_2030_proxy_pct:car(b),car_downside_2030_proxy_pct:car(d),car_upside_2030_proxy_pct:car(u),package_sha256:t.completionEvidence.packageFingerprint,macro_sha256:t.completionEvidence.macroFingerprint,reviewer:t.completionEvidence.reviewer,source_commit:sha});
}
if(!rows.length)throw Error('No accepted models; do not substitute provisional banks.');
const cols=Object.keys(rows[0]),quote=v=>'"'+String(v??'').replaceAll('"','""')+'"';
const format=(k,v)=>v==null?'':typeof v==='number'?v.toFixed(k.endsWith('_pct')?4:3):v;
const content=[cols,...rows.map(r=>cols.map(k=>format(k,r[k])))].map(r=>r.map(quote).join(',')).join('\n')+'\n';
clean();
if(execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim()!==sha)throw Error('Input commit changed during generation');
fs.writeFileSync(out,content);
console.log(JSON.stringify({source_commit:sha,accepted:rows.length,roster:state.tasks.length,excluded:state.tasks.filter(t=>t.acceptance!=='accepted').map(t=>({slug:t.slug,stage:t.reviewStage})),totals:Object.fromEntries(['assets_2025_m','customer_deposits_2025_m','pat_2025_m'].map(k=>[k,{total:rows.reduce((a,r)=>a+(r[k]??0),0),n:rows.filter(r=>r[k]!=null).length}]))},null,2));
