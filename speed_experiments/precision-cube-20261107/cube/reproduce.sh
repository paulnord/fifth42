#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p bin
g++ -std=c++17 -O3 -Wall -Wextra src/emulated.cpp -o bin/emulated
g++ -std=c++17 -O1 -fsanitize=undefined -fno-sanitize-recover=all src/emulated.cpp -o bin/emulated-ubsan
python3 -m unittest -v test_cube_core
python3 validate_cube.py
