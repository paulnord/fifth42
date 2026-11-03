CXX := /usr/bin/g++-13
NVCC := /usr/local/cuda-12.8/bin/nvcc
CPPFLAGS := -Isrc
CXXFLAGS := -O3 -std=c++17 -Wall -Wextra -Wconversion
NVCCFLAGS := -O3 -std=c++17 -ccbin $(CXX) -arch=sm_86 -Icompat -Isrc -Xcompiler=-Wall,-Wextra
LDLIBS := -lgmpxx -lgmp
HEADERS := src/exact.hpp src/search_common.hpp src/row_search.hpp src/tuning_options.hpp src/gmp_oracle.hpp
.PHONY: all test test-gpu
all: bin/search_cpu bin/search_gpu bin/search_emulated bin/search_emulated_sanitize bin/cuda_smoke bin/arithmetic_cpu bin/arithmetic_cpu_sanitize bin/search_cpu_sanitize bin/compare_high bin/reference_cpu bin/sparse_host
bin:
	mkdir -p bin runs
compat/bits/mathcalls.h: configure_cuda.py
	python3 configure_cuda.py
bin/search_cpu: src/search_cpu.cpp $(HEADERS) | bin
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $< -o $@ $(LDLIBS)
bin/reference_cpu: ../src/search_cpu.cpp ../src/exact.hpp ../src/search_common.hpp | bin
	$(CXX) -I../src $(CXXFLAGS) $< -o $@
bin/search_gpu: src/search_gpu.cu src/sparse_self_test.inc $(HEADERS) compat/bits/mathcalls.h | bin
	$(NVCC) $(NVCCFLAGS) $< -o $@ $(LDLIBS)
bin/cuda_smoke: src/cuda_smoke.cu compat/bits/mathcalls.h | bin
	$(NVCC) $(NVCCFLAGS) $< -o $@
bin/search_emulated: src/search_emulated.cpp $(HEADERS) | bin
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $< -o $@
bin/search_emulated_sanitize: src/search_emulated.cpp $(HEADERS) | bin
	$(CXX) $(CPPFLAGS) -O1 -g -std=c++17 -fsanitize=address,undefined -fno-sanitize-recover=all $< -o $@
bin/arithmetic_cpu: tests/arithmetic.cpp src/exact.hpp | bin
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $< -o $@
bin/arithmetic_cpu_sanitize: tests/arithmetic.cpp src/exact.hpp | bin
	$(CXX) $(CPPFLAGS) -O1 -g -std=c++17 -fsanitize=undefined -fno-sanitize-recover=all $< -o $@
bin/search_cpu_sanitize: src/search_cpu.cpp $(HEADERS) | bin
	$(CXX) $(CPPFLAGS) -O1 -g -std=c++17 -fsanitize=undefined -fno-sanitize-recover=all $< -o $@ $(LDLIBS)
bin/compare_high: tests/compare_high.cpp $(HEADERS) | bin
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $< -o $@
bin/sparse_host: tests/sparse_host.cpp $(HEADERS) | bin
	$(CXX) $(CPPFLAGS) -O1 -g -std=c++17 -fsanitize=undefined -fno-sanitize-recover=all $< -o $@ $(LDLIBS)
test: all
	./bin/sparse_host
	python3 tests/test_search.py --cpu-only
	python3 tests/test_optimized.py --cpu-only
	python3 tests/test_jobs.py
test-gpu: all
	python3 check_idle.py
	./bin/sparse_host
	python3 tests/test_search.py --require-gpu
	python3 tests/test_optimized.py --require-gpu
