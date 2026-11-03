CXX := /usr/bin/g++-13
NVCC := /usr/local/cuda-12.8/bin/nvcc
CPPFLAGS := -Isrc
CXXFLAGS := -O3 -std=c++17 -Wall -Wextra -Wconversion
NVCCFLAGS := -O3 -std=c++17 -ccbin $(CXX) -arch=sm_86 -Icompat -Isrc -Xcompiler=-Wall,-Wextra

.PHONY: all cpu gpu smoke test test-gpu check-cuda13 clean test-optimized baseline
all: cpu gpu smoke bin/search_emulated bin/search_emulated_sanitize bin/compare_high bin/reference_cpu bin/reference_gpu
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

bin/reference_cpu: ../src/search_cpu.cpp ../src/exact.hpp ../src/search_common.hpp | bin
	$(CXX) -I../src $(CXXFLAGS) $< -o $@

bin/reference_gpu: ../src/search_gpu.cu ../src/exact.hpp ../src/search_common.hpp compat/bits/mathcalls.h | bin
	$(NVCC) $(NVCCFLAGS) -I../src $< -o $@

baseline: bin/reference_cpu bin/reference_gpu
	python3 prepare_baseline.py

bin/search_gpu: src/search_gpu.cu src/exact.hpp src/search_common.hpp src/row_search.hpp src/tuning_options.hpp compat/bits/mathcalls.h | bin
	$(NVCC) $(NVCCFLAGS) $< -o $@

bin/search_emulated: src/search_emulated.cpp src/exact.hpp src/search_common.hpp src/row_search.hpp src/tuning_options.hpp | bin
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $< -o $@

bin/search_emulated_sanitize: src/search_emulated.cpp src/exact.hpp src/search_common.hpp src/row_search.hpp src/tuning_options.hpp | bin
	$(CXX) $(CPPFLAGS) -O1 -g -std=c++17 -fsanitize=address,undefined -fno-sanitize-recover=all $< -o $@

bin/compare_high: tests/compare_high.cpp src/exact.hpp src/row_search.hpp | bin
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $< -o $@

bin/arithmetic_cpu: tests/arithmetic.cpp src/exact.hpp | bin
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $< -o $@

bin/arithmetic_cpu_sanitize: tests/arithmetic.cpp src/exact.hpp | bin
	$(CXX) $(CPPFLAGS) -O1 -g -std=c++17 -fsanitize=undefined -fno-sanitize-recover=all $< -o $@

bin/search_cpu_sanitize: src/search_cpu.cpp src/exact.hpp src/search_common.hpp | bin
	$(CXX) $(CPPFLAGS) -O1 -g -std=c++17 -fsanitize=undefined -fno-sanitize-recover=all $< -o $@

test: all bin/arithmetic_cpu bin/arithmetic_cpu_sanitize bin/search_cpu_sanitize
	python3 tests/test_search.py --cpu-only
	python3 tests/test_optimized.py --cpu-only

test-gpu: all bin/arithmetic_cpu bin/arithmetic_cpu_sanitize bin/search_cpu_sanitize
	python3 check_idle.py
	python3 prepare_baseline.py
	python3 tests/test_search.py --require-gpu
	python3 tests/test_optimized.py --require-gpu

check-cuda13: | bin
	/usr/local/cuda-13.4/bin/nvcc -O3 -std=c++17 -ccbin $(CXX) -arch=sm_86 src/cuda_smoke.cu -o bin/cuda_smoke_13
	./bin/cuda_smoke_13

clean:
	rm -f bin/search_cpu bin/search_gpu bin/cuda_smoke bin/arithmetic_cpu bin/arithmetic_cpu_sanitize bin/search_cpu_sanitize
