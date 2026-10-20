from pathlib import Path
import subprocess,json,datetime
R=Path(__file__).resolve().parents[1]; E=R/'evidence'
tshark='/Applications/Wireshark.app/Contents/MacOS/tshark'
cap=E/'wireshark-browser.pcapng'
def run(*args):return subprocess.check_output([tshark,'-2','-r',str(cap),*args],text=True)
(E/'final-http-details.txt').write_text(run('-Y','http','-V'))
(E/'final-http.json').write_text(run('-Y','http','-T','json','--no-duplicate-keys'))
(E/'final-http-summary.tsv').write_text(run('-Y','http','-T','fields','-e','frame.number','-e','tcp.stream','-e','ip.src','-e','tcp.srcport','-e','ip.dst','-e','tcp.dstport','-e','http.request.method','-e','http.request.uri','-e','http.response.code','-e','http.request_in','-e','http.response_in','-e','http.request.line','-e','http.response.line'))
packets=json.loads((E/'final-http.json').read_text())
L=[p['_source']['layers'] for p in packets]
def scalar(v):return v[0] if isinstance(v,list) else v
def num(p):return int(p['frame']['frame.number'])
def reqs(path):return [p for p in L if path in scalar(p.get('http',{}).get('http.request.full_uri','')) and 'http.request' in p['http']]
def response(req):return next(p for p in L if scalar(p.get('http',{}).get('http.request_in',''))==str(num(req)))
b=reqs('file1.html')[0];br=response(b)
first,cond=reqs('file2.html');fr=response(first);cr=response(cond)
fav=next(p for p in reqs('/favicon.ico') if p['tcp']['tcp.stream']==b['tcp']['tcp.stream']);favr=response(fav)
A=json.loads((E/'final-actions.json').read_text())['log']
def when(action):
 t=next(a['time'] for a in A if a['action']==action)
 return (datetime.datetime.fromisoformat(t.replace('Z','+00:00'))+datetime.timedelta(hours=8)).strftime('%H:%M:%S')
data={'formal':True,'frames':{'basic_req':num(b),'basic_res':num(br),'favicon_req':num(fav),'favicon_res':num(favr),'first_req':num(first),'first_res':num(fr),'cond_req':num(cond),'cond_res':num(cr)},'client':b['ip']['ip.src'],'server':b['ip']['ip.dst'],'basic_port':b['tcp']['tcp.srcport'],'basic_stream':b['tcp']['tcp.stream'],'basic_tcp_len':br['tcp']['tcp.len'],'first_time':when('first'),'second_time':when('second'),'reload_time':when('reload')}
assert br['http']['http.content_length_header']=='128'
assert fr['http']['http.content_length_header']=='371'
assert any('304' in key for key in cr['http'])
assert not cr['http'].get('http.file_data')
assert b['tcp']['tcp.stream']==fav['tcp']['tcp.stream']
assert next(a['cache'] for a in A if a['action']=='cacheObservation')[0]['transferSize']==0
(E/'report-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2));print(json.dumps(data,ensure_ascii=False,indent=2))
