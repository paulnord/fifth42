#!/usr/bin/env bash
set -euo pipefail
test "$#" -eq 1 || { echo 'Usage: build_cpu.sh NEW_AB_DIRECTORY' >&2; exit 2; }
work=$(realpath "$1")
for variant in baseline low64; do
  mkdir -p "$work/$variant/bin"
  test ! -e "$work/$variant/bin/scaling_cpu" && test ! -e "$work/$variant/bin/scaling_cpu_ubsan" || { echo 'Refusing binary overwrite' >&2; exit 2; }
  g++ -std=c++17 -O3 -Wall -Wextra -Werror -pthread \
    "$work/$variant/src/scaling_cpu.cpp" -o "$work/$variant/bin/scaling_cpu"
  g++ -std=c++17 -O1 -g -fsanitize=undefined -fno-sanitize-recover=all -pthread \
    "$work/$variant/src/scaling_cpu.cpp" -o "$work/$variant/bin/scaling_cpu_ubsan"
done
sha256sum "$work"/{baseline,low64}/bin/* > "$work/cpu-binary-sha256.txt"
