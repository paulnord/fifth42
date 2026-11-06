import json,pathlib,subprocess,os
p=pathlib.Path(__file__).parent
src=p.parent/'fifth42-other-sieves-20261106'
packets=p.parent/'fifth42-primitivity-20261106'
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
rows=[]
for case,arg,cap in [('small1000','-42,42',42),('high8','-42,42',42),('high32','-42,42',42),('controls100','12,384,2951,-960',2951),('small1000','interval',42),('high8','interval',42),('high32','interval',42),('controls100','interval',2951)]:
 name=case+('.interval' if arg=='interval' else '.target')
 with (packets/(case+'.packet')).open() as f:
  result=subprocess.run([str(p/'bench-rebuilt'),arg,str(cap),'1'],stdin=f,capture_output=True,text=True,check=True)
 d=json.loads(result.stdout);prior=json.loads((src/(name+'.json')).read_text())
 for k in ['all','shape','equal_hit_sets','hit_records','hits']:assert d[k]==prior[k],(name,k)
 for k in prior['variants']:assert d['variants'][k]['exact_tests']==prior['variants'][k]['exact_tests'],(name,k)
 row={'sample':name,'exact_counts_and_hits_match':True,'points':d['all'],'shape':d['shape'],'hits':d['hit_records']}
 rows.append(row);print(row,flush=True)
(p/'packet-recheck.json').write_text(json.dumps(rows,indent=2)+'\n')
