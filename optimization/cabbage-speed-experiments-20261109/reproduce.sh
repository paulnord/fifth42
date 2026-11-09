#!/bin/sh
set -eu
if [ "$#" -lt 2 ]; then
    echo 'Usage: reproduce.sh NEW_ABSOLUTE_OUTPUT PINNED_PYTHON [NVCC] [--benchmarks]' >&2
    exit 2
fi
handoff_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
experiment_output=$1
pinned_python=$2
case "$experiment_output" in /*) ;; *) echo 'Output must be absolute' >&2; exit 2;; esac
test ! -e "$experiment_output"
export NVCC=${3:-/home/pnord/scratch/saved-root-pAjTHBhR/cuda-13.2/nvidia/cu13/bin/nvcc}
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
"$pinned_python" - "$handoff_root" "$experiment_output" <<'PY'
import hashlib,json,sys,tarfile
from pathlib import Path
handoff,output=map(Path,sys.argv[1:]);output.mkdir()
with tarfile.open(handoff/'source.tar.gz','r:gz') as archive:archive.extractall(output,filter='data')
root=output/'tested-source';manifest=json.loads((handoff/'source-manifest.json').read_text())
for name,expected in manifest['files'].items():
    path=root/name
    if hashlib.sha256(path.read_bytes()).hexdigest()!=expected:raise RuntimeError('Source mismatch: '+name)
(root/'results').mkdir(exist_ok=True)
print('All bundled source and executable hashes verified',flush=True)
PY
cd "$experiment_output/tested-source"
"$pinned_python" build.py
"$pinned_python" build_extra.py
"$pinned_python" validate.py reference
"$pinned_python" validation_suite.py
"$pinned_python" final_validation_suite.py
"$pinned_python" range_fixture.py
if [ "${4:-}" = '--benchmarks' ]; then
    "$pinned_python" resource_runner.py reproduce-host "$pinned_python" host_matrix.py
    "$pinned_python" resource_runner.py reproduce-width "$pinned_python" width_matrix.py
    "$pinned_python" resource_runner.py reproduce-native "$pinned_python" native_benchmark.py
    "$pinned_python" resource_runner.py reproduce-candidate "$pinned_python" candidate_matrix.py
fi
echo 'Finite reproduction checks passed'
