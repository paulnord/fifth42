# Fifth42: Colab GPU tests for Gemini

**[Open and run in Google Colab](https://colab.research.google.com/github/paulnord/fifth42/blob/daac4d600cfdd01c34349e3d1da25fc7cde95953/colab/20261112/Fifth42_Colab_Tests.ipynb)**

Open [Fifth42_Colab_Tests.ipynb](Fifth42_Colab_Tests.ipynb) in Google Colab and give
Gemini [GEMINI_HANDOFF.txt](GEMINI_HANDOFF.txt). Select **L4 GPU** for the first run
if offered. The notebook obtains all sources and data from an immutable GitHub
commit and checks their hashes. No uploads or campus filesystem access are needed.

This is a bounded exact-integer benchmark, with **zero new scientific coverage**.
Local CPU/GMP verification passed. **The first Colab L4 replay passed all 42
packet checks against independent GMP**, including fresh GMP reproduction and
incomplete-response rejection.

## What it tests

- 23 production-sized native packets containing 775,687,194 coefficient positions.
- 16 tiny native packets containing 13,748,364 positions.
- Nonempty positive and negative residual controls, exact reconstruction, complete
  per-task counts, and rejection of a deliberately incomplete response.
- GPU kernel, native RPC and complete replay/verification time, with startup separate.

The realistic 23-request stream remains **byte-identical** after coalescing under
unchanged 50-million-point packet limits. The runner does not report a fictional
batching speedup for that case. Tiny packets combine 16 requests into one.

## First Colab result: NVIDIA L4

The supplied [L4 report](results/benchmark-l4.json) contains seven repetitions per
case. [Artifact review](results/colab-l4-review.json) confirmed source/data hashes,
trial completeness and the reported timing summaries.

| Prepared input | Requests | Positions | Median replay | Median kernel |
| --- | ---: | ---: | ---: | ---: |
| Production-sized | 23 | 775,687,194 | 35.42 ms | 17.61 ms |
| Tiny, separate | 16 | 13,748,364 | 4.091 ms | 2.250 ms |
| Tiny, combined | 1 | 13,748,364 | 0.727 ms | 0.351 ms |

Tiny-packet replay improved 5.63x. Production-sized requests stayed byte-identical,
so that result supplies no production batching speedup. The benchmark completed
in 41.08 seconds including fresh GMP checks; GPU startup was 0.203 seconds.
Compute-unit usage was not recorded, so cost efficiency remains unmeasured.
These short packet replays do not establish sustained or full-pipeline throughput.
Keep L4 as a validated test backend; stronger hardware needs a matched comparison
including CPU preparation and actual credit usage before adoption.

A [second L4 run](results/benchmark-l4-r2.json) also passed all 42 packet/GMP
checks. Median production-sized replay was 35.40 ms (0.03% below the first run),
with 17.61 ms kernel time; tiny batching improved 5.63x. Its
[artifact review](results/colab-l4-r2-review.json) confirms the same inputs and
seven repetitions per case. Cost remains unrecorded.

A [third supplied ZIP](results/benchmark-l4-r3.json) reports **NVIDIA L4** in its
hardware record, although it was supplied for the A100 comparison. All 42 checks
passed and production-sized replay was 35.36 ms. It is archived as another L4
result. The A100 assignment requires a device-name check before building or
benchmarking. A later ZIP confirmed A100 and completed the comparison below.

The [matched A100 comparison](GPU_COMPARISON.md) passed all 42 packet/GMP checks
on NVIDIA A100-SXM4-40GB. Median production-sized replay was **36.84 ms** versus
L4's **35.40 ms** (A100 took 4.06% longer); kernel time was **18.86 ms** versus
**17.61 ms**. This short replay establishes no A100 speed advantage. Keep L4 as
the validated replay backend; the next useful measurement is CPU preparation and
full-pipeline throughput. Compute-unit rates remain unrecorded. H100 was unavailable.

## CPU preparation and local pipeline scaling

**[Open the pipeline test in Colab](https://colab.research.google.com/github/paulnord/fifth42/blob/421164a6a7e55091a027b2d1a1dc2a5631fa620b/colab/20261112/pipeline/Fifth42_Pipeline_Tests.ipynb)** ·
[Gemini instructions](pipeline/GEMINI_HANDOFF.txt) · [Scope and interpretation](pipeline/README.md)

Use the GPU already connected. Compare 1, 2, 4 and 8 CPU preparation workers over
three randomized repetitions, including exact planning/certification, GPU replay,
verification and locally durable journals. The same nine windows must regenerate
the original 23 packet byte streams and certificates. All 42 independent GMP
checks and durable journal recovery must pass. Python 3.12 and the original exact
dependency guards are preserved in an isolated runtime environment.

The [Colab L4 pipeline results](pipeline_results/REPORT.md) passed all checks.
Median local pipeline time fell from **2.050 s with one preparation worker to
0.606 s with eight (3.38x)**. Kernel execution stayed near 18 ms, while the consumer
still waited 0.376 s for prepared work at eight workers. CPU preparation and its
coordination limit this configuration. Eight workers is the next Colab baseline;
production remains unchanged. The complete result ZIP and an independent review
of its 36 journals/276 native receipts are published with the report.

Download Fifth42_Pipeline_Results.zip before releasing the runtime. The runner is
bounded to eight minutes and the whole notebook to fifteen minutes. Remote
mirrors/network delivery and production GMP audit scheduling are excluded;
there is zero new search coverage and no demonstrated production speedup.

## Next test: CPU preparation batching and dispatch

**[Open the new batching notebook in Colab](https://colab.research.google.com/github/paulnord/fifth42/blob/a552a30d30eb86ad5ee4f0800c6df5ae3691486a/colab/20261112/batching/Fifth42_Batching_Tests.ipynb)** ·
[Gemini instructions](batching/GEMINI_HANDOFF.txt) · [Scope and policies](batching/README.md)

Hold preparation at eight workers. Compare batches of 1/2/4/8 original windows
and process-pool map chunk sizes 8/32, with three randomized repetitions. Each
trial makes three passes over the same verified nine windows, retaining separate
per-pass journals and unchanged native packet bytes/certificate identities.
The matched windows=1/chunks=8 baseline is included in every repetition.

All eight policies passed local CPU correctness and repeated-pass recovery checks;
Colab GPU timing results remain pending. No original dependency/math/native guards
are removed. Run top to bottom on a CUDA GPU with at least nine allocated logical
CPUs, then download **Fifth42_Batching_Results.zip**. Setup/testing is bounded to
fifteen minutes. This is a local replay policy test with zero new search coverage.

## Run

The notebook rebuilds native code for the GPU actually assigned using
`nvcc -arch=native`. It uses Python standard-library code and C++/CUDA/GMP; the
preparation host's pinned Python3.12/gmpy2/fpylll environment is not needed.
The notebook installs `libgmp-dev` before building and imports the Colab download
helper in the result-export cell, so a fresh runtime has both requirements.
For a manual build, install `libgmp-dev` and ensure `g++` is available first.

The GPU command is:

```bash
python3 build.py --gpu
python3 colab_bench.py --backend gpu --repeats 7 --max-seconds 180 --verify-gmp
```

Keep the Colab Pro notebook open and download its result ZIP before disconnecting.
Record the compute-unit rate/balance from Colab's UI when visible. The code cannot
infer account billing. A stronger GPU is a comparison candidate, not a promised
speedup for this integer workload or its CPU-heavy preparation pipeline.

## Files and integrity

Readable native and Python sources are in this directory. `transport/` contains
text chunks of the compressed source/data bundle so every Git file stays within
the repository's 256 KiB text-file limit. The notebook decodes them automatically;
this does not require Git LFS or a release attachment. The transport manifest
checks each chunk and the reconstructed archive; the archive has internal hashes.
`load_bundle.py` provides the same reconstruction for a local repository checkout.

`results/` contains the local CPU/GMP checks and input-export provenance. Hardware
process details were removed and build paths made relative for publication; exact
results and timing samples remain. The dataset is regenerated at representative
Ada/Cabbage windows and is not a live Ada packet capture.

GPU comparisons do not include CPU planning, network transfers, cloud checkpoints
or durable production journals. Any later scientific search needs a new disjoint
reservation, the exact exclusions and independently reconciled durable receipts.

[Colab usage guidance](https://research.google.com/colaboratory/faq.html) ·
[CUDA architecture options](https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/)
