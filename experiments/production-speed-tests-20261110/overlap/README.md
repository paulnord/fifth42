# TEST_ONLY two-stream candidate

Current production protocol has exactly one request in flight: host sends a frame,
waits for a result, then sends the next. Merely using `cudaMemcpyAsync` cannot
create cross-request overlap. This candidate keeps that protocol unchanged and
splits **each packet's tasks** across two independent CUDA streams, with separate
pinned and device buffers. Task IDs and exact coverage counts remain global.
Uploads and downloads in one lane may overlap the other lane's kernel. A packet
with only one task gets no useful overlap. Both streams are synchronized before a
response or error; overflow in either lane or the combined output returns no
coverage. No production integration, restart, ledger or reservation is involved.

Copy `scaling_gpu_overlap.cu` beside the baseline `scaling_gpu.cu` in the isolated
worker's `native-baseline/src/`, retaining the original headers/vendor code.
Build with the **same compiler flags and architecture as the baseline**, e.g.

```
nvcc -O3 -std=c++17 -arch=sm_86 native-baseline/src/scaling_gpu_overlap.cu -o bin/scaling_gpu_overlap
```

First run `make_controls.py CONTROL_DIR`, then use `bench_overlap.py` with
`--baseline .../scaling_gpu --candidate .../scaling_gpu_overlap --gmp .../gmp_reference
--packets CONTROL_DIR --output FRESH_RESULT_DIR`. It performs a full GMP
comparison before and during alternating repeated timings. Controls include
zero/one/odd/even/many task counts, nonempty residual -30, and empty hit sets.
Also run existing native arithmetic/range and candidate-capacity tests; those
must pass before representative timing.

For a meaningful performance result, export representative **already certified**
packets for sparse/middle/dense original-cell windows to `.packet` files and run
both engines on exactly those bytes. Small controls do not predict production
speed. Report task/chunk counts and packet sizes, medians of complete RPC time,
and CPU utilization. This replay excludes CPU preparation, GMP auditing of live
production, and durable writes. A win still requires end-to-end integration tests.

The candidate `kernel_seconds` is the **sum of per-stream event intervals**, not
critical-path wall time. Use harness `rpc_seconds` for timing comparisons. The
experiment deliberately makes no promise that two streams help; extra launches,
GPU contention, pinned memory and small packets may make it slower.

Local verification: harness syntax checked; six controls pass independent GMP
and CPU framed-engine replay. CUDA has **not** been compiled or run in the author
workspace (no nvcc/GPU). Cabbage must run those gates. No speedup claimed.
