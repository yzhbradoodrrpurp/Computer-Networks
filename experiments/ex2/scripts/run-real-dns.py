#!/usr/bin/env python3
"""Run lab B with real ping/nslookup and Wireshark dumpcap; requires root for BPF/cache flush."""
import os,subprocess,time,json,signal,pwd,datetime
from pathlib import Path
R=Path(__file__).resolve().parents[1]; E=R/'evidence'
SUPPLEMENT=os.environ.get('EX2_SUPPLEMENT')=='1'
FINAL=os.environ.get('EX2_FINAL')=='1'
if SUPPLEMENT:E=E/'supplement'
if FINAL:E=R/'evidence/final'
E.mkdir(exist_ok=True)
USER=os.environ.get('SUDO_USER')
if os.geteuid()!=0 or not USER:raise SystemExit('Please run via sudo /bin/bash scripts/capture-real-dns.sh')
account=pwd.getpwnam(USER); actions=[]
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def command(name,args,timeout=20):
 item={'name':name,'command':args,'start_utc':stamp(),'start_epoch':time.time()}
 try:
  p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=timeout)
  item.update(returncode=p.returncode,output=p.stdout)
 except subprocess.TimeoutExpired as e:item.update(returncode=124,output=(e.stdout or b'').decode(errors='replace') if isinstance(e.stdout,bytes) else e.stdout or '')
 item.update(end_utc=stamp(),end_epoch=time.time());actions.append(item)
 (E/(name+'.txt')).write_text('$ '+' '.join(args)+'\n'+item['output'])
 (E/'real-actions.json').write_text(json.dumps(actions,ensure_ascii=False,indent=2))
 print(name, 'exit',item['returncode'],flush=True)
 time.sleep(.6)
def flush(prefix):
 command(prefix+'-flush',['/usr/bin/dscacheutil','-flushcache'])
 command(prefix+'-mdns-hup',['/usr/bin/killall','-HUP','mDNSResponder'])
 time.sleep(2)
cap=E/'2023141220023_易治行_实验2_DNS.pcapng'
if cap.exists():raise SystemExit('Capture already exists; preserve it before another run.')
command('os-version',['/usr/bin/sw_vers'])
command('resolver-config',['/usr/sbin/scutil','--dns'])
command('interface-en0',['/sbin/ifconfig','en0'])
command('dumpcap-version',['/Applications/Wireshark.app/Contents/MacOS/dumpcap','--version'])
log=open(E/'dumpcap.log','w')
filt='port 53 or icmp' if (SUPPLEMENT or FINAL) else '((host 202.115.39.9 or host 202.115.39.6) and port 53) or icmp'
interface='pktap,all' if SUPPLEMENT else 'en0'
p=subprocess.Popen(['/Applications/Wireshark.app/Contents/MacOS/dumpcap','-i',interface,'-f',filt,'-a','duration:180','-w',str(cap)],stdout=log,stderr=log)
try:
 time.sleep(2)
 if p.poll() is not None:raise RuntimeError((E/'dumpcap.log').read_text())
 if cap.exists():os.chown(cap,account.pw_uid,account.pw_gid)
 print('正在抓取 DNS；将自动清缓存、执行四次 ping 和四次 nslookup，完成后自动结束。',flush=True)
 for domain,key in [('www.baidu.com','baidu'),('www.scu.edu.cn','scu')]:
  flush(key)
  command(key+'-ping-first',['/sbin/ping','-c','3','-i','0.3','-W','1000',domain],15)
  command(key+'-ping-repeat',['/sbin/ping','-c','3','-i','0.3','-W','1000',domain],15)
  command(key+'-cache',['/usr/bin/dscacheutil','-cachedump','-entries','Host'])
 for domain,key in [('www.baidu.com.','baidu'),('www.scu.edu.cn.','scu')]:
  for typ in ['A','CNAME']:
   command(key+'-nslookup-'+typ,['/usr/bin/nslookup','-type='+typ,domain,'202.115.39.9'])
 time.sleep(2)
finally:
 if p.poll() is None:p.send_signal(signal.SIGINT)
 try:p.wait(timeout=10)
 except subprocess.TimeoutExpired:p.terminate();p.wait(timeout=5)
 log.close()
 for file in E.iterdir():
  if file.is_file():os.chown(file,account.pw_uid,account.pw_gid)
print('抓包与命令记录已保存：'+str(cap),flush=True)
