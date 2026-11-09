CXX ?= g++
NVCC ?= /usr/local/cuda/bin/nvcc
SCALING_HEADERS := src/stream_io.hpp src/io.hpp src/kernel.hpp vendor/exact.hpp
.PHONY: scaling scaling-host
scaling: scaling-host bin/scaling_gpu
scaling-host: bin/scaling_cpu bin/scaling_cpu_sanitize bin/scaling_oracle
bin:
	mkdir -p bin
bin/scaling_cpu: src/scaling_cpu.cpp $(SCALING_HEADERS) | bin
	$(CXX) -std=c++17 -O3 -Wall -Wextra -Werror -pthread $< -o $@
bin/scaling_cpu_sanitize: src/scaling_cpu.cpp $(SCALING_HEADERS) | bin
	$(CXX) -std=c++17 -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=all -pthread $< -o $@
bin/scaling_gpu: src/scaling_gpu.cu $(SCALING_HEADERS) | bin
	$(NVCC) -std=c++17 -O3 -arch=sm_86 -ccbin $(CXX) $< -o $@
bin/scaling_oracle: scaling_oracle.cpp | bin
	$(CXX) -std=c++17 -O3 -Wall -Wextra -Werror $< -o $@
