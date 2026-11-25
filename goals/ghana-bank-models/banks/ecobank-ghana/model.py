import csv, json, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MACRO_PATH = os.path.normpath(os.path.join(BASE_DIR, '..', '..', 'sector', 'macro-assumptions', 'macro.csv'))
HIST_PATH = os.path.join(BASE_DIR, 'financials.csv')
ASSUMP_PATH = os.path.join(BASE_DIR, 'assumptions.json')
FORECAST_PATH = os.path.join(BASE_DIR, 'forecast.csv')
CHECKS_PATH = os.path.join(BASE_DIR, 'checks.md')

def load_hist():
    hist = {}
    rows = []
    with open(HIST_PATH, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            rows.append(r)
            p = r['period']
            hist.setdefault(p, {})[r['line_item']] = None if r['value'] == '' else float(r['value'])
    return hist, rows

def load_macro():
    macro = {}
    with open(MACRO_PATH, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            if r['value'] != '':
                macro[(r['scenario'], r['year'], r['driver'])] = float(r['value'])
    return macro

def check_historical(hist, hist_rows):
    res = []
    for p in ['FY2021', 'FY2022', 'FY2023', 'FY2024', 'FY2025', '9M-2026']:
        d = hist[p]
        bs = d['total_assets'] - (d['total_liabilities'] + d['total_equity'])
        as_sum = d['total_assets'] - (d['cash_and_bog_balances'] + d['investment_securities'] + d['loans_and_advances_net'] + d['property_equipment_intangibles'] + d['other_assets'])
        ls_sum = d['total_liabilities'] - (d['customer_deposits'] + d['due_to_banks'] + d['borrowings'] + d['other_liabilities'])
        eq_sum = d['total_equity'] - (d['stated_capital'] + d['retained_earnings'] + d['reserves_other'])
        nii = d['net_interest_income'] - (d['interest_income'] - d['interest_expense'])
        toi = d['total_operating_income'] - (d['net_interest_income'] + (d['fee_commission_income'] - d['fee_commission_expense']) + d['net_trading_income'] + d['other_operating_income'])
        opex = d['staff_costs'] + d['depreciation_amortisation'] + d['other_operating_expenses'] + (d.get('x_lease_finance_cost') or 0.0)
        mod_loss = d.get('x_modification_loss') or 0.0
        pbt = d['profit_before_tax'] - (d['total_operating_income'] - opex - d['impairment_charge'] - mod_loss)
        pat = d['profit_after_tax'] - (d['profit_before_tax'] - d['income_tax'])
        max_abs = max(abs(x) for x in [bs, as_sum, ls_sum, eq_sum, nii, toi, pbt, pat])
        res.append((p, bs, nii, toi, pbt, pat, max_abs))
    missing_src = sum(1 for r in hist_rows if r['status'] == 'reported' and (not r['source_id'] or not r['page']))
    nonblank_unavail = sum(1 for r in hist_rows if r['status'] == 'unavailable' and r['value'] != '')
    dups = len(hist_rows) - len(set((r['period'], r['statement'], r['line_item']) for r in hist_rows))
    return res, missing_src, nonblank_unavail, dups

def run():
    hist, hist_rows = load_hist()
    macro = load_macro()
    with open(ASSUMP_PATH, encoding='utf-8') as f:
        assump = json.load(f)

    years = assump['forecast_years']
    fy25 = hist['FY2025']
    q3 = hist['9M-2026']
    # CAR proxy anchored on 9M-2026 reported 18.19% CAR
    rwa_density_q3 = (q3['total_equity'] / (q3['car_pct'] / 100.0)) / q3['total_assets']

    fc_rows = []
    fc_checks = []

    for scen in ['base', 'downside', 'upside']:
        drv = assump['drivers'][scen]
        prev = dict(fy25)
        npl_prev = q3['npl_pct']

        for yr in years:
            pol = macro[(scen, yr, 'policy_rate_pct')]
            tb91 = macro[(scen, yr, 'tbill_91d_pct')]
            tb364 = macro[(scen, yr, 'tbill_364d_pct')]
            bond = macro[(scen, yr, 'govt_bond_yield_pct')]
            cpi = macro[(scen, yr, 'inflation_cpi_pct')]
            gdp = macro[(scen, yr, 'gdp_growth_pct')]
            fx_end = macro[(scen, yr, 'ghs_per_usd_end')]
            crr = macro[(scen, yr, 'crr_pct')] / 100.0
            min_car = macro[(scen, yr, 'min_car_pct')]

            # Macro-linked growth drivers for FY2027E+ (FY2026E anchored on 9M-2026 actuals + Q4)
            nom_gdp = ((1.0 + gdp / 100.0) * (1.0 + cpi / 100.0) - 1.0) * 100.0
            loan_spread = {'base': 1.0, 'downside': -2.0, 'upside': 2.5}[scen]
            dep_spread = {'base': 0.0, 'downside': -1.5, 'upside': 1.5}[scen]
            opex_spread = {'base': 2.0, 'downside': 2.5, 'upside': 1.5}[scen]

            y_inv = (0.5 * tb364 + 0.5 * bond + drv['yield_on_investments_spread_over_blend_pct']['value']) / 100.0
            y_loan = (pol + drv['yield_on_loans_spread_over_policy_pct']['value']) / 100.0
            cof = max(0.015, (tb91 + drv['cost_of_funds_spread_over_tbill91_pct']['value']) / 100.0)
            cor = drv['cost_of_risk_pct'][yr] / 100.0
            tax_r = drv['tax_rate_pct']['value'] / 100.0
            payout = drv['dividend_payout_pct']['value'] / 100.0
            target_car = drv['target_car_pct']['value']

            if yr == 'FY2026E':
                # Anchor balance sheet on 9M-2026 actuals + Q4 growth
                q4_loan_g = {'base': 0.03, 'downside': 0.01, 'upside': 0.04}[scen]
                q4_dep_g = {'base': 0.025, 'downside': 0.01, 'upside': 0.035}[scen]
                loans_net = q3['loans_and_advances_net'] * (1.0 + q4_loan_g)
                cust_dep = q3['customer_deposits'] * (1.0 + q4_dep_g)
                due_to_banks = q3['due_to_banks'] * (1.0 + q4_dep_g * 0.5)
                borrowings = q3['borrowings']
                other_liab = q3['other_liabilities'] * 1.01
                ppe_int = q3['property_equipment_intangibles'] * 1.01
                oth_assets = q3['other_assets'] * 1.01

                # Anchor income statement on 9M-2026 YTD + explicit Q4 estimate
                q4_scale = {'base': 1.0 / 3.0, 'downside': 0.28, 'upside': 0.36}[scen]
                fee_inc = q3['fee_commission_income'] * (1.0 + q4_scale)
                fee_exp = q3['fee_commission_expense'] * (1.0 + q4_scale)
                trd_inc = q3['net_trading_income'] * (1.0 + q4_scale)
                oth_inc = q3['other_operating_income'] * (1.0 + q4_scale)
                staff = q3['staff_costs'] * (1.0 + q4_scale)
                da = q3['depreciation_amortisation'] * (1.0 + q4_scale)
                oth_opex = q3['other_operating_expenses'] * (1.0 + q4_scale)
                lease_fin = q3['x_lease_finance_cost'] * (1.0 + q4_scale)
                impairment = q3['impairment_charge'] + (0.5 * (q3['loans_and_advances_net'] + loans_net)) * (cor / 4.0)
                q4_int_inc_est = (0.5 * (q3['loans_and_advances_net'] + loans_net) * y_loan + q3['investment_securities'] * y_inv) / 4.0
                q4_int_exp_est = (0.5 * (q3['customer_deposits'] + cust_dep + q3['due_to_banks'] + due_to_banks + q3['borrowings'] + borrowings) * cof) / 4.0
                int_inc = q3['interest_income'] + q4_int_inc_est
                int_exp = q3['interest_expense'] + q4_int_exp_est
                nii = int_inc - int_exp
                toi = nii + (fee_inc - fee_exp) + trd_inc + oth_inc
                pbt = toi - staff - da - oth_opex - lease_fin - impairment
                tax = q3['income_tax'] + max(0.0, (pbt - q3['profit_before_tax']) * tax_r)
                pat = pbt - tax
                # Preserve 9M-2026 actual dividend (390.288m) + 9M OCI (21.906m) already in 9M-2026 equity
                q4_pat = pat - q3['profit_after_tax']
                total_liab = cust_dep + due_to_banks + borrowings + other_liab
                stated_cap = q3['stated_capital']
                ret_earn = q3['retained_earnings'] + q4_pat
                res_other = q3['reserves_other']
                total_eq = stated_cap + ret_earn + res_other
                total_assets = total_liab + total_eq
                rem_assets = total_assets - loans_net - ppe_int - oth_assets
                cash_bog = max(cust_dep * crr, rem_assets * 0.50)
                inv_sec = rem_assets - cash_bog
            else:
                loan_g = (nom_gdp + loan_spread) / 100.0
                dep_g = (nom_gdp + dep_spread) / 100.0
                opex_g = (cpi + opex_spread) / 100.0
                fee_g = (nom_gdp) / 100.0
                trd_g = drv['trading_income_growth_pct'][yr] / 100.0

                loans_net = prev['loans_and_advances_net'] * (1.0 + loan_g)
                cust_dep = prev['customer_deposits'] * (1.0 + dep_g)
                due_to_banks = prev['due_to_banks'] * (1.0 + dep_g * 0.5)
                borrowings = prev['borrowings']
                other_liab = prev['other_liabilities'] * (1.0 + cpi / 100.0)
                total_liab = cust_dep + due_to_banks + borrowings + other_liab
                ppe_int = prev['property_equipment_intangibles'] * 1.03
                oth_assets = prev['other_assets'] * 1.02

                avg_loans = 0.5 * (prev['loans_and_advances_net'] + loans_net)
                avg_dep = 0.5 * (prev['customer_deposits'] + cust_dep + prev['due_to_banks'] + due_to_banks + prev['borrowings'] + borrowings)
                fee_inc = prev['fee_commission_income'] * (1.0 + fee_g)
                fee_exp = prev['fee_commission_expense'] * (1.0 + fee_g * 0.8)
                trd_inc = prev['net_trading_income'] * (1.0 + trd_g)
                oth_inc = prev['other_operating_income'] * 1.05
                staff = prev['staff_costs'] * (1.0 + opex_g)
                da = prev['depreciation_amortisation'] * 1.04
                oth_opex = prev['other_operating_expenses'] * (1.0 + opex_g)
                lease_fin = prev['x_lease_finance_cost'] * 1.02
                impairment = avg_loans * cor

                # Solve closing investment_securities & interest_income iteratively so int_inc uses exact avg(prev_inv, inv_sec)
                inv_sec = prev['investment_securities'] * (1.0 + dep_g * 0.8)
                for _ in range(12):
                    avg_inv = 0.5 * (prev['investment_securities'] + inv_sec)
                    int_inc = avg_loans * y_loan + avg_inv * y_inv
                    int_exp = avg_dep * cof
                    nii = int_inc - int_exp
                    toi = nii + (fee_inc - fee_exp) + trd_inc + oth_inc
                    pbt = toi - staff - da - oth_opex - lease_fin - impairment
                    tax = max(0.0, pbt * tax_r)
                    pat = pbt - tax
                    # Enforce target_car_pct dividend gate
                    div = max(0.0, pat * payout)
                    stated_cap = prev['stated_capital']
                    ret_earn = prev['retained_earnings'] + pat - div
                    res_other = prev['reserves_other']
                    total_eq = stated_cap + ret_earn + res_other
                    total_assets = total_liab + total_eq
                    car_test = (total_eq / (total_assets * rwa_density_q3)) * 100.0
                    if car_test < target_car and div > 0:
                        div = 0.0
                        ret_earn = prev['retained_earnings'] + pat
                        total_eq = stated_cap + ret_earn + res_other
                        total_assets = total_liab + total_eq
                    rem_assets = total_assets - loans_net - ppe_int - oth_assets
                    cash_bog = max(cust_dep * crr, rem_assets * 0.50)
                    inv_sec = rem_assets - cash_bog

            avg_eq = 0.5 * (prev['total_equity'] + total_eq)
            avg_as = 0.5 * (prev['total_assets'] + total_assets)
            car_pct = (total_eq / (total_assets * rwa_density_q3)) * 100.0
            npl_step = {'base': -1.0, 'downside': 1.2, 'upside': -1.5}[scen]
            npl_pct = max(5.0, min(25.0, npl_prev + npl_step))
            npl_prev = npl_pct
            ldr_pct = (loans_net / cust_dep) * 100.0
            cti_pct = ((staff + da + oth_opex + lease_fin) / toi) * 100.0
            roe_pct = (pat / avg_eq) * 100.0
            roa_pct = (pat / avg_as) * 100.0

            items = [
                ('income_statement', 'interest_income', int_inc, 'GHS millions', f'FY26E anchored on 9M-26+Q4; FY27E+ avg loans*y_loan + avg inv*y_inv (y_inv linked to macro.csv tbill_364d+bond).'),
                ('income_statement', 'interest_expense', int_exp, 'GHS millions', 'Linked to macro.csv tbill_91d_pct.'),
                ('income_statement', 'net_interest_income', nii, 'GHS millions', 'interest_income - interest_expense.'),
                ('income_statement', 'fee_commission_income', fee_inc, 'GHS millions', 'Linked to nominal GDP (gdp_growth_pct + inflation_cpi_pct from macro.csv).'),
                ('income_statement', 'fee_commission_expense', fee_exp, 'GHS millions', '0.8x fee growth.'),
                ('income_statement', 'net_trading_income', trd_inc, 'GHS millions', 'FY26E anchored on 9M-26; FY27E+ trading growth.'),
                ('income_statement', 'other_operating_income', oth_inc, 'GHS millions', 'FY26E anchored on 9M-26; FY27E+ 5% growth.'),
                ('income_statement', 'total_operating_income', toi, 'GHS millions', 'NII + net fees + trading + other operating income.'),
                ('income_statement', 'staff_costs', staff, 'GHS millions', 'Linked to inflation_cpi_pct from macro.csv.'),
                ('income_statement', 'depreciation_amortisation', da, 'GHS millions', '4% annual growth.'),
                ('income_statement', 'other_operating_expenses', oth_opex, 'GHS millions', 'Linked to inflation_cpi_pct from macro.csv.'),
                ('income_statement', 'x_lease_finance_cost', lease_fin, 'GHS millions', 'Consistent with historical separate line item.'),
                ('income_statement', 'impairment_charge', impairment, 'GHS millions', 'avg net loans * cost_of_risk.'),
                ('income_statement', 'profit_before_tax', pbt, 'GHS millions', 'total_operating_income - opex - x_lease_finance_cost - impairment.'),
                ('income_statement', 'income_tax', tax, 'GHS millions', 'profit_before_tax * tax_rate (includes levies).'),
                ('income_statement', 'profit_after_tax', pat, 'GHS millions', 'profit_before_tax - income_tax.'),
                ('balance_sheet', 'cash_and_bog_balances', cash_bog, 'GHS millions', 'Respects >= crr_pct (20%) on customer_deposits; includes due_from_banks aggregate.'),
                ('balance_sheet', 'due_from_banks', None, 'GHS millions', 'Not split from cash_and_bog_balances (same basis as historical summary statements).'),
                ('balance_sheet', 'investment_securities', inv_sec, 'GHS millions', 'Balancing liquid asset = total_assets - loans - ppe - other - cash; solved iteratively with interest_income.'),
                ('balance_sheet', 'loans_and_advances_gross', None, 'GHS millions', 'Not split in GSE summary history; net loans projected.'),
                ('balance_sheet', 'loan_loss_allowance', None, 'GHS millions', 'Not split in GSE summary history; net loans projected.'),
                ('balance_sheet', 'loans_and_advances_net', loans_net, 'GHS millions', 'FY26E anchored on 9M-26; FY27E+ linked to nominal GDP.'),
                ('balance_sheet', 'property_equipment_intangibles', ppe_int, 'GHS millions', '3% annual growth.'),
                ('balance_sheet', 'other_assets', oth_assets, 'GHS millions', '2% annual growth.'),
                ('balance_sheet', 'total_assets', total_assets, 'GHS millions', 'total_liabilities + total_equity.'),
                ('balance_sheet', 'customer_deposits', cust_dep, 'GHS millions', 'FY26E anchored on 9M-26; FY27E+ linked to nominal GDP.'),
                ('balance_sheet', 'due_to_banks', due_to_banks, 'GHS millions', '0.5 * deposit_growth.'),
                ('balance_sheet', 'borrowings', borrowings, 'GHS millions', 'Held flat.'),
                ('balance_sheet', 'other_liabilities', other_liab, 'GHS millions', 'Tracks CPI inflation.'),
                ('balance_sheet', 'total_liabilities', total_liab, 'GHS millions', 'Sum of liability items.'),
                ('balance_sheet', 'stated_capital', stated_cap, 'GHS millions', 'Held flat.'),
                ('balance_sheet', 'retained_earnings', ret_earn, 'GHS millions', 'Prior retained_earnings + PAT - dividends (9M-26 OCI/div preserved in FY26E).'),
                ('balance_sheet', 'reserves_other', res_other, 'GHS millions', 'Held flat.'),
                ('balance_sheet', 'total_equity', total_eq, 'GHS millions', 'stated_capital + retained_earnings + reserves_other.'),
                ('ratios', 'car_pct', car_pct, '%', 'Proxy only (not prudential RWA): total_equity / (total_assets * 9M-26_RWA_density).'),
                ('ratios', 'tier1_pct', None, '%', 'Not projected separately; CET1/Tier 1 unavailable in summary history.'),
                ('ratios', 'npl_pct', npl_pct, '%', 'Estimated NPL path anchored on 9M-2026 reported 14.99%.'),
                ('ratios', 'ldr_pct', ldr_pct, '%', 'loans_and_advances_net / customer_deposits * 100 (net basis).'),
                ('ratios', 'cost_to_income_pct', cti_pct, '%', '(staff + da + other_opex + x_lease_finance_cost) / total_operating_income * 100.'),
                ('ratios', 'roe_pct', roe_pct, '%', 'profit_after_tax / average total_equity * 100.'),
                ('ratios', 'roa_pct', roa_pct, '%', 'profit_after_tax / average total_assets * 100.'),
            ]
            for stmt, item, val, unit, note in items:
                status = 'unavailable' if val is None else 'estimated'
                v_str = '' if val is None else f'{val:.3f}'
                fc_rows.append(['ecobank-ghana', scen, yr, stmt, item, v_str, unit, 'MODEL-ESTIMATE', status, note])

            bs_diff = total_assets - (total_liab + total_eq)
            as_diff = total_assets - (cash_bog + inv_sec + loans_net + ppe_int + oth_assets)
            ls_diff = total_liab - (cust_dep + due_to_banks + borrowings + other_liab)
            eq_diff = total_eq - (stated_cap + ret_earn + res_other)
            nii_diff = nii - (int_inc - int_exp)
            toi_diff = toi - (nii + (fee_inc - fee_exp) + trd_inc + oth_inc)
            pbt_diff = pbt - (toi - staff - da - oth_opex - lease_fin - impairment)
            pat_diff = pat - (pbt - tax)
            max_fc_res = max(abs(x) for x in [bs_diff, as_diff, ls_diff, eq_diff, nii_diff, toi_diff, pbt_diff, pat_diff])
            crr_ok = cash_bog >= cust_dep * crr - 1e-6
            car_ok = car_pct >= min_car
            fc_checks.append((scen, yr, max_fc_res, car_pct, min_car, car_ok, crr_ok, pat, roe_pct))

            prev = {
                'loans_and_advances_net': loans_net, 'customer_deposits': cust_dep,
                'due_to_banks': due_to_banks, 'borrowings': borrowings, 'other_liabilities': other_liab,
                'investment_securities': inv_sec, 'property_equipment_intangibles': ppe_int, 'other_assets': oth_assets,
                'total_assets': total_assets, 'stated_capital': stated_cap, 'retained_earnings': ret_earn,
                'reserves_other': res_other, 'total_equity': total_eq,
                'fee_commission_income': fee_inc, 'fee_commission_expense': fee_exp,
                'net_trading_income': trd_inc, 'other_operating_income': oth_inc,
                'staff_costs': staff, 'depreciation_amortisation': da, 'other_operating_expenses': oth_opex,
                'x_lease_finance_cost': lease_fin,
            }

    with open(FORECAST_PATH, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['bank', 'scenario', 'period', 'statement', 'line_item', 'value', 'unit', 'source_id', 'status', 'notes'])
        w.writerows(fc_rows)

    hist_res, missing_src, nonblank_unavail, dups = check_historical(hist, hist_rows)
    lines = [
        '# Checks: Ecobank Ghana PLC (`ecobank-ghana`)',
        '',
        'All historical and forecast checks dynamically computed by `model.py` from `financials.csv`, `assumptions.json`, and `sector/macro-assumptions/macro.csv`.',
        '',
        '## 1. Historical Checks (recomputed from `financials.csv`)',
        '| Period | BS Residual | NII Residual | TOI Residual | PBT Residual | PAT Residual | Max Abs Residual |',
        '| --- | --- | --- | --- | --- | --- | --- |',
    ]
    for p, bs, nii, toi, pbt, pat, max_abs in hist_res:
        lines.append(f'| {p} | {bs:.3f} | {nii:.3f} | {toi:.3f} | {pbt:.3f} | {pat:.3f} | {max_abs:.3f} |')
    lines.extend([
        f'- Missing `source_id`/`page` on `reported` rows: **{missing_src}**',
        f'- Non-blank `value` on `unavailable` rows: **{nonblank_unavail}**',
        f'- Duplicate `(period, statement, line_item)` keys: **{dups}**',
        '',
        '## 2. Forecast Checks (`FY2026E–FY2030E`, recomputed)',
        '| Scenario | Year | Max Residual | Est. CAR Proxy (%) | Min CAR (%) | CAR >= Min | CRR >= 20% | Est. PAT (GHS m) | Est. ROE (%) |',
        '| --- | --- | --- | --- | --- | --- | --- | --- | --- |',
    ])
    for scen, yr, max_res, car_pct, min_car, car_ok, crr_ok, pat, roe_pct in fc_checks:
        lines.append(f'| {scen} | {yr} | {max_res:.3f} | {car_pct:.2f}% | {min_car:.2f}% | {"PASS" if car_ok else "FAIL"} | {"PASS" if crr_ok else "FAIL"} | {pat:.1f} | {roe_pct:.1f}% |')
    lines.extend([
        '',
        '## 3. Spot-checks & Caveats',
        '- `EGH25` p. 1 (Bank 2025): `total_assets` = `46,076,237` GHS \'000 (`46076.237` GHS m); `profit_after_tax` = `1,792,352` GHS \'000 (`1792.352` GHS m).',
        '- `EGH26Q3` p. 1 (Bank Sep-26): `customer_deposits` = `36,100,191` GHS \'000 (`36100.191` GHS m).',
        '- `EGH24` p. 1 (Bank 2023): `x_modification_loss` = `937,762` GHS \'000 (`937.762` GHS m).',
        '- **CRR screening caveat:** `cash_and_bog_balances` includes due-from-banks in the summary statements; exact BoG cedi CRR eligibility cannot be isolated without note disclosures.',
        '- **CAR caveat:** Forecast `car_pct` is a proxy anchored on 9M-2026 reported 18.19% CAR (`total_equity / (total_assets * RWA_density)`), not a prudential Tier 1+Tier 2 calculation.',
    ])
    with open(CHECKS_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    print(f'EGH: wrote {len(fc_rows)} forecast rows, max hist residual={max(x[6] for x in hist_res):.3f}, max fc residual={max(x[2] for x in fc_checks):.3f}')

if __name__ == '__main__':
    run()
