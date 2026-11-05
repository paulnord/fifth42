#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 -m unittest -v test_lattice5 audit_tests 2>&1 | tee results/all-tests.txt
python3 reproduce.py --bound 1000
python3 compare_upstream.py
python3 -m py_compile lattice5.py reproduce.py compare_upstream.py test_lattice5.py audit_tests.py
# Optional published backend experiment; install both pinned requirements first.
if [[ " $* " == *" --published-backends "* ]]; then
  python3 -m unittest -v test_backends test_modular_filters 2>&1 | tee results/published-backend-tests.txt
  python3 -O -m unittest -v test_backends test_modular_filters 2>&1 | tee results/published-backend-tests-optimized.txt
  python3 benchmark_backends.py | tee results/backend-benchmark.log
  python3 benchmark_modular_filters.py > results/modular_filters_benchmark.json
  python3 benchmark_modular_filters.py --backend fpylll > results/modular_filters_fpylll_benchmark.json
  python3 benchmark_modular_full.py --backend fpylll > results/modular_filters_full_fpylll.json
  python3 benchmark_enumeration.py | tee results/enumeration-benchmark.log
  python3 benchmark_widths.py | tee results/width-benchmark.log
fi
python3 -m py_compile modular_filters.py benchmark_backends.py benchmark_modular_filters.py benchmark_modular_full.py test_backends.py test_modular_filters.py
# Separate optional arithmetic experiment; compiled_experiment/requirements.txt required.
if [[ " $* " == *" --compiled-rationals "* ]]; then
  python3 compiled_experiment/test_mpq.py 2>&1 | tee results/compiled-final-tests.txt
  python3 -O compiled_experiment/test_mpq.py 2>&1 | tee results/compiled-final-tests-optimized.txt
  python3 compiled_experiment/benchmark_mpq.py
  python3 compiled_experiment/large_controls_mpq.py
fi
