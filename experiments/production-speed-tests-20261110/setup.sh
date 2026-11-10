#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")" && pwd)
REPO=$(cd "$HERE/../.." && pwd)
OUT=${1:?Usage: bash setup.sh NEW_LOCAL_DIRECTORY}
[[ ! -e "$OUT" ]] || { echo 'Output must not exist' >&2; exit 2; }
mkdir -p "$OUT"
OUT=$(cd "$OUT" && pwd)
python3 - "$REPO/ada_validation/wide-groups-20261109" <<'PY_CHECK'
import hashlib,json,sys
from pathlib import Path
p=Path(sys.argv[1]);m=json.loads((p/'experiment-manifest.json').read_text())['worker_files']
for name,digest in m.items():
 if name.startswith('bin/') or '/bin/' in name:continue
 f=p/'worker'/name
 if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest()!=digest:raise SystemExit('Source mismatch: '+name)
PY_CHECK
cp -a "$REPO/ada_validation/wide-groups-20261109/worker" "$OUT/worker"
cp "$HERE"/*.py "$OUT/"
cp -a "$HERE/warm" "$HERE/sealed" "$HERE/overlap" "$OUT/"
cp "$HERE/run_all.sh" "$OUT/"
cp "$OUT/overlap/scaling_gpu_overlap.cu" "$OUT/worker/native-baseline/src/"
python3 -c 'import sys; assert sys.version_info[:2] == (3,12), "Python 3.12 required"'
python3 -m venv "$OUT/venv"
"$OUT/venv/bin/python" -m pip install 'sympy==1.14.0' 'gmpy2==2.2.2' 'fpylll==0.6.4' 'cysignals==1.12.5' 'numpy==2.3.5'
command -v nvcc >/dev/null
command -v g++ >/dev/null
mkdir "$OUT/worker/bin"
g++ -O3 -std=c++17 "$OUT/worker/independent/gmp_reference.cpp" -lgmpxx -lgmp -o "$OUT/worker/bin/gmp_reference"
nvcc -O3 -std=c++17 -arch=sm_86 "$OUT/worker/native-baseline/src/scaling_gpu.cu" -o "$OUT/worker/bin/scaling_gpu"
nvcc -O3 -std=c++17 -arch=sm_86 "$OUT/worker/native-baseline/src/scaling_gpu_overlap.cu" -o "$OUT/worker/bin/scaling_gpu_overlap"
"$OUT/venv/bin/python" - "$OUT" <<'PY'
import hashlib,json,sys
from pathlib import Path
p=Path(sys.argv[1]); w=p/'worker'
files={str(f.relative_to(w)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(w.rglob('*')) if f.is_file()}
(p/'experiment-manifest.json').write_text(json.dumps({'TEST_ONLY':True,'worker_files':files},indent=2)+'\n')
PY
printf '\nPrepared %s\nNext (only on quiescent test hardware):\ntimeout --signal=TERM --kill-after=10s 40m bash %s/run_all.sh\n' "$OUT" "$OUT"
