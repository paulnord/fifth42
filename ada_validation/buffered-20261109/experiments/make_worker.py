"""Recreate the exact pre-buffering source layout for experiment reproduction."""
import argparse,hashlib,json,shutil
from pathlib import Path
R=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--release-worker',type=Path,default=R.parent/'worker');p.add_argument('--output',type=Path,default=R/'worker');p.add_argument('--allow-rebuilt-binaries',action='store_true');a=p.parse_args()
m=json.loads((R/'baseline-manifest.json').read_bytes());a.output.mkdir(mode=0o700,parents=True,exist_ok=False)
for name,expected in m['files'].items():
 src=R/'baseline-overrides'/name
 if not src.exists():src=a.release_worker/name
 if not src.exists():raise RuntimeError('Build or provide the pinned native/GMP binary first: '+name)
 actual=hashlib.sha256(src.read_bytes()).hexdigest()
 if actual!=expected:
  if not ('bin' in Path(name).parts and a.allow_rebuilt_binaries):raise RuntimeError('Baseline source differs: '+name)
  m['files'][name]=actual
 dest=a.output/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
(a.output/'baseline-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps(dict(status='baseline_source_recreated',binary_hashes_are_host_specific=a.allow_rebuilt_binaries,output=str(a.output))))
