#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
exec 9>/tmp/fifth42-experimental-benchmark.lock
flock -n 9 || { echo 'Another experimental benchmark owns the lock'; exit 2; }
P="$PWD/venv/bin/python"
"$P" -c 'import os,subprocess; assert os.getloadavg()[0]<=4,"CPU load guard"; s=subprocess.check_output(["nvidia-smi","--query-compute-apps=pid","--format=csv,noheader,nounits"],text=True); assert not s.strip(),"GPU compute workload active"'
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export LATTICE_SOURCE="$PWD/worker/source/lattice_prototype/compiled_experiment/lattice5_snapshot.py"
export PYTHONPATH="$PWD/worker:$PWD/worker/source/lattice_gpu"
R="$PWD/diagnostics-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir "$R"
"$P" -m unittest discover -s warm -v >"$R/warm-tests.log" 2>&1
"$P" -m unittest discover -s sealed -v >"$R/sealed-tests.log" 2>&1
"$P" warm/benchmark_warm_reduction.py --source "$LATTICE_SOURCE" --precision-policy "$PWD/worker/source/lattice_gpu/precision_policy.py" --output "$R/warm.json"
"$P" sealed/benchmark_packets.py --worker "$PWD/worker" --output "$R/sealed.json"
# The group runner checks GPU compute processes/load and includes exact nonempty controls.
"$P" run_groups.py
"$P" export_packets.py "$R/packets"
"$P" overlap/make_controls.py "$R/controls"
"$P" overlap/test_engine_errors.py --engine "$PWD/worker/bin/scaling_gpu_overlap" --controls "$R/controls"
for F in controls packets; do
 "$P" overlap/bench_overlap.py --baseline "$PWD/worker/bin/scaling_gpu" --candidate "$PWD/worker/bin/scaling_gpu_overlap" --gmp "$PWD/worker/bin/gmp_reference" --packets "$R/$F" --output "$R/overlap-$F"
done
printf 'All requested tests completed; inspect %s and results-* (no production changes).\n' "$R"
