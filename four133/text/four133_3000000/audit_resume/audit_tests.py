import importlib.util,json,subprocess,hashlib,shutil
from pathlib import Path
R=Path(__file__).resolve().parent
D=R/'isolated/run_incremental.py'
s=importlib.util.spec_from_file_location('driver',D);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def run(p,*extra):
 return subprocess.run(['python3',str(D),'--test','--run-dir',str(p),'--chunk-size','3',*extra],capture_output=True,text=True)
def clone(name):
 p=R/name
 if p.exists():shutil.rmtree(p)
 shutil.copytree(R/'run',p);return p
results={}
p=clone('partial'); logs=sorted(p.glob('*.log'));target=logs[0];original=target.read_bytes();target.with_suffix('.partial').write_bytes(original[:original.find(b'CHECKPOINT')+50]);target.unlink()
j=json.loads((p/'progress.json').read_text()); j['chunks']=[c for c in j['chunks'] if c['branch']!='22' or c['start']!=1]; (p/'progress.json').write_text(json.dumps(j))
r=run(p);results['truncated_partial_reexecuted']=r.returncode==0 and target.exists() and not target.with_suffix('.partial').exists()
# Timing differs but exact counters and per-gap candidate tuples must agree.
def normalized(p):
 j=json.loads((p/'progress.json').read_text());return [(c['branch'],c['start'],c['end'],*[c[k] for k in m.KEYS],c['candidates']) for c in j['chunks']]
results['partial_restart_same_computation']=normalized(p)==normalized(R/'run')
p=clone('completed');hashes={x.name:m.digest(x) for x in p.glob('*.log')};r=run(p);results['all_existing_no_execution']=r.returncode==0 and 'RUNNING' not in r.stdout and hashes=={x.name:m.digest(x) for x in p.glob('*.log')}
p=clone('tamper');x=sorted(p.glob('*.log'))[-1];x.write_text(x.read_text().replace('wall=','wall=0',1));r=run(p);results['changed_completed_rejected']=r.returncode!=0 and 'Completed chunk changed' in r.stderr
p=clone('truncated_complete');x=sorted(p.glob('*.log'))[0];x.write_text(x.read_text().split('CHUNK_DONE')[0]);r=run(p);results['truncated_complete_rejected']=r.returncode!=0
p=clone('config_mismatch');c=json.loads((p/'config.json').read_text());c['previous_bound']=499;(p/'config.json').write_text(json.dumps(c));r=run(p);results['config_mismatch_rejected']=r.returncode!=0 and 'configuration differs' in r.stderr
p=clone('hash_drop');logs=sorted(p.glob('*.log'));logs[0].unlink();r=run(p,'--max-new-chunks','0');saved=json.loads((p/'progress.json').read_text());x=logs[-1];x.write_text(x.read_text().replace('wall=','wall=0',1));r2=run(p);results['missing_recorded_chunk_rejected_without_hash_loss']=r.returncode!=0 and saved['completed_chunks']==19 and r2.returncode!=0
config=json.loads((R/'run/config.json').read_text());specs=list(m.specs(config));covered={b:[h for sp in specs if sp['branch']==b for h in range(sp['start'],sp['end']+1)] for b in ['22','31pos','31neg']};results['test_exact_branch_h_union']=all(v==list(range(1,m.max_gap(b,1000,42 if b=='22' else 1200)+1)) for b,v in covered.items());results['test_ranges']={k:[min(v),max(v),len(v)] for k,v in covered.items()}
c=dict(config,bound=3000000,previous_bound=2100000,test_mode=False,test_sum=None,moduli=m.MODULI,chunk_size=1024);ps=list(m.specs(c));results['production_exact_branch_modulus_h_union']=all([h for sp in ps if sp['branch']==b and sp['modulus']==mod for h in range(sp['start'],sp['end']+1)]==list(range(1,m.max_gap(b,3000000,42 if b=='22' else m.D-42 if b=='31neg' else m.D+42)+1)) for mod in m.MODULI for b in covered);results['production_chunk_count']=len(ps);results['production_gap_limits']={b:m.max_gap(b,3000000,42 if b=='22' else m.D-42 if b=='31neg' else m.D+42) for b in covered};results['source_sha']=m.digest(R/'isolated/search133_incremental.cpp');results['driver_sha']=m.digest(D)
(R/'audit_report.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))

p=clone('noncontiguous');x=sorted(p.glob('*.log'))[0];x.unlink();j=json.loads((p/'progress.json').read_text());j['chunks']=[c for c in j['chunks'] if c['branch']!='22' or c['start']!=1];(p/'progress.json').write_text(json.dumps(j));r=run(p,'--max-new-chunks','0');j=json.loads((p/'progress.json').read_text());results['noncontiguous_completed_hashes_retained']=r.returncode==0 and len(j['chunks'])==18;r=run(p);results['noncontiguous_resume_completes']=r.returncode==0 and normalized(p)==normalized(R/'run')
import sys,io,contextlib
v=m.validate_chunk
def inject(*args):
 rec=v(*args)
 if rec['branch']=='22' and rec['start']==1:rec['exact_solutions']=[{'fault_injection':True}]
 return rec
m.validate_chunk=inject;p=clone('existing_exact_fault_injection');sys.argv=['driver','--test','--run-dir',str(p),'--chunk-size','3'];out=io.StringIO()
with contextlib.redirect_stdout(out):m.main()
results['existing_exact_stop_fault_injection']=json.loads((p/'progress.json').read_text())['status']=='exact_solution_found' and 'RUNNING' not in out.getvalue()
(R/'audit_report.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
