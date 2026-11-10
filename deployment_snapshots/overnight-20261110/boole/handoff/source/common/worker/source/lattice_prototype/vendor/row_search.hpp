#pragma once
#include "exact.hpp"

enum class Variant { baseline, cached, pruned, highword };

struct PackedPowers {
    const I192* p;
    HD I192 get(int i) const { return p[i]; }
};
struct SplitPowers {
    const std::uint64_t* lo;
    const Upper128* hi;
    HD I192 get(int i) const { return {lo[i], hi[i]}; }
};

HD inline int compare(I192 a, I192 b) {
    return a < b ? -1 : (b < a ? 1 : 0);
}
HD inline bool high_less(Upper128 a, Upper128 b) {
    return a<b;
}

// The exact high word of a+b is either h or h+1, depending on carry.
// If both possibilities order the same way against the goal, low words
// cannot change that answer. Otherwise fall back to full 128-bit addition.
HD inline int compare_high_first(SplitPowers p, int i, int j,
                                Upper128 ah, Upper128 bh, I192 goal) {
    const Upper128 h = ah + bh;
    if (high_less(h, goal.hi) && high_less(h+1, goal.hi)) return -1;
    if (high_less(goal.hi, h) && high_less(goal.hi, h+1)) return 1;
    return compare(I192{p.lo[i],ah} + I192{p.lo[j],bh}, goal);
}

template<class Powers>
HD int lower_power(Powers p, int n, I192 key) {
    int lo = 0, hi = n;
    while (lo < hi) {
        const int mid = lo + (hi-lo)/2;
        if (p.get(mid) < key) lo = mid+1;
        else hi = mid;
    }
    return lo;
}
template<class Powers>
HD int upper_power(Powers p, int n, I192 key) {
    int lo = 0, hi = n;
    while (lo < hi) {
        const int mid = lo + (hi-lo)/2;
        if (!(key < p.get(mid))) lo = mid+1;
        else hi = mid;
    }
    return lo;
}

struct PairRange {
    int i, j, a_stop, b_start;
    HD bool valid() const { return i <= j && i < a_stop && j >= b_start; }
};

template<class Powers>
HD PairRange feasible_range(Powers p, int n, I192 goal) {
    if (!n) return {0,-1,0,0};
    const I192 first = p.get(0), last = p.get(n-1);
    if (goal < first+first || last+last < goal) return {0,-1,0,0};
    // If a < goal-max, even b=max is too small. If b > goal-min,
    // even a=min is too large. Both subtractions fit under MAX_BOUND's proof.
    const int i = lower_power(p,n,goal+(-last));
    const int j = upper_power(p,n,goal+(-first))-1;
    // Arithmetic right shift implements floor(goal/2) without signed shifts.
    const I192 floor_half=goal.floor_half();
    const I192 ceil_half = floor_half + I192{goal.lo & 1,0};
    // In any ordered solution a<=b, a^5 <= floor(goal/2) and
    // b^5 >= ceil(goal/2). Keep equality for repeated variables.
    return {i,j,upper_power(p,n,floor_half),lower_power(p,n,ceil_half)};
}

template<class Emit>
HD unsigned long long baseline_row(PackedPowers p, int n, I192 goal, Emit emit) {
    int i = 0, j = n-1;
    unsigned long long steps = 0;
    while (i <= j) {
        const int c = compare(p.get(i)+p.get(j),goal);
        ++steps;
        if (c < 0) ++i;
        else if (c > 0) --j;
        else { emit(i,j); ++i; --j; }
    }
    return steps;
}

template<bool Prune, class Emit>
HD unsigned long long cached_row(PackedPowers p, int n, I192 goal, Emit emit) {
    PairRange r = Prune ? feasible_range(p,n,goal) : PairRange{0,n-1,n,0};
    if (!r.valid()) return 0;
    I192 a = p.get(r.i), b = p.get(r.j);
    unsigned long long steps = 0;
    while (r.valid()) {
        const int c = compare(a+b,goal);
        ++steps;
        if (c < 0) {
            ++r.i;
            if (r.valid()) a = p.get(r.i);
        } else if (c > 0) {
            --r.j;
            if (r.valid()) b = p.get(r.j);
        } else {
            emit(r.i,r.j); ++r.i; --r.j;
            if (r.valid()) { a = p.get(r.i); b = p.get(r.j); }
        }
    }
    return steps;
}

template<class Emit>
HD unsigned long long highword_row(SplitPowers p, int n, I192 goal, Emit emit) {
    PairRange r = feasible_range(p,n,goal);
    if (!r.valid()) return 0;
    Upper128 a = p.hi[r.i], b = p.hi[r.j];
    unsigned long long steps = 0;
    while (r.valid()) {
        const int c = compare_high_first(p,r.i,r.j,a,b,goal);
        ++steps;
        if (c < 0) {
            ++r.i;
            if (r.valid()) a = p.hi[r.i];
        } else if (c > 0) {
            --r.j;
            if (r.valid()) b = p.hi[r.j];
        } else {
            emit(r.i,r.j); ++r.i; --r.j;
            if (r.valid()) { a = p.hi[r.i]; b = p.hi[r.j]; }
        }
    }
    return steps;
}
