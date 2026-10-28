#!/usr/bin/env python3
"""Extract original DNS fields and associate commands using recorded time windows."""
from pathlib import Path
import subprocess,json,csv,os,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];E=R/'evidence'
if os.environ.get('EX2_FINAL')=='1':E=E/'final'
O=R/'evidence/final-analysis' if os.environ.get('EX2_FINAL')=='1' else E
O.mkdir(exist_ok=True)
TS='/Applications/Wireshark.app/Contents/MacOS/tshark'
cap=E/'2023141220023_易治行_实验2_DNS.pcapng'
if not cap.exists():raise SystemExit('Formal capture is not available yet.')
base=[TS,'-n','-r',str(cap)]
fil='dns.qry.name == "www.baidu.com" || dns.qry.name == "www.scu.edu.cn"'
for name,args in [('real-dns-details.txt',['-Y',fil,'-V']),('real-dns.json',['-Y',fil,'-T','json','--no-duplicate-keys']),('real-dns.pdml',['-Y',fil,'-T','pdml']),('icmp-summary.txt',['-Y','icmp','-T','fields','-e','frame.number','-e','frame.time_epoch','-e','ip.src','-e','ip.dst','-e','icmp.type'])]:
 p=subprocess.run(base+args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
 (O/name).write_bytes(p.stdout)
actions=json.loads((E/'real-actions.json').read_text());root=ET.parse(O/'real-dns.pdml').getroot();packets=[]
for packet in root.findall('packet'):
 fields={}
 for field in packet.iter('field'):
  if field.get('name'):fields.setdefault(field.get('name'),[]).append(field.get('show',field.get('value','')))
 def first(k):return fields.get(k,[''])[0]
 epoch=float(first('frame.time_epoch'))
 matches=[x['name'] for x in actions if x['start_epoch']<=epoch<=x['end_epoch']]
 d={'frame':int(first('frame.number')),'time_epoch':epoch,'actions':matches,'src':first('ip.src'),'dst':first('ip.dst'),'sport':first('udp.srcport') or first('tcp.srcport'),'dport':first('udp.dstport') or first('tcp.dstport'),'transport':'UDP' if first('udp.srcport') else 'TCP','id':first('dns.id'),'response':first('dns.flags.response'),'AA':first('dns.flags.authoritative'),'RD':first('dns.flags.recdesired'),'RA':first('dns.flags.recavail'),'rcode':first('dns.flags.rcode'),'query':first('dns.qry.name'),'qtype':first('dns.qry.type'),'response_to':first('dns.response_to'),'response_in':first('dns.response_in'),'answers':first('dns.count.answers'),'CNAME':fields.get('dns.cname',[]),'A':fields.get('dns.a',[]),'AAAA':fields.get('dns.aaaa',[]),'RR_names':fields.get('dns.resp.name',[]),'RR_types':fields.get('dns.resp.type',[]),'TTL':fields.get('dns.resp.ttl',[]),'resource_records':[]}
 for group in packet.iter('field'):
  if group.get('show') not in ['Answers','Authoritative nameservers','Additional records']:continue
  for field in group:
   kids=list(field)
   if any(f.get('name')=='dns.resp.name' for f in kids):
    d['resource_records'].append({'section':group.get('show'),'summary':field.get('showname',field.get('show')),'fields':{k.get('name'):k.get('show',k.get('value')) for k in kids if k.get('name')}})
 packets.append(d)
(O/'analysis.json').write_text(json.dumps(packets,ensure_ascii=False,indent=2))
with (O/'real-dns-summary.tsv').open('w') as f:
 cols=['frame','actions','src','dst','sport','dport','transport','id','response','AA','RD','RA','rcode','query','qtype','response_to','response_in','answers','CNAME','A','TTL']
 w=csv.DictWriter(f,fieldnames=cols,delimiter='\t',extrasaction='ignore');w.writeheader();w.writerows(packets)
print(json.dumps(packets,ensure_ascii=False,indent=2))
