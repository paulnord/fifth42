#!/usr/bin/env bash
# Isolated, read-only with respect to existing production directories/services.
set -euo pipefail
HERE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
OUT=${1:-"$HOME/fifth42-cgbn-test-$(date -u +%Y%m%dT%H%M%SZ)"}
mkdir -p "$OUT"
exec > >(tee "$OUT/run.log") 2>&1
printf 'Evidence directory: %s\n' "$OUT"
for tool in git python3 nvcc nvidia-smi curl tar sha256sum; do command -v "$tool" >/dev/null || { echo "BLOCKED: missing $tool. No packages or drivers changed."; exit 2; }; done
# CGBN requires the GMP development header for nvcc's host pass.
HOST_CXX=${CXX:-$(command -v g++-13 || command -v g++)}
printf '#include <gmp.h>\nint main(){return 0;}\n' | "$HOST_CXX" -x c++ - -lgmp -o "$OUT/gmp-header-check"
nvidia-smi > "$OUT/nvidia-smi.txt"
if [ -n "$(nvidia-smi --query-compute-apps=pid --format=csv,noheader)" ]; then
  echo 'BLOCKED: another GPU compute process is active. No process stopped.'; exit 2
fi
nvcc --version > "$OUT/nvcc-version.txt"
uname -a > "$OUT/uname.txt"
python3 --version > "$OUT/python-version.txt"
(cd "$HERE" && sha256sum -c SHA256SUMS)
CGBN=114601b07ae8c3e4d46b250208ea8d9def7a12f0
if [ ! -d "$OUT/CGBN/.git" ]; then git clone https://github.com/NVlabs/CGBN.git "$OUT/CGBN"; fi
git -C "$OUT/CGBN" checkout --detach "$CGBN"
test "$(git -C "$OUT/CGBN" rev-parse HEAD)" = "$CGBN"
python3 "$HERE/test_cpu.py" | tee "$OUT/cpu-validation.txt"
# Probe the actual toolkit even when nvcc is a shell wrapper. Never eval its output.
nvcc --dryrun -x cu /dev/null > "$OUT/nvcc-dryrun.txt" 2>&1
CUDA_SOURCE_ROOT=${CUDA_ROOT:-$(sed -n 's/^#\$ TOP=//p' "$OUT/nvcc-dryrun.txt" | head -n 1)}
[ -n "$CUDA_SOURCE_ROOT" ] || { echo 'BLOCKED: set CUDA_ROOT to the actual toolkit root'; exit 2; }
STAGED_NVCC=$(python3 "$HERE/stage_cuda.py" "$CUDA_SOURCE_ROOT" "$OUT/cuda-overlay")
NVCC=("$STAGED_NVCC" -ccbin "$HOST_CXX")

for tpi in 4 8 16 32; do
  "${NVCC[@]}" -O3 -std=c++17 -arch=sm_86 -DROOT_TPI="$tpi" -I"$OUT/CGBN/include" "$HERE/root_cuda.cu" -lgmp -o "$OUT/root-tpi$tpi"
  python3 "$HERE/test_host_guards.py" "$OUT/root-tpi$tpi" "$OUT/guards-cgbn-tpi$tpi"
  for count in 256 1024 4096; do
    python3 "$HERE/gpu_check.py" --binary "$OUT/root-tpi$tpi" --count "$count" --output "$OUT/tpi$tpi-count$count"
  done
done
# NVIDIA SDK terms apply; see README. Isolated installation only.
if [ "${CUPQC_DOWNLOAD:-1}" = 1 ] && [ -z "${CUPQC_ROOT:-}" ]; then
  command -v curl >/dev/null
  echo 'Downloading proprietary NVIDIA cuPQC 0.6.0 into this isolated evidence directory.'
  curl --fail --location --retry 2 https://developer.nvidia.com/downloads/compute/cupqc/downloads/secure/cupqc-sdk-0.6.0-x86_64.tar.gz -o "$OUT/cupqc.tar.gz"
  echo '8026ac00d81130180d2ff0afb3eb9bce852b76cc6a02141f9e45b799a17ae571  cupqc.tar.gz' | (cd "$OUT" && sha256sum -c -)
  tar -xzf "$OUT/cupqc.tar.gz" -C "$OUT"
  CUPQC_ROOT="$OUT/cupqc-sdk-0.6.0-x86_64"
fi
if [ -n "${CUPQC_ROOT:-}" ]; then
  test -f "$CUPQC_ROOT/include/cupqc/bigint.hpp" || test -f "$CUPQC_ROOT/include/bigint.hpp" || { echo 'BLOCKED: CUPQC_ROOT has no bigint.hpp'; exit 2; }
  find "$CUPQC_ROOT" -maxdepth 3 -type f -name '*cupqc*' -print > "$OUT/cupqc-sdk-files.txt"
  for tpi in 4 8 16 32; do
    "${NVCC[@]}" -O3 -std=c++17 -dlto -arch=sm_86 -DROOT_TPI="$tpi" -DROOT_SM=860 -I"$CUPQC_ROOT/include/cupqc" -I"$CUPQC_ROOT/include" -L"$CUPQC_ROOT/lib" -L"$CUPQC_ROOT/lib64" "$HERE/root_cupqc.cu" -lcupqc-bigint -o "$OUT/cupqc-tpi$tpi"
    python3 "$HERE/test_host_guards.py" "$OUT/cupqc-tpi$tpi" "$OUT/guards-cupqc-tpi$tpi"
    for count in 256 1024 4096; do
      LD_LIBRARY_PATH="$CUPQC_ROOT/lib:$CUPQC_ROOT/lib64:${LD_LIBRARY_PATH:-}" python3 "$HERE/gpu_check.py" --binary "$OUT/cupqc-tpi$tpi" --count "$count" --output "$OUT/cupqc-tpi$tpi-count$count"
    done
  done
else
  echo 'BLOCKED cuPQC: SDK not installed/configured. Set CUPQC_ROOT to an authorized cuPQC 0.6.0 installation and rerun. No cuPQC test pass claimed.' | tee "$OUT/cupqc-BLOCKED.txt"
fi
python3 "$HERE/summarize.py" "$OUT"
echo 'DONE: isolated correctness/root timing only. Production left unchanged.'
