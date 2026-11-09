"""Run finite scratch commands; abort own process group on resource conflict."""
import json,os,signal,subprocess,sys,time
from pathlib import Path
root=Path(__file__).resolve().parent
name=sys.argv[1];command=sys.argv[2:]
log=root/(name+'-resources.jsonl')
clock=os.sysconf('SC_CLK_TCK')
def processes():
 out={}
 for p in Path('/proc').iterdir():
  if not p.name.isdigit():continue
  try:
   s=(p/'stat').read_text();a=s[s.rindex(')')+2:].split()
   out[int(p.name)]=(int(a[1]),int(a[11])+int(a[12]),s[s.index('(')+1:s.rindex(')')])
  except (OSError,ValueError,IndexError):pass
 return out
def descendants(allp):
 ids={os.getpid()};old=set()
 while ids!=old:
  old=set(ids);ids.update(p for p,v in allp.items() if v[0] in ids)
 return ids
def gpu():
 s=subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader,nounits'],text=True,timeout=5).strip()
 return [int(x) for x in s.splitlines() if x]
if gpu():raise RuntimeError('GPU already has compute work')
prior=processes();previous=time.monotonic();began=previous
with (root/(name+'.txt')).open('w') as stream:
 proc=subprocess.Popen(command,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
 try:
  while proc.poll() is None:
   time.sleep(.5);now=time.monotonic();current=processes();own=descendants(current)
   foreign_gpu=[p for p in gpu() if p not in own]
   busy=[]
   for pid,(ppid,ticks,cmd) in current.items():
    if pid in own or pid not in prior:continue
    rate=(ticks-prior[pid][1])/clock/(now-previous)
    if rate>.5:busy.append(dict(pid=pid,command=cmd,cpu_cores=rate))
   row=dict(elapsed=now-began,foreign_gpu=foreign_gpu,foreign_busy_cpu=busy,load=os.getloadavg())
   with log.open('a') as out:out.write(json.dumps(row)+'\n')
   if foreign_gpu or busy:raise RuntimeError('Resource conflict: '+json.dumps(row))
   if now-began>600:raise TimeoutError('Overall finite scratch stage budget')
   prior=current;previous=now
  rc=proc.wait()
  if rc:raise RuntimeError(f'{name}: exit {rc}; see {name}.txt')
 except BaseException as error:
  if proc.poll() is None:
   os.killpg(proc.pid,signal.SIGTERM)
   try:proc.wait(timeout=3)
   except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
  (root/(name+'-failure.json')).write_text(json.dumps(dict(error=str(error),command=command,seconds=time.monotonic()-began),indent=2)+'\n')
  raise
(root/(name+'-execution.json')).write_text(json.dumps(dict(command=command,exit_code=rc,seconds=time.monotonic()-began),indent=2)+'\n')
print(name,'passed',round(time.monotonic()-began,3),'seconds')
