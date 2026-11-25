import re,difflib,sys
md=open('/home/claude/agentroom/goals/ghana-bank-models/reports/iconka/Ghana_Banking_Sector_Research_2026-2030.md',encoding='utf-8').read()
pdf=open('/tmp/pp/paper.txt',encoding='utf-8').read()
def strip_md(s):
    s=re.sub(r'\[([^\]]*)\]\([^)]*\)',r'\1',s)           # links -> text
    s=re.sub(r'^\|?\s*[-: |]+\|?\s*$','',s,flags=re.M)     # table separators
    s=s.replace('|',' ')
    s=re.sub(r'[#*`>]','',s)
    return s
def words(s): return re.findall(r"[A-Za-z0-9À-ɏ.,%$£()\-–—’'/:;+=<>&]+",s)
a=words(strip_md(md)); b=words(pdf)
print(len(a),len(b))
# compare as multisets of tokens first
from collections import Counter
ca,cb=Counter(a),Counter(b)
onlymd={k:v-cb.get(k,0) for k,v in ca.items() if v>cb.get(k,0)}
onlypdf={k:v-ca.get(k,0) for k,v in cb.items() if v>ca.get(k,0)}
print('tokens more in MD than PDF:',sum(onlymd.values()),'; more in PDF than MD:',sum(onlypdf.values()))
print(sorted(onlymd.items(),key=lambda x:-x[1])[:60])
print(sorted(onlypdf.items(),key=lambda x:-x[1])[:60])
