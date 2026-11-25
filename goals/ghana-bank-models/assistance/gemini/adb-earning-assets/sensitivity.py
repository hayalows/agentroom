"""Isolated ADB short-bill income sensitivity; never writes to canonical model files.
Run: python sensitivity.py /path/to/goals/ghana-bank-models
Requires unchanged owner model with the explicit expressions below.
"""
import csv, hashlib, pathlib, shutil, subprocess, sys, tempfile

root=pathlib.Path(sys.argv[1]).resolve()
bank=root/"banks"/"adb"
macro=root/"sector"/"macro-assumptions"/"macro.csv"
share=3561.795/(9902.445-3306.666)
def rows(p):
    with p.open(encoding="utf-8-sig",newline="") as f:
        return {(r["scenario"],r["period"],r["line_item"]):r["value"] for r in csv.DictReader(f)}
source=(bank/"model.py").read_text()
canonical=rows(bank/"forecast.csv")
print("Owner model SHA256",hashlib.sha256((bank/"model.py").read_bytes()).hexdigest())
print("Macro SHA256",hashlib.sha256(macro.read_bytes()).hexdigest())
print("2025 short bills / non-mandatory-reserve cash",share)
print("variant,scenario,year,interest_income,net_interest_income,profit_after_tax,total_equity,car_pct,cash_and_bog_balances,max_identity_residual")
for weight in (0,.5,1):
    with tempfile.TemporaryDirectory() as td:
        target=pathlib.Path(td)/"banks"/"adb"
        shutil.copytree(bank,target)
        mtarget=pathlib.Path(td)/"sector"/"macro-assumptions"/"macro.csv"
        mtarget.parent.mkdir(parents=True)
        shutil.copy2(macro,mtarget)
        code=source
        def replace(old,new):
            global code
            if code.count(old)!=1: raise ValueError("Owner code changed: "+old)
            code=code.replace(old,new)
        if weight:
            replace("                inv_sec = q3['investment_securities']\n",
                    "                inv_sec = q3['investment_securities']\n                cash_bog = q3['cash_and_bog_balances']\n")
            replace("                    q4_int_exp =",
                    f"                    q4_int_inc += {share*weight!r} * 0.5 * (max(0,q3['cash_and_bog_balances']-crr*q3['customer_deposits']) + max(0,cash_bog-crr*cust_dep)) * (tb91/100.0) / 4.0\n                    q4_int_exp =")
            replace("                inv_sec = prev['investment_securities'] * (1.0 + dep_g * 0.8)\n",
                    "                inv_sec = prev['investment_securities'] * (1.0 + dep_g * 0.8)\n                cash_bog = prev['cash_and_bog_balances']\n")
            replace("                    int_inc = avg_loans * y_loan + avg_inv * y_inv",
                    f"                    int_inc = avg_loans * y_loan + avg_inv * y_inv + {share*weight!r} * 0.5 * (max(0,prev['cash_and_bog_balances']-crr*prev['customer_deposits']) + max(0,cash_bog-crr*cust_dep)) * (tb91/100.0)")
            replace("                'total_assets': total_assets, 'stated_capital': stated_cap,",
                    "                'total_assets': total_assets, 'cash_and_bog_balances': cash_bog, 'stated_capital': stated_cap,")
        (target/"model.py").write_text(code,encoding="utf-8")
        run=subprocess.run([sys.executable,"-I",str(target/"model.py")],capture_output=True,text=True,check=True)
        result=rows(target/"forecast.csv")
        if not weight:
            assert result==canonical, "Zero-weight replay differs from canonical forecast"
        assert len(result)==600
        for s in ("base","downside","upside"):
            for y in ("FY2026E","FY2027E","FY2028E","FY2029E","FY2030E"):
                def v(k): return float(result[s,y,k])
                resid=max(abs(v("total_assets")-v("total_liabilities")-v("total_equity")),
                    abs(v("total_assets")-sum(v(k) for k in ("cash_and_bog_balances","investment_securities","loans_and_advances_net","property_equipment_intangibles","other_assets"))),
                    abs(v("net_interest_income")-v("interest_income")+v("interest_expense")),
                    abs(v("profit_after_tax")-v("profit_before_tax")+v("income_tax")))
                assert resid<=.004, (weight,s,y,resid)
                if y in ("FY2026E","FY2027E","FY2030E"):
                    print(",".join(map(str,[weight,s,y,*[v(k) for k in ("interest_income","net_interest_income","profit_after_tax","total_equity","car_pct","cash_and_bog_balances")],round(resid,6)])))
print("PASS: exact baseline replay; 45 scenario-year balance/earnings checks.")
