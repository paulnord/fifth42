import json,sys
from pathlib import Path
out=Path(sys.argv[1]);rows=[]
for p in sorted(out.glob('tpi*-count*/report.json')):
 r=json.loads(p.read_text());r['case']=p.parent.name;r['gpu_timing_log']=(p.parent/'gpu.stderr').read_text();rows.append(r)
(out/'SUMMARY.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Completed test groups:',len(rows));print('Report:',out/'SUMMARY.json')
