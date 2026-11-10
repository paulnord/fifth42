"""Append all protected claims while retaining the exact existing three stages."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT));import controller
old=Path('/home/pnord/boole-overnight-controller-20261109/production-plan.json')
prior=json.loads(old.read_bytes());new=json.loads((ROOT/'stages.json').read_bytes())['stages']
plan=dict(prior,stages=prior['stages']+new,controller_sha256=controller.sha(ROOT/'controller.py'),
 helper_sha256={str(ROOT/'delegated_publication.py'):controller.sha(ROOT/'delegated_publication.py')},
 status_file=str(ROOT/'PRODUCTION_STATUS.json'),shared_status_file='/mnt/nfs_share/fifth42-integration-20261109/extend-20261110/boole/PRODUCTION_STATUS.json',
 predecessor_plan_sha256=controller.sha(old),grant_sha256='7c8422f5e9086519db3bc8ad2e8eeab8d7d1d60706f9b327766ba0a069c6a389',
 additional_reserved_cells=4250000001,additional_claims=67,total_stages=70,
 authorization='User: validate Ada handoff locally and append the 67 exact protected claims after Boole existing queue; preserve current compute and final copier; deadline unchanged.',
 publication_share='/mnt/nfs_share/boole-delegated-publishing-20261109')
for stage in plan['stages']:controller.load_stage(stage)
assert plan['stages'][:3]==prior['stages']
controller.atomic(ROOT/'production-plan.json',plan)
print(json.dumps(dict(status='prepared_pending_actual_gpu_validation',stages=len(plan['stages']),plan_sha256=controller.sha(ROOT/'production-plan.json'))))
