#pragma once
#include <cstdint>

#ifdef __CUDACC__
#define HD __host__ __device__
#else
#define HD
#endif

// Two's-complement signed 128-bit value. All limb operations are unsigned.
// Comparisons flip the sign bit before comparing the high word.
struct alignas(16) I128 {
    std::uint64_t lo, hi;
    HD static I128 from_i64(std::int64_t n) {
        return {static_cast<std::uint64_t>(n), n < 0 ? UINT64_MAX : 0};
    }
    HD I128 operator+(I128 b) const {
        const std::uint64_t l = lo + b.lo;
        return {l, hi + b.hi + static_cast<std::uint64_t>(l < lo)};
    }
    HD I128 operator-() const {
        const std::uint64_t l = ~lo + 1;
        return {l, ~hi + static_cast<std::uint64_t>(l == 0)};
    }
    HD bool operator==(I128 b) const { return lo == b.lo && hi == b.hi; }
    HD bool operator<(I128 b) const {
        const std::uint64_t sign = UINT64_C(1) << 63;
        return hi == b.hi ? lo < b.lo : (hi ^ sign) < (b.hi ^ sign);
    }
};
static_assert(sizeof(I128) == 16, "128-bit storage");

inline I128 pack(__int128 n) {
    const auto u = static_cast<unsigned __int128>(n);
    return {static_cast<std::uint64_t>(u), static_cast<std::uint64_t>(u >> 64)};
}

inline __int128 fifth(int n) {
    const __int128 x = n;
    const __int128 x2 = x * x;
    return x2 * x2 * x;
}

// At B <= 35,000,000: 3*B^5 + 2^63 < 2^127.
// No real intermediate wraps; wrapping is used only inside limb arithmetic.
constexpr int MAX_BOUND = 35000000;
