import os,sys,json,pathlib,subprocess,time,fcntl,importlib.util
BASE=pathlib.Path(__file__).resolve().parent
if len(sys.argv)>1:
 mode=sys.argv[1]; fixture=BASE/'fixture';spec=importlib.util.spec_from_file_location('driver',fixture/'run_parallel.py');d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
 original_run=d.subprocess.run;original_validate=d.validate_chunk
 def run(cmd,**kw):
  if str(cmd[0]).find('engine_')<0:return original_run(cmd,**kw)
  start=int(cmd[5]);rd=BASE/mode
  if mode=='crash':
   code='import os,sys,time;open(sys.argv[1],"w").write(str(os.getpid()));time.sleep(3);os.execv(sys.argv[2],sys.argv[2:])'
   return original_run([sys.executable,'-c',code,str(rd/'child.pid'),*cmd],**kw)
  time.sleep(.25 if start==1 else .05)
  if mode=='failure' and start==1:raise RuntimeError('injected worker failure')
  if mode=='active_stop' and start==1:(rd/'STOP').touch()
  return original_run(cmd,**kw)
 def validate(path,*a):
  r=original_validate(path,*a)
  if mode=='exact' and r['start']==5:r['exact_solutions']=[{'test_only':'injected stop-control signal'}]
  return r
 d.subprocess.run=run;d.validate_chunk=validate
 sys.argv=['run_parallel.py','--test','--run-dir',str(BASE/mode),'--chunk-size','4','--workers','3' if mode!='crash' else '1']
 d.main();sys.exit()
results=[]
for mode in ['outorder','failure','active_stop','exact']:
 p=subprocess.run([sys.executable,__file__,mode],capture_output=True,text=True);(BASE/(mode+'.stdout')).write_text(p.stdout+p.stderr)
 j=json.loads((BASE/mode/'progress.json').read_text())
 assert p.returncode==(1 if mode=='failure' else 0)
 if mode=='outorder':assert 'h00001_' not in next(x for x in p.stdout.splitlines() if x.startswith('CHUNK_OK'));assert j['completed_chunks']==15
 if mode=='failure':assert j['status']=='failed' and len(j['errors'])>=1 and j['completed_chunks']>0
 if mode=='active_stop':assert j['status']=='paused' and 3<=j['completed_chunks']<15
 if mode=='exact':assert j['status']=='exact_solution_found' and 3<=j['completed_chunks']<=4
 results.append(dict(mode=mode,status=j['status'],completed=j['completed_chunks']))
out=(BASE/'crash.stdout').open('w');p=subprocess.Popen([sys.executable,__file__,'crash'],stdout=out,stderr=out)
pidfile=BASE/'crash/child.pid'
while not pidfile.exists():time.sleep(.02)
child=int(pidfile.read_text());p.kill();p.wait();lock=(BASE/'crash/run.lock').open('a+')
try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
except BlockingIOError:pass
else:raise AssertionError('Run lock escaped orphan child')
os.kill(child,0)
results.append({'mode':'crash','finding':'SIGKILL parent: inherited child flock blocks restart until engine exits','child_pid':child})
time.sleep(3.2);fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);lock.close()
p=subprocess.run([sys.executable,str(BASE/'fixture/run_parallel.py'),'--test','--run-dir',str(BASE/'crash'),'--chunk-size','4','--workers','2'],capture_output=True,text=True)
assert p.returncode==0,(p.stdout,p.stderr)
assert json.loads((BASE/'crash/progress.json').read_text())['completed_chunks']==15
results.append({'mode':'crash_resume','finding':'Resume succeeds after orphan exit; partial reexecuted and all 15 chunks complete'})
(BASE/'scenario_results.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
