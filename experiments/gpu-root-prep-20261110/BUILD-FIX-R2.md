# Revision 2: diagnosed build failures

Cabbage report `6fd18655edcfb4693ff8ed0377c23d3df36cda2f` tested revision 1 and correctly stopped without claiming GPU results.

## CGBN

Our source omitted `gmp.h` before `cgbn/cgbn.h`. CGBN selects its supported host adapter using the GMP header guard; without it, `cgbn_cpu.h` emits `You must use GMP for now`. This was a source/include-order defect, not absent gmpy2. Revision 2 includes the header, links `-lgmp`, and checks the development header/library before building.

## cuPQC

The exact `nvlink fatal: elfLink linker library load error` was reproduced using the same PyPI CUDA 13.2.78 compiler. The split package stores `libnvvm.so.4` in `nvidia/cu13/lib`; the compiler directs nvlink to `nvidia/cu13/nvvm`, where the expected `lib64/libnvvm.so` is missing. Adding the expected private library layout fixed the link. `LD_LIBRARY_PATH` alone and an `-Xnvlink` override did not fix it because nvcc appends its own path. The runner stages a private overlay rather than modifying the installed compiler.

## Validation boundary

Compilation and linking can now be tested in a CPU-only environment. This does NOT demonstrate GPU arithmetic correctness or speed. Cabbage must still run every exact certificate and reject malformed inputs before performance comparisons. Do not restart or modify production as part of this experiment.
