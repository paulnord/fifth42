# Fifth42: longer matched batching test

The previous L4 experiment found a roughly 10–11% local throughput improvement
from preparing four or eight windows together. Eight was only 0.48% ahead of four
and the sample ranges overlapped. This follow-up compares **1, 4 and 8 windows per
CPU preparation batch**, holds map chunk size at **8**, and runs **five randomized
matched repetitions** with **12 passes per trial**. Preparation uses eight workers.

Run the notebook on your current CUDA GPU with at least nine allocated CPU cores
in its affinity. It checks and records the actual device; an A100 is not required.
The benchmark remains bounded to eight minutes, with fifteen minutes for the
whole setup/test session. Download `Fifth42_Sustained_Batching_Results.zip` before
disconnecting. If it fails, run the final export cell to retain its failure log.

Each trial visits the same nine original windows 12 times: 108 window visits,
276 unchanged native requests, 27,648 logical-cell visits and 9,308,246,328
coefficient positions. The full run has 15 trials, 1,620 window visits, 4,140 native
requests and 540 per-pass/per-region journals. There are still only nine unique
input windows. This is repeated benchmark work with **zero new search coverage**.

The planning sources, dependency pins, exact certificates, independent GMP
preflight, native limits and native code are unchanged. The new runner differs
from the preceding batching runner in its bounded repetition/pass profile and
three-policy selection. It still uses the original eight-record / 0.25-second
journal policy and exact per-original-window receipts. The finite export allowance
is 96 MiB to retain every additional journal, not just timing summaries.

The scheduler's ready-buffer behavior differs between single- and multiwindow
preparation. These are complete scheduling-policy comparisons. Map wall time
includes computation, IPC and deserialization; stage sums overlap. Longer trials
reduce short-run noise but do not establish thermal steady state, production
throughput, a global optimum or compute-unit cost efficiency.

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONHASHSEED=0 \
  pipeline-venv/bin/python batching_sustained/batch_bench.py \
  --backend gpu --workers 8 --batch-windows 1 4 8 --map-chunksizes 8 \
  --passes 12 --repeats 5 --max-seconds 480
```

Every run repeats the fresh independent GMP preflight on all 42 original packets,
including nonempty controls and incomplete-response rejection. Every regenerated
packet and certificate must match the original independent oracle. Every journal
must close and reopen at its complete durable cursor. Stop on any mismatch.

The independent `review_results.py` checks exported hashes, build/source/input
identity, complete matched trials, all journal chains/cursors and every native
count/hit receipt against the saved GMP oracle. Its default profile is the full
GPU run above; explicit smaller CPU parameters exist only for local reproduction.
It reports each repetition's four-versus-eight throughput ratio and payload sizes
so a near tie can be reported as a tie. Keep production unchanged pending separate
production validation.
