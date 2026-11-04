#!/usr/bin/env python3
"""Rerun archived audits only in disposable copies; preserve all frozen evidence."""
import hashlib,json,subprocess,sys,time
from pathlib import Path

ROOT=Path(__file__).resolve().parent
HANDOFF=ROOT.parent/'four133-handoff'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    start=time.monotonic();records=[]
    subprocess.run([sys.executable,str(HANDOFF/'verify_bundle.py')],cwd=HANDOFF,check=True)
    for bound in (2100000,3000000,4000000):
        name='four133_extension' if bound==2100000 else f'four133_{bound}'
        copy=HANDOFF/'fresh-audits'/str(bound)/name
        frozen=HANDOFF/'frozen'/name
        commands=([['audit_independent_counts.py','run_2100000.log'],['audit_independent_counts.py','run_2100000_mod2.log'],['audit_complementary_independent.py']]
                  if bound==2100000 else [['audit_production_counts.py','--require-complete']])
        for command in commands:
            p=subprocess.run([sys.executable,*command],cwd=copy,capture_output=True,text=True,check=True)
            (copy/(command[0]+('.mod2' if 'mod2' in ' '.join(command) else '')+'.fresh-output.txt')).write_text(p.stdout)
        names=['audit_independent_counts.json','audit_independent_counts_mod2.json'] if bound==2100000 else ['audit_production_report.json']
        for report in names:
            fresh=json.loads((copy/report).read_text());old=json.loads((frozen/report).read_text())
            fresh.pop('seconds',None);old.pop('seconds',None)
            assert fresh==old,(bound,report)
        records.append({'bound':bound,'audit_reports':{f:sha(frozen/f) for f in names},'raw_log_sha256':{str(p.relative_to(frozen)):sha(p) for p in (frozen/'runs').glob('*.log')} if bound>2100000 else {p.name:sha(p) for p in frozen.glob('run_2100000*.log')},'complete':True,'exact_solutions':[]})
    subprocess.run([sys.executable,str(HANDOFF/'verify_bundle.py')],cwd=HANDOFF,check=True)
    result={'archive_sha256':sha(HANDOFF/'four133_4000000_reproduction.tar.gz'),'archive_bytes':5749673,'pinned_commit':'6160c2f765c3898cb328968ad823dd13badd0ddd','verified_bound':4000000,'frozen_evidence_preserved':True,'fresh_raw_log_audits':records,'seconds':time.monotonic()-start}
    (ROOT/'prior-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'verified_bound':4000000,'stages':len(records),'seconds':result['seconds']},indent=2))

if __name__=='__main__':main()
