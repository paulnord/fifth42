CXX := /usr/bin/g++-13
NVCC := /usr/local/cuda-12.8/bin/nvcc
CPPFLAGS := -Isrc
CXXFLAGS := -O3 -std=c++17 -Wall -Wextra -Wconversion
NVCCFLAGS := -O3 -std=c++17 -ccbin $(CXX) -arch=sm_86 -Icompat -Isrc -Xcompiler=-Wall,-Wextra

.PHONY: all cpu gpu smoke test test-gpu check-cuda13 clean
all: cpu gpu smoke
cpu: bin/search_cpu
gpu: bin/search_gpu
smoke: bin/cuda_smoke

bin:
	mkdir -p bin

compat/bits/mathcalls.h: configure_cuda.py
	python3 configure_cuda.py

bin/cuda_smoke: src/cuda_smoke.cu compat/bits/mathcalls.h | bin
	$(NVCC) $(NVCCFLAGS) $< -o $@

bin/search_cpu: src/search_cpu.cpp src/exact.hpp src/search_common.hpp | bin
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $< -o $@

bin/search_gpu: src/search_gpu.cu src/exact.hpp src/search_common.hpp compat/bits/mathcalls.h | bin
	$(NVCC) $(NVCCFLAGS) $< -o $@

bin/arithmetic_cpu: tests/arithmetic.cpp src/exact.hpp | bin
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $< -o $@

bin/arithmetic_cpu_sanitize: tests/arithmetic.cpp src/exact.hpp | bin
	$(CXX) $(CPPFLAGS) -O1 -g -std=c++17 -fsanitize=undefined -fno-sanitize-recover=all $< -o $@

bin/search_cpu_sanitize: src/search_cpu.cpp src/exact.hpp src/search_common.hpp | bin
	$(CXX) $(CPPFLAGS) -O1 -g -std=c++17 -fsanitize=undefined -fno-sanitize-recover=all $< -o $@

test: all bin/arithmetic_cpu bin/arithmetic_cpu_sanitize bin/search_cpu_sanitize
	python3 tests/test_search.py

test-gpu: all bin/arithmetic_cpu bin/arithmetic_cpu_sanitize bin/search_cpu_sanitize
	python3 tests/test_search.py --require-gpu

check-cuda13: | bin
	/usr/local/cuda-13.4/bin/nvcc -O3 -std=c++17 -ccbin $(CXX) -arch=sm_86 src/cuda_smoke.cu -o bin/cuda_smoke_13
	./bin/cuda_smoke_13

clean:
	rm -f bin/search_cpu bin/search_gpu bin/cuda_smoke bin/arithmetic_cpu bin/arithmetic_cpu_sanitize bin/search_cpu_sanitize
