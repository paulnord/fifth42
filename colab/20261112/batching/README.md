# Fifth42: CPU preparation batching and process-pool dispatch

This is the follow-up to the Colab worker-scaling result. Hold preparation at
**eight workers**, and compare **1, 2, 4 and 8 original windows per CPU preparation
batch**, each with process-pool map chunk sizes **8 and 32**. The eight policies
run in randomized order with three repetitions. A matched windows=1/chunks=8
baseline is included in every repetition.

Each trial replays the original nine-window dataset **three times**. That gives
27 window visits, 69 unchanged native requests, 6,912 logical-cell visits and
2,327,061,582 coefficient positions per trial. There remain only nine unique
windows / 2,304 unique logical cells. Every pass has separate per-region durable
journals, and every generated packet and certificate identity must match the
published independent oracle. This is repeated benchmark work with zero new
scientific coverage; production and ownership remain unchanged.

The native packets are not combined. Original arithmetic, native limits, exact
certification, output checks and the eight-record / 0.25-second journal policy
stay intact. The frozen scheduler's multiwindow path performs fewer process-pool
round trips while retaining each original execution and journal window.

## Measurements and interpretation

Report median local pipeline time and logical-cell visits/second, speedup over
the matched baseline, consumer waiting for preparation, process-pool map call
count/time, original segment count, parent consistency checks, native RPC/kernel
time, local journal writes and durable recovery. A pool map includes worker
computation, IPC and parent deserialization; its wall time does not isolate
serialization cost. The canonical certificate/native serialization is unchanged.

The frozen scheduler uses two ready items for single-window preparation and one
ready batch for multiwindow preparation. These are policy comparisons with that
derived queue behavior, not an experiment holding window-level queue depth fixed.
Queue depth is measured in preparation batches. Compare actual waiting time and
payload sizes; do not compare raw depth numbers as though each item represented
the same amount of work. Prepared items have a 12 MiB cap and all policies stay
within a common 48 MiB reservation ceiling. Native mathematical limits are unchanged.

All timing trials include planning/certification, assembly, checked native work,
verification and the final local journal flush. Pool/engine startup, fresh GMP
preflight and journal reopening are reported separately. The fresh preflight
checks all 42 original packets and nonempty controls, and rejects an intentionally
incomplete response. The arithmetic profile from the previous test need not be
repeated because this experiment changes scheduling only.

The test still excludes remote mirrors/network delivery and production GMP audit
scheduling. Repeated inputs and short samples do not establish sustained or
distributed production throughput. No adoption follows automatically.

## Run

Use the current CUDA GPU runtime; L4 is sufficient. CPU affinity must leave room
for eight workers plus the coordinator. The notebook reuses the immutable original
input bundle and pinned planning sources, sets up a separate Python 3.12 environment,
installs GMP headers and exact pinned dependencies, and rebuilds for the actual GPU.
No existing runtime or production source guards are removed.

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONHASHSEED=0 \
  pipeline-venv/bin/python batching/batch_bench.py --backend gpu --workers 8 \
  --batch-windows 1 2 4 8 --map-chunksizes 8 32 --passes 3 --repeats 3 \
  --max-seconds 480
```

Stop on any source, packet/certificate, count/hit, original-window routing or
durable-recovery mismatch. The runner is bounded to eight minutes and the complete
notebook session to fifteen minutes. Download `Fifth42_Batching_Results.zip`, which
contains the current report, build/log details, all pass-specific journals and
source identities, before releasing the runtime. Its export allowance is 64 MiB.
