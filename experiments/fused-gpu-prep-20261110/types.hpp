#pragma once
#include <cstdint>
constexpr unsigned WIDTH=4096,LIMBS=128,BLOCK=128,VALUES=16;
struct Mem { uint32_t _limbs[LIMBS]; };
struct Input { uint64_t lo,hi,left,right,den,cap; uint32_t bits; };
struct Output { Mem value[VALUES]; };
