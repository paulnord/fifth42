#!/usr/bin/env bash
set -euo pipefail
BUNDLE=$(cd -- "$(dirname -- "$0")" && pwd)
OUT=${1:?Usage: bash reproduce.sh NEW_LOCAL_SCRATCH_DIRECTORY}
[[ ! -e "$OUT" ]] || { echo 'Output must not exist' >&2; exit 2; }
(cd "$BUNDLE" && sha256sum -c SHA256SUMS)
mkdir -p "$OUT"
OUT=$(cd "$OUT" && pwd)
tar -xzf "$BUNDLE/source.tar.gz" -C "$OUT"
PYTHON=${PYTHON:-/home/pnord/scratch/fifth42-production-speed-tests-7sfz9xet/bench/venv/bin/python}
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
# These dependencies were already installed in the tested isolated Python env.
# To prepare another Python3.12 venv locally:
# python3.12 -m venv NEW_VENV
# NEW_VENV/bin/python -m pip install sympy==1.14.0 gmpy2==2.2.2 fpylll==0.6.4 cysignals==1.12.5 numpy==2.3.5
"$PYTHON" - "$BUNDLE/source-manifest.json" "$OUT" <<'PY'
import hashlib,json,sys
from pathlib import Path
root=Path(sys.argv[2])
for name,meta in json.loads(Path(sys.argv[1]).read_text())['files'].items():
 assert hashlib.sha256((root/name).read_bytes()).hexdigest()==meta['sha256'],name
PY
"$PYTHON" "$OUT/gpu_candidate/test_candidate.py"
"$PYTHON" "$OUT/gpu_candidate/test_flat_buffer.py"
"$PYTHON" "$OUT/gpu_candidate/review/test_no_lll.py"
"$PYTHON" "$OUT/test_service_failure.py" --output "$OUT/service-failure-repeat.json"
# Stable Cabbage GPU-owner lease and load guards are held by run_bounded.py.
for FAULT in none zero-u status1; do
  EXTRA=()
  [[ "$FAULT" == none ]] || EXTRA=(--case known-positive-group4 --proposal-fault "$FAULT")
  "$PYTHON" "$OUT/run_bounded.py" --log "$OUT/controls-$FAULT.log" "$PYTHON" "$OUT/integration_controls.py" --workers 16 --output "$OUT/controls-$FAULT" "${EXTRA[@]}"
done
"$PYTHON" "$OUT/run_bounded.py" --log "$OUT/controls-lll.log" "$PYTHON" "$OUT/integration_controls.py" --workers 16 --case known-positive-group4 --quality-gate exact-lll --output "$OUT/controls-lll"
"$PYTHON" "$OUT/run_matrix.py" --output "$OUT/matrix" --repeats 3 --patches 32768 --seconds 1200
# The archive contains the exact tested small binaries. If rebuilding is desired,
# do it only in a NEW scratch revision and rerun every correctness gate first:
# NVCC=/home/pnord/scratch/fifth42-gpu-root-test-d3wai41j/installation-check/cuda-local-layout/bin/nvcc
# "$NVCC" -ccbin /usr/bin/g++-13 -std=c++17 -O3 -arch=sm_86 -Xcompiler -fPIC -shared "$OUT/gpu_candidate/gpu_lll.cu" -o "$OUT/gpu_candidate/libgpu_lll.so"
# CGBN_ROOT=/home/pnord/scratch/fifth42-gpu-root-test-d3wai41j/evidence/CGBN
# for SEED in 0 1; do
#   NAME=power; [[ "$SEED" == 0 ]] || NAME=seeded
#   "$NVCC" -ccbin /usr/bin/g++-13 -O3 -std=c++17 -arch=sm_86 -DROOT_TPI=8 -DROOT_FLOAT_SEED="$SEED" -I"$CGBN_ROOT/include" "$OUT/newton/root_newton.cu" -lgmp -o "$OUT/newton/root_newton_${NAME}_tpi8"
# done
# Root repetition uses the published exact fixtures, without requiring old scratch inputs:
# mkdir "$OUT/raw-original"
# cat "$BUNDLE"/raw-evidence.tar.gz.part* | tar -xz -C "$OUT/raw-original"
# cp -a "$OUT/raw-original/newton/evidence" "$OUT/newton/"
# ROOT_SKIP_NATIVE=0 timeout --signal=TERM --kill-after=5s 30s "$PYTHON" "$OUT/newton/run_gpu_tests.py"
