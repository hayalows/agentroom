// GCB executable model. Node 18+; no dependencies. Pure forecast function was executed against the repo inputs in the cloud.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
function parseCSV(text) {
  const out=[]; let row=[], v="", quoted=false;
  for(let i=0;i<text.length;i++){
    const c=text[i]; if(quoted){if(c==='"'&&text[i+1]==='"'){v+='"';i++;}else if(c==='"')quoted=false;else v+=c;}
    else if(c==='"'&&v==="")quoted=true;else if(c===','){row.push(v);v="";}else if(c==='\n'){row.push(v);if(row.some(Boolean))out.push(row);row=[];v="";}else if(c!=='\r')v+=c;
  }
  if(v||row.length){row.push(v);out.push(row);} if(quoted)throw Error("unterminated CSV quote");
  const h=out.shift(); return out.map(r=>{if(r.length!==h.length)throw Error("CSV column count "+r.length+" != "+h.length);return Object.fromEntries(h.map((k,i)=>[k,r[i]]));});
}
function build(finText, assumptionText, macroText){
  const A=JSON.parse(assumptionText), D=A.drivers, M=parseCSV(macroText), H=parseCSV(finText);
  const scenarios=["base","downside","upside"], periods=A.forecast_periods;
  const keysI="interest_income interest_expense net_interest_income fee_commission_income fee_commission_expense net_trading_income other_operating_income total_operating_income staff_costs depreciation_amortisation other_operating_expenses impairment_charge profit_before_tax income_tax profit_after_tax".split(" ");
  const keysB="cash_and_bog_balances due_from_banks investment_securities loans_and_advances_gross loan_loss_allowance loans_and_advances_net property_equipment_intangibles other_assets total_assets customer_deposits due_to_banks borrowings other_liabilities total_liabilities stated_capital retained_earnings reserves_other total_equity".split(" ");
  const keysR="car_pct tier1_pct npl_pct ldr_pct cost_to_income_pct roe_pct roa_pct".split(" ");
  const hist=(t,k)=>{const r=H.find(x=>x.period===t&&x.line_item===k);if(!r||r.value===""||!Number.isFinite(+r.value))throw Error("Missing historical "+t+" "+k);return +r.value;};
  const macro=(s,t,k)=>{const r=M.find(x=>x.scenario===s&&x.year===t&&x.driver===k);if(!r||r.status==="unavailable"||r.value===""||!Number.isFinite(+r.value))throw Error("Missing shared macro "+s+" "+t+" "+k);return +r.value;};
  const obj=(t,keys,exclude=[])=>Object.fromEntries(keys.filter(k=>!exclude.includes(k)).map(k=>[k,hist(t,k)]));
  const year25=obj("FY2025",keysB), q3=obj("9M-2026",keysB,["loans_and_advances_gross","loan_loss_allowance"]), qI=obj("9M-2026",keysI);
  q3.loans_and_advances_gross=q3.loans_and_advances_net/(1-year25.loan_loss_allowance/year25.loans_and_advances_gross);q3.loan_loss_allowance=q3.loans_and_advances_gross-q3.loans_and_advances_net;
  const rwaDensity=(hist("FY2025","x_risk_weighted_assets")-year25.loans_and_advances_gross)/(year25.total_assets-year25.loans_and_advances_gross);
  const rwa=(assets,gross)=>gross+rwaDensity*(assets-gross), q3Rwa=rwa(q3.total_assets,q3.loans_and_advances_gross), q3Capital=q3Rwa*hist("9M-2026","car_pct")/100;
  const q3Tier1=q3Capital*hist("FY2025","x_tier1_capital")/hist("FY2025","x_regulatory_capital");
  const pct=x=>x/100, avg=(x,y)=>(x+y)/2, clip=(x,lo,hi)=>Math.max(lo,Math.min(x,hi));
  const funding=b=>b.customer_deposits+b.due_to_banks+b.borrowings;
  const asNonCash=b=>b.due_from_banks+b.investment_securities+b.loans_and_advances_net+b.property_equipment_intangibles+b.other_assets;
  const costs=i=>i.staff_costs+i.depreciation_amortisation+i.other_operating_expenses;
  const rows=[], checks=[], summary=[], header=["bank","period","statement","line_item","value","unit","source_id","page","status","notes","scenario"];
  const noteI={interest_income:"Q4 2026 9M run-rate; 2027+ average net loans times loan yield plus average securities times investment yield plus average interbank assets times policy-linked interbank yield.",interest_expense:"Q4 funding sensitivity; later average total deposits, due-to-banks and borrowings times blended funding cost.",net_interest_income:"Interest income minus interest expense.",fee_commission_income:"9M run-rate plus Q4 scenario, then nominal GDP proxy plus fee growth spread.",fee_commission_expense:"Prior fee-expense ratio adjusted for scenario; Q4 run-rate for 2026.",net_trading_income:"Run-rate in 2026; subsequent underlying trading growth plus USD translation P&L.",other_operating_income:"Run-rate then fee-growth proxy.",total_operating_income:"NII + fee income - fee expense + trading + other operating income.",staff_costs:"Q4 run-rate plus cost sensitivity; then CPI plus cost-growth spread.",depreciation_amortisation:"Q4 run-rate plus cost sensitivity; then CPI plus cost-growth spread.",other_operating_expenses:"Q4 run-rate plus cost sensitivity; then CPI plus cost-growth spread.",impairment_charge:"9M actual + estimated Q4 loan charge; later average gross loans times scenario cost of risk; no assumed sovereign one-off.",profit_before_tax:"Operating income - staff - depreciation - other opex - impairment.",income_tax:"2026 actual 9M tax + estimated tax on positive Q4 PBT; later blended tax on positive PBT.",profit_after_tax:"PBT less income tax."};
  const noteB={cash_and_bog_balances:"Residual assets after funding, equity and noncash assets; negative is an infeasible funding gap, not available cash.",due_from_banks:"Deposit-growth proxy plus separately modeled USD translation.",investment_securities:"Deposit-growth proxy plus separately modeled USD translation.",loans_and_advances_gross:"FY2026 net/(1-allowance ratio); 2027+ organic growth plus USD translation grossed up.",loan_loss_allowance:"Gross loans times scenario allowance ratio; distinct from annual impairment expense.",loans_and_advances_net:"Gross minus allowance; FY2026 anchored to actual 9M net loans.",property_equipment_intangibles:"Inflation plus operating-expense spread, quarter-weighted in 2026.",other_assets:"Inflation plus operating-expense spread, quarter-weighted in 2026.",total_assets:"Cash plus noncash asset components.",customer_deposits:"Organic deposit growth plus USD translation after FY2026.",due_to_banks:"Deposit-growth proxy.",borrowings:"Deposit-growth proxy; no automatic funding injected to mask cash gap.",other_liabilities:"Deposit-growth proxy.",total_liabilities:"Sum of modeled liabilities.",stated_capital:"Held constant; no assumed capital raise.",retained_earnings:"Opening retained earnings plus incremental modeled PAT minus modeled dividend.",reserves_other:"Held constant; no forecast OCI or reserve transfers.",total_equity:"Stated capital + retained earnings + reserves."};
  function row(s,t,statement,key,value,unit,note){if(!Number.isFinite(value))throw Error("Non-finite forecast "+s+" "+t+" "+key);rows.push(["gcb",t,statement,key,value.toFixed(unit==="%"?4:3),unit,"assumptions.json; ../../sector/macro-assumptions/macro.csv","","estimated",note+" | scenario="+s,s]);}
  for(const s of scenarios){
    let prevB={...q3}, prevI=null, prevCap=q3Capital, prevTier=q3Tier1, prevFx=null, prevTradingUnderlying=null;
    for(let j=0;j<periods.length;j++){
      const t=periods[j], first=j===0, b={}, i={}, risk=D.cost_of_risk[s], allow=pct(D.allowance_to_gross_pct[s]), gd=macro(s,t,"gdp_growth_pct"), inf=macro(s,t,"inflation_cpi_pct"), pol=macro(s,t,"policy_rate_pct"), endFx=macro(s,t,"ghs_per_usd_end"), crr=macro(s,t,"crr_pct"), minCAR=macro(s,t,"min_car_pct"), minPaid=macro(s,t,"min_capital_ghs_m"), carTarget=minCAR+D.capital_ratio_target_pct[s];
      const nominal=gd+inf, lg=first?D.loan_growth[s].q4_pct:clip(nominal+D.loan_growth[s].spread_pp,-10,35), dg=first?D.deposit_growth[s].q4_pct:clip(nominal+D.deposit_growth[s].spread_pp,-10,35), og=inf+D.opex_growth[s], fg=nominal+D.fee_growth[s], fxDelta=first?0:endFx-prevFx, fx=D.fx.usd_assets_m, fxNet=(fx.cash+fx.due_from_banks+fx.net_loans+fx.securities-D.fx.usd_deposits_m)*fxDelta;
      b.customer_deposits=prevB.customer_deposits*(1+pct(dg))+D.fx.usd_deposits_m*fxDelta;
      for(const k of ["due_to_banks","borrowings","other_liabilities"])b[k]=prevB[k]*(1+pct(dg));
      b.total_liabilities=b.customer_deposits+b.due_to_banks+b.borrowings+b.other_liabilities;
      b.due_from_banks=prevB.due_from_banks*(1+pct(dg))+fx.due_from_banks*fxDelta;
      b.investment_securities=prevB.investment_securities*(1+pct(dg))+fx.securities*fxDelta;
      if(first){b.loans_and_advances_net=prevB.loans_and_advances_net*(1+pct(lg));b.loans_and_advances_gross=b.loans_and_advances_net/(1-allow);}
      else{b.loans_and_advances_gross=prevB.loans_and_advances_gross*(1+pct(lg))+fx.net_loans*fxDelta/(1-allow);}
      b.loan_loss_allowance=b.loans_and_advances_gross*allow;b.loans_and_advances_net=b.loans_and_advances_gross-b.loan_loss_allowance;
      for(const k of ["property_equipment_intangibles","other_assets"])b[k]=prevB[k]*(1+pct(og)/(first?4:1));
      const loanYield=pol+D.loan_yield[s], investmentYield=macro(s,t,"tbill_364d_pct")*D.investment_yield.weights.tbill_364d_pct+macro(s,t,"govt_bond_yield_pct")*D.investment_yield.weights.govt_bond_yield_pct, cofund=pol*D.cost_of_funds[s];
      const loanCharge=Math.max(avg(prevB.loans_and_advances_gross,b.loans_and_advances_gross)*pct(risk)/(first?4:1),b.loan_loss_allowance-prevB.loan_loss_allowance,0);
      let underlyingTrading;
      if(first){
        const rev=D.q4_income_runrate_multiplier[s], cm=D.model_structure.q4_cost_multiplier[s], fm=D.model_structure.q4_funding_multiplier[s];
        for(const k of ["interest_income","fee_commission_income","net_trading_income","other_operating_income"])i[k]=qI[k]*(1+rev/3);
        i.interest_expense=qI.interest_expense*(1+fm/3);
        i.fee_commission_expense=qI.fee_commission_expense*(1+rev*D.model_structure.fee_expense_ratio_multiplier[s]/3);
        for(const k of ["staff_costs","depreciation_amortisation","other_operating_expenses"])i[k]=qI[k]*(1+cm/3);
        i.impairment_charge=qI.impairment_charge+loanCharge; underlyingTrading=i.net_trading_income;
      }else{
        i.interest_income=avg(prevB.loans_and_advances_net,b.loans_and_advances_net)*pct(loanYield)+avg(prevB.investment_securities,b.investment_securities)*pct(investmentYield)+avg(prevB.due_from_banks,b.due_from_banks)*pct(pol*D.model_structure.interbank_yield_policy_factor);
        i.interest_expense=avg(funding(prevB),funding(b))*pct(cofund);
        i.fee_commission_income=prevI.fee_commission_income*(1+pct(fg));i.fee_commission_expense=i.fee_commission_income*(prevI.fee_commission_expense/prevI.fee_commission_income)*D.model_structure.fee_expense_ratio_multiplier[s];
        underlyingTrading=prevTradingUnderlying*(1+pct(nominal+D.model_structure.trading_growth_spread_pp[s]));i.net_trading_income=underlyingTrading+fxNet;
        i.other_operating_income=prevI.other_operating_income*(1+pct(fg));
        for(const k of ["staff_costs","depreciation_amortisation","other_operating_expenses"])i[k]=prevI[k]*(1+pct(og));
        i.impairment_charge=loanCharge;
      }
      i.net_interest_income=i.interest_income-i.interest_expense;i.total_operating_income=i.net_interest_income+i.fee_commission_income-i.fee_commission_expense+i.net_trading_income+i.other_operating_income;
      i.profit_before_tax=i.total_operating_income-costs(i)-i.impairment_charge;
      i.income_tax=first?qI.income_tax+Math.max(0,i.profit_before_tax-qI.profit_before_tax)*pct(D.tax_rate_pct[s]):Math.max(0,i.profit_before_tax)*pct(D.tax_rate_pct[s]);
      i.profit_after_tax=i.profit_before_tax-i.income_tax;
      const incPAT=first?i.profit_after_tax-qI.profit_after_tax:i.profit_after_tax, preEquity=prevB.total_equity+incPAT, preAssets=b.total_liabilities+preEquity, preCash=preAssets-asNonCash(b), preRwa=rwa(preAssets,b.loans_and_advances_gross), preCap=prevCap+incPAT, reserve=b.customer_deposits*pct(crr);
      const div=Math.max(0,Math.min(Math.max(incPAT,0)*pct(D.dividend_payout_pct[s]),preCap-preRwa*pct(carTarget),preCash-reserve));
      b.stated_capital=prevB.stated_capital;b.reserves_other=prevB.reserves_other;b.retained_earnings=prevB.retained_earnings+incPAT-div;b.total_equity=b.stated_capital+b.retained_earnings+b.reserves_other;b.total_assets=b.total_liabilities+b.total_equity;b.cash_and_bog_balances=b.total_assets-asNonCash(b);
      const cap=preCap-div,tier=prevTier+incPAT-div, rw=rwa(b.total_assets,b.loans_and_advances_gross), car=100*cap/rw;
      const openingAnnual=first?year25:prevB;
      const ratios={car_pct:car,tier1_pct:100*tier/rw,npl_pct:D.npl_pct[s],ldr_pct:100*b.loans_and_advances_gross/b.customer_deposits,cost_to_income_pct:100*costs(i)/i.total_operating_income,roe_pct:100*i.profit_after_tax/avg(openingAnnual.total_equity,b.total_equity),roa_pct:100*i.profit_after_tax/avg(openingAnnual.total_assets,b.total_assets)};
      for(const k of keysI)row(s,t,"income_statement",k,i[k],"GHS millions",noteI[k]);
      for(const k of keysB)row(s,t,"balance_sheet",k,b[k],"GHS millions",noteB[k]);
      for(const k of keysR)row(s,t,"ratios",k,ratios[k],"%",k==="car_pct"?"Proxy regulatory capital divided by proxy RWA; not a BoG regulatory return.":k==="tier1_pct"?"Estimated tier 1 capital/RWA; Q3 starting tier 1 inferred from FY2025 capital structure.":k==="npl_pct"?"Estimated scenario NPL target; not loan-level migration model.":k==="ldr_pct"?"Gross loans / customer deposits.":k==="cost_to_income_pct"?"Operating expenses excluding impairments / total operating income.":"PAT / mean opening and closing annual balance.");
      const short=Math.max(0,rw*pct(minCAR)-cap), cashGap=Math.max(0,reserve-b.cash_and_bog_balances), allowanceMovement=prevB.loan_loss_allowance+loanCharge-b.loan_loss_allowance;
      for(const [k,v,n] of [["x_regulatory_capital",cap,"Proxy Q3 capital from 14.6% CAR times estimated RWA plus cumulative retained modeled earnings."],["x_tier1_capital",tier,"Proxy initial tier1/capital relation from FY2025; retained modeled earnings."],["x_risk_weighted_assets",rw,"Gross loans plus calibrated FY2025 residual risk intensity times assets minus gross loans."],["x_model_dividends",div,first?"Estimated Q4-only dividends; observed 9M retained earnings already includes YTD equity movements.":"Estimated annual dividends constrained by pre-dividend CAR target and cash reserve proxy."],["x_cash_reserve_proxy",reserve,"CRR times modeled year-end deposits; screening proxy, not actual eligible reserve."],["x_cash_reserve_gap",cashGap,"Positive value is reserve proxy shortfall; not automatically funded."],["x_capital_shortfall",short,"Additional regulatory capital needed to reach shared minimum CAR; not assumed raised."],["x_allowance_other_movement",allowanceMovement,"Opening modeled allowance + modeled loan impairment charge - closing modeled allowance; positive implied write-offs/other reductions; provision floor prevents an unfunded allowance build. FY2026 Q4 only."]])row(s,t,"balance_sheet",k,v,"GHS millions",n);
      row(s,t,"income_statement","x_fx_revaluation_pnl",fxNet,"GHS millions",first?"Q4 separate FX translation not estimated; actual 9M includes realized YTD. Zero incremental translation assumption, not observed.":"USD net exposure at FY2025 x annual change in shared closing USD/GHS rate; included in net trading income, not additive.");
      row(s,t,"income_statement","x_model_loan_impairment",loanCharge,"GHS millions",first?"Estimated Q4-only impairment; actual nine-month aggregate preserved.":"Estimated annual loan impairment included in total impairment charge.");
      row(s,t,"income_statement","x_derecognition_loss_investments",0,"GHS millions","No repeat of one-off DDEP derecognition assumed; not an actual number.");
      for(const [k,v,n] of [["x_min_car_pct",minCAR,"Shared macro minimum CAR screening threshold."],["x_capital_target_pct",carTarget,"Shared minimum plus scenario management buffer."],["x_investment_yield_pct",investmentYield,"50:50 weighted shared 364-day bill and 10-year bond rates; FY2026 income anchored on run-rate."],["x_loan_yield_pct",loanYield,"Policy rate plus scenario spread; FY2026 income anchored on run-rate."],["x_cost_of_funds_pct",cofund,"Policy rate times scenario factor; FY2026 expense anchored on run-rate."]])row(s,t,"ratios",k,v,"%",n);
      const residuals=[b.total_assets-b.total_liabilities-b.total_equity,b.total_assets-b.cash_and_bog_balances-asNonCash(b),b.total_liabilities-b.customer_deposits-b.due_to_banks-b.borrowings-b.other_liabilities,b.total_equity-b.stated_capital-b.retained_earnings-b.reserves_other,i.net_interest_income-i.interest_income+i.interest_expense,i.total_operating_income-i.net_interest_income-i.fee_commission_income+i.fee_commission_expense-i.net_trading_income-i.other_operating_income,i.profit_before_tax-i.total_operating_income+costs(i)+i.impairment_charge,i.profit_after_tax-i.profit_before_tax+i.income_tax,b.loans_and_advances_net-b.loans_and_advances_gross+b.loan_loss_allowance];
      const max=Math.max(...residuals.map(Math.abs));if(max>1e-7)throw Error("Accounting check failed "+s+" "+t);
      checks.push({s,t,max,car,minCAR,capitalGap:short,cash:b.cash_and_bog_balances,reserve,cashGap,paid:b.stated_capital,minPaid,allowanceMovement,pat:i.profit_after_tax,assets:b.total_assets,loan:b.loans_and_advances_gross,deposit:b.customer_deposits,div});
      summary.push({s,t,assets:b.total_assets,pat:i.profit_after_tax,car,cashGap,capitalGap:short,ldr:ratios.ldr_pct,roe:ratios.roe_pct});
      prevB=b;prevI=i;prevCap=cap;prevTier=tier;prevFx=endFx;prevTradingUnderlying=underlyingTrading;
    }
  }
  const fmt=x=>Number(x).toFixed(3), quote=x=>'"'+String(x).replaceAll('"','""')+'"';
  const csv=[header,...rows].map(r=>r.map(quote).join(",")).join("\n")+"\n";
  const mark="<!-- FORECAST CHECKS GENERATED -->";
  const lines=[mark,"## Forecast checks (generated from shared macro scenarios)","","All forecast rows estimated. Currency GHS millions; ratios percentages. Accounting arithmetic checked before rounding. Cash reserve and CAR checks are screening proxies, not regulatory returns. A negative cash residual or positive gap is a flagged financing requirement; not an assumed funding source.","",`Rows: ${rows.length}; scenario-years: ${checks.length}; FY2025 residual RWA density: ${rwaDensity.toFixed(6)}; estimated September 2026 RWA: ${fmt(q3Rwa)}; initial proxy regulatory capital: ${fmt(q3Capital)} (anchored to observed 14.6% CAR).`,"","| Scenario | Year | Max bridge residual | CAR % | Min CAR % | Capital gap | Cash | CRR proxy | Reserve gap | Paid capital vs min | Allowance other movement |","|---|---|---:|---:|---:|---:|---:|---:|---:|---|---:|"];
  for(const x of checks)lines.push(`| ${x.s} | ${x.t} | ${fmt(x.max)} | ${fmt(x.car)} | ${fmt(x.minCAR)} | ${fmt(x.capitalGap)} | ${fmt(x.cash)} | ${fmt(x.reserve)} | ${fmt(x.cashGap)} | ${fmt(x.paid)} / ${fmt(x.minPaid)} | ${fmt(x.allowanceMovement)} |`);
  lines.push("",`Accounting bridges: PASS (${checks.length}/${checks.length}). Capital below shared minimum: ${checks.filter(x=>x.capitalGap>1e-6).length}/${checks.length} flagged. Cash reserve proxy shortfalls: ${checks.filter(x=>x.cashGap>1e-6).length}/${checks.length} flagged. Negative cash: ${checks.filter(x=>x.cash<0).length}/${checks.length} flagged. Paid capital below shared minimum: ${checks.filter(x=>x.paid<x.minPaid).length}/${checks.length}. Negative allowance-other movement: ${checks.filter(x=>x.allowanceMovement<-1e-6).length}/${checks.length}; this is an unexplained allowance bridge component, not a reported recovery.`,`FY2026 estimated earnings retain actual 9M income and estimate Q4 only. FY2026 tax does not override reported 9M. FX translation separately estimated from FY2027; EUR/GBP and actual interim USD balances unavailable. Full prudential risk weights, OCI, capital deductions and liquidity eligibility are not available, so model is a simplified scenario analysis. Current paid-up capital threshold verification and non-GCB reported ratio comparisons remain open. Independent review required.`,"");
  return {csv,forecastChecks:lines.join("\n"),summary,checks,rows:rows.length};
}
const here=path.dirname(fileURLToPath(import.meta.url));
const read=x=>fs.readFileSync(path.resolve(here,x),'utf8');
const a=read('assumptions.json');
const result=build(read('financials.csv'),a,read(JSON.parse(a).macro_file));
const checksPath=path.join(here,'checks.md');
const marker='<!-- FORECAST CHECKS GENERATED -->';
const historical=fs.existsSync(checksPath)?fs.readFileSync(checksPath,'utf8').split(marker)[0].trimEnd():'# GCB checks';
fs.writeFileSync(path.join(here,'forecast.csv'),result.csv);
fs.writeFileSync(checksPath,historical+'\n\n'+result.forecastChecks+'\n');
console.log(JSON.stringify({rows:result.rows,summary:result.summary},null,2));
