#include <cuda_runtime.h>
#include <cstdio>

__global__ void check_kernel(unsigned long long* p) {
    const unsigned i = threadIdx.x;
    p[i] = (0xffffffffffffffffULL - i) + (i + 2ULL);
}

int main() {
    int count = 0;
    cudaError_t e = cudaGetDeviceCount(&count);
    if (e != cudaSuccess || count < 1) {
        std::fprintf(stderr, "cudaGetDeviceCount: %s (%d), devices=%d\n",
                     cudaGetErrorString(e), int(e), count);
        return 1;
    }
    cudaDeviceProp prop{};
    e = cudaGetDeviceProperties(&prop, 0);
    if (e != cudaSuccess) return 2;
    std::printf("GPU: %s, compute capability %d.%d\n", prop.name, prop.major, prop.minor);
    unsigned long long* d = nullptr;
    e = cudaMalloc(&d, 256 * sizeof(*d));
    if (e != cudaSuccess) return 3;
    check_kernel<<<1, 256>>>(d);
    e = cudaGetLastError();
    if (e != cudaSuccess) return 4;
    unsigned long long h[256];
    e = cudaMemcpy(h, d, sizeof(h), cudaMemcpyDeviceToHost);
    if (e != cudaSuccess) {
        std::fprintf(stderr, "kernel/copy: %s\n", cudaGetErrorString(e));
        return 5;
    }
    for (auto v : h) if (v != 1ULL) return 6;
    e = cudaFree(d);
    if (e != cudaSuccess) return 7;
    std::puts("PASS: nvcc + requested host compiler + GPU executed and checked 256 results");
}
