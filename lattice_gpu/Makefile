CXX ?= g++
NVCC ?= /usr/local/cuda/bin/nvcc
HEADERS := src/kernel.hpp src/io.hpp vendor/exact.hpp
.PHONY: all
all: bin/emulated bin/emulated-sanitized bin/cuda
bin:
	mkdir -p bin
bin/emulated: src/emulated.cpp $(HEADERS) | bin
	$(CXX) -std=c++17 -O3 -Wall -Wextra -Werror $< -o $@
bin/emulated-sanitized: src/emulated.cpp $(HEADERS) | bin
	$(CXX) -std=c++17 -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=all $< -o $@
bin/cuda: src/enumerate.cu $(HEADERS) | bin
	$(NVCC) -std=c++17 -O3 -arch=sm_86 -ccbin $(CXX) $< -o $@
