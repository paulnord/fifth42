"""Freeze the prepared release before tests/start; never update a running release."""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
config=json.loads((ROOT/'config.json').read_text())
if Path(config['output']).exists():raise RuntimeError('Actual run already exists; release cannot change')
if config['ledger_claim_sha256']!='DRAFT':raise RuntimeError('Claimed runtime cannot be overwritten')
files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
       for folder in ('source','bin','native-baseline','independent','precision')
       for p in (ROOT/folder).rglob('*') if p.is_file() and not p.is_symlink()}
for name in ('policy.py','packed_worker.py','search_supervisor.py','launch_weekend.py',
             'ada_export_store.py','gpu_validation.py','host_validation.py','bounded_check.py',
             'prepare_handoff.py'):
    files[name]=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
release=dict(created_utc=datetime.now(timezone.utc).isoformat(),files=files,
     actual_cuda_source='native-baseline/src/scaling_gpu.cu',actual_kernel='native-baseline/src/kernel.hpp',
     actual_gpu_binary='bin/scaling_gpu',independent_gmp_source='independent/gmp_reference.cpp',
     original_native_templates_in_host_tree='Not compiled; actual validated range-overlay sources are in native-baseline',
     compiler='/usr/bin/g++-13',cuda_compiler='/usr/local/cuda-13.4/bin/nvcc',cuda_arch='sm_86')
release['external_files']={name:hashlib.sha256(Path(name).read_bytes()).hexdigest() for name in (
    '/home/pnord/fifth-lattice-optimizations-ada-20261105/benchmark_ada.py',
    '/home/pnord/fifth42-low64-review-20261106/handoff/bundle/fifth42-coordinator-20261105/lattice_gpu/benchmark.py')}
(ROOT/'release-manifest.json').write_text(json.dumps(release,indent=2)+'\n')
config['manifest_sha256']=hashlib.sha256((ROOT/'release-manifest.json').read_bytes()).hexdigest()
config['ledger_runtime_identity']=config['manifest_sha256']
(ROOT/'config.json').write_text(json.dumps(config,indent=2)+'\n')
print(json.dumps(dict(files=len(files),manifest_sha256=config['manifest_sha256'])))
