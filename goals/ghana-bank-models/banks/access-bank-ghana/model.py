"""Access Ghana scenario estimates; standard library; amounts in GHS millions."""
import csv, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
def readcsv(path):
    with open(path, encoding='utf-8', newline='') as f: return list(csv.DictReader(f))
hist = readcsv(os.path.join(HERE, 'financials.csv'))
with open(os.path.join(HERE, 'assumptions.json'), encoding='utf-8') as f: settings = json.load(f)
macro = {(r['scenario'], r['year'], r['driver']): float(r['value']) for r in readcsv(os.path.join(HERE, settings['macro_source'])) if r['value']}
def h(period):
    return {r['line_item']:float(r['value']) for r in hist if r['period']==period and r['value']}
q = h('9M-2026'); annual = h('FY2025')
rows=[]; results=[]
for scenario, a in settings['scenarios'].items():
    prior = dict(q)
    capital_density = (q['total_equity'] / (q['car_pct']/100)) / q['total_assets']
    for year in range(2026,2031):
        yr=f'FY{year}E'
        def m(driver): return macro[(scenario,yr,driver)]
        nominal=(1+m('gdp_growth_pct')/100)*(1+m('inflation_cpi_pct')/100)-1
        growth=max(-0.5,nominal+a['growth_spread_pp']/100)
        q4=year==2026
        loan=prior['loans_and_advances_net']*(1+(a['q4_loan_growth'] if q4 else growth))
        deposit=prior['customer_deposits']*(1+(a['q4_deposit_growth'] if q4 else growth))
        due=prior['due_to_banks']*(1+(a['q4_deposit_growth']/2 if q4 else growth/2))
        borrow=prior['borrowings']; lease=prior['x_lease_obligation']
        liability_other=prior['other_liabilities']*(1+(0.01 if q4 else m('inflation_cpi_pct')/100))
        total_liab=deposit+due+borrow+lease+liability_other
        ppe=prior['property_equipment_intangibles']*(1.01 if q4 else 1.03)
        other_asset=prior['other_assets']*(1.01 if q4 else 1.02)
        cash=prior['x_cash_and_cash_equivalents']*(1+(a['q4_deposit_growth'] if q4 else growth))
        trading_assets=prior['x_nonpledged_trading_assets']
        if q4:
            scale=1+a['q4_flow_fraction']; interest=q['interest_income']*scale; expense=q['interest_expense']*scale
            netfee=q['x_net_fee_commission']*scale; trading=q['net_trading_income']*scale; otherinc=q['other_operating_income']*scale
            staff=q['staff_costs']*scale; depn=q['depreciation_amortisation']*scale; otherexp=q['other_operating_expenses']*scale
            impairment=q['impairment_charge']+0.5*(q['loans_and_advances_net']+loan)*a['annual_credit_cost_pct']/400
            nii=interest-expense; op=nii+netfee+trading+otherinc
            pbt=op-staff-depn-otherexp-impairment
            tax=q['income_tax']+max(0,pbt-q['profit_before_tax'])*0.35
            pat=pbt-tax; retained=q['retained_earnings']+pat-q['profit_after_tax']; reserve=q['reserves_other']
        else:
            policy_delta=(m('policy_rate_pct')-macro[(scenario,f'FY{year-1}E','policy_rate_pct')])/100
            bill_delta=(m('tbill_91d_pct')-macro[(scenario,f'FY{year-1}E','tbill_91d_pct')])/100
            # Interest sensitivity is illustrative and applies only half the rate change to the earning/funding bases.
            interest=max(0,prior['interest_income']*(1+growth)+0.5*policy_delta*(loan+prior['investment_securities']))
            expense=max(0,prior['interest_expense']*(1+growth)+0.5*bill_delta*deposit)
            netfee=prior['x_net_fee_commission']*(1+growth); trading=prior['net_trading_income']*(1+growth); otherinc=prior['other_operating_income']*(1+growth)
            staff=prior['staff_costs']*(1+m('inflation_cpi_pct')/100); depn=prior['depreciation_amortisation']*1.03; otherexp=prior['other_operating_expenses']*(1+m('inflation_cpi_pct')/100)
            impairment=0.5*(prior['loans_and_advances_net']+loan)*a['annual_credit_cost_pct']/100
            nii=interest-expense; op=nii+netfee+trading+otherinc; pbt=op-staff-depn-otherexp-impairment
            tax=max(0,pbt)*0.35; pat=pbt-tax
            dividend=max(0,pat)*a['payout']; retained=prior['retained_earnings']+pat-dividend; reserve=prior['reserves_other']
        equity=q['stated_capital']+retained+reserve; assets=total_liab+equity
        invest=assets-cash-trading_assets-loan-ppe-other_asset
        car=100*equity/(assets*capital_density) if assets>0 else None
        npl=max(0,prior['npl_pct']+a['npl_step_pp'])
        avg_equity=0.5*((annual['total_equity'] if q4 else prior['total_equity'])+equity)
        avg_assets=0.5*((annual['total_assets'] if q4 else prior['total_assets'])+assets)
        values={'interest_income':interest,'interest_expense':expense,'net_interest_income':nii,'x_net_fee_commission':netfee,'net_trading_income':trading,'other_operating_income':otherinc,'total_operating_income':op,'staff_costs':staff,'depreciation_amortisation':depn,'other_operating_expenses':otherexp,'impairment_charge':impairment,'profit_before_tax':pbt,'income_tax':tax,'profit_after_tax':pat,'x_cash_and_cash_equivalents':cash,'x_nonpledged_trading_assets':trading_assets,'investment_securities':invest,'loans_and_advances_net':loan,'property_equipment_intangibles':ppe,'other_assets':other_asset,'total_assets':assets,'customer_deposits':deposit,'due_to_banks':due,'borrowings':borrow,'x_lease_obligation':lease,'other_liabilities':liability_other,'total_liabilities':total_liab,'stated_capital':q['stated_capital'],'retained_earnings':retained,'reserves_other':reserve,'total_equity':equity,'car_pct':car,'npl_pct':npl,'ldr_pct':100*loan/deposit if deposit>0 else None,'cost_to_income_pct':100*(staff+depn+otherexp)/op if op>0 else None,'roe_pct':100*pat/avg_equity if avg_equity>0 else None,'roa_pct':100*pat/avg_assets if avg_assets>0 else None}
        income_keys={'interest_income','interest_expense','net_interest_income','x_net_fee_commission','net_trading_income','other_operating_income','total_operating_income','staff_costs','depreciation_amortisation','other_operating_expenses','impairment_charge','profit_before_tax','income_tax','profit_after_tax'}
        for key,value in values.items():
            statement='income_statement' if key in income_keys else ('ratios' if key in {'car_pct','npl_pct','ldr_pct','cost_to_income_pct','roe_pct','roa_pct'} else 'balance_sheet')
            note='Net loans/customer deposits, percent' if key=='ldr_pct' else 'Operating expenses/pre-impairment operating income, percent' if key=='cost_to_income_pct' else 'Scenario estimate; see assumptions.json'
            rows.append(['access-bank-ghana',scenario,yr,statement,key,'' if value is None else f'{value:.3f}','%' if statement=='ratios' else 'GHS millions','MODEL-ESTIMATE','unavailable' if value is None else 'estimated',note])
        for stmt,key in [('income_statement','fee_commission_income'),('income_statement','fee_commission_expense'),('balance_sheet','cash_and_bog_balances'),('balance_sheet','due_from_banks'),('balance_sheet','loans_and_advances_gross'),('balance_sheet','loan_loss_allowance'),('ratios','tier1_pct')]:
            rows.append(['access-bank-ghana',scenario,yr,stmt,key,'','%' if stmt=='ratios' else 'GHS millions','MODEL-ESTIMATE','unavailable','Separate component not projected; see assumptions'])
        results.append((scenario,yr,assets-total_liab-equity,invest,car,m('min_car_pct'),pat))
        prior=values

with open(os.path.join(HERE,'forecast.csv'),'w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['bank','scenario','period','statement','line_item','value','unit','source_id','status','notes']);w.writerows(rows)
with open(os.path.join(HERE,'checks.md'),'w',encoding='utf-8') as f:
    f.write('# Access Bank Ghana forecast checks\n\nHistorical bridge checkpoint: checks-history.md. Forecast values are estimates; run model.py to rebuild.\n\n| Scenario | Year | Balance residual GHS m | Investment securities GHS m | CAR proxy % | Minimum scenario % | PAT GHS m |\n|---|---|---:|---:|---:|---:|---:|\n')
    for s,y,b,i,c,minimum,p in results:f.write(f'| {s} | {y} | {b:.3f} | {i:.3f} | {c if c is not None else "unavailable"} | {minimum:.2f} | {p:.3f} |\n')
    f.write('\nNegative investment securities indicate an infeasible balance sheet. CAR is an estimate calibrated to September 2026; calculate the difference from the macro minimum and flag shortfalls. Cash includes non-BoG balances; actual reserve compliance is unavailable. This model does not add capital automatically. Verify forecast logic and income components independently before use.\n')
print(f'wrote {len(rows)} rows; negative investments: {sum(i<0 for _,_,_,i,_,_,_ in results)}; CAR below scenario minimum: {sum(c is None or c<minimum for _,_,_,_,c,minimum,_ in results)}')
