import os,subprocess,json,time,pathlib
p=pathlib.Path(__file__).resolve().parent;cpu=min(os.sched_getaffinity(0));os.sched_setaffinity(0,{cpu})
for case,targets in [('small1000','-42,42'),('high8','-42,42'),('high32','-42,42'),('controls100','12,384,2951,-960')]:
 start=time.perf_counter()
 r=subprocess.run([str(p/'bench'),targets,'7'],stdin=(p/(case+'.packet')).open(),stdout=(p/(case+'.results.json')).open('w'),stderr=subprocess.PIPE,text=True,timeout=90)
 print(case,r.returncode,round(time.perf_counter()-start,3),r.stderr,flush=True)
 if r.returncode:raise RuntimeError(r.stderr)
 d=json.loads((p/(case+'.results.json')).read_text());print({k:v for k,v in d.items() if k not in ('hits','timings')},flush=True);print({k:round(v['median_seconds'],6) for k,v in d['timings'].items()},flush=True)
(p/'machine.json').write_text(json.dumps(dict(cpu=cpu,platform=__import__('platform').platform(),compiler=subprocess.check_output(['g++','--version'],text=True).splitlines()[0]),indent=2))
