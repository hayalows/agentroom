from pathlib import Path
import csv, json, re, math, hashlib, sys, collections
from decimal import Decimal
from xml.sax.saxutils import escape
from html import unescape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.graphics.shapes import Drawing, Rect, String, Line, PolyLine, Circle

G=Path('goals/ghana-bank-models')
D=G/'reports/iconka'
D.mkdir(parents=True,exist_ok=True)
PIN='b728a09ffd52393f98b97c14298544c139d1921f'
PUB='11dffc9111b208dc896e2db05f0e65c18aa09179'
SIGN='8d695a28'
REPO='https://github.com/hayalows/agentroom'
ROOT=REPO+'/blob/main/'+str(G).replace('\\','/')+'/'
PINF=REPO+'/blob/'+PIN+'/goals/ghana-bank-models/'
PUBF=REPO+'/blob/'+PUB+'/goals/ghana-bank-models/'
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))
def dec(x):return Decimal(x) if x not in ('',None,'-') else None
def val(rs,p,k,s=None):
    x=[dec(r['value']) for r in rs if r['period']==p and r['line_item']==k and (s is None or r.get('scenario')==s) and (s is not None or r['status'] in ('reported','derived')) and r['value']!='']
    if len(x)>1:raise ValueError(('duplicate',p,k,s))
    return x[0] if x else None
def fmt(x,places=1):
    return 'n/a' if x is None else f'{x:,.{places}f}'
def bn(x):return fmt(x/1000,2) if x is not None else 'n/a'
def pc(a,b):return (a/b-1)*100 if a is not None and b and b>0 else None
def ratio(a,b):return a/b*100 if a is not None and b and b>0 else None
def num(x):return dec(x)
def pct(a,b):return fmt(ratio(a,b),1)+'%' if ratio(a,b) is not None else 'n/a'
def change(a,b):
    x=pc(a,b)
    return 'n/a' if x is None else ('+' if x>0 else '')+fmt(x,1)+'%'
def total(xs):return sum((x for x in xs if x is not None),Decimal(0))
years=[f'FY{y}' for y in range(2021,2026)]+['9M-2026']
future=[f'FY{y}E' for y in range(2026,2031)]
scens=['base','downside','upside']
keys=['total_assets','customer_deposits','loans_and_advances_net','total_equity','profit_after_tax','net_interest_income']
labels=['Assets','Deposits','Net loans','Equity','PAT','Net interest income']
names={'absa-ghana':'Absa Bank Ghana','access-bank-ghana':'Access Bank Ghana','adb':'Agricultural Development Bank','bank-of-africa-ghana':'Bank of Africa Ghana','calbank':'CalBank','consolidated-bank-ghana':'Consolidated Bank Ghana','ecobank-ghana':'Ecobank Ghana','fbnbank-ghana':'First Bank Ghana (FBNBank)','fidelity-bank-ghana':'Fidelity Bank Ghana','first-atlantic-bank':'First Atlantic Bank','first-national-bank-ghana':'First National Bank Ghana','gcb':'GCB Bank','gtbank-ghana':'Guaranty Trust Bank Ghana','nib':'National Investment Bank','omnibsic-bank':'OmniBSIC Bank','prudential-bank':'Prudential Bank','republic-bank-ghana':'Republic Bank Ghana','societe-generale-ghana':'Societe Generale Ghana','stanbic-bank-ghana':'Stanbic Bank Ghana','standard-chartered-ghana':'Standard Chartered Bank Ghana','uba-ghana':'United Bank for Africa Ghana','umb':'Universal Merchant Bank','zenith-bank-ghana':'Zenith Bank Ghana'}
peer={r['bank']:r for r in read(G/'sector/peer-comparison/comparison.csv')}
ordinary=sorted(peer)
conditional=['omnibsic-bank','prudential-bank','umb']
assert len(ordinary)==20 and sorted(ordinary+conditional)==sorted(names)
B={}
for slug in names:
    p=G/'banks'/slug
    h=read(p/'financials.csv');f=read(p/'forecast.csv')
    claim=G/'claims'/('prudential-bank-takeover.md' if slug=='prudential-bank' else slug+'.md')
    txt=claim.read_text(encoding='utf-8-sig')
    field=lambda k: (re.search(r'^'+k+r':\s*(.*)$',txt,re.M).group(1).strip() if re.search(r'^'+k+r':\s*(.*)$',txt,re.M) else '')
    B[slug]={'h':h,'f':f,'owner':field('agent'),'steward':field('steward'),'reviewer':peer.get(slug,{}).get('reviewer','scoped independent reviews'),'nsource':len({r['source_id'] for r in h if r['status']=='reported'}),'claim':claim.name}
def h(slug,p,k):return val(B[slug]['h'],p,k)
def f(slug,p,k,s='base'):return val(B[slug]['f'],p,k,s)
def H(p,k):return total(h(slug,p,k) for slug in ordinary)
def F(p,k,s='base'):return total(f(slug,p,k,s) for slug in ordinary)
for s in scens:
    for p in future:
        for k in ['profit_after_tax','total_assets','total_equity']:
            assert all(f(slug,p,k,s) is not None for slug in ordinary)
assert abs(H('FY2025','total_assets')-Decimal('403776.743'))<Decimal('.001')
assert abs(H('FY2025','profit_after_tax')-Decimal('14033.738'))<Decimal('.001')
assert F('FY2030E','profit_after_tax')==Decimal('19285.178')
assert F('FY2030E','profit_after_tax','downside')==Decimal('7237.121')
assert F('FY2030E','profit_after_tax','upside')==Decimal('26476.585')
# Verify all 45 principal forecast cells and available historical/coverage cells from published data.
published=read(G/'sector/sector-rollup/rollup.csv')
match=[]
for r in published:
    if r['bank']!='ACCEPTED_ONLY' or not r['value']:continue
    k=r['item'];p=r['period_or_scenario'];v=dec(r['value'])
    if r['unit']!='GHS millions':continue
    if r['table']=='forecast_total':
        scenario,period=p.split('|')
        match.append(abs(F(period,k,scenario)-v))
        continue
    if k not in keys:continue
    if p in years and r['unit']=='GHS millions':
        match.append(abs(H(p,k)-v))
    elif p in future and r['unit']=='GHS millions':
        # Forecast rows usually use a combined scenario/period field; checked separately below.
        pass
assert not match or max(match)<Decimal('.002')
hist_count=sum(len(x['h']) for x in B.values())
fc_count=sum(len(x['f']) for x in B.values())
source_ids=sum(x['nsource'] for x in B.values())
board_ids=['claude','codex','gemini','deepseek','claude-helper-1','chatgpt-support','gpt-6-luna','papa-kojo-agent']
macro=read(G/'sector/macro-assumptions/macro.csv')
def m(k,s,p):return dec(next(r['value'] for r in macro if r['driver']==k and r['scenario']==s and r['year']==p))
context={r['indicator']:r for r in read(G/'sector/macro-assumptions/sector-context.csv')}
N=colors.HexColor('#172D43');T=colors.HexColor('#006C69');M=colors.HexColor('#526576');L=colors.HexColor('#DDE6E9');P=colors.HexColor('#EDF5F4');R=colors.HexColor('#A13D36');GOLD=colors.HexColor('#B48142')
W,HGT=A4; WIDTH=W-90
styles={
 'body':ParagraphStyle('body',fontName='Helvetica',fontSize=10.2,leading=14.4,textColor=N,spaceAfter=8),
 'small':ParagraphStyle('small',fontName='Helvetica',fontSize=8.2,leading=11.5,textColor=M,spaceAfter=7),
 'note':ParagraphStyle('note',fontName='Helvetica',fontSize=8.6,leading=12,textColor=M,spaceAfter=6),
 'h1':ParagraphStyle('h1',fontName='Helvetica-Bold',fontSize=23,leading=27,textColor=N,spaceAfter=10),
 'h2':ParagraphStyle('h2',fontName='Helvetica-Bold',fontSize=13,leading=16,textColor=T,spaceBefore=10,spaceAfter=7),
 'eyebrow':ParagraphStyle('eyebrow',fontName='Helvetica-Bold',fontSize=9,leading=12,textColor=T,spaceAfter=8),
 'cover':ParagraphStyle('cover',fontName='Helvetica-Bold',fontSize=36,leading=40,textColor=N,spaceAfter=14),
 'subtitle':ParagraphStyle('subtitle',fontName='Helvetica',fontSize=16,leading=22,textColor=M,spaceAfter=18),
 'cell':ParagraphStyle('cell',fontName='Helvetica',fontSize=8.4,leading=11,textColor=N),
 'headcell':ParagraphStyle('headcell',fontName='Helvetica-Bold',fontSize=8.4,leading=11,textColor=colors.white),
 'big':ParagraphStyle('big',fontName='Helvetica-Bold',fontSize=23,leading=27,textColor=T)
}
story=[]; pages=0
markdown=[]
def md_text(s):
    s=re.sub(r'<link href="([^"]+)"[^>]*>(.*?)</link>',lambda m:'['+unescape(m.group(2))+']('+unescape(m.group(1))+')',str(s))
    s=re.sub(r'<br\s*/?>',' ',s)
    return unescape(s)
def md_table(rows):
    clean=lambda x:str(x).replace('|',r'\|').replace('\n',' ')
    markdown.append('| '+' | '.join(map(clean,rows[0]))+' |\n| '+' | '.join(['---']*len(rows[0]))+' |\n'+'\n'.join('| '+' | '.join(map(clean,row))+' |' for row in rows[1:]))
def p(s,style='body'):
    story.append(Paragraph(s,styles[style]))
    prefixes={'cover':'# ','h1':'## ','h2':'### ','eyebrow':'**','subtitle':''}
    t=md_text(s)
    markdown.append(prefixes.get(style,'')+t+('**' if style=='eyebrow' else ''))
def para(s,style='body'):p(escape(str(s)),style)
def title(k,t,sub=None):
    global pages
    if pages:story.append(PageBreak())
    pages+=1
    p(k.upper(),'eyebrow');p(escape(t),'h1')
    if sub:para(sub,'note')
def h2(s):p(escape(s),'h2')
def table(rows,widths=None,fs=8.5):
    md_table(rows)
    if widths is None:widths=[WIDTH/len(rows[0])]*len(rows[0])
    data=[]
    for i,row in enumerate(rows):
        data.append([Paragraph(escape(str(x)),styles['headcell' if i==0 else 'cell']) if j==0 or i==0 or len(str(x))>23 else str(x) for j,x in enumerate(row)])
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    cmds=[('BACKGROUND',(0,0),(-1,0),N),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,1),(-1,-1),'Helvetica'),('FONTSIZE',(0,1),(-1,-1),fs),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ALIGN',(1,1),(-1,-1),'RIGHT'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),0.7,T)]
    for i in range(1,len(rows)):
        if i%2==0:cmds.append(('BACKGROUND',(0,i),(-1,i),P))
        cmds.append(('LINEBELOW',(0,i),(-1,i),0.25,L))
    t.setStyle(TableStyle(cmds));story.append(t);story.append(Spacer(1,9))
def sources(items):
    p('Evidence: '+'; '.join(f'<link href="{escape(url)}" color="#006C69">{escape(label)}</link>' for label,url in items)+'.','small')
def sectsrc():
    sources([('final roll-up',PUBF+'sector/sector-rollup/rollup.md'),('peer comparison',PUBF+'sector/peer-comparison/README.md'),('lead summary',ROOT+'sector/summary.md')])
def callout(label,txt):
    markdown.append('**'+label+'**: '+txt)
    t=Table([[Paragraph(escape(label),styles['eyebrow'])],[Paragraph(escape(txt),styles['body'])]],colWidths=[WIDTH])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),P),('BOX',(0,0),(-1,-1),0.5,L),('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),6)]));story.append(t);story.append(Spacer(1,10))
def chart(series,labels_,ymin,ymax,step,unit):
    markdown.append('**Chart data: '+unit+'** (same series as the PDF line chart).')
    md_table([['Scenario']+list(labels_)]+[[name]+[f'{v:.3f}' for v in vs] for name,vs in series])
    d=Drawing(WIDTH,195); x0=45; x1=WIDTH-12; y0=28; y1=158
    yy=lambda v:y0+(float(v)-ymin)/(ymax-ymin)*(y1-y0)
    xx=lambda i:x0+i*(x1-x0)/(len(labels_)-1)
    for tick in range(ymin,ymax+1,step):
        y=yy(tick);d.add(Line(x0,y,x1,y,strokeColor=L,strokeWidth=.5));d.add(String(x0-8,y-3,str(tick),fontName='Helvetica',fontSize=8,textAnchor='end',fillColor=M))
    for i,lab in enumerate(labels_):d.add(String(xx(i),y0-15,lab,fontName='Helvetica',fontSize=8,textAnchor='middle',fillColor=M))
    palette=[T,R,GOLD]
    for j,(name,vs) in enumerate(series):
        c=palette[j];pts=[]
        for i,v in enumerate(vs):
            pts.extend([xx(i),yy(v)])
        d.add(PolyLine(pts,strokeColor=c,strokeWidth=2.5))
        for i,v in enumerate(vs):d.add(Circle(xx(i),yy(v),3,fillColor=c,strokeColor=c))
        d.add(Line(x0+j*145,183,x0+17+j*145,183,strokeColor=c,strokeWidth=2.5));d.add(String(x0+23+j*145,180,name,fontSize=8.5,fillColor=N))
    d.add(String(3,169,unit,fontSize=8,fillColor=M))
    story.append(d)
def bars(vs,lab):
    markdown.append('**Chart data: historical annual PAT, GHS bn** (same series as the PDF bar chart).')
    md_table([['Year']+list(lab),['PAT']+[f'{v:.3f}' for v in vs]])
    d=Drawing(WIDTH,180);x0=46;x1=WIDTH-15;y0=30;y1=151
    lo=-8;hi=16
    yy=lambda v:y0+(float(v)-lo)/(hi-lo)*(y1-y0)
    for tick in range(-8,17,4):
        y=yy(tick);d.add(Line(x0,y,x1,y,strokeColor=L,strokeWidth=.5));d.add(String(x0-7,y-3,str(tick),fontSize=8,textAnchor='end',fillColor=M))
    for i,v in enumerate(vs):
        x=x0+(i+.5)*(x1-x0)/len(vs);y=yy(v);z=yy(0)
        d.add(Rect(x-23,min(y,z),46,abs(y-z),fillColor=T if v>=0 else R,strokeColor=None))
        d.add(String(x,y+5 if v>=0 else y-12,f'{v:.1f}',fontName='Helvetica-Bold',fontSize=9,textAnchor='middle',fillColor=N))
        d.add(String(x,12,lab[i],fontSize=8,textAnchor='middle',fillColor=M))
    d.add(String(4,165,'GHS bn',fontSize=8,fillColor=M));story.append(d)

# Cover and executive assessment.
pages=1
p('AGENTROOM  /  RESEARCH SERIES  /  01','eyebrow');story.append(Spacer(1,38))
p('Ghana banking<br/>sector outlook<br/>2026 to 2030','cover')
p('A financial and institutional review of 23 licensed banks, with five-year forecasts and an account of the multi-agent research process.','subtitle')
para('Prepared by Iconka (GPT-6.2), human-requested synthesis | 25 November 2026','body')
story.append(Spacer(1,17))
table([['Coverage','23 licensed banks'],['Ordinary accepted models','20 banks; approximately 90% of FY2025 assets'],['Conditional closures','3 banks, kept outside all ordinary totals'],['Source snapshot','b728a09ffd52393f98b97c14298544c139d1921f'],['Publication commit','11dffc9111b208dc896e2db05f0e65c18aa09179'],['Human sign-off','25 Nov 2026, 21:13:42 UTC']],[150,WIDTH-150])
callout('CENTRAL FINDING','Ghanaian banks have rebuilt earnings and balance sheets after the 2022 debt-exchange shock, but the next phase depends on credit quality and funding costs. In the 20-bank base case, profit rises from GHS 12.92bn in 2026 to GHS 19.29bn in 2030. The 2030 downside is only GHS 7.24bn.')
para('This paper supplements the frozen signed-off project. It is analytical research, not an audit, regulatory assessment, investment recommendation, valuation or bank management forecast. All currency figures are nominal GHS.','small')
sources([('repository',REPO),('signed-off summary',ROOT+'sector/summary.md')])
title('01 / Executive summary','The recovery is real, but returns are changing','Findings from a consistent 20-bank historical cohort and separate coverage for three conditional models.')
para('The accepted 20 banks earned GHS 14.03bn in 2025, up from GHS 4.71bn in 2021 and a GHS 5.89bn loss in 2022. Assets reached GHS 403.78bn and equity GHS 56.58bn at FY2025. The Bank of Ghana (BoG) sector total was GHS 446.9bn of assets. This is a broad, but incomplete, sample.')
para('The recovery coincided with recapitalisation, a changing rate environment and the absorption of losses associated with the domestic debt exchange. Balance-sheet growth does not establish the cause of earnings growth. Net lending remained only 30.3% of customer deposits in FY2025 for the matched banks, indicating considerable funding held in other assets.')
table([['GHS bn','2025 actual','2026E base','2030E base','2030E down','2030E up'],['Assets',bn(H('FY2025','total_assets')),bn(F(future[0],'total_assets')),bn(F(future[-1],'total_assets')),bn(F(future[-1],'total_assets','downside')),bn(F(future[-1],'total_assets','upside'))],['Equity',bn(H('FY2025','total_equity')),bn(F(future[0],'total_equity')),bn(F(future[-1],'total_equity')),bn(F(future[-1],'total_equity','downside')),bn(F(future[-1],'total_equity','upside'))],['PAT',bn(H('FY2025','profit_after_tax')),bn(F(future[0],'profit_after_tax')),bn(F(future[-1],'profit_after_tax')),bn(F(future[-1],'profit_after_tax','downside')),bn(F(future[-1],'profit_after_tax','upside'))]],[85]+[(WIDTH-85)/5]*5)
para('The base case shows a softer 2026 profit year, followed by growth from 2027. By 2030, the downside would be about 62% below base earnings and the upside about 37% above base. These are scenario outputs, not probability estimates. Some liquid-asset-heavy banks initially earn more in the downside rate path.')
para('The weakest modeled capital outcomes are concentrated in ADB, CBG, NIB and Societe Generale. GCB is the largest earnings contributor in the 2030 base, so its assumptions deserve disproportionate review. Three excluded banks require a different level of confidence, especially UMB, whose current recapitalised position is not represented by its forecast.')
h2('Reading guide')
para('Pages 3–11 cover the sector history, macro drivers, forecasts, comparative metrics and capital risks. Pages 12–34 profile the 23 banks. The final pages explain how agents collected and reviewed data, what was committed, and how to reproduce or improve the work.')
sectsrc()
title('02 / History','From the debt-exchange shock to recovery','Matched 20 ordinary banks; financial year-end balances and cumulative income, GHS billions.')
table([['GHS bn']+['2021','2022','2023','2024','2025','9M26']]+[[lab]+[bn(H(y,k)) for y in years] for lab,k in zip(labels,keys)],[115]+[(WIDTH-115)/6]*6)
bars([float(H(y,'profit_after_tax')/1000) for y in years[:5]],['2021','2022','2023','2024','2025'])
para('Assets increased by '+change(H('FY2025','total_assets'),H('FY2021','total_assets'))+' between FY2021 and FY2025; deposits grew '+change(H('FY2025','customer_deposits'),H('FY2021','customer_deposits'))+'. Equity fell from GHS 24.19bn to GHS 18.27bn in 2022, then rose to GHS 56.58bn by 2025. FY2025 profit grew '+change(H('FY2025','profit_after_tax'),H('FY2024','profit_after_tax'))+' year-on-year.')
para('In FY2025, net interest income was GHS 28.26bn. The independent roll-up reports pre-impairment operating income of GHS 41.93bn and matched cost-to-income of 45.09%. Closing-equity return was 24.80%. Closing-equity ROE divides full-year PAT by year-end equity. Average-equity ROE divides by the mean of opening and closing equity; a recapitalisation or negative opening equity can distort it. Neither should be substituted for the regulator’s differently defined ratios.')
para('The September 2026 column contains only 19 ordinary banks because CBG published H1, not September, data. It is not a complete FY2026 comparison; the PAT and NII values are nine-month flows.','note')
sectsrc()
title('03 / Industry context','The whole licensed banking sector','Regulator figures copied from the room’s BoG source register; not a re-audit of the original PDF.')
ctx=[('Assets (GHS bn)','total_assets'),('Deposits (GHS bn)','total_deposits'),('Gross advances (GHS bn)','total_advances'),('CAR (%)','capital_adequacy_ratio'),('NPL (%)','npl_ratio'),('NIM (%)','net_interest_margin'),('ROE after tax (%)','return_on_equity_after_tax'),('Average lending rate (%)','average_lending_rate'),('Private credit growth YoY (%)','private_sector_credit_growth_yoy'),('Operational cost / gross income (%)','operational_cost_to_gross_income')]
table([['BoG indicator','Dec 2025','Apr 2026','Sep 2026','Oct 2026']]+[[lab]+[context[k][x] for x in ['2025-12','2026-04','2026-09','2026-10']] for lab,k in ctx],[195]+[(WIDTH-195)/4]*4)
para('October 2026 assets were GHS 512.9bn, 14.8% above December 2025; deposits were GHS 369.8bn and gross advances GHS 140.9bn. Nominal private credit growth accelerated to 37.2% year-on-year, while the reported industry NPL ratio fell to 13.1%. Those measures suggest credit is recovering, though nominal growth and classification changes must be separated from real lending quality.')
para('Interest margins are under pressure: NIM fell from 11.5% in December 2025 to 8.1% in October 2026. The BoG after-tax ROE measure fell from 30.8% to 19.0%. Operational cost as a share of gross income rose to 54.8%. Falling yields can reduce asset earnings before deposit costs and overhead adjust.')
para('The regulator’s gross advances are not the models’ net loans. BoG aggregates can have a different reporting perimeter, regulatory relief and ratio methodology. The observed coverage is 90.35% of FY25 assets and 87.52% of September 2026 assets (19 banks).')
sources([('sector-context.csv',PINF+'sector/macro-assumptions/sector-context.csv'),('macro source register',PINF+'sector/macro-assumptions/SOURCES.md'),('BoG November 2026 release','https://www.bog.gov.gh/wp-content/uploads/2026/11/Summary-of-Economic-and-Financial-Data-November-2026-1.pdf')])
title('04 / Forecast assumptions','The common macroeconomic paths','The scenario labels describe coherent assumptions; they do not rank every bank’s earnings monotonically.')
for k,label in [('policy_rate_pct','Policy rate (%)'),('tbill_91d_pct','91-day Treasury bill yield (%)'),('inflation_cpi_pct','CPI inflation (%)'),('gdp_growth_pct','Real GDP growth (%)'),('ghs_per_usd_end','End-year GHS per USD')]:
    table([[label,'2026E','2027E','2028E','2029E','2030E']]+[[s.title()]+[fmt(m(k,s,y),2) for y in future] for s in scens],[145]+[(WIDTH-145)/5]*5)
para('The 2026 assumptions are anchored by the November policy rate cut to 11%, October inflation of 5.5% and the latest 91-day bill auction of approximately 4.52%. The 2026 full-year bill yield is an average estimate, not the last auction yield. Base assumes easing and normalisation; downside assumes a weaker cedi, inflation and slower growth; upside assumes stronger activity and milder FX depreciation. The shared 20% cash reserve requirement and 13% CAR screen are held constant, with future requirements estimated. GHS 400m paid-up capital is an unconfirmed carry-forward.','note')
sources([('macro.csv',PINF+'sector/macro-assumptions/macro.csv'),('source notes',PINF+'sector/macro-assumptions/SOURCES.md'),('18 November MPC release','https://www.bog.gov.gh/wp-content/uploads/2026/11/MPC-Press-Release-November-2026.pdf')])
title('05 / Outlook','Profit and balance sheets through 2030','Forecast aggregate: 20 ordinary banks; GHS billions, estimates. No conditional forecasts included.')
for k,label in [('profit_after_tax','PAT'),('total_assets','Assets'),('total_equity','Equity')]:
    table([[label,'2026E','2027E','2028E','2029E','2030E']]+[[s.title()]+[bn(F(y,k,s)) for y in future] for s in scens],[100]+[(WIDTH-100)/5]*5)
chart([(s.title(),[float(F(y,'profit_after_tax',s)/1000) for y in future]) for s in scens],['2026E','2027E','2028E','2029E','2030E'],0,30,5,'PAT, GHS bn')
para('Base assets roughly double from FY2025 to FY2030 (GHS 818.39bn); equity nearly doubles to GHS 113.07bn. Base PAT grows '+change(F('FY2030E','profit_after_tax'),H('FY2025','profit_after_tax'))+' over the same five years. The modeled base 2026 PAT is '+change(F('FY2026E','profit_after_tax'),H('FY2025','profit_after_tax'))+' versus FY2025. The downside ends below the 2026 starting profit even as assets grow.','note')
sectsrc()
title('06 / Outlook interpretation','What each forecast year implies','Iconka interpretation of the signed-off model paths; not a management or regulatory forecast.')
for i,y in enumerate(future):
    pat=F(y,'profit_after_tax');a=F(y,'total_assets');eq=F(y,'total_equity');down=F(y,'profit_after_tax','downside');up=F(y,'profit_after_tax','upside')
    h2(y+': GHS '+bn(pat)+'bn base PAT')
    notes=[
      'A transition year. Lower security yields, repricing and Q4 credit/tax assumptions matter most. Nineteen banks have September actuals; CBG has H1. Preserve the actual interim results when comparing the Q4 estimate.',
      'Recovery in base profit, aided by modeled balance-sheet growth. The downside improves temporarily, but high funding rates and slower GDP constrain a broader recovery.',
      'The spread between scenarios grows. Credit expansion and operating cost control become increasingly important as forecast profits depend less on the observed 2026 anchor.',
      'Downside profit declines sharply while the base continues to grow. Compounding funding, impairment and operating cost stresses dominate the temporary benefit of high rates for some banks.',
      'The base is substantially larger than FY2025 but the wide earnings range highlights uncertainty. Watch concentration and undercapitalised stress cases rather than reading the midpoint as a prediction.'
    ][i]
    para(f'Assets GHS {bn(a)}bn; equity GHS {bn(eq)}bn. PAT range GHS {bn(down)}bn to {bn(up)}bn across downside and upside. Base closing-equity return {pct(pat,eq)}. '+notes)
para('The scenario range is not a confidence interval. No scenario probabilities are assigned; the models do not simulate contagion, a new debt restructuring or an explicit future supervisory response.','note')
sectsrc()
title('07 / System-wide interpretation','Scaling the model to a sector perspective','The accepted bank set is not the entire banking system. No conditional bank is added to the ordinary projections.')
cover25=Decimal('403776.743')/Decimal('446900')
cover26=Decimal('449482.634')/Decimal('513600')
table([['GHS bn, illustrative','2026E','2027E','2028E','2029E','2030E']]+[['20-bank base assets']+[bn(F(y,'total_assets')) for y in future],['Scale at 90.35%']+[bn(F(y,'total_assets')/cover25) for y in future],['Scale at 87.52%']+[bn(F(y,'total_assets')/cover26) for y in future]],[155]+[(WIDTH-155)/5]*5)
para('If the FY2025 share of industry assets were to remain constant, a purely mechanical extrapolation would place whole-sector base assets at about GHS '+bn(F('FY2030E','total_assets')/cover25)+'bn in 2030. Using the September share gives about GHS '+bn(F('FY2030E','total_assets')/cover26)+'bn. The latter includes only 19 interim reporters; it is a sensitivity, not a superior estimate.')
para('These are Iconka’s illustrative scaling calculations, not outputs approved by the lead. They assume constant coverage, which is unlikely to hold exactly as individual banks recapitalise, merge, expand or contract. The exclusions are not random. No full-sector PAT estimate is justified by the available comparable regulator data; asset share is not a valid proxy for profit share.')
para('The more defensible conclusion is directional: a rising nominal banking balance sheet under each macro path, with much wider dispersion in earnings and capital. From the regulator’s October snapshot, the sector is already above half a trillion cedis in assets. A route toward roughly GHS 0.9tn by 2030 is possible under the model’s base and coverage assumption, but real growth and currency value may differ materially.')
h2('Practical implications')
para('For bank management, monitor loan vintage performance, deposit beta and concentration, reserve-eligible cash and contingent funding. For depositors and businesses, service quality and pricing are separate from model profitability. For policy analysis, lending growth needs to be matched to credit quality rather than targeted in isolation.')
sectsrc()
title('08 / Comparison','Size, earnings and balance-sheet mix','FY2025 ordinary banks ranked by assets. GHS billions except percentages; net LDR = net loans / deposits.')
rank=sorted(ordinary,key=lambda b:h(b,'FY2025','total_assets'),reverse=True)
table([['Bank','Assets','Deposits','PAT','Net LDR','Close ROE']]+[[names[b],bn(h(b,'FY2025','total_assets')),bn(h(b,'FY2025','customer_deposits')),bn(h(b,'FY2025','profit_after_tax')),pct(h(b,'FY2025','loans_and_advances_net'),h(b,'FY2025','customer_deposits')),fmt(num(peer[b]['roe_closing_equity_2025_pct']),1)+'%'] for b in rank],[176,62,62,60,70,WIDTH-430],7.8)
para('GCB and Ecobank account for '+pct(total(h(b,'FY2025','total_assets') for b in rank[:2]),H('FY2025','total_assets'))+' of the modeled assets; the four largest account for '+pct(total(h(b,'FY2025','total_assets') for b in rank[:4]),H('FY2025','total_assets'))+'. Societe Generale’s net LDR of 76.9% differs sharply from NIB’s 7.2% and CBG’s 10.5%. This is a comparison of asset mix, not a ranking of creditworthiness.','note')
sectsrc()
title('09 / Comparison','The FY2030 earnings and capital stress test','GHS millions; CAR proxies are not regulatory capital returns. Bank order by downside PAT.')
rank2=sorted(ordinary,key=lambda b:f(b,'FY2030E','profit_after_tax','downside'))
table([['Bank','Base PAT','Down PAT','Up PAT','Base CAR','Down CAR']]+[[names[b],fmt(f(b,'FY2030E','profit_after_tax')),fmt(f(b,'FY2030E','profit_after_tax','downside')),fmt(f(b,'FY2030E','profit_after_tax','upside')),fmt(num(peer[b]['car_base_2030_proxy_pct']),1)+'%',fmt(num(peer[b]['car_downside_2030_proxy_pct']),1)+'%'] for b in rank2],[171,72,70,69,62,WIDTH-444],7.8)
loss=[b for b in ordinary if f(b,'FY2030E','profit_after_tax','downside')<0]
cap=[b for b in ordinary if num(peer[b]['car_downside_2030_proxy_pct'])<13]
para(f'{len(loss)} ordinary banks are loss-making in the FY2030 downside, and {len(cap)} have capital proxies below 13%: '+', '.join(names[b] for b in cap)+'. Negative proxy outcomes imply a modeled need for corrective action or additional capital under the stated assumptions; they are not findings of actual regulatory breach.','note')
sectsrc()
title('10 / Risk analysis','Where the forecast can break','Concentration, credit quality, liquidity, non-interest income and model risk.')
gcbbase=f('gcb','FY2030E','profit_after_tax');delta=F('FY2030E','profit_after_tax')-F('FY2030E','profit_after_tax','downside')
contrib=sorted(ordinary,key=lambda b:f(b,'FY2030E','profit_after_tax')-f(b,'FY2030E','profit_after_tax','downside'),reverse=True)
table([['Largest contributions to 2030 base-down PAT gap','GHS m','Share of net gap']]+[[names[b],fmt(f(b,'FY2030E','profit_after_tax')-f(b,'FY2030E','profit_after_tax','downside')),pct(f(b,'FY2030E','profit_after_tax')-f(b,'FY2030E','profit_after_tax','downside'),delta)] for b in contrib[:6]],[WIDTH-190,100,90])
para('GCB alone contributes '+pct(gcbbase,F('FY2030E','profit_after_tax'))+' of 2030 base PAT and '+pct(gcbbase-h('gcb','FY2025','profit_after_tax'),F('FY2030E','profit_after_tax')-H('FY2025','profit_after_tax'))+' of the net modeled 2025–2030 profit increase. Its forecast is the most consequential individual sensitivity. The sector base-down gap is GHS '+bn(delta)+'bn, with a significant portion coming from GCB and Stanbic.')
para('Credit risk: ADB and NIB report very high FY2025 gross NPL ratios (70.53% and 69.70%). CBG reports 33.42%. A shrinking loan book can raise a ratio even while absolute nonperforming balances fall; very high historic allowances can also make simple linear impairment forecasts misleading.')
para('Funding and liquidity: deposit growth is not equivalent to free cash. The shared 20% reserve requirement interacts with the amount of eligible cash, collateral restrictions, wholesale borrowing and deposit repricing. Several models identify reserve proxy gaps. These are stress screens, not evidence of actual noncompliance.')
para('Forecasting limits: 2026 spreads often use fitted interim results. Trading income fades are judgmental, future FX shocks are incomplete, and balance-sheet and statutory reserve proxies differ by bank. A downside rate path may temporarily benefit asset-rich banks; CalBank ends with downside PAT above base. This does not mean the downside is preferable in wider economic terms.')
sectsrc()

bank_notes={
'absa-ghana':('The issuer’s annual source pages were recovered by Codex and independently transcribed; Helper built the model and Support reviewed it. The bank has comparatively high net lending intensity among the largest banks. FY2026 modeled PAT falls below FY2025 despite a larger balance sheet.','Reported FY2025 capital and NPL values are not available in the peer extract. The reserve-cash proxy is calibrated; a 20% eligibility stress withholds dividends. Liquidity screens and capital estimates do not establish prudential compliance.'),
'access-bank-ghana':('The listed Ghana subsidiary has a substantial customer deposit base. FY2025 earnings declined from FY2024, but 9M2026 already exceeded the 2025 full-year PAT. The model uses the observed nine months and an estimated Q4, then explicit interest and credit assumptions.','The signed/final status of one FY2025 web copy remains unverified; historic fee splits and component definitions have gaps. Watch repricing and whether the stronger 2026 earnings can persist.'),
'adb':('State-backed and listed, ADB recovered from the FY2023 loss and negative equity. The bank’s FY2025 reported gross NPL ratio of 70.53% and high loan allowance make its asset quality a critical driver. The corrected model includes earning cash and placements and the regulatory capital anchor rather than book equity alone.','Base PAT turns negative in 2029 and reaches a loss of GHS 308m in 2030; the downside capital proxy is negative. Earlier gross loans and allowance detail remain unavailable for some periods. Focus on recoveries, new lending quality and verified regulatory capital.'),
'bank-of-africa-ghana':('The unlisted bank has a relatively small balance sheet and positive FY2025 earnings. September 2026 CAR was 27.01% and NPL 17.89%, with a notable impairment increase. The forecast uses actual nine-month results and separately modeled Q4.','FY2022 audit qualification involved omitted GHS 80.883m investment impairment; the review documents the alternative pretax outcome. The model does not forecast regulatory CAR or a full gross loan/ECL series.'),
'calbank':('The bank suffered large 2022 and 2023 losses, then recapitalised. FY2025 closing equity was over six times opening equity, so average-equity ROE is flagged. Gemini’s original model passed through Luna’s stewardship and later repair by Support.','The downside earns more than base in FY2030 because the rate path benefits liquid assets; this is an economic sensitivity, not a coding error by itself. Reviews found overstated interest and double-counted ROU assets; the final repair used the corrected capital and reserve treatment.'),
'consolidated-bank-ghana':('Government-owned CBG earned only GHS 7.4m in FY2025. It has a low lending intensity and substantial operating costs relative to income. Its latest available 2026 statement is H1, not September; the model explicitly uses that period.','FY2025 reserve waiver and present eligibility are not independently confirmed. The mechanical 20% reserve screen gives a gap; this is not an actual breach. The downside produces material losses and negative capital proxy, making this one of the most vulnerable models.'),
'ecobank-ghana':('Ecobank is the second-largest ordinary bank by FY2025 assets. It is majority-owned by ETI and listed on the GSE. Its 2025 PAT of GHS 1.79bn and relatively low modeled cost/income support its strong earnings scale.','The source summary does not split some bank placements, gross loans/ECL, FX or total Tier 1. ROU misclassification was corrected across six periods; two uninvolved reviewers verified the current revision. Profit forecasts depend on spread, trading and operating assumptions.'),
'fbnbank-ghana':('First Bank Ghana is distinct from First National Bank Ghana. FY2025 PAT dropped sharply to GHS 16.7m despite a positive balance sheet, and nine-month 2026 earnings improved. The 2030 base recovers but its downside is loss-making.','The group’s Ghana-specific annual summary pages do not give full IFRS notes; future FX, gross loans/ECL and NPL are unavailable. Capital and eligible reserve screens are proxies. Historical asset changes merit review of actual funding and portfolio movements.'),
'fidelity-bank-ghana':('The privately owned universal bank has substantial 2025 deposits and a 33.1% return on closing equity. September 2026 net loans grew strongly from FY2025. Gemini originated the data work and Codex completed the authorized stewardship.','No full Q3 capital numerator, RWA or gross loan disclosure was available. The downside proxy CAR is above base because slower growth and dividend suspension offset weaker profits. Watch the quality and pricing of rapid loan origination.'),
'first-atlantic-bank':('The bank was listed on the GSE in December 2025 and reported strong asset and deposit expansion over the historical period. Its net LDR is low relative to peers, which leaves earnings sensitive to investment and deposit pricing.','Reserve and settlement sensitivity tests identify material gaps under modeled assumptions. The mandatory BoG cash share varied materially between FY2024 and FY2025. Do not equate the modeled cash pool with regulatory eligibility.'),
'first-national-bank-ghana':('FirstRand group’s Ghana subsidiary returned to positive earnings following 2022 and 2023 losses. At September 2026 it still had a retained deficit of GHS 309.925m; the model assumes no dividend or further equity injection.','The 2030 base shows a profitable recovery but the downside is just below break-even. Capital proxy and trading asset sensitivity are explicitly tested; future gross loan, ECL and regulatory CAR are not directly projected.'),
'gcb':('GCB is the largest accepted bank by FY2025 assets, deposits, and PAT. By September 2026, net loans exceeded GHS 25bn; reported NPL fell to 4.8% from 10.31% FY2025 while CAR moved from 18.02% to 14.6%.','GCB’s GHS 5.19bn 2030 base profit drives a large share of sector growth, while its downside is GHS 0.96bn. Its loan growth and loss assumptions are material to the aggregate; the wider downside needs regular reruns with new source data.'),
'gtbank-ghana':('GTBank has a relatively low net LDR and strong 2025 closing-equity return of 33.3%. September 2026 reported CAR was 24.08% and NPL 3.67%; nine-month actual dividends were GHS 604.370m. Claude’s initial model was repaired by Support as steward.','The Q4 model holds September loan/deposit balances flat; later distributions depend on reserves, capital and distributable profits. Its high downside CAR proxy reflects risk/denominator and payout dynamics, not a prediction of increased regulatory resilience.'),
'nib':('NIB is state-controlled, with negative opening FY2025 equity and a recapitalisation-related turnaround. Average-equity ROE is not meaningful. FY2025 reported NPL was 69.70%; net LDR is extremely low.','The model excludes new government support, dividends and share-deposit reclassification. Downside FY2030 CAR proxy is 11.17% and reserve proxy gaps appear in all modeled scenario-years. The capital structure and source data require further monitoring.'),
'omnibsic-bank':('Conditional closure: FY2021 full annual statement is unavailable; FY2022–FY2025 and September 2026 are the primary historical coverage. Deposits and assets grew rapidly, with a lower FY2026 base profit than FY2025.','Its 2030 base remains profitable but downside is a large loss. FY2025 actual RWA density 22.58% is used as a central proxy; stress densities 38% and 48% are separately shown. September regulatory capital and RWA remain unknown. Do not include in ordinary totals.'),
'prudential-bank':('Conditional closure: September 2026 bank-only statement inaccessible. FY2025 audited data show equity of only GHS 60.9m, CAR -20.19%, NPL 57%, going-concern uncertainty and capital shortfall of GHS 1.012bn. FY2025 profit included an impairment reversal.','The model assumes conditional capital transaction recognition at FY2026 close and tests alternative funding, recognition and tax cases. The actual post-investment position is unavailable. Base remains loss-making through 2030; this is not a current prudential judgment.'),
'republic-bank-ghana':('The listed subsidiary of Republic Financial Holdings was profitable in FY2025, with a relatively high net LDR. September 2026 assets and deposits were lower than FY2025, while net loans rose. DeepSeek originated the model and Codex repaired it.','The downside combines higher operating costs and credit stress; a separate sensitivity tests collateral, wholesale funding and reserve assumptions. 2030 downside PAT is negative but its modeled capital ratio stays above 13%.'),
'societe-generale-ghana':('The listed bank has the highest FY2025 net LDR among the accepted banks, approximately 76.9%. This gives it a different earning-asset and credit-risk profile from liquidity-heavy peers. FY2025 PAT declined from 2024.','The combined downside assumes inflation plus higher opex growth and credit stress. The model preserves actual interim tax and dividend movements. 2030 downside PAT is negative and CAR proxy falls below 13%; the result is sensitive to cost pass-through.'),
'stanbic-bank-ghana':('Stanbic is the third-largest bank by FY2025 assets. It earned GHS 1.61bn in 2025; September 2026 reported CAR was 23.32% and NPL 9.54% versus 24.63% FY2025. DeepSeek’s early model received multiple source and methodology reviews.','The downside 2030 PAT is only GHS 126m versus base GHS 1.21bn. The material difference makes asset yields, funding, impairment and expense growth key sector sensitivities. Reviewers recovered earlier loan-note evidence and resolved the forecast bridges.'),
'standard-chartered-ghana':('The listed Ghana bank had substantial FY2025 earnings and a low net LDR. September 2026 assets and deposits were below FY2025. Claude built the model and Codex accepted the stewardship. Independent reviewers resolved earlier comparative and reserve issues.','The model retains reported 9M tax and dividends, with no extra Q4 dividend; subsequent payouts depend on statutory reserve, earnings and capital. Exact holding company ownership dates and some comparative presentations have caveats.'),
'uba-ghana':('The Ghana subsidiary of United Bank for Africa reported FY2025 NPL of 2.11%, a low ratio relative to peers. PAT rose from GHS 164m in 2024 to GHS 407m in 2025. The model uses the bank-only statements.','The modeled downside rate path initially boosts earnings; by 2030 upside PAT is below base. Regulatory CAR, Tier 1 and NPL forecasts are unavailable; capital figures are calibrated proxies, not regulatory returns.'),
'umb':('Conditional closure: FY2025 annual report and 2026 primary statements are unavailable. September 2025 PAT included a large impairment reversal. July 2026 recapitalisation was reported by the Ministry of Finance but its transaction amount, instrument and regulatory recognition were not verified.','This is a September 2025-anchored counterfactual, not a current post-recapitalisation outlook. PwC Q2 2026 secondary benchmark: assets GHS 16.684bn, deposits GHS 11.5375bn, H1 PBT GHS 195.1m, CAR 13.0%. Do not treat these as primary history or add UMB to ordinary totals.'),
'zenith-bank-ghana':('Zenith has a large deposit franchise and strong FY2025 closing-equity return (32.7%). September 2026 PAT already exceeded the FY2025 total. It is an unlisted subsidiary of Zenith Bank PLC, with Ghana bank-only statements.','Forecast capital uses an equity adjustment and asset-density proxy calibrated to Sep 2026 CAR. Dividend constraints and rate-driven scenario differences were reviewed. Continued funding growth and credit quality matter to the strong base profit trajectory.')
}
# Individual pages: one consistent data sheet per bank.
for i,slug in enumerate(sorted(names)):
    item=B[slug];pr=peer.get(slug,{})
    title(f'Bank profile {i+1:02d} / 23',names[slug],('Ordinary accepted model' if slug in ordinary else 'CONDITIONAL CLOSURE / excluded from ordinary aggregate')+' | GHS millions; percentages where stated.')
    table([['Reported/derived history','FY21','FY22','FY23','FY24','FY25','9M26']]+[[lab]+[fmt(h(slug,y,k)) for y in years] for lab,k in zip(labels,keys)],[120]+[(WIDTH-120)/6]*6,7.9)
    if slug=='consolidated-bank-ghana':
        para('H1-2026 actual (not included above): assets '+fmt(h(slug,'H1-2026','total_assets'))+'m; PAT '+fmt(h(slug,'H1-2026','profit_after_tax'))+'m.','small')
    if slug=='umb':
        para('September 2025 is the last primary interim anchor. FY2025 and 2026 actuals are deliberately blank.','small')
    h2('Five-year model estimates')
    table([['GHS m','2026E','2027E','2028E','2029E','2030E']]+[[s.title()+' PAT']+[fmt(f(slug,y,'profit_after_tax',s)) for y in future] for s in scens]+[['Base assets']+[fmt(f(slug,y,'total_assets')) for y in future],['Base equity']+[fmt(f(slug,y,'total_equity')) for y in future]],[105]+[(WIDTH-105)/5]*5,8)
    if slug in ordinary:
        roa=pr.get('roa_2025_pct');npl=pr.get('reported_npl_2025_pct');car=pr.get('reported_car_2025_pct')
        para('FY25: net LDR '+pct(h(slug,'FY2025','loans_and_advances_net'),h(slug,'FY2025','customer_deposits'))+'; closing-equity ROE '+fmt(num(pr['roe_closing_equity_2025_pct']),1)+'%; reported CAR '+(fmt(num(car),1)+'%' if num(car) is not None else 'n/a')+'; reported NPL '+(fmt(num(npl),1)+'%' if num(npl) is not None else 'n/a')+'. FY30E CAR proxy (base/down/up): '+ '/'.join(fmt(num(pr['car_'+s+'_2030_proxy_pct']),1) for s in scens)+'%.','note')
    para(bank_notes[slug][0])
    para(bank_notes[slug][1])
    para('Evidence trail: '+item['owner']+(' (original); steward '+item['steward'] if item['steward'] else ' (original)')+'; '+item['reviewer']+(' (manifest reviewer)' if slug in ordinary else '')+'. '+str(len(item['h']))+' historical rows; '+str(len(item['f']))+' forecast rows; '+str(item['nsource'])+' reported-source IDs. Rows include unavailable and auxiliary records, not independent audited data points.','small')
    sources([('financials',PINF+'banks/'+slug+'/financials.csv'),('forecast',PINF+'banks/'+slug+'/forecast.csv'),('sources',PINF+'banks/'+slug+'/sources.md'),('method and limitations',PINF+'banks/'+slug+'/README.md'),('claim',ROOT+'claims/'+item['claim'])])
title('Research operations / 01','How the room was organised','A multi-agent research exercise, not a single-agent financial model.')
para('Claude started the banking goal at 12:29:58 UTC on 25 November. Codex, Gemini and the lead began the first claims within four minutes. DeepSeek joined at 12:48, Helper and Support joined to expand capacity, Luna joined at 13:52 and Papa Kojo Agent at 16:16. The eight research participants worked from a shared GitHub repository, not a common conversational memory.')
para('The lead verified 23 licensed banks against the BoG register, established a common model specification, macro assumptions, ownership and review rules. A bank owner first pushed a claim before starting, reducing duplicate work. Agents stored historical CSVs, sources, assumptions, engines, forecasts and checks in a bank-specific folder. An independent reviewer challenged source coverage, arithmetic, economic assumptions and model behaviour.')
para('When an agent paused because of usage limits, the room used explicitly authorised stewardship rather than silent reassignment. The original author remained credited, the steward repaired or completed the work, and the review evidence remained in the repository. Blocked review substitution required two independent exact-version PASS verdicts and finding-by-finding evidence. Shared reporting used a separate accepted-only gate.')
table([['Inventory at completion','Count / scope'],['Research participants before Iconka',str(len(board_ids))],['Licensed bank models',str(len(B))],['Historical CSV records (all banks)',f'{hist_count:,}'],['Forecast CSV records (all banks)',f'{fc_count:,}'],['Bank-specific reported source IDs (sum, not deduplicated)',str(source_ids)],['Review Markdown files',str(sum(1 for x in (G/'reviews').glob('*.md')))],['Assistance files',str(sum(1 for x in (G/'assistance').rglob('*') if x.is_file()))],['Goal-path commits at input pin / sign-off','1,036 / 1,054 (git rev-list)'],['Elapsed setup to sign-off','8h 43m 44s']],[WIDTH-185,185])
para('Counts are file/record counts, not audit tests or unique filings. Git commit count includes documentation, board posts, claim changes, source work, reviews and report publication; it is not a measure of research quality. The commit identity may be the same GitHub account across agents. Attribution uses claims, named boards and review files.','note')
sources([('room rules',REPO+'/blob/main/AGENTS.md'),('completion protocol',REPO+'/blob/main/COMPLETION-PROTOCOL.md'),('goal',ROOT+'GOAL.md'),('signed-off summary',ROOT+'sector/summary.md')])
title('Research operations / 02','Who did the research and coordination','Ownership is taken from claims; reviews from the published peer manifest and board evidence.')
roles={
'claude':'Lead and coordinator: verified roster, shared macro v1.1, authored SCB and GTBank, original QA and roll-up; resolved disputes and conditional scope, assigned final same-pin generation, independently verified 190 peer cells and recorded human sign-off.',
'codex':'Major bank builder and source-recovery contributor; GCB, Access, CBG, First Bank, First Atlantic, NIB, OmniBSIC and UMB. Stewarded Fidelity, SCB and Republic. Recovered issuer materials, independently challenged forecasts and built earnings/stress diagnostics.',
'gemini':'Original Ecobank, CalBank, ADB and Fidelity models; independent macro review, source classifications and later exact-version Ecobank/Omni reviews. At final pin reproduced QA report and verified 258 ordinary plus 72 diagnostic cells.',
'deepseek':'Original Societe Generale, Stanbic and Republic models; sourced annual/interim history and forecast engines. SG and Stanbic accepted; Republic handed off after explicit pause, with original authorship and review findings preserved.',
'claude-helper-1':'Original Absa, UBA and Zenith; initial Prudential claim released. Stewarded ADB and OmniBSIC documentation repair, performed source/engine checks and final clean-LF independent roll-up and peer verification (233 and 199 cells).',
'chatgpt-support':'Built Bank of Africa and First National; stewarded CalBank, GTBank, QA and sector roll-up; developed accepted-only comparison, resolved source and calculation issues, published final reports at exact pin and verified output hashes.',
'gpt-6-luna':'Independent UBA review, source/visual retrieval assistance, CalBank steward repair. Submitted corrected seven-file model on exact fingerprints before pausing; later stewards/reviewers retained the prior blockers until resolved.',
'papa-kojo-agent':'Source researcher, Prudential takeover owner, independent SCB and many bank checks; identified ADB earning-asset/capital defect, helped recover missing source evidence; final raw-data Decimal verification: 818 cells, zero mismatches.'
}
for ag in board_ids:
    h2(ag)
    para(roles[ag])
sources([(a+' board',ROOT+'board/'+a+'.md') for a in board_ids])
title('Research operations / 03','Claim ownership and final peer review','A review listed here is the manifest’s ordinary reviewer, not an exhaustive list of everyone who contributed.')
table([['Bank','Original owner','Final steward','Manifest reviewer']]+[[names[b],B[b]['owner'],B[b]['steward'] or '—',B[b]['reviewer'] if b in ordinary else 'Conditional scope'] for b in sorted(names)],[178,112,111,WIDTH-401],8)
para('Prudential was initially claimed by Helper, released, and reclaimed by Papa Kojo Agent under the takeover record. Luna was an earlier CalBank steward; Support is the final steward. Bank package authorship does not confer independent reviewer eligibility.','note')
sources([('claims directory',REPO+'/tree/main/goals/ghana-bank-models/claims'),('final comparison CSV',PUBF+'sector/peer-comparison/comparison.csv'),('conditional closures',ROOT+'review-resolutions/CONDITIONAL-CLOSURES.md')])
title('Research operations / 04','The timeline and key commits','Selected auditable checkpoints rather than a full listing of the 1,054 goal-path commits through sign-off.')
table([['UTC / 25 Nov','Commit','Event'],['12:29:58','4cb7d80','Goal, claim system and model specification created.'],['12:33:01','a45aa5d','Codex claimed GCB.'],['12:33:21','176aff9','Claude claimed roster verification.'],['12:33:41','501a0af','Claude claimed common macro assumptions.'],['12:33:58','3cd4ac3','GCB source register committed.'],['14:17','Board logs','Lead paused; reduced-team handoff policy later implemented.'],['15:23','7140b0a1 (package)','Luna submitted CalBank repair; needs-review, not closed.'],['16:32','98d28c32','Papa Kojo Agent SCB independent PASS.'],['19:27','01dc72f7','Codex current-version Ecobank independent PASS.'],['20:49','e5e6b3a0 (package)','Helper documentation-only OmniBSIC fix; fresh reviews required.'],['20:55','0dfee1e','Gemini fresh scoped OmniBSIC PASS.'],['21:03:33','b728a09','Final pinned research inputs; all bank/sector inputs frozen.'],['21:07:24','11dffc9','Support published nine exact-pin generated files.'],['21:10:10','43a98ec','Papa independent final 818-check review.'],['21:11:57','1d64cef','Lead peer comparison PASS and final summary.'],['21:12:19','27cf04f','Gemini final QA and sector-rollup PASS.'],['21:13:42','8d695a2','Lead recorded human sign-off.']],[86,106,WIDTH-192],8)
para('Package SHA-256 prefixes are deliberately labeled as package identifiers, not Git commits. Commit IDs are short prefixes of actual repository entries or board-reported commits. The final report source pin predates publication; later board messages do not change the accepted data.','note')
sources([('goal commit history',REPO+'/commits/main/goals/ghana-bank-models'),('final source pin',REPO+'/commit/'+PIN),('report publication',REPO+'/commit/'+PUB),('sign-off',REPO+'/commit/8d695a2')])
title('Research operations / 05','Why independent review mattered','Arithmetic passing is necessary, but it does not guarantee sensible forecasts or faithful accounting classifications.')
para('CalBank: early model reviews found overstated interest income and capital, including a right-of-use asset classification problem. Several repair rounds and stewardship changes followed. The final forecast is lower confidence than an audited regulatory return, but the relevant blockers were preserved and resolved.')
para('ADB: a previously accepted model was reopened after Papa Kojo Agent found omitted earnings on cash and placements in the signed FY2025 report, available gross loan/ECL detail, and a capital numerator that did not reflect regulatory capital. Helper corrected it and independent reviewers passed the revised package. This is evidence that acceptance could be revoked when new facts emerged.')
para('Ecobank: six periods of right-of-use asset reclassification were checked. Codex and Support verified exact new fingerprints without having performed the model repair. Forecast values changed even though the model code and assumptions did not; source classification mattered.')
para('OmniBSIC: the final six-note documentation patch did not change numerical output. Despite this, the package fingerprint changed, requiring fresh scoped PASS verdicts by Support and Gemini. UMB and Prudential remained separate because unavailable primary filings could not be recovered after extensive attempts.')
table([['Final verification (reported by agents)','Result'],['Support generation and Decimal check','258 ordinary + 72 diagnostics; max GHS 0.000499m rounding; 491 peer checks'],['Helper independent recomputation','233 roll-up + 199 peer cells; zero mismatches'],['Papa Kojo Agent independent recomputation','818 checks (258 + 72 + 440 + 48); zero mismatches'],['Gemini independent final QA / roll-up','Byte-identical report; 258 ordinary + 72 diagnostics verified'],['Claude final peer comparison','190 independently recomputed cells, zero mismatches'],['QA across 20 ordinary banks','0 FAIL / 0 WARN'],['Raw conditional QA','2 FAIL + 2 WARN; retained source coverage flags']],[165,WIDTH-165])
para('These test counts overlap. They cannot be added to claim a total of unique verified cells. Tests do not constitute a full audit of the source statements or an independent validation of the forecast assumptions.','small')
sources([('final QA scope',PUBF+'sector/qa-sweep/FINAL-SCOPE.md'),('final QA review',ROOT+'reviews/gemini-of-claude-qa-sweep.md'),('final roll-up review',ROOT+'reviews/claude-helper-1-of-claude-sector-rollup.md'),('lead summary',ROOT+'sector/summary.md')])
title('Research operations / 06','Evidence boundaries and next research priorities','Iconka’s assessment: what the study does well, and where stronger evidence could change its findings.')
para('The strongest aspects are broad bank coverage, reproducible model packages, historical balance-sheet and income bridges, explicit missing values, a common macro input and a review process that caught substantive mistakes. The accepted-only roll-up also avoids mixing incomparable data or quietly admitting incomplete banks.')
para('The greatest weaknesses are reliance on simplified forecast drivers, estimated capital and liquidity proxies, incomplete regulatory notes, and a short observable calibration window. Source spot-checks cannot replace an audit. Some bank README headings still say needs-review even though the signed-off claim and manifest later passed; the final status is governed by the exact accepted package and lead decision, not an old heading.')
h2('Priority follow-up work')
para('1. Retrieve Prudential September 2026, OmniBSIC FY2021 and UMB FY2025/2026 issuer statements; re-review and rebind those packages before admission to an ordinary roll-up. For UMB specifically, reconcile the post-recapitalisation balance sheet and regulatory capital recognition.')
para('2. Refresh FY2026 actuals once published. Compare actual Q4 income and balance sheets with the forecast. Report signed forecast errors bank by bank, identify drivers and revise assumptions only where the evidence supports it.')
para('3. Add a monthly deposit and asset repricing schedule, explicit sovereign holdings and bond maturities, loan vintage/default/migration dynamics, deposit concentration and liquidity runoff. Use regulatory RWA and eligible cash disclosures where possible.')
para('4. Build an evidence-backed macro history, including missing CPI and bill yields, then backtest the forecasting framework before applying it to longer horizons. Use explicit alternate FX paths and funding stress. Do not assign probabilities without a defensible calibration.')
para('5. Track model and source provenance separately from operational coordination. Record missing links, direct visual checks and each model’s source vintage. Retain a versioned, immutable acceptance manifest for later reruns.')
callout('CONCLUSION','The models provide a useful map of Ghanaian banking, rather than an exact picture of future performance. The most credible expectation is a larger system in nominal cedis with diverging bank profitability and a material downside for weaker portfolios. Use the forecasts to ask sharper questions, update them with actual results, and preserve their uncertainty.')
sectsrc()
title('Appendix','Reproduction and references','Source evidence is the signed-off repository; external primary links are those recorded by the agents.')
para('The original room worked at source commit '+PIN+'; final outputs published '+PUB+'; the roll-up input fingerprint is b59a8526d5026b87a05f4a92784148fd1c8f801d2f5f637548dc2454e9f760e3; the macro fingerprint is b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df.')
para('For exact bank work, clone with core.autocrlf=false and check out the source commit. Run Python model.py or Node model.mjs within each bank folder. Use the bank’s sources.md, financials.csv, assumptions.json, forecast.csv and checks.md; files include page references and reported, derived, estimated and unavailable labels.')
para('The final roll-up and peer outputs are published separately. Run rollup.mjs with an external output directory, then --check; run verify_snapshot.py against the input and output. Reproduce peer comparison with compare.mjs and QA with validate.py. The signed-off summary defines accepted and conditional scope. Do not edit frozen bank/sector files merely to regenerate output.')
h2('Main references')
for label,url in [
('1. Verified roster and model specification',PINF+'ROSTER.md'),
('2. Source specification',PINF+'MODEL-SPEC.md'),
('3. Signed-off sector summary',ROOT+'sector/summary.md'),
('4. Published roll-up and CSV',PUBF+'sector/sector-rollup/rollup.md'),
('5. Published peer comparison',PUBF+'sector/peer-comparison/README.md'),
('6. Macro source register',PINF+'sector/macro-assumptions/SOURCES.md'),
('7. Exact acceptance manifest',PUBF+'sector/sector-rollup/manifest.json'),
('8. Conditional closures',ROOT+'review-resolutions/CONDITIONAL-CLOSURES.md'),
('9. QA scope',PUBF+'sector/qa-sweep/FINAL-SCOPE.md'),
('10. Bank-specific source registers and forecast files',REPO+'/tree/'+PIN+'/goals/ghana-bank-models/banks'),
('11. Review evidence',REPO+'/tree/main/goals/ghana-bank-models/reviews'),
('12. Agent boards',REPO+'/tree/main/goals/ghana-bank-models/board')]:
    p('<link href="'+escape(url)+'" color="#006C69">'+escape(label)+'</link>','body')
para('This synthesis recomputes principal totals from the repository CSVs and uses the final peer file for selected capital and profitability ratios. It relies on the room’s source reviews, not a new examination of each original filing. The constant-coverage extrapolation is new, illustrative analysis.','note')

out=D/'Ghana_Banking_Sector_Research_2026-2030.pdf'
def footer(c,doc):
    c.saveState();c.setStrokeColor(L);c.line(45,39,W-45,39);c.setFillColor(M);c.setFont('Helvetica',8)
    c.drawString(45,26,'ICONKA  /  GHANA BANKING SECTOR RESEARCH  /  25 NOV 2026')
    c.drawRightString(W-45,26,f'{doc.page:02d}')
    c.restoreState()
doc=SimpleDocTemplate(str(out),pagesize=A4,leftMargin=45,rightMargin=45,topMargin=43,bottomMargin=50,title='Ghana Banking Sector Outlook 2026 to 2030',author='Iconka | Agentroom',subject='Signed-off bank research synthesis',pageCompression=1)
md_out=D/'Ghana_Banking_Sector_Research_2026-2030.md'
if '--markdown-only' in sys.argv or '--with-markdown' in sys.argv:
    md_out.write_text('\n\n'.join(markdown)+'\n',encoding='utf-8',newline='\n')
    print('MARKDOWN',md_out,md_out.stat().st_size,'SHA256',hashlib.sha256(md_out.read_bytes()).hexdigest(),'blocks',len(markdown))
if '--markdown-only' not in sys.argv:
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
print('CREATED',out,'planned pages',pages,'bytes',out.stat().st_size,'SHA256',hashlib.sha256(out.read_bytes()).hexdigest())
print('COUNTS',hist_count,fc_count,source_ids,'aggregate cross-checks',len(match),'max',max(match) if match else 'n/a')
