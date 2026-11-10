#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")" && pwd)
OUT=${1:?Usage: bash run.sh NEW_EVIDENCE_DIRECTORY}
[[ ! -e "$OUT" ]] || { echo 'Refusing existing output directory' >&2; exit 2; }
mkdir -p "$OUT";OUT=$(cd "$OUT" && pwd)
exec > >(tee "$OUT/run.log") 2>&1
python3 - "$OUT" <<'PY_DISK'
import shutil,sys
if shutil.disk_usage(sys.argv[1]).free<5*1024**3:raise SystemExit("BLOCKED: require5GiB free for local SDK/compiler output/evidence")
PY_DISK
(cd "$HERE" && sha256sum -c SHA256SUMS)
for tool in python3 git curl tar nvcc nvidia-smi g++;do command -v "$tool" >/dev/null;done
nvidia-smi > "$OUT/device.txt"
[[ -z "$(nvidia-smi --query-compute-apps=pid --format=csv,noheader)" ]] || { echo 'BLOCKED: active GPU compute process; no process stopped';exit 2; }
python3 -m venv "$OUT/venv"
PY="$OUT/venv/bin/python"
"$PY" -m pip install 'gmpy2==2.2.2' 'fpylll==0.6.4' 'cysignals==1.12.5' 'numpy==2.3.5'
"$PY" -m pip freeze > "$OUT/python-packages.txt"
HOST_CXX=${CXX:-$(command -v g++-13 || command -v g++)}
printf '#include <gmp.h>\nint main(){return 0;}\n' | "$HOST_CXX" -x c++ - -lgmp -o "$OUT/gmp-check"
nvcc --version > "$OUT/nvcc-version.txt"
nvcc --dryrun -x cu /dev/null > "$OUT/nvcc-dryrun.txt" 2>&1
ROOT=${CUDA_ROOT:-$(sed -n 's/^#\$ TOP=//p' "$OUT/nvcc-dryrun.txt" | head -1)}
[[ -n "$ROOT" ]] || { echo 'BLOCKED: set CUDA_ROOT';exit 2; }
NVCC=$("$PY" "$HERE/stage_cuda.py" "$ROOT" "$OUT/cuda-overlay")
git clone https://github.com/NVlabs/CGBN.git "$OUT/CGBN"
git -C "$OUT/CGBN" checkout --detach 114601b07ae8c3e4d46b250208ea8d9def7a12f0
if [[ -z "${CUPQC_ROOT:-}" ]];then
 echo 'NVIDIA cuPQC SDK download/use accepts Math SDK terms: https://docs.nvidia.com/cuda/cupqc/additional/license.html'
 curl --fail --location --retry 2 https://developer.nvidia.com/downloads/compute/cupqc/downloads/secure/cupqc-sdk-0.6.0-x86_64.tar.gz -o "$OUT/cupqc.tar.gz"
 echo '8026ac00d81130180d2ff0afb3eb9bce852b76cc6a02141f9e45b799a17ae571  cupqc.tar.gz' | (cd "$OUT" && sha256sum -c -)
 tar -xzf "$OUT/cupqc.tar.gz" -C "$OUT";CUPQC_ROOT="$OUT/cupqc-sdk-0.6.0-x86_64"
fi
"$HOST_CXX" -O2 -std=c++17 "$HERE/cpu_model.cpp" -lgmpxx -lgmp -o "$OUT/cpu_model"
"$PY" "$HERE/test_reference.py" --model "$OUT/cpu_model" | tee "$OUT/cpu-tests.txt"
for tpi in 8 16;do
 "$NVCC" -ccbin "$HOST_CXX" -O3 -std=c++17 -arch=sm_86 -DROOT_TPI=$tpi -I"$OUT/CGBN/include" "$HERE/fused_cgbn.cu" -lgmp -o "$OUT/cgbn$tpi" > "$OUT/build-cgbn$tpi.log" 2>&1
 "$NVCC" -ccbin "$HOST_CXX" -O3 -std=c++17 -dlto -arch=sm_86 -DROOT_TPI=$tpi -I"$CUPQC_ROOT/include/cupqc" -I"$CUPQC_ROOT/include" "$HERE/fused_cupqc.cu" -L"$CUPQC_ROOT/lib" -lcupqc-bigint -lgmp -o "$OUT/cupqc$tpi" > "$OUT/build-cupqc$tpi.log" 2>&1
 for backend in cgbn cupqc;do
  "$PY" "$HERE/test_guards.py" "$OUT/$backend$tpi" "$OUT/guards-$backend$tpi"
  "$PY" "$HERE/benchmark.py" --binary "$OUT/$backend$tpi" --count 4 --repeats 1 --region edge --output "$OUT/smoke-$backend$tpi"
 done
done
# All exact smoke checks must pass before bounded timing sweep.
for tpi in 8 16;do
 for region in cabbage boole;do
  for group in 4 8;do
   for count in 256 4096;do
    for backend in cgbn cupqc;do
     "$PY" "$HERE/benchmark.py" --binary "$OUT/$backend$tpi" --count "$count" --region "$region" --group "$group" --output "$OUT/$backend-tpi$tpi-$region-g$group-n$count"
    done
   done
  done
 done
done
"$PY" "$HERE/summarize.py" "$OUT"
echo 'DONE: no production files, checkpoints, leases or services changed.'
