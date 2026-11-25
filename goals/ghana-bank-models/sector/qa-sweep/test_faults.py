# Fault tests for QA v1.2, on copied bank data only.
import csv,importlib.util,sys,tempfile,shutil
from pathlib import Path
root=Path(sys.argv[1]);validator=Path(sys.argv[2])
spec=importlib.util.spec_from_file_location("qa",validator);qa=importlib.util.module_from_spec(spec);spec.loader.exec_module(qa)
goal=root/'goals/ghana-bank-models';slug='zenith-bank-ghana'
assert qa.num('NaN') is None and qa.num('Infinity') is None and qa.num('-inf') is None and qa.num('0')==0
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:
        r=csv.DictReader(f);return r.fieldnames,list(r)
def write(p,h,rows):
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=h,extrasaction='ignore');w.writeheader();w.writerows(rows)
with tempfile.TemporaryDirectory(prefix='qa-support-faults-') as t:
    t=Path(t);b=t/'banks'/slug;b.parent.mkdir();shutil.copytree(goal/'banks'/slug,b)
    c=t/'claims';c.mkdir()
    qa.BANKS=str(b.parent);qa.CLAIMS=str(c)
    (c/(slug+'.md')).write_text('agent: original\nstatus: released\n')
    (c/(slug+'-takeover.md')).write_text('agent: replacement\nstatus: needs-review\n')
    assert qa.claim_status(slug)==('replacement','needs-review')
    h,rows=read(b/'forecast.csv');hh,history=read(b/'financials.csv')
    def find(sc,y,item):return next(x for x in rows if x['scenario']==sc and x['period']==y and x['line_item']==item)
    original=qa.check_bank(slug);assert not original['fail'],original
    # Duplicate, bogus key, later PAT corruption, invalid status, invalid value,
    # unavailable numeric, wrong bank, only one scenario-year deliberately removed.
    d=[dict(x) for x in rows];d.insert(1,dict(d[0]));rows=d
    find('base','FY2026E','loan_loss_allowance')['line_item']='bogus_item'
    find('base','FY2028E','profit_after_tax')['value']='1'
    find('base','FY2027E','interest_income')['status']='reported'
    find('base','FY2029E','net_interest_income')['value']='NaN'
    find('upside','FY2027E','total_assets')['bank']='wrong-bank'
    x=find('upside','FY2028E','car_pct');x['status']='unavailable';x['value']='10'
    rows=[x for x in rows if not(x['scenario']=='downside' and x['period']=='FY2030E')]
    write(b/'forecast.csv',h,rows)
    fail=qa.check_bank(slug)['fail'];print('FAULTS',fail)
    for msg in ('duplicate forecast row','bogus_item','base FY2028E PAT','forecast invalid status','non-finite','wrong-bank','unavailable forecast row has a value',"forecast missing scenario-years: ['downside|FY2030E']"):
        assert any(msg in x for x in fail),msg
    assert not any("base|FY2027E" in x and "missing scenario-years" in x for x in fail)
    # Missing columns should be detected without KeyError.
    write(b/'forecast.csv',[x for x in h if x!='bank'],rows)
    assert any('forecast.csv lacks column bank' in x for x in qa.check_bank(slug)['fail'])
    write(b/'financials.csv',[x for x in hh if x!='period'],history)
    assert any('financials.csv columns' in x for x in qa.check_bank(slug)['fail'])
print('PASS: takeover + finite-number guards + 8 simultaneous fault classes + both missing-header cases; no truncated later checks')

# Real source-note regression: exact bridge amounts, no broad write-off exemption.
assert qa.loan_bridge_memo("x_amounts_written_off_bridge")
assert not qa.loan_bridge_memo("x_unrelated_writeoff")
for note in ("Other asset categories including applicable investments in equity/subsidiaries and tax assets; excludes PPE/ROU.", "Sum of other asset components excluding ROU; reversed the duplicate deduction of 89.070m. Bank-only; see sources.md."):
    assert qa.rou_note_state(note)=="excluded",note
for note in ("Sum of restricted cash, investment other than securities, tax assets, ROU assets, and other assets.", "Sum of non-pledged trading assets, other assets, tax assets, ROU assets, investment in subsidiaries, and assets held for sale."):
    assert qa.rou_note_state(note)=="included",note
qa.BANKS=str(goal/'banks');qa.CLAIMS=str(goal/'claims')
pbl=qa.check_bank('prudential-bank');cal=qa.check_bank('calbank')
assert not any("gross loans" in x for x in pbl["fail"]),pbl
assert not any("right-of-use" in x for x in pbl["warn"]+cal["warn"]), (pbl,cal)
# ADB/Ecobank may be corrected by owners in later snapshots; verify every explicitly included period is flagged.
for bank in ('adb','ecobank-ghana'):
    _,hr=read(goal/'banks'/bank/'financials.csv')
    n=sum(1 for x in hr if x['line_item']=='other_assets' and qa.rou_note_state(x['notes'])=='included')
    report=qa.check_bank(bank)
    assert sum('note indicates right-of-use inclusion' in x for x in report['warn'])==n,(bank,n,report)
    print(bank,'explicit ROU periods flagged',n)
print('PASS: real Prudential loan bridge, CalBank/Prudential exclusions, all explicit ROU inclusion periods')
