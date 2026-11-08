# Cabbage saved-root test — 2026-11-08

CPU reproduction passed. GPU validation stopped on the first rejected high-shell packet; no paired GPU result is available. No deployment or new production coverage.

## Isolation and identity

- Host: cabbage; AMD Ryzen 9 5950X, 16 cores/32 logical CPUs, 125 GiB RAM. Initial load 0.39/0.30/0.28; 120 GiB available. No competing compute job observed. Existing background services left running.
- RTX 3060, 12 GiB; driver 595.99.02, driver-reported CUDA 13.2. Initially 0% utilization, 25 MiB, Xorg only; no compute process. Rechecked before GPU testing and before every request; no resource conflict detected.
- Repository paulnord/fifth42, branch handoff/exact-root-reuse-20261108, HEAD be5fcb6d5818d70035a9f2a8f31812f5f1f8b53f. Fresh clone under this report directory.
- Read both handoff README.md and TECHNICAL-REPORT.md. Archive SHA-256 9a96836119eb45d89159542aec1891ae5efdf398794ba269cf8223ae59524059 passed ARCHIVE_SHA256SUMS; all PACKAGE_SHA256SUMS entries passed, both explicitly and inside reproduce.sh.
- All outputs, new journals, environments and binaries are local scratch files. No Ada/Boole connections, production files, services, journals, checkpoints, or shared ledger were accessed or modified.

## Versions

- Python 3.12.16; sympy==1.14.0, fpylll==0.6.4, cysignals==1.12.5, numpy==2.3.5, gmpy2==2.2.2, mpmath==1.3.0.
- CPU compiler: g++ 15.2.0 (Ubuntu 15.2.0-16ubuntu1). GPU host compiler: g++-13 13.4.0 (Ubuntu 13.4.0-10ubuntu1). Ubuntu 26.04.1 LTS.
- Bootstrap uv 0.13.7. Python 3.12.16 downloaded by uv; separate venv. Default host Python 3.14.4 was not used for reproduction.
- Installed CUDA 12.3.52 at /opt/nvidia/hpc_sdk rejects GCC >12. No unsupported-compiler override used. Scratch toolkit used: nvidia-cuda-nvcc, nvidia-cuda-crt, nvidia-nvvm 13.2.78; nvidia-cuda-runtime 13.2.75. Initial unused toolkit resolution selected newer CRT/NVVM, so a second separate directory pinned all components before building.

## Commands

These are the historical commands from the scratch test. `ROOT` is the original local scratch directory, set below. Commands stopped after the failed GPU validation; no paired GPU benchmark was run.

```sh
ROOT=/home/pnord/scratch/saved-root-pAjTHBhR
hostname -f; uptime; nproc; free -h
ps -eo pid,user,pcpu,pmem,etime,args --sort=-pcpu
nvidia-smi
git clone --single-branch --branch handoff/exact-root-reuse-20261108 https://github.com/paulnord/fifth42.git repo
git -C repo rev-parse HEAD
cd repo/optimization/exact-root-reuse-20261108
cat README.md TECHNICAL-REPORT.md
sha256sum -c ARCHIVE_SHA256SUMS
unzip -q fifth42-exact-root-reuse-20261108.zip
cd fifth42-exact-root-reuse
sha256sum -c PACKAGE_SHA256SUMS
python3 -m venv "$ROOT/bootstrap"
"$ROOT/bootstrap/bin/pip" install uv
"$ROOT/bootstrap/bin/uv" venv --python 3.12 "$ROOT/venv"
"$ROOT/bootstrap/bin/uv" pip install --python "$ROOT/venv/bin/python" sympy==1.14.0 fpylll==0.6.4 cysignals==1.12.5 numpy==2.3.5 gmpy2==2.2.2
/usr/bin/time -p timeout 900 sh reproduce.sh "$ROOT/cpu" "$ROOT/venv/bin/python" --benchmark > "$ROOT/reproduction.log" 2>&1
"$ROOT/bootstrap/bin/pip" install --target "$ROOT/cuda-13.2" nvidia-cuda-nvcc==13.2.78 nvidia-cuda-crt==13.2.78 nvidia-nvvm==13.2.78 nvidia-cuda-runtime==13.2.75
cd "$ROOT/cpu/candidate/source/lattice_gpu"
make -f scaling.mk bin/scaling_gpu NVCC="$ROOT/cuda-13.2/nvidia/cu13/bin/nvcc" CXX=g++-13
"$ROOT/venv/bin/python" "$ROOT/make_gpu_probe.py"
cd "$ROOT/cpu"
ROOT_REUSE_VARIANT=baseline GPU_LOG="$ROOT/gpu/validation-baseline-raw.json" timeout 120 "$ROOT/venv/bin/python" gpu_probe.py validate --output "$ROOT/gpu/validation-baseline.json" > "$ROOT/gpu/validation-baseline.log" 2>&1
```

ROOT=/home/pnord/scratch/saved-root-pAjTHBhR. See make_gpu_probe.py for the exact scratch harness derivation from run_probe.py; it uses the existing EngineSession and exact decoders, caps each GPU request at 30 seconds, checks for foreign compute processes, and preserves raw responses. Baseline/candidate CUDA source hashes are identical; the optimization changes host Python only. The same compiled GPU binary was intended for both variants.

## CPU results

- Exit 0; real 98.12 s, user 212.65 s, sys 6.07 s.
- 142 tests passed: 6 root reuse, 107 coordinator/native package, 24 lattice/backend/filter, 5 compiled GMP.
- All 16 baseline/candidate native records matched, including CPU and UBSan, three nonempty full positive small domains and five selected high-shell windows per binary. Independent GMP counts and candidate records matched; small-domain oracle sets matched.
- All 30 pipeline trials passed exact task/certificate/geometry/packet signatures, point counts, exact hit sets, first-chunk GMP audits and durable journal prefix recovery.
- Timing uses four allowed logical CPUs, one persistent CPU native engine, bounded prefetch, fresh preparation, local durable journal commits. Startup/shutdown are separate in each result.json; full-precision trial timings, startup/shutdown, counts and identity hashes are in [cpu/benchmark-results.json](cpu/benchmark-results.json). Detailed per-worker stage arrays remain in the original local file. This supplied reproduction is CPU-only.

| Window label | Patches | Baseline samples (seconds) | Candidate samples (seconds) | Median B/C | Throughput ratio |
|---|---:|---|---|---|---|
| boole | 4096 | 1.786602968, 1.768802447, 1.772967493, 1.757001171, 1.759011078 | 1.687064610, 1.703723260, 1.700798269, 1.701074386, 1.688537271 | 1.768802447/1.700798269 | 1.039984x |
| ada | 4096 | 1.795027377, 1.763573528, 1.758462219, 1.777696817, 1.788424172 | 1.731766057, 1.704351228, 1.697733806, 1.708885045, 1.702113273 | 1.777696817/1.704351228 | 1.043034x |
| higher_cost | 1024 | 1.506671019, 1.504523635, 1.510098613, 1.862269317, 1.761529397 | 1.535875151, 1.505933507, 1.520280525, 1.487298282, 1.497690298 | 1.510098613/1.505933507 | 1.002766x |

Labels refer only to numeric windows on Cabbage, not connections to the named hosts. The high-cost baseline has outliers; its 0.3% median difference does not demonstrate a reliable gain.

## GPU results and stopping point

Inspected scaling.mk, check_devices.py, host_optimization_benchmark.py, engine_session.py, coordinator_pipeline.py, and scaling_gpu.cu. Used the persistent scaling GPU engine, not the CPU-only reproduction. Baseline-only controls below passed exact per-task expected/visited counts and normalized full native hit records against independent GMP, then exact decoded hit sets against the fifth-power-table oracle. Direct host hits are included in final hit totals.

| Bound/cap | Coefficient points | Native hits | Final hits incl. direct | RPC wall s | Engine s | CUDA event kernel s |
|---|---:|---:|---:|---:|---:|
| 34/384 | 275699 | 4 | 6 | 0.001334492001 | 0.001167420000 | 0.000750592000 |
| 100/2951 | 589483 | 10 | 25 | 0.000413264963 | 0.000311103000 | 0.000189600000 |
| 1000/42 | 4483388 | 2 | 2 | 0.000987671025 | 0.000820828000 | 0.000596800000 |

The fourth request (first high-shell window: lo=100000000001, hi=200000000000, first=3000000000, four patches) returned:

```json
{"request_id": 4, "box_complete": false, "error": "invalid base range"}
```

Rejected RPC wall time: 0.000137156982 s. The exact packet SHA-256 is 709642c7e118fbb5378be02f1827f90e244223fc443efb8d715e90e7e69e6af9.
Coordinator raised ValueError: Invalid native point count type because the failure response has no points_visited. Read-only inspection explains the rejection: src/kernel.hpp fixes LATTICE_MAX_BASE=100000000000, and src/io.hpp rejects task cmax above that limit. The requested high-shell domain exceeds it. No limit was changed.

Stopped immediately: no candidate GPU validation, no baseline/candidate GPU exact comparison, no paired GPU benchmark, and no GPU trial journals were created. This is an incomplete GPU validation with a native domain rejection, not an observed root-reuse mathematical discrepancy. The three baseline control timings are single observations, not optimization speedups.

## Limits and retained evidence

- CPU results measure this Cabbage CPU and local filesystem only. No NFS, shared ledger, service integration, or full-shell acceptance.
- GPU baseline controls cover three bounded small domains only. Requested high-shell GPU comparison remains blocked by the supplied CUDA engine range guard. No successful GPU validation claim for the candidate.
- No production deployment or new production coverage. Timing samples are short and scheduling/frequency variation is uncontrolled.
- Published CPU evidence: [all 30 trial timing records](cpu/benchmark-results.json), [baseline validation](cpu/validation-baseline.json), [candidate validation](cpu/validation-candidate.json), and test output in `cpu/*-tests.txt`. Full per-chunk/per-worker stage arrays, trial directories and scratch journals remain local; their original file hashes are recorded in [publication-manifest.json](publication-manifest.json).
- GPU evidence: [raw responses with exact counts/hits/timings](gpu/validation-baseline-raw.json), [traceback](gpu/validation-baseline.txt), [compiler output](gpu-build.txt), [harness derivation](make_gpu_probe.py), and [executed harness](cpu/gpu_probe.py). The `.txt` logs are byte-for-byte copies of the original `.log` files.
- No test is left running; final GPU state returned to Xorg-only / 25 MiB / 0% utilization.

Final resource snapshot, after all tests stopped, showed unrelated Neo4j container startup/admin processes consuming CPU. They were left untouched. No further timing was attempted. CPU availability was checked initially and during correctness checks, but was not continuously sampled throughout all 30 trials; scheduling contention cannot be excluded as a source of the high-cost outliers.

## Published evidence

This report and its compact evidence are published independently of the optimization patch. The tested handoff is pinned at [be5fcb6](https://github.com/paulnord/fifth42/tree/be5fcb6d5818d70035a9f2a8f31812f5f1f8b53f/optimization/exact-root-reuse-20261108). The original baseline source is pinned at `da4e1e312ce1558c9d8cf027c009f8b400f22b83`. No handoff sources were merged into `main`.

[SHA256SUMS](SHA256SUMS) authenticates the published files. The compact CPU benchmark export omits only each trial's detailed `rows` stage arrays; all other trial fields and every raw timing sample are retained. `publication-manifest.json` records that transformation and hashes the local originals. Raw journals, binaries, virtual environments and toolkits are not published. Some original script metadata says “cloud”; the actual host for these new results was Cabbage, as recorded above.
