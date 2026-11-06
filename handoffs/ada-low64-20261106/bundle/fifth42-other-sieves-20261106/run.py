import os,subprocess,json,pathlib,time
p=pathlib.Path(__file__).resolve().parent; q=p.parent/'fifth42-primitivity-20261106'
cpu=min(os.sched_getaffinity(0)); os.sched_setaffinity(0,{cpu})
for case,arg,cap in [('small1000','-42,42',42),('high8','-42,42',42),('high32','-42,42',42),('controls100','12,384,2951,-960',2951),('small1000','interval',42),('high8','interval',42),('high32','interval',42),('controls100','interval',2951)]:
 name=case+('.interval' if arg=='interval' else '.target');start=time.perf_counter()
 subprocess.run([str(p/'bench'),arg,str(cap),'11'],stdin=(q/(case+'.packet')).open(),stdout=(p/(name+'.json')).open('w'),check=True,timeout=120)
 d=json.loads((p/(name+'.json')).read_text());print(name,round(time.perf_counter()-start,2),{k:d[k] for k in ['all','shape','equal_hit_sets','hit_records']},flush=True);print(d['variants'],flush=True)
(p/'machine.json').write_text(json.dumps({'cpu':cpu,'compiler':subprocess.check_output(['g++','--version'],text=True).splitlines()[0],'platform':__import__('platform').platform()},indent=2))
