#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 -m unittest -v test_lattice5 audit_tests 2>&1 | tee results/all-tests.txt
python3 reproduce.py --bound 1000
python3 compare_upstream.py
python3 -m py_compile lattice5.py reproduce.py compare_upstream.py test_lattice5.py audit_tests.py
