# Fifth42: Colab GPU tests for Gemini

**[Open and run in Google Colab](https://colab.research.google.com/github/paulnord/fifth42/blob/cfbe8059d452e2e60923b0a01a9a1ae7eb52236d/colab/20261112/Fifth42_Colab_Tests.ipynb)**

Open [Fifth42_Colab_Tests.ipynb](Fifth42_Colab_Tests.ipynb) in Google Colab and give
Gemini [GEMINI_HANDOFF.txt](GEMINI_HANDOFF.txt). Select **L4 GPU** for the first run
if offered. The notebook obtains all sources and data from an immutable GitHub
commit and checks their hashes. No uploads or campus filesystem access are needed.

This is a bounded exact-integer benchmark, with **zero new scientific coverage**.
Local CPU/GMP verification passed. **Colab GPU testing remains pending.**

## What it tests

- 23 production-sized native packets containing 775,687,194 coefficient positions.
- 16 tiny native packets containing 13,748,364 positions.
- Nonempty positive and negative residual controls, exact reconstruction, complete
  per-task counts, and rejection of a deliberately incomplete response.
- GPU kernel, native RPC and complete replay/verification time, with startup separate.

The realistic 23-request stream remains **byte-identical** after coalescing under
unchanged 50-million-point packet limits. The runner does not report a fictional
batching speedup for that case. Tiny packets combine 16 requests into one.

## Run

The notebook rebuilds native code for the GPU actually assigned using
`nvcc -arch=native`. It uses Python standard-library code and C++/CUDA/GMP; the
preparation host's pinned Python3.12/gmpy2/fpylll environment is not needed.
If development headers are missing, install `libgmp-dev` and `g++` in Colab.

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
