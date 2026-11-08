#!/bin/sh
set -eu
nvcc=/home/pnord/scratch/saved-root-pAjTHBhR/cuda-13.2/nvidia/cu13/bin/nvcc
"$nvcc" -std=c++17 -O3 -arch=sm_86 -ccbin g++-13 device/src/scaling_gpu.cu -o device/bin/scaling_gpu
"$nvcc" -std=c++17 -O3 -arch=sm_86 -ccbin g++-13 device/src/enumerate.cu -o device/bin/cuda
for target in emulated scaling_cpu; do
 g++-13 -std=c++17 -O3 -Wall -Wextra -Werror -pthread "device/src/$target.cpp" -o "device/bin/$target"
 g++-13 -std=c++17 -O1 -g -fsanitize=undefined -fno-sanitize-recover=all -pthread "device/src/$target.cpp" -o "device/bin/${target}_ubsan"
done
