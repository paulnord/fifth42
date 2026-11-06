#!/usr/bin/env bash
# Invoke only through ada_guard.py. Builds in the isolated A/B directory.
set -euo pipefail
test "$#" -eq 1 || { echo 'Usage: build_gpu.sh NEW_AB_DIRECTORY' >&2; exit 2; }
work=$(realpath "$1")
: "${NVCC:=/usr/local/cuda/bin/nvcc}"
: "${CUDA_ARCH:?Set CUDA_ARCH to the verified device target, e.g. sm_86 or sm_89}"
[[ "$CUDA_ARCH" =~ ^sm_[0-9]+$ ]] || { echo 'Invalid CUDA_ARCH' >&2; exit 2; }
for variant in baseline low64; do
  mkdir -p "$work/$variant/bin"
  test ! -e "$work/$variant/bin/scaling_gpu" || { echo 'Refusing binary overwrite' >&2; exit 2; }
  "$NVCC" -std=c++17 -O3 -arch="$CUDA_ARCH" -ccbin g++ -Xptxas=-v \
    "$work/$variant/src/scaling_gpu.cu" -o "$work/$variant/bin/scaling_gpu" \
    > "$work/$variant/cuda-build.stdout" 2> "$work/$variant/cuda-build.stderr"
done
sha256sum "$work"/{baseline,low64}/bin/scaling_gpu > "$work/gpu-binary-sha256.txt"
