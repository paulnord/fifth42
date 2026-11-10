"""Validate on the actual GPU when the current compute stage finishes naturally."""
import argparse,hashlib,json,os,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT));import controller
PYTHON='/home/pnord/boole-results-20261107/venv312/bin/python'
def main():
 p=argparse.ArgumentParser();p.add_argument('--source-sha256',required=True);p.add_argument('--stages-sha256',required=True);a=p.parse_args()
 controller.require(controller.sha(__file__)==a.source_sha256 and controller.sha(ROOT/'stages.json')==a.stages_sha256,'Validation input changed')
 prior=json.loads(Path('/home/pnord/boole-overnight-20261109/worker/production-config.json').read_bytes())
 stages=json.loads((ROOT/'stages.json').read_bytes())['stages'];first=stages[0]
 controller.atomic(ROOT/'LOCAL_VALIDATION_STATUS.json',dict(status='waiting_for_natural_boundary',active_compute=prior['service_name'],source_sha256=a.source_sha256))
 while controller.unit(prior['service_name'])['ActiveState']=='active':
  controller.require(time.time()<1794351300,'No time remains for local validation');time.sleep(2)
 local=Path(prior['output']);cp=json.loads((local/'checkpoint.json').read_bytes());sup=json.loads((local.parent/'supervisor.json').read_bytes())
 controller.require(cp['next_patch']==prior['range_end'] and sup['status']=='finished' and sup['error'] is None and sup['worker_exit_code']==0 and sup['leases_released'],'Current segment did not finish normally')
 controller.require(controller.free_lock('/home/pnord/boole-production-validation-20261107/gpu-owner.lock'),'GPU owner is not released')
 while os.getloadavg()[0]>=17:time.sleep(1)
 controller.atomic(ROOT/'LOCAL_VALIDATION_STATUS.json',dict(status='actual_gpu_tests_running',source_sha256=a.source_sha256))
 result=subprocess.run([PYTHON,'-B','-u',str(Path(first['root'])/'validate_boole_services.py'),'--revision','delegated-r1'],capture_output=True,text=True,timeout=330)
 (ROOT/'actual-gpu.stdout').write_text(result.stdout);(ROOT/'actual-gpu.stderr').write_text(result.stderr)
 controller.require(result.returncode==0,'Actual local GPU validation failed: '+result.stderr[-4000:])
 actual=Path(first['root'])/'runtime-validation.json';raw=actual.read_bytes();controller.require(json.loads(raw)['status']=='passed','Actual GPU validation did not pass')
 (ROOT/'actual-gpu-validation.json').write_bytes(raw);actual_sha=controller.sha(ROOT/'actual-gpu-validation.json')
 assert len({s['code_equivalence_sha256'] for s in stages})==1
 for stage in stages:
  c=controller.load_stage(stage)
  code="import sys;sys.path[:0]=sys.argv[1:3];import policy;policy.load_config(sys.argv[3])"
  w=Path(stage['root'])/'worker';subprocess.run([PYTHON,'-B','-c',code,str(w),str(w/'source/lattice_gpu'),stage['config']],check=True,timeout=30)
  report=dict(status='passed',manifest_sha256=stage['manifest_sha256'],config_sha256=stage['config_sha256'],TEST_ONLY=False,
   scientific_coverage=False,validation_scope='Exact executable code tested by actual Boole GPU finite, signal and deadline services; this frozen claim configuration separately admitted against live protected ledger.',
   code_equivalence_sha256=stage['code_equivalence_sha256'],representative_actual_gpu_run=first['root'],actual_gpu_validation_sha256=actual_sha,
   actual_gpu_cases=[dict(case=r['case'],status=r['status'],chunks=r['checkpoint']['chunks'],gmp_audited_chunks=r['local_audit']['new_gmp_audited_chunks']) for r in json.loads(raw)['cases']],
   guard_validation_sha256=controller.sha(ROOT/'guard-validation.json'),each_production_stage='Runs nonempty controls and first-chunk full independent GMP comparison again before committing.')
  controller.atomic(Path(stage['root'])/'runtime-validation.json',report)
 controller.atomic(ROOT/'LOCAL_VALIDATION_STATUS.json',dict(status='passed',stages=67,actual_gpu_validation_sha256=actual_sha,code_equivalence_sha256=stages[0]['code_equivalence_sha256']))
 print(json.dumps(dict(status='passed',stages=67,actual_gpu_validation_sha256=actual_sha)),flush=True)
if __name__=='__main__':
 try:main()
 except BaseException as e:
  controller.atomic(ROOT/'LOCAL_VALIDATION_FAILURE.json',dict(status='failed',error=repr(e)));raise
