#include <cuda_runtime.h>
__global__ void smoke(int *p) { *p=42; }
int main(){ int *p; if(cudaMalloc(&p,sizeof(int))!=cudaSuccess)return 1; smoke<<<1,1>>>(p); int n=0; auto e=cudaMemcpy(&n,p,sizeof(int),cudaMemcpyDeviceToHost); cudaFree(p); return e==cudaSuccess&&n==42?0:2; }
