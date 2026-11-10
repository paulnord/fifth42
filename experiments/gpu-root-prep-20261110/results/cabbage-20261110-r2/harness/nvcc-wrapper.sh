#!/bin/bash
set -euo pipefail
root_flags=()
for arg in "$@"; do
  if [[ ${arg##*/} == root_cuda.cu ]]; then root_flags=(-include gmp.h -lgmp); fi
done
exec /home/pnord/scratch/fifth42-gpu-root-test-d3wai41j/installation-check/cuda-local-layout/bin/nvcc -ccbin /usr/bin/g++-13 "${root_flags[@]}" "$@"
