// Supplemental output-based earnings bridge. No forecast engine modifications.
import {csv,pin,ordinary,years} from './diagnostic.mjs';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
export function earningsBridge(slug,text,blob=''){
 const rows=csv(text);
 const fields=['net_interest_income','total_operating_income','impairment_charge','profit_before_tax','profit_after_tax','interest_income','interest_expense'];
 const get=(s,y,k)=>{const r=rows.filter(x=>x.scenario===s&&x.period==='FY'+y+'E'&&x.statement==='income_statement'&&x.line_item===k);
  if(r.length!==1||r[0].status!=='estimated'||r[0].value.trim()===''||!Number.isFinite(Number(r[0].value))||r[0].bank!==slug)throw Error(slug+' '+s+' '+y+' '+k);
  return Number(r[0].value);
 };
 return {slug,blob,years:years.map(y=>{
  const B=Object.fromEntries(fields.map(k=>[k,get('base',y,k)])),D=Object.fromEntries(fields.map(k=>[k,get('downside',y,k)]));
  const gap={
   nii:B.net_interest_income-D.net_interest_income,
   noninterest:(B.total_operating_income-B.net_interest_income)-(D.total_operating_income-D.net_interest_income),
   impairment:D.impairment_charge-B.impairment_charge,
   other_costs:(D.total_operating_income-D.profit_before_tax-D.impairment_charge)-(B.total_operating_income-B.profit_before_tax-B.impairment_charge),
   tax_levy:(D.profit_before_tax-D.profit_after_tax)-(B.profit_before_tax-B.profit_after_tax),
  };
  const pat=B.profit_after_tax-D.profit_after_tax,ii=B.interest_income-D.interest_income,ie=D.interest_expense-B.interest_expense;
  if(Math.abs(pat-Object.values(gap).reduce((a,b)=>a+b,0))>.0051||Math.abs(gap.nii-ii-ie)>.0051)throw Error(slug+' bridge failed '+y);
  return {year:y,pat,ii,ie,...gap};
 })};
}
export function aggregate(banks){
 if(banks.length!==ordinary.length||new Set(banks.map(x=>x.slug)).size!==ordinary.length||!ordinary.every(x=>banks.some(b=>b.slug===x)))throw Error('ordinary roster mismatch');
 const fields=['pat','nii','noninterest','impairment','other_costs','tax_levy','ii','ie'];
 const sum=(a)=>Object.fromEntries(fields.map(k=>[k,a.reduce((s,x)=>s+x[k],0)]));
 const annual=years.map(y=>({year:y,...sum(banks.map(b=>b.years.find(v=>v.year===y)))}));
 const cumulative=sum(annual);
 return {pin,ordinary_count:banks.length,annual,cumulative,banks:banks.map(b=>({slug:b.slug,fy2030:b.years.find(v=>v.year===2030),cumulative:sum(b.years)})).sort((a,b)=>b.fy2030.pat-a.fy2030.pat)};
}
if(process.argv[1]&&path.resolve(process.argv[1])===path.resolve(fileURLToPath(import.meta.url))){
 const banks=ordinary.map(slug=>{const file='goals/ghana-bank-models/banks/'+slug+'/forecast.csv';return earningsBridge(slug,execFileSync('git',['show',pin+':'+file],{encoding:'utf8',maxBuffer:8*1024*1024}),execFileSync('git',['rev-parse',pin+':'+file],{encoding:'utf8'}).trim())});
 console.log(JSON.stringify(aggregate(banks),null,2));
}
