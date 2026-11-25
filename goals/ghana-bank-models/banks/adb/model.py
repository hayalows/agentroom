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
        as_sum = d['total_assets'] - (d['cash_and_bog_balances'] + (d.get('due_from_banks') or 0.0) + d['investment_securities'] + d['loans_and_advances_net'] + d['property_equipment_intangibles'] + d['other_assets'])
        ls_sum = d['total_liabilities'] - (d['customer_deposits'] + (d.get('due_to_banks') or 0.0) + d['borrowings'] + d['other_liabilities'])
        eq_sum = d['total_equity'] - (d['stated_capital'] + d['retained_earnings'] + d['reserves_other'])
        nii = d['net_interest_income'] - (d['interest_income'] - d['interest_expense'])
        toi = d['total_operating_income'] - (d['net_interest_income'] + (d['fee_commission_income'] - d['fee_commission_expense']) + d['net_trading_income'] + d['other_operating_income'])
        opex = d['staff_costs'] + d['depreciation_amortisation'] + d['other_operating_expenses']
        pbt = d['profit_before_tax'] - (d['total_operating_income'] - opex - d['impairment_charge'])
        pat = d['profit_after_tax'] - (d['profit_before_tax'] - d['income_tax'])
        max_abs = max(abs(x) for x in [bs, as_sum, ls_sum, eq_sum, nii, toi, pbt, pat])
        res.append((p, bs, nii, toi, pbt, pat, max_abs))
    missing_src = sum(1 for r in hist_rows if r['status'] == 'reported' and (not r['source_id'] or not r['page']))
    nonblank_unavail = sum(1 for r in hist_rows if r['status'] == 'unavailable' and r['value'] != '')
    dups = len(hist_rows) - len(set((r['period'], r['statement'], r['line_item']) for r in hist_rows))
    return res, missing_src, nonblank_unavail, dups

def run(share_override=None, write=True, plc_incl_override=None, loan_shift=0.0):
    hist, hist_rows = load_hist()
    macro = load_macro()
    with open(ASSUMP_PATH, encoding='utf-8') as f:
        assump = json.load(f)

    years = assump['forecast_years']
    fy25 = hist['FY2025']
    q3 = hist['9M-2026']
    # Regulatory-capital proxy (v2): FY2025 reported regulatory capital (note 5.7.2) rolled to 9M-2026 by the
    # change in book equity, then RWA backed out of the reported 9M-2026 CAR. Level is regulatory, not book equity.
    cap0 = fy25['x_regulatory_capital'] + (q3['total_equity'] - fy25['total_equity'])
    rwa0 = cap0 / (q3['car_pct'] / 100.0)
    rwa_density_q3 = rwa0 / q3['total_assets']
    def car_of(te, ta):
        return ((cap0 + te - q3['total_equity']) / (ta * rwa_density_q3)) * 100.0

    oc24 = fy24_cash_other = hist['FY2024']['cash_and_bog_balances'] - hist['FY2024']['x_cash_treasury_bills_under_91d'] - hist['FY2024']['x_cash_mandatory_reserve_included']
    oc25 = fy25['cash_and_bog_balances'] - fy25['x_cash_treasury_bills_under_91d'] - fy25['x_cash_mandatory_reserve_included']
    y_plc = fy25['x_interest_income_placements'] / (0.5 * (oc24 + oc25))  # FY2025 placements income over average other cash
    yields = {}
    fc_rows = []
    fc_checks = []
    cap_info = (fy25['x_regulatory_capital'], cap0, rwa0, rwa_density_q3)

    for scen in ['base', 'downside', 'upside']:
        drv = assump['drivers'][scen]
        prev = dict(fy25)
        npl_prev = q3['npl_pct']
        tiers = drv['statutory_reserve_tiers']['value']
        fund_prev = fy25['x_statutory_reserve']

        q4_loan_g = drv['q4_2026_loan_growth_pct']['value'] / 100.0
        q4_dep_g = drv['q4_2026_deposit_growth_pct']['value'] / 100.0
        q4_scale = drv['q4_2026_flow_scale']['value']
        loan_spread = drv['loan_spread_over_nom_gdp_pct']['value']
        dep_spread = drv['deposit_spread_over_nom_gdp_pct']['value']
        opex_spread = drv['opex_spread_over_cpi_pct']['value']
        npl_step = drv['npl_step_pct']['value']
        tax_r = drv['tax_rate_pct']['value'] / 100.0
        payout = drv['dividend_payout_pct']['value'] / 100.0
        target_car = drv['target_car_pct']['value']
        sb_share = drv['short_bill_share_of_noncash_reserve_cash']['value'] if share_override is None else share_override
        other_share = 1.0 - drv['short_bill_share_of_noncash_reserve_cash']['value']
        plc_incl = drv['placements_inclusion']['value'] if plc_incl_override is None else plc_incl_override

        for yr in years:
            pol = macro[(scen, yr, 'policy_rate_pct')]
            tb91 = macro[(scen, yr, 'tbill_91d_pct')]
            tb364 = macro[(scen, yr, 'tbill_364d_pct')]
            bond = macro[(scen, yr, 'govt_bond_yield_pct')]
            cpi = macro[(scen, yr, 'inflation_cpi_pct')]
            gdp = macro[(scen, yr, 'gdp_growth_pct')]
            crr = macro[(scen, yr, 'crr_pct')] / 100.0
            min_car = macro[(scen, yr, 'min_car_pct')]

            nom_gdp = ((1.0 + gdp / 100.0) * (1.0 + cpi / 100.0) - 1.0) * 100.0
            y_inv = (0.5 * tb364 + 0.5 * bond + drv['yield_on_investments_spread_over_blend_pct']['value']) / 100.0
            y_loan = (pol + drv['yield_on_loans_spread_over_policy_pct']['value'] + loan_shift) / 100.0
            cof = max(0.02, (tb91 + drv['cost_of_funds_spread_over_tbill91_pct']['value']) / 100.0)
            cor = drv['cost_of_risk_pct'][yr] / 100.0

            if yr == 'FY2026E':
                loans_net = q3['loans_and_advances_net'] * (1.0 + q4_loan_g)
                cust_dep = q3['customer_deposits'] * (1.0 + q4_dep_g)
                borrowings = q3['borrowings']
                other_liab = q3['other_liabilities'] * 1.01
                total_liab = cust_dep + borrowings + other_liab
                ppe_int = q3['property_equipment_intangibles'] * 1.01
                oth_assets = q3['other_assets'] * 1.01

                fee_inc = q3['fee_commission_income'] * (1.0 + q4_scale)
                fee_exp = q3['fee_commission_expense'] * (1.0 + q4_scale)
                trd_inc = q3['net_trading_income'] * (1.0 + q4_scale)
                oth_inc = q3['other_operating_income'] * (1.0 + q4_scale)
                staff = q3['staff_costs'] * (1.0 + q4_scale)
                da = q3['depreciation_amortisation'] * (1.0 + q4_scale)
                oth_opex = q3['other_operating_expenses'] * (1.0 + q4_scale)
                impairment = q3['impairment_charge'] + (0.5 * (q3['loans_and_advances_net'] + loans_net)) * (cor / 4.0)

                inv_sec = q3['investment_securities']
                cash_bog = q3['cash_and_bog_balances']
                iter_diff = 0.0
                for _ in range(15):
                    inv_prev = inv_sec
                    nc_avg = max(0.0, 0.5 * ((q3['cash_and_bog_balances'] - crr * q3['customer_deposits']) + (cash_bog - crr * cust_dep)))
                    cash_inc = sb_share * nc_avg * (tb91 / 100.0) / 4.0
                    plc_inc = plc_incl * other_share * nc_avg * y_plc / 4.0
                    q4_int_inc = (0.5 * (q3['loans_and_advances_net'] + loans_net) * y_loan + 0.5 * (q3['investment_securities'] + inv_sec) * y_inv) / 4.0 + cash_inc + plc_inc
                    q4_int_exp = (0.5 * (q3['customer_deposits'] + cust_dep + q3['borrowings'] + borrowings) * cof) / 4.0
                    int_inc = q3['interest_income'] + q4_int_inc
                    int_exp = q3['interest_expense'] + q4_int_exp
                    nii = int_inc - int_exp
                    toi = nii + (fee_inc - fee_exp) + trd_inc + oth_inc
                    pbt = toi - staff - da - oth_opex - impairment
                    tax = q3['income_tax'] + max(0.0, (pbt - q3['profit_before_tax']) * tax_r)
                    pat = pbt - tax
                    q4_pat = pat - q3['profit_after_tax']
                    stated_cap = q3['stated_capital']
                    ret_earn = q3['retained_earnings'] + q4_pat
                    res_other = q3['reserves_other']
                    total_eq = stated_cap + ret_earn + res_other
                    total_assets = total_liab + total_eq
                    rem_assets = total_assets - loans_net - ppe_int - oth_assets
                    cash_bog = max(cust_dep * crr, rem_assets * 0.60)
                    inv_sec = rem_assets - cash_bog
                    iter_diff = abs(inv_sec - inv_prev)
            else:
                loan_g = (nom_gdp + loan_spread) / 100.0
                dep_g = (nom_gdp + dep_spread) / 100.0
                opex_g = (cpi + opex_spread) / 100.0
                fee_g = nom_gdp / 100.0
                trd_g = drv['trading_income_growth_pct'][yr] / 100.0

                loans_net = prev['loans_and_advances_net'] * (1.0 + loan_g)
                cust_dep = prev['customer_deposits'] * (1.0 + dep_g)
                borrowings = prev['borrowings']
                other_liab = prev['other_liabilities'] * (1.0 + cpi / 100.0)
                total_liab = cust_dep + borrowings + other_liab
                ppe_int = prev['property_equipment_intangibles'] * 1.02
                oth_assets = prev['other_assets'] * 1.02

                avg_loans = 0.5 * (prev['loans_and_advances_net'] + loans_net)
                avg_dep = 0.5 * (prev['customer_deposits'] + cust_dep + prev['borrowings'] + borrowings)
                fee_inc = prev['fee_commission_income'] * (1.0 + fee_g)
                fee_exp = prev['fee_commission_expense'] * (1.0 + fee_g * 0.8)
                trd_inc = prev['net_trading_income'] * (1.0 + trd_g)
                oth_inc = prev['other_operating_income'] * 1.03
                staff = prev['staff_costs'] * (1.0 + opex_g)
                da = prev['depreciation_amortisation'] * 1.03
                oth_opex = prev['other_operating_expenses'] * (1.0 + opex_g)
                impairment = avg_loans * cor

                inv_sec = prev['investment_securities'] * (1.0 + dep_g * 0.8)
                cash_bog = prev['cash_and_bog_balances']
                iter_diff = 0.0
                for _ in range(15):
                    inv_prev = inv_sec
                    avg_inv = 0.5 * (prev['investment_securities'] + inv_sec)
                    nc_avg = max(0.0, 0.5 * ((prev['cash_and_bog_balances'] - crr * prev['customer_deposits']) + (cash_bog - crr * cust_dep)))
                    cash_inc = sb_share * nc_avg * (tb91 / 100.0)
                    plc_inc = plc_incl * other_share * nc_avg * y_plc
                    int_inc = avg_loans * y_loan + avg_inv * y_inv + cash_inc + plc_inc
                    int_exp = avg_dep * cof
                    nii = int_inc - int_exp
                    toi = nii + (fee_inc - fee_exp) + trd_inc + oth_inc
                    pbt = toi - staff - da - oth_opex - impairment
                    tax = max(0.0, pbt * tax_r)
                    pat = pbt - tax
                    div = max(0.0, pat * payout) if (prev['retained_earnings'] + pat > 0) else 0.0
                    stated_cap = prev['stated_capital']
                    ret_earn = prev['retained_earnings'] + pat - div
                    res_other = prev['reserves_other']
                    total_eq = stated_cap + ret_earn + res_other
                    total_assets = total_liab + total_eq
                    car_test = car_of(total_eq, total_assets)
                    if car_test < target_car and div > 0:
                        ret_earn = prev['retained_earnings'] + pat
                        total_eq = stated_cap + ret_earn + res_other
                        total_assets = total_liab + total_eq
                    rem_assets = total_assets - loans_net - ppe_int - oth_assets
                    cash_bog = max(cust_dep * crr, rem_assets * 0.60)
                    inv_sec = rem_assets - cash_bog
                    iter_diff = abs(inv_sec - inv_prev)

            band = next(pct for lim, pct in tiers if (fund_prev / q3['stated_capital'] * 100.0) < lim)
            xfer_year = band / 100.0 * max(0.0, pat)
            if yr == 'FY2026E':
                stat_xfer = max(0.0, xfer_year - q3['x_statutory_transfer'])
                stat_fund = q3['x_statutory_reserve'] + stat_xfer
            else:
                stat_xfer = xfer_year
                stat_fund = fund_prev + stat_xfer
            fund_prev = stat_fund
            ret_earn -= stat_xfer
            res_other += stat_xfer
            avg_eq = 0.5 * (prev['total_equity'] + total_eq)
            avg_as = 0.5 * (prev['total_assets'] + total_assets)
            car_pct = car_of(total_eq, total_assets)
            npl_pct = max(10.0, npl_prev + npl_step)
            npl_prev = npl_pct
            net_ldr = (loans_net / cust_dep) * 100.0
            if scen == 'base' and yr == 'FY2027E':
                yields.update(y_loan=y_loan * 100.0, y_inv=y_inv * 100.0, tb91=tb91, y_plc=y_plc * 100.0, loan_share=1.0)
            cti_pct = ((staff + da + oth_opex) / toi) * 100.0
            roe_pct = None if avg_eq <= 0 else (pat / avg_eq) * 100.0
            roa_pct = (pat / avg_as) * 100.0

            items = [
                ('income_statement', 'interest_income', int_inc, 'GHS millions', 'FY26E = 9M-26 + iterative Q4; FY27E+ = avg loans*y_loan + avg inv*y_inv + short-bill income on non-reserve cash (macro.csv).'),
                ('income_statement', 'x_interest_on_placements_other_cash', plc_inc, 'GHS millions', 'Memo, included in interest_income: placements_inclusion x other (non-bill) non-reserve cash x FY2025 placements yield over average other cash. FY2026E is the Q4 piece only.'),
                ('income_statement', 'x_interest_on_cash_short_bills', cash_inc, 'GHS millions', 'Memo, included in interest_income: short_bill_share x non-reserve cash x 91-day bill rate. FY2026E is the Q4 piece only (9M actual already contains its own).'),
                ('income_statement', 'interest_expense', int_exp, 'GHS millions', 'Linked to macro.csv tbill_91d_pct.'),
                ('income_statement', 'net_interest_income', nii, 'GHS millions', 'interest_income - interest_expense.'),
                ('income_statement', 'fee_commission_income', fee_inc, 'GHS millions', 'Linked to nominal GDP (macro.csv).'),
                ('income_statement', 'fee_commission_expense', fee_exp, 'GHS millions', '0.8x fee growth.'),
                ('income_statement', 'net_trading_income', trd_inc, 'GHS millions', 'FY26E anchored on 9M-26; FY27E+ trading growth.'),
                ('income_statement', 'other_operating_income', oth_inc, 'GHS millions', 'FY26E anchored on 9M-26; FY27E+ 3% growth.'),
                ('income_statement', 'total_operating_income', toi, 'GHS millions', 'NII + net fees + trading + other operating income.'),
                ('income_statement', 'staff_costs', staff, 'GHS millions', 'Linked to inflation_cpi_pct (macro.csv).'),
                ('income_statement', 'depreciation_amortisation', da, 'GHS millions', '3% annual growth.'),
                ('income_statement', 'other_operating_expenses', oth_opex, 'GHS millions', 'Linked to inflation_cpi_pct (macro.csv).'),
                ('income_statement', 'impairment_charge', impairment, 'GHS millions', 'avg net loans * cost_of_risk (independent of NPL path).'),
                ('income_statement', 'profit_before_tax', pbt, 'GHS millions', 'total_operating_income - opex - impairment.'),
                ('income_statement', 'income_tax', tax, 'GHS millions', 'profit_before_tax * tax_rate.'),
                ('income_statement', 'profit_after_tax', pat, 'GHS millions', 'profit_before_tax - income_tax.'),
                ('balance_sheet', 'cash_and_bog_balances', cash_bog, 'GHS millions', 'Proxy screen >= crr_pct (20%) on customer_deposits; includes due_from_banks aggregate. Non-reserve part earns short_bill_share x 91-day bill rate (v2).'),
                ('balance_sheet', 'due_from_banks', None, 'GHS millions', 'Combined with cash_and_bog_balances (same basis as FY23-9M26).'),
                ('balance_sheet', 'investment_securities', inv_sec, 'GHS millions', 'Balancing liquid asset; solved iteratively with interest_income.'),
                ('balance_sheet', 'loans_and_advances_gross', None, 'GHS millions', 'Not disclosed in GSE summary statements.'),
                ('balance_sheet', 'loan_loss_allowance', None, 'GHS millions', 'Not disclosed in GSE summary statements.'),
                ('balance_sheet', 'loans_and_advances_net', loans_net, 'GHS millions', 'FY26E anchored on 9M-26; FY27E+ linked to nominal GDP.'),
                ('balance_sheet', 'property_equipment_intangibles', ppe_int, 'GHS millions', '2% annual growth.'),
                ('balance_sheet', 'other_assets', oth_assets, 'GHS millions', '2% annual growth.'),
                ('balance_sheet', 'total_assets', total_assets, 'GHS millions', 'total_liabilities + total_equity.'),
                ('balance_sheet', 'customer_deposits', cust_dep, 'GHS millions', 'FY26E anchored on 9M-26; FY27E+ linked to nominal GDP.'),
                ('balance_sheet', 'due_to_banks', None, 'GHS millions', 'Not separately reported.'),
                ('balance_sheet', 'borrowings', borrowings, 'GHS millions', 'Held flat.'),
                ('balance_sheet', 'other_liabilities', other_liab, 'GHS millions', 'Tracks CPI inflation.'),
                ('balance_sheet', 'total_liabilities', total_liab, 'GHS millions', 'Sum of liability items.'),
                ('balance_sheet', 'stated_capital', stated_cap, 'GHS millions', 'Held flat (no automatic capital injection assumed).'),
                ('balance_sheet', 'retained_earnings', ret_earn, 'GHS millions', 'Prior retained_earnings + PAT - dividends - statutory transfer.'),
                ('balance_sheet', 'x_statutory_reserve', stat_fund, 'GHS millions', 'Memo, a component of reserves_other: opening fund + transfer. FY2026E = reported 9M-2026 fund + Q4 top-up.'),
                ('balance_sheet', 'x_statutory_transfer', stat_xfer, 'GHS millions', 'Memo, moves from retained_earnings to reserves_other (total equity unchanged): tier % x positive PAT (FY2026E: full-year transfer less 150.857 already transferred in 9M, floor 0). Tier from opening fund / stated capital.'),
                ('balance_sheet', 'reserves_other', res_other, 'GHS millions', 'Prior reserves_other + statutory transfer (x_statutory_transfer).'),
                ('balance_sheet', 'total_equity', total_eq, 'GHS millions', 'stated_capital + retained_earnings + reserves_other.'),
                ('ratios', 'car_pct', car_pct, '%', 'v2 proxy: (FY2025 regulatory capital + change in book equity since FY2025) / (total assets x RWA density), anchored on reported 9M-2026 CAR 27.41%; no capital injection assumed.'),
                ('ratios', 'tier1_pct', None, '%', 'Not projected separately.'),
                ('ratios', 'npl_pct', npl_pct, '%', 'Estimated recovery path from 66.32% in 9M-2026.'),
                ('ratios', 'ldr_pct', None, '%', 'Canonical gross LDR unavailable in the forecast (gross loans are not modelled). Net basis is in x_net_ldr_pct.'),
                ('ratios', 'x_net_ldr_pct', net_ldr, '%', 'loans_and_advances_net / customer_deposits * 100 (net basis).'),
                ('ratios', 'cost_to_income_pct', cti_pct, '%', 'opex / total_operating_income * 100.'),
                ('ratios', 'roe_pct', roe_pct, '%', 'profit_after_tax / average total_equity * 100 (blank when avg_eq <= 0).'),
                ('ratios', 'roa_pct', roa_pct, '%', 'profit_after_tax / average total_assets * 100.'),
            ]
            for stmt, item, val, unit, note in items:
                status = 'unavailable' if val is None else 'estimated'
                v_str = '' if val is None else f'{val:.3f}'
                fc_rows.append(['adb', scen, yr, stmt, item, v_str, unit, 'MODEL-ESTIMATE', status, note])

            bs_diff = total_assets - (total_liab + total_eq)
            as_diff = total_assets - (cash_bog + inv_sec + loans_net + ppe_int + oth_assets)
            ls_diff = total_liab - (cust_dep + borrowings + other_liab)
            eq_diff = total_eq - (stated_cap + ret_earn + res_other)
            nii_diff = nii - (int_inc - int_exp)
            toi_diff = toi - (nii + (fee_inc - fee_exp) + trd_inc + oth_inc)
            pbt_diff = pbt - (toi - staff - da - oth_opex - impairment)
            pat_diff = pat - (pbt - tax)
            max_fc_res = max(abs(x) for x in [bs_diff, as_diff, ls_diff, eq_diff, nii_diff, toi_diff, pbt_diff, pat_diff])
            inv_ok = inv_sec >= 0.0
            car_ok = car_pct >= min_car
            fc_checks.append((scen, yr, max_fc_res, iter_diff, inv_ok, car_pct, min_car, car_ok, pat, roe_pct, total_eq, total_assets))

            prev = {
                'loans_and_advances_net': loans_net, 'customer_deposits': cust_dep,
                'borrowings': borrowings, 'other_liabilities': other_liab,
                'cash_and_bog_balances': cash_bog, 'investment_securities': inv_sec, 'property_equipment_intangibles': ppe_int, 'other_assets': oth_assets,
                'total_assets': total_assets, 'stated_capital': stated_cap, 'retained_earnings': ret_earn,
                'reserves_other': res_other, 'total_equity': total_eq,
                'fee_commission_income': fee_inc, 'fee_commission_expense': fee_exp,
                'net_trading_income': trd_inc, 'other_operating_income': oth_inc,
                'staff_costs': staff, 'depreciation_amortisation': da, 'other_operating_expenses': oth_opex,
            }

    if not write:
        return fc_checks

    with open(FORECAST_PATH, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['bank', 'scenario', 'period', 'statement', 'line_item', 'value', 'unit', 'source_id', 'status', 'notes'])
        w.writerows(fc_rows)

    hist_res, missing_src, nonblank_unavail, dups = check_historical(hist, hist_rows)
    # v2 source-bridge checks (FY2024, FY2025) and short-bill sensitivity
    bridge = []
    for p in ['FY2024', 'FY2025']:
        d = hist[p]
        bridge.append((p, 'gross loans - allowance - net loans', d['loans_and_advances_gross'] - d['loan_loss_allowance'] - d['loans_and_advances_net']))
        bridge.append((p, 'note 8 components - interest_income', d['x_interest_income_loans'] + d['x_interest_income_govt_securities'] + d['x_interest_income_placements'] - d['interest_income']))
        bridge.append((p, 'regulatory capital - CET1 - tier 2', d['x_regulatory_capital'] - d['x_cet1_capital'] - d['x_tier2_capital']))
        bridge.append((p, 'cash - short bills - mandatory reserve (must be >= 0)', d['cash_and_bog_balances'] - d['x_cash_treasury_bills_under_91d'] - d['x_cash_mandatory_reserve_included']))
    rou_rows = [(p, hist[p]['x_right_of_use_assets'], hist[p]['property_equipment_intangibles']) for p in ['FY2021', 'FY2022', 'FY2023', 'FY2024', 'FY2025', '9M-2026']]
    sens = {s: run(s, False) for s in (0.0, 0.27)}
    sens[None] = fc_checks
    def pick(rows, scen, yr):
        return next(r for r in rows if r[0] == scen and r[1] == yr)
    lines = [
        '# Checks: Agricultural Development Bank PLC (`adb`)',
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
        f'- Note: `9M-2026` PAT residual of `0.001` GHS m reflects 1-thousand rounding in `ADB26Q3` (`478,525 - 176,812 = 301,713` vs. reported `301,714`).',
        f'- Missing `source_id`/`page` on `reported` rows: **{missing_src}**',
        f'- Non-blank `value` on `unavailable` rows: **{nonblank_unavail}**',
        f'- Duplicate `(period, statement, line_item)` keys: **{dups}**',
        '',
        '## 2. Forecast Checks (`FY2026E–FY2030E`, recomputed)',
        '| Scenario | Year | Max Residual | Iter Conv Residual | Inv Sec >= 0 | Est. CAR Proxy (%) | Min CAR (%) | CAR >= Min | Est. PAT (GHS m) | Est. ROE (%) |',
        '| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |',
    ])
    for scen, yr, max_res, iter_diff, inv_ok, car_pct, min_car, car_ok, pat, roe_pct, _te, _ta in fc_checks:
        roe_str = 'N/A (avg_eq<=0)' if roe_pct is None else f'{roe_pct:.1f}%'
        lines.append(f'| {scen} | {yr} | {max_res:.3f} | {iter_diff:.6f} | {"PASS" if inv_ok else "FAIL"} | {car_pct:.2f}% | {min_car:.2f}% | {"PASS" if car_ok else "FAIL"} | {pat:.1f} | {roe_str} |')
    lines.extend([
        '',
        '## 3. Source bridges and short-bill sensitivity (v2)',
        '| Period | Bridge | Residual (GHS m) |',
        '| --- | --- | --- |',
    ])
    for p, label, v in bridge:
        lines.append(f'| {p} | {label} | {v:.3f} |')
    lines.append(f'- Capital proxy anchors: FY2025 reported regulatory capital {cap_info[0]:.3f}; rolled to 9M-2026 by the change in book equity = {cap_info[1]:.3f}; implied RWA = {cap_info[2]:.3f}; RWA / total assets = {cap_info[3]*100:.2f}%. Reported FY2025 RWA / total assets = {hist["FY2025"]["x_risk_weighted_assets"]/hist["FY2025"]["total_assets"]*100:.2f}%.')
    lines.append('- Right-of-use assets are inside `property_equipment_intangibles` once (never in `other_assets`): ' + '; '.join(f'{p} {r:.3f} of {pp:.3f}' for p, r, pp in rou_rows) + '. `ROU <= PPE` holds in every period: ' + ('PASS' if all(r <= pp for _, r, pp in rou_rows) else 'FAIL') + '.')
    lines.append('')
    lines.append('Short-bill share of non-reserve cash (driver `short_bill_share_of_noncash_reserve_cash`; FY2025 observed 54.0% = 3561.795 / (9902.445 - 3306.666)). Model value 54.0%; 0% removes only the short-bill line (placements income, ROU and the capital proxy stay as in the model).')
    lines.append('| Share | Scenario | FY2026E PAT | FY2027E PAT | FY2030E PAT | FY2030E CAR proxy |')
    lines.append('| --- | --- | --- | --- | --- | --- |')
    for s, label in ((0.0, '0%'), (0.27, '27%'), (None, '54% (model)')):
        for scen in ('base', 'downside', 'upside'):
            a, b, c = pick(sens[s], scen, 'FY2026E'), pick(sens[s], scen, 'FY2027E'), pick(sens[s], scen, 'FY2030E')
            lines.append(f'| {label} | {scen} | {a[8]:.1f} | {b[8]:.1f} | {c[8]:.1f} | {c[5]:.2f}% |')
    # --- v2 round 2: component yields, earning-base sensitivities, capital stress, statutory memo
    h24, h25 = hist['FY2024'], hist['FY2025']
    avg_net = 0.5 * (h24['loans_and_advances_net'] + h25['loans_and_advances_net'])
    avg_gross = 0.5 * (h24['loans_and_advances_gross'] + h25['loans_and_advances_gross'])
    sec24 = h24['investment_securities'] + h24['x_cash_treasury_bills_under_91d']
    sec25 = h25['investment_securities'] + h25['x_cash_treasury_bills_under_91d']
    lines.extend([
        '',
        'Component yield table. FY2025 observed (note 8 / balance sheet) against the base FY2027E model rate. This is a calibration comparison, not a back-test of the engine, because FY2025 macro inputs are not in `macro.csv`.',
        '| Component | FY2025 observed | Basis | Base FY2027E model |',
        '| --- | --- | --- | --- |',
        f'| Loan interest / average loans | {h25["x_interest_income_loans"]/avg_net*100:.2f}% | net loans (model basis) | {yields["y_loan"]:.2f}% policy rate + spread |',
        f'| Loan interest / average loans | {h25["x_interest_income_loans"]/avg_gross*100:.2f}% | gross loans (not modelled) | n/a |',
        f'| Government securities interest / average (investment securities + short bills) | {h25["x_interest_income_govt_securities"]/(0.5*(sec24+sec25))*100:.2f}% | note 8 against balances | {yields["y_inv"]:.2f}% blend, plus {yields["tb91"]:.2f}% 91-day bill on the short-bill share of cash |',
        f'| Placements interest / average other (non-bill, non-reserve) cash | {y_plc*100:.2f}% | cash less short bills less mandatory reserve | {yields["y_plc"]:.2f}% held constant |',
        f'| Mandatory reserve / customer deposits | {h25["x_cash_mandatory_reserve_included"]/h25["customer_deposits"]*100:.2f}% | note 18 | 20% CRR proxy (macro.csv); the reserve is an eligibility proxy only |',
        '',
        'Earning-base sensitivities (base scenario; each row changes one driver, the others stay at model values).',
        '| Driver | Setting | FY2026E PAT | FY2027E PAT | FY2030E PAT | FY2030E CAR proxy |',
        '| --- | --- | --- | --- | --- | --- |',
    ])
    for label, kw in (('placements inclusion', dict(plc_incl_override=0.0)), ('placements inclusion', dict(plc_incl_override=0.5)), ('placements inclusion', None), ('loan yield spread', dict(loan_shift=-2.0)), ('loan yield spread', dict(loan_shift=2.0))):
        rr = fc_checks if kw is None else run(write=False, **kw)
        setting = '100% (model)' if kw is None else (f"{kw['plc_incl_override']*100:.0f}%" if 'plc_incl_override' in kw else f"{kw['loan_shift']:+.0f} pp")
        a_, b_, c_ = pick(rr, 'base', 'FY2026E'), pick(rr, 'base', 'FY2027E'), pick(rr, 'base', 'FY2030E')
        lines.append(f'| {label} | {setting} | {a_[8]:.1f} | {b_[8]:.1f} | {c_[8]:.1f} | {c_[5]:.2f}% |')
    d_v1 = (q3['total_equity'] / (q3['car_pct'] / 100.0)) / q3['total_assets']
    lines.extend([
        '',
        'Capital stress (static, FY2030E; absolute gap = capital needed to reach the minimum CAR less capital held, GHS m). Illustrative: no interim regulatory numerator or RWA is published, so these show how far the proxy depends on the numerator and the RWA density.',
        '| Scenario | Basis | Numerator | RWA density | CAR | Gap to min CAR |',
        '| --- | --- | --- | --- | --- | --- |',
    ])
    for scen in ('base', 'downside', 'upside'):
        r_ = pick(fc_checks, scen, 'FY2030E')
        te_, ta_, mc_ = r_[10], r_[11], r_[6]
        num_reg = cap0 + te_ - q3['total_equity']
        for lab, num, dens in (('model proxy (regulatory numerator)', num_reg, rwa_density_q3), ('book equity numerator, version 1 density', te_, d_v1), ('regulatory numerator, 38% density', num_reg, 0.38), ('regulatory numerator, 48% density', num_reg, 0.48)):
            rwa_ = ta_ * dens
            lines.append(f'| {scen} | {lab} | {num:.1f} | {dens*100:.2f}% | {num/rwa_*100:.2f}% | {max(0.0, mc_/100.0*rwa_ - num):.1f} |')
    lines.extend([
        '',
        'A negative CAR that becomes less negative at a higher density is not an improvement in capital: compare the absolute gaps.',
        '',
        'Statutory reserve memo (forecast rows `x_statutory_reserve`, `x_statutory_transfer`): the 9M-2026 fund (534.049m) and year-to-date transfer (150.857m, 50.0% of PAT) are reported; the three Act 930 s34 bands (50% / 25% / 12.5%, as re-read by Codex) are in `assumptions.json` and the steward did not read the Act. Transfers move amounts between reserves and retained earnings, so total equity and CAR are unaffected. Year-by-year amounts are in `forecast.csv`; the table shows the transfer tier amounts for positive-profit years.',
        '| Scenario | Year | PAT | 12.5% | 25% | 50% |',
        '| --- | --- | --- | --- | --- | --- |',
    ])
    for scen in ('base', 'downside', 'upside'):
        for r_ in fc_checks:
            if r_[0] == scen and r_[8] > 0:
                lines.append(f'| {scen} | {r_[1]} | {r_[8]:.1f} | {r_[8]*0.125:.1f} | {r_[8]*0.25:.1f} | {r_[8]*0.5:.1f} |')
    lines.extend([
        '',
        '## 4. Spot-checks & Caveats',
        '- `ADB25` p. 1: `total_assets` = `17,887,521` GHS \'000 (`17887.521` GHS m); `profit_after_tax` = `367,291` GHS \'000 (`367.291` GHS m).',
        '- `ADB26Q3` p. 1–2: `customer_deposits` = `15,362,718` GHS \'000 (`15362.718` GHS m); `profit_after_tax` = `301,714` GHS \'000 (`301.714` GHS m).',
        '- **CRR proxy caveat:** `cash_and_bog_balances` includes `due_from_banks` in FY2023–9M-2026 summary statements; `cash_bog >= 20% * customer_deposits` is a liquidity proxy screen, not regulatory BoG cedi CRR compliance.',
        '- **CAR & solvency caveat:** Forecast `car_pct` is a proxy: FY2025 reported regulatory capital (note 5.7.2) rolled forward by the change in book equity, over total assets x RWA density backed out of the reported `9M-2026` `27.41%` CAR, with no automatic capital injection assumed. Where `car_pct < 13%` (flagged `FAIL`), that reflects the proxy under stressed/normalizing yields rather than a demonstrated regulatory breach.',
    ])
    with open(CHECKS_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    print(f'ADB: wrote {len(fc_rows)} forecast rows, max hist={max(x[6] for x in hist_res):.3f}, max fc={max(x[2] for x in fc_checks):.3f}, max iter={max(x[3] for x in fc_checks):.6f}')

if __name__ == '__main__':
    run()
