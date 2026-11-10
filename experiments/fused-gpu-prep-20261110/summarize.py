import json,sys
from pathlib import Path
root=Path(sys.argv[1]);reports=[]
for p in sorted(root.glob('*/report.json')):
 d=json.loads(p.read_text());d['path']=str(p.relative_to(root));reports.append(d)
(root/'SUMMARY.json').write_text(json.dumps({'scope':'NOT production throughput. Fused roots+geometry; normalization, LLL, bounds, certificates on CPU. No candidate enumeration. Warm estimates exclude host process/preflight/serialization. Cold totals include2 kernel passes.', 'reports':reports},indent=2)+'\n')
print('Reports:',len(reports),'See SUMMARY.json; do not promote any variant from kernel-only time.')
