// Exact-version accepted-only sector roll-up, plus separate diagnostic files.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {isDeepStrictEqual} from 'node:util';
import {partitionTasks} from './conditional-scope.mjs';
const here=path.dirname(fileURLToPath(import.meta.url));
const opt={};let check=false;
for(let i=2;i<process.argv.length;i++){
 const k=process.argv[i];if(k==='--check'){check=true;continue}
 if(!['--input-root','--output-dir'].includes(k)||!process.argv[i+1]||Object.hasOwn(opt,k))throw Error('Usage: rollup.mjs [--input-root ROOT] [--output-dir DIR] [--check]');
 opt[k]=process.argv[++i];
}
const root=path.resolve(opt['--input-root']??path.resolve(here,'../../../..'));
const out=path.resolve(opt['--output-dir']??here),goal='ghana-bank-models',dir=path.join(root,'goals',goal);
const git=(...args)=>execFileSync('git',args,{cwd:root,encoding:'utf8'}).trim();
const clean=()=>{const s=git('status','--porcelain','--untracked-files=all');if(s)throw Error('Input checkout must be clean: '+s.slice(0,400))};
const hash=s=>createHash('sha256').update(s).digest('hex');
clean();const sha=git('rev-parse','HEAD');
const {evaluateRoom}=await import(pathToFileURL(path.join(root,'scripts/completion.mjs')).href);
const {csv}=await import(pathToFileURL(path.join(root,'scripts/bank-gate.mjs')).href);
const state=await evaluateRoom(root,goal);
const tasks=state.tasks.slice().sort((a,b)=>a.slug.localeCompare(b.slug));
const {accepted,excluded,conditional,markers}=partitionTasks(tasks,dir);
const read=p=>fs.readFileSync(p,'utf8');
const ctxText=read(path.join(dir,'sector/macro-assumptions/sector-context.csv'));
const ctx=Object.fromEntries(csv(ctxText).map(r=>[r.indicator,r]));
const evidence=accepted.map(t=>({bank:t.slug,...t.completionEvidence}));
for(const e of evidence)if(!e.packageFingerprint||!e.macroFingerprint||!e.reviewSha256)throw Error('Incomplete evidence '+e.bank);
const exclusions=excluded.map(t=>({bank:t.slug,owner:t.owner??null,status:t.status??null,stage:t.reviewStage??null,conditional:markers[t.slug]?.label??null,packageFingerprint:t.gate?.fingerprint??null,macroFingerprint:t.gate?.macroFingerprint??null}));
const diagnosticInputs=Object.fromEntries(excluded.map(t=>[t.slug,Object.fromEntries(['financials.csv','forecast.csv'].map(f=>{const p=path.join(dir,'banks',t.slug,f);return [f,fs.existsSync(p)?hash(read(p)):null]}))]));
const generatorSha256=hash(read(fileURLToPath(import.meta.url))), scopeClassifierSha256=hash(read(path.join(here,'conditional-scope.mjs')));
const inputFingerprint=hash(JSON.stringify({evidence,exclusions,diagnosticInputs,conditionalMarkers:markers,context:hash(ctxText),generator:generatorSha256,scopeClassifier:scopeClassifierSha256}));
const prior=check?JSON.parse(read(path.join(out,'manifest.json'))):null;
if(check&&(prior.inputFingerprint!==inputFingerprint||!/^[0-9a-f]{40}$/.test(prior.sourceCommit)))throw Error('STALE: eligibility, package, diagnostics, context or generator inputs changed');
const sourceCommit=prior?.sourceCommit??sha;
const periods=['FY2021','FY2022','FY2023','FY2024','FY2025','9M-2026'];
const years=Array.from({length:5},(_,i)=>'FY'+(2026+i)+'E'),scenarios=['base','downside','upside'];
const items=['total_assets','customer_deposits','loans_and_advances_net','total_equity','profit_after_tax','operating_income_pre_impairment','net_interest_income'];
const num=r=>r&&typeof r.value==='string'&&r.value.trim()!==''&&r.status!=='unavailable'&&Number.isFinite(+r.value)?+r.value:null;
function getTable(bank,name,history=false){
 const file=path.join(dir,'banks',bank,name+'.csv');
 if(!fs.existsSync(file))return new Map();
 const m=new Map();
 for(const r of csv(read(file))){
  const k=[history?'':r.scenario,r.period,r.line_item].join('|');
  if(m.has(k))throw Error('duplicate row '+bank+' '+k);
  m.set(k,history&&!['reported','derived'].includes(r.status)?null:num(r));
 }
 return m;
}
const H=new Map(),F=new Map();
for(const t of accepted){H.set(t.slug,getTable(t.slug,'financials',true));F.set(t.slug,getTable(t.slug,'forecast'))}
const hist=(b,p,i)=>{
 if(i==='operating_income_pre_impairment'){
  const a=['net_interest_income','fee_commission_income','fee_commission_expense','net_trading_income','other_operating_income'].map(k=>hist(b,p,k));
  return a.some(v=>v==null)?null:a[0]+a[1]-a[2]+a[3]+a[4];
 }
 return H.get(b)?.get('|'+p+'|'+i)??null;
};
const forecast=(b,s,p,i)=>F.get(b)?.get(s+'|'+p+'|'+i)??null;
const names=accepted.map(t=>t.slug);
const sum=a=>a.reduce((x,y)=>x+y,0);
function aggregate(banks,fn){
 const pairs=banks.map(b=>[b,fn(b)]).filter(([,v])=>v!=null&&Number.isFinite(v));
 return {value:pairs.length?sum(pairs.map(x=>x[1])):null,n:pairs.length,banks:pairs.map(x=>x[0])};
}
function pairRatio(banks,n,d){
 const pairs=banks.map(b=>[b,n(b),d(b)]).filter(([,a,z])=>a!=null&&z!=null&&Number.isFinite(a)&&Number.isFinite(z)&&z>0);
 const denom=sum(pairs.map(x=>x[2]));
 return {value:denom>0?100*sum(pairs.map(x=>x[1]))/denom:null,n:pairs.length,banks:pairs.map(x=>x[0])};
}
const quote=v=>'"'+String(v??'').replaceAll('"','""')+'"';
const toCsv=rows=>rows.map(r=>r.map(quote).join(',')).join('\n')+'\n';
const fmt=(v,d=3)=>v==null?'n/a':v.toLocaleString('en-US',{minimumFractionDigits:d,maximumFractionDigits:d});
const rows=[['table','period_or_scenario','item','bank','value','unit','n_banks_reporting','n_banks_eligible','reporting_banks','source_commit','input_fingerprint']];
const record=(table,period,item,bank,a,unit='GHS millions')=>rows.push([table,period,item,bank,a.value==null?'':a.value.toFixed(unit==='percent'?4:3),unit,a.n,names.length,a.banks.join(';'),sourceCommit,inputFingerprint]);
const display=(a,d=3)=>fmt(a.value,d)+' ('+a.n+'/'+names.length+')';
const md=['# Ghana banking models: accepted-only sector roll-up','', 'Source commit: `'+sourceCommit+'`','Input fingerprint: `'+inputFingerprint+'`','', '**'+names.length+' of '+tasks.length+' licensed-bank models ordinarily accepted.** These are partial coverage totals, not the whole banking sector.','Accepted banks: '+(names.join(', ')||'none')+'.','Conditional and otherwise excluded models appear only in the separate diagnostics and exclusion manifest. No conditional model enters ordinary totals even if the supervisor reports accepted.','', '## 1. Coverage against Bank of Ghana aggregates','', '| Measure | Period | Accepted banks (GHS bn; count) | BoG (GHS bn) | Indicative coverage |','|---|---|---:|---:|---:|'];
for(const [item,key,p,col] of [['total_assets','total_assets','FY2025','2025-12'],['total_assets','total_assets','9M-2026','2026-09'],['customer_deposits','total_deposits','FY2025','2025-12'],['customer_deposits','total_deposits','9M-2026','2026-09']]){
 const a=aggregate(names,b=>hist(b,p,item)),v=ctx[key]?.[col],den=v!=null&&v.trim()!==''&&Number.isFinite(+v)&&+v>0?+v:null;
 const cov=a.value!=null&&den!=null?100*a.value/1000/den:null;
 record('coverage',p,item,'ACCEPTED_ONLY',a);
 record('coverage_ratio',p,item,'ACCEPTED_ONLY',{...a,value:cov},'percent');
 md.push('| '+item+' | '+p+' | '+fmt(a.value==null?null:a.value/1000,3)+' ('+a.n+'/'+names.length+') | '+fmt(den,1)+' | '+(cov==null?'n/a':fmt(cov,2)+'%')+' |');
}
md.push('','Bank-only values compared with same-month sector aggregates; definitions may differ. No net-loan versus gross-advance coverage comparison.','', '## 2. Historical totals (GHS millions; reporting/eligible banks)','', '| Item | '+periods.join(' | ')+' |','|---|'+periods.map(()=>'---:').join('|')+'|');
for(const i of items){
 const vals=periods.map(p=>{const a=aggregate(names,b=>hist(b,p,i));record('history_total',p,i,'ACCEPTED_ONLY',a);return display(a)});
 md.push('| '+i+' | '+vals.join(' | ')+' |');
}
md.push('','Only reported or derived historical observations are included; unavailable and estimated historical rows are excluded. Pre-impairment operating income is recomputed from net interest income + net fees + net trading + other operating income; incomplete components remain missing.','', '## 3. FY2025 bank comparison','', '| Bank | Assets | Deposits | Net loans | Equity | PAT | Net LDR % | Closing-equity ROE % | Cost/income % |','|---|---:|---:|---:|---:|---:|---:|---:|---:|');
const p='FY2025';
const costs=b=>{const v=['staff_costs','depreciation_amortisation','other_operating_expenses'].map(i=>hist(b,p,i));return v.some(x=>x==null)?null:sum(v)};
const ratios=[['net_ldr',b=>hist(b,p,'loans_and_advances_net'),b=>hist(b,p,'customer_deposits')],['closing_equity_roe',b=>hist(b,p,'profit_after_tax'),b=>hist(b,p,'total_equity')],['cost_to_income',costs,b=>hist(b,p,'operating_income_pre_impairment')]];
const metrics=['total_assets','customer_deposits','loans_and_advances_net','total_equity','profit_after_tax'];
for(const b of names.slice().sort((a,b)=>(hist(b,p,'total_assets')??-Infinity)-(hist(a,p,'total_assets')??-Infinity)||a.localeCompare(b))){
 const vv=metrics.map(i=>{const a=aggregate([b],x=>hist(x,p,i));record('bank_fy2025',p,i,b,a);return fmt(a.value)});
 for(const [i,n,d] of ratios){const a=pairRatio([b],n,d);record('bank_fy2025',p,i,b,a,'percent');vv.push(fmt(a.value,2))}
 md.push('| '+b+' | '+vv.join(' | ')+' |');
}
md.push('','Combined ratios use only banks with both observations and positive denominators. Closing-equity ROE is not comparable to an average-equity or differently defined BoG ROE. No averages of individual bank ratios.','', '| Ratio | Matched-bank value % |','|---|---:|');
for(const [i,n,d] of ratios){const a=pairRatio(names,n,d);record('paired_ratio',p,i,'ACCEPTED_ONLY',a,'percent');md.push('| '+i+' | '+display(a,2)+' |')}
md.push('','## 4. Scenario totals (GHS millions; reporting/eligible banks)','', 'Forecasts are model estimates on shared macro paths, not audited results or guaranteed outcomes. Different calibration, capital proxies and unfunded stress cases limit interpretation.','');
for(const i of ['profit_after_tax','total_assets','total_equity']){
 md.push('### '+i,'','| Scenario | '+years.join(' | ')+' |','|---|'+years.map(()=>'---:').join('|')+'|');
 for(const s of scenarios){const vv=years.map(p=>{const a=aggregate(names,b=>forecast(b,s,p,i));record('forecast_total',s+'|'+p,i,'ACCEPTED_ONLY',a);return display(a)});md.push('| '+s+' | '+vv.join(' | ')+' |')}
 md.push('');
}
md.push('## 5. Excluded models','', '| Bank | Status | Review stage |','|---|---|---|',...exclusions.filter(e=>!e.conditional).map(e=>'| '+e.bank+' | '+(e.status??'unknown')+' | '+(e.stage??'unknown')+' |'),'','See provisional.csv for separate bank-level diagnostics. No excluded or conditional figures are added to ordinary accepted totals. See manifest.json for exact review, package and macro evidence and output hashes.','');
const diagnosticErrors=[];
md.push('## 6. Conditional scope (separate; no aggregate)','', 'A marker is a scope decision, not a PASS or closure. Historical values below are reported/derived only; forecasts are estimates. No figures in this block enter ordinary totals.','', '| Bank | Scope | Claim status | Review stage | FY25 assets (m) | FY25 PAT (m) | FY26E base PAT (m) | FY30E base PAT (m) |','|---|---|---|---|---:|---:|---:|---:|');
const provisional=[['bank','claim_status','review_stage','period_or_scenario','item','value','unit','classification','source_commit']];
for(const t of excluded){
 // Unaccepted work is illustrative only. No aggregation across these banks.
 const safeTable=(name,history=false)=>{try{return getTable(t.slug,name,history)}catch(e){diagnosticErrors.push({bank:t.slug,table:name,error:String(e.message)});return new Map()}};
 const h=safeTable('financials',true),f=safeTable('forecast'),label=markers[t.slug]?.label;
 if(label)md.push('| '+[t.slug,label,t.status??'unknown',t.reviewStage??'unknown',fmt(h.get('|FY2025|total_assets')),fmt(h.get('|FY2025|profit_after_tax')),fmt(f.get('base|FY2026E|profit_after_tax')),fmt(f.get('base|FY2030E|profit_after_tax'))].join(' | ')+' |');
 for(const p of ['FY2025','9M-2026'])for(const i of ['total_assets','customer_deposits','profit_after_tax']){
  const v=h.get('|'+p+'|'+i);provisional.push([t.slug,t.status,t.reviewStage,p,i,v==null?'':v.toFixed(3),'GHS millions',label?label+'; historical observation':'unaccepted historical observation',sourceCommit]);
 }
 for(const s of scenarios)for(const p of ['FY2026E','FY2030E'])for(const i of ['total_assets','profit_after_tax','total_equity']){
  const v=f.get(s+'|'+p+'|'+i);provisional.push([t.slug,t.status,t.reviewStage,s+'|'+p,i,v==null?'':v.toFixed(3),'GHS millions',label?label+'; scenario estimate':'unaccepted scenario estimate',sourceCommit]);
 }
}
const files={'rollup.md':md.join('\n')+'\n','rollup.csv':toCsv(rows),'provisional.csv':toCsv(provisional)};
clean();if(git('rev-parse','HEAD')!==sha)throw Error('HEAD changed during generation');
const summary={sourceCommit,inputFingerprint,accepted:names.length,roster:tasks.length,excluded:excluded.length,conditional:conditional.length,totals:Object.fromEntries(['total_assets','customer_deposits','profit_after_tax'].map(i=>[i,aggregate(names,b=>hist(b,'FY2025',i))]))};
const metadata={schema:3,...summary,acceptedEvidence:evidence,exclusions,diagnosticInputs,diagnosticErrors,conditionalMarkers:markers,sectorContextSha256:hash(ctxText),generatorSha256,scopeClassifierSha256,outputHashes:Object.fromEntries(Object.entries(files).map(([k,v])=>[k,hash(v)]))};
if(check){
 const m=prior;
 for(const [k,v] of Object.entries(metadata))if(!isDeepStrictEqual(m[k],v))throw Error('STALE or modified manifest field: '+k);
 if(typeof m.generatedAt!=='string'||!Number.isFinite(Date.parse(m.generatedAt)))throw Error('Invalid generation timestamp');
 for(const [f,s] of Object.entries(files))if(hash(read(path.join(out,f)))!==hash(s))throw Error('STALE or modified output: '+f);
 console.log(JSON.stringify({...summary,checkedCommit:sha,fresh:true},null,2));
}else{
 fs.mkdirSync(out,{recursive:true});
 for(const [f,s] of Object.entries(files))fs.writeFileSync(path.join(out,f),s);
 fs.writeFileSync(path.join(out,'manifest.json'),JSON.stringify({generatedAt:new Date().toISOString(),...metadata},null,2)+'\n');
 console.log(JSON.stringify({...summary,diagnosticErrors},null,2));
}
