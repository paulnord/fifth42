import os,sys,json,pathlib,subprocess,hashlib,shutil,fcntl,time
BASE=pathlib.Path(__file__).resolve().parent; FIX=BASE/'fixture'; DRIVER=FIX/'run_parallel.py'
results=[]
def run(name,*args,ok=True):
 p=subprocess.run([sys.executable,str(DRIVER),'--test','--run-dir',str(BASE/name),'--chunk-size','4',*args],capture_output=True,text=True)
 (BASE/(name+'.stdout')).write_text(p.stdout+p.stderr)
 assert (p.returncode==0)==ok,(name,p.returncode,p.stdout,p.stderr)
 return p
def progress(name): return json.loads((BASE/name/'progress.json').read_text())
run('resume','--workers','3','--max-new-chunks','2');p=progress('resume');assert p['completed_chunks']==2 and p['status']=='paused';results.append('Parallel bounded dispatch: 2 completions and no extra chunks')
part=BASE/'resume/m97_22_h00009_00012.partial';part.write_text('INTERRUPTED INCOMPLETE DATA\n')
run('resume','--workers','2','--max-new-chunks','1');p=progress('resume');assert p['completed_chunks']==3 and not part.exists();results.append('Worker-count 3 to 2 resume and incomplete partial rerun passed')
run('resume','--workers','4');p=progress('resume');assert p['completed_chunks']==15 and p['completed_checkpoints']==53 and p['status']=='completed_awaiting_independent_audit';assert len({(r['branch'],r['start']) for r in p['chunks']})==15;results.append('All three branches: unique dispatch, 15 chunks / 53 checkpoints, 4-worker completion')
run('resume','--workers','1');assert progress('resume')['completed_chunks']==15;results.append('Fully completed restart launches no work')
shutil.copytree(BASE/'resume',BASE/'tamper');log=next((BASE/'tamper').glob('*.log'));log.write_text(log.read_text().replace('wall=','wall=0',1));run('tamper','--workers','2',ok=False);results.append('Changed completed log hash rejected')
shutil.copytree(BASE/'resume',BASE/'missing');next((BASE/'missing').glob('*.log')).unlink();run('missing',ok=False);results.append('Missing previously recorded log rejected')
(BASE/'stop').mkdir();(BASE/'stop/STOP').touch();run('stop','--workers','3');assert progress('stop')['completed_chunks']==0 and progress('stop')['status']=='paused';results.append('Preexisting STOP dispatches no work')
(BASE/'lock').mkdir();lock=(BASE/'lock/run.lock').open('a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);run('lock',ok=False);lock.close();results.append('Contending coordinator rejected before build/config mutation')
(BASE/'results.json').write_text(json.dumps(results,indent=2));print('\n'.join(results))
