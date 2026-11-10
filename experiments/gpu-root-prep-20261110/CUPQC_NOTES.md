# cuPQC-BigInt backend provenance and limits

`root_cupqc.cu` implements the same 2048-bit division-free exact root comparison
as the CGBN backend. Each root uses ROOT_TPI=4,8,16,32 cooperating lanes. The
host guard proves every shifted input and even rejected candidate product fits
2048 bits; `mul_low` therefore preserves the entire mathematical product.

The code was checked against NVIDIA cuPQC SDK **0.6.0** headers and then
compiled and linked locally with NVIDIA CUDA 13.2.78, runtime 13.2.75, NVVM
13.2.78, and CRT 13.2.78, targeting sm_86. All four cooperative variants
(4, 8, 16, 32 lanes) compiled. This workspace has no GPU: **GPU arithmetic
correctness, speed, and integration remain untested**. Successful Cabbage exact
fixture runs are mandatory before any performance conclusion.

The first Cabbage build exposed a pip-toolchain layout bug. It was reproduced
locally: NVVM's library resides in `cu13/lib/libnvvm.so.4`, but nvcc's LTO link
sets `-nvvmpath=cu13/nvvm` and expects `nvvm/lib64/libnvvm.so`. `stage_cuda.py`
creates a private overlay with the expected library link, without changing the
original CUDA installation or drivers. Merely setting LD_LIBRARY_PATH did not
fix this case; `-Xnvlink --nvvmpath` was overridden by nvcc's later default.

SDK download (official URL; redirects to a temporary signed NVIDIA URL):
https://developer.nvidia.com/downloads/compute/cupqc/downloads/secure/cupqc-sdk-0.6.0-x86_64.tar.gz

Observed archive size: 189031499 bytes.
SHA256: `8026ac00d81130180d2ff0afb3eb9bce852b76cc6a02141f9e45b799a17ae571`
Extracted directory: `cupqc-sdk-0.6.0-x86_64`.

NVIDIA states that downloading/using the SDK accepts its Math SDK license:
https://docs.nvidia.com/cuda/cupqc/additional/license.html
The SDK is not included or relicensed in this source package. Public volunteer
redistribution needs a separate license review; do not treat it as CGBN's
permissive source license.

Example compilation for our Ampere RTX cards:

```sh
nvcc -O3 -std=c++17 -dlto -arch=sm_86 -DROOT_SM=860 -DROOT_TPI=8 \
  -I"$CUPQC_ROOT/include/cupqc" -I"$CUPQC_ROOT/include" \
  root_cupqc.cu -L"$CUPQC_ROOT/lib" -lcupqc-bigint -o root_cupqc_tpi8
```

It shares the CGBN binary protocol and `gpu_check.py` certificates. It avoids
unsupported warp division, uint64 constructors/conversion, and error policies.
CUDA launch/runtime failures are checked. Exact arithmetic correctness and
full output certificates must still pass on every test instance.

References:
- https://docs.nvidia.com/cuda/cupqc/libraries/cupqc_bigint/cupqc_bigint_usage.html
- https://docs.nvidia.com/cuda/cupqc/libraries/cupqc_bigint/cupqc_bigint_feature.html
- https://docs.nvidia.com/cuda/cupqc/libraries/cupqc_bigint/api/device.html
