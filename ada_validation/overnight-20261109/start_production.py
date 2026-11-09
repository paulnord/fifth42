"""Launch the validated Ada continuation, independent final copier and reporting."""
from datetime import datetime,timezone
import hashlib,json,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent; W=ROOT/'worker'
REPORTER=Path('/home/pnord/ada-overnight-reporting-20261109')
PYTHON='/home/pnord/fifth-lattice-optimizations-ada-20261105/venv/bin/python'
def main():
    cfg=json.loads((W/'config.json').read_bytes())
    assert json.loads((ROOT/'READY.json').read_bytes())['status']=='ready'
    assert not (ROOT/'production-start.json').exists()
    from validate_sources import helper
    guard=helper();handles,leased=guard.acquire_leases(guard.resources(),True)
    for handle in handles:handle.close()
    events=[]
    def run(command):
        result=subprocess.run(command,capture_output=True,text=True,timeout=70)
        row=dict(command=command,exit_code=result.returncode,stdout=result.stdout,stderr=result.stderr)
        events.append(row)
        (ROOT/'production-start.json').write_text(json.dumps(dict(started_utc=datetime.now(timezone.utc).isoformat(),commands=events),indent=2)+'\n')
        result.check_returncode(); print(json.dumps(row),flush=True)
    runtime=max(60,int(cfg['stop_epoch']+1800-time.time()))
    def service(unit,cwd,script,args=()):
        return ['systemd-run','--user','--unit='+unit,'--collect','--service-type=exec','--property=Restart=no','--property=Nice=19','--property=UMask=0077','--property=RuntimeMaxSec='+str(runtime),'--working-directory='+str(cwd),'--property=StandardOutput=append:'+str(cwd/(unit+'.stdout.log')),'--property=StandardError=append:'+str(cwd/(unit+'.stderr.log')),PYTHON,'-B','-u',str(script),*args]
    # The previous terminal snapshot has already been published and read back.
    digest=hashlib.sha256((W/'config.json').read_bytes()).hexdigest()
    run(service('ada-overnight-final-copy-20261109',ROOT,W/'finalize_replica.py',['--config',str(W/'config.json'),'--config-sha256',digest,'--wait']))
    run(service('ada-overnight-collector-20261109',REPORTER,REPORTER/'collector.py'))
    run([PYTHON,'-B',str(W/'launch_weekend.py'),'--launch'])
    print('Production service started; publisher will start after the first verified replica.',flush=True)
if __name__=='__main__':main()
