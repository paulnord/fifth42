#pragma once
#include "exact.hpp"
#include <algorithm>
#include <chrono>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

struct Options {
    int bound = -1;
    std::int64_t target = 42;
    long long start = 0, stop = -1;
    unsigned capacity = 10000;
    bool filtered = true;
};
inline long long parse_integer(const std::string& s) {
    std::size_t pos = 0;
    const long long n = std::stoll(s, &pos);
    if (pos != s.size()) throw std::runtime_error("invalid integer: " + s);
    return n;
}
inline Options parse_options(int argc, char** argv) {
    Options o;
    for (int i = 1; i < argc; i += 2) {
        if (i + 1 == argc) throw std::runtime_error("missing option value");
        const std::string k = argv[i], v = argv[i+1];
        if (k == "--filter") {
            if (v != "mod11" && v != "none") throw std::runtime_error("invalid filter");
            o.filtered = v == "mod11";
        } else {
            const long long n = parse_integer(v);
            if (k == "--bound") {
                if (n < 0 || n > MAX_BOUND)
                    throw std::runtime_error("bound must be in [0," + std::to_string(MAX_BOUND) + "]");
                o.bound = static_cast<int>(n);
            } else if (k == "--target") o.target = n;
            else if (k == "--row-start") o.start = n;
            else if (k == "--row-stop") o.stop = n;
            else if (k == "--capacity") {
                if (n < 1 || n > 1000000) throw std::runtime_error("capacity must be in [1,1000000]");
                o.capacity = static_cast<unsigned>(n);
            } else throw std::runtime_error("unknown option: " + k);
        }
    }
    if (o.bound < 0) throw std::runtime_error("--bound required");
    if (o.filtered && (o.target % 11 + 11) % 11 != 9)
        throw std::runtime_error("mod11 filter proved only for target == 9 (mod 11)");
    return o;
}
inline bool residue_minus_one(int n) {
    const int r = (n % 11 + 11) % 11;
    return r == 2 || r == 6 || r == 7 || r == 8 || r == 10;
}
inline std::size_t row_count(const Options& o) {
    return o.filtered ? static_cast<std::size_t>(2 * (o.bound / 11) + 1)
                      : static_cast<std::size_t>(2 * o.bound + 1);
}
inline int row_z(const Options& o, std::size_t r) {
    return o.filtered ? 11 * (static_cast<int>(r) - o.bound / 11)
                      : static_cast<int>(r) - o.bound;
}
inline void check_rows(Options& o) {
    const auto n = static_cast<long long>(row_count(o));
    if (o.stop == -1) o.stop = n;
    if (o.start < 0 || o.stop < o.start || o.stop > n)
        throw std::runtime_error("invalid half-open row interval");
}
struct Table {
    std::vector<int> xs;
    std::vector<I192> powers;
};
inline Table make_table(const Options& o) {
    Table t;
    const std::size_t max_n = static_cast<std::size_t>(2 * o.bound + 1);
    const std::size_t estimate = o.filtered ? max_n * 5 / 11 + 10 : max_n;
    t.xs.reserve(estimate);
    t.powers.reserve(estimate);
    for (int n = -o.bound; n <= o.bound; ++n) {
        if (!o.filtered || residue_minus_one(n)) {
            t.xs.push_back(n);
            t.powers.push_back(fifth(n));
        }
    }
    return t;
}
struct Hit { int a, b, z; };
inline bool hit_less(const Hit& a, const Hit& b) {
    if (a.z != b.z) return a.z < b.z;
    if (a.a != b.a) return a.a < b.a;
    return a.b < b.b;
}
inline void print_result(const char* backend, const Options& o, const Table& t,
                         const std::vector<Hit>& hits, std::uint64_t steps,
                         double seconds, double setup_seconds) {
    std::cout << "{\"arithmetic_bits\":192,\"backend\":\"" << backend << "\",\"bound\":" << o.bound
              << ",\"target\":" << o.target << ",\"filter\":\""
              << (o.filtered ? "mod11" : "none") << "\",\"row_start\":" << o.start
              << ",\"row_stop\":" << o.stop << ",\"total_rows\":" << row_count(o)
              << ",\"x_count\":" << t.xs.size() << ",\"steps\":" << steps
              << ",\"search_seconds\":" << seconds << ",\"setup_seconds\":" << setup_seconds
              << ",\"hits\":[";
    for (std::size_t i = 0; i < hits.size(); ++i) {
        if (i) std::cout << ',';
        std::cout << '[' << hits[i].a << ',' << hits[i].b << ',' << hits[i].z << ']';
    }
    std::cout << "]}\n";
}
using Clock = std::chrono::steady_clock;
inline double seconds_since(Clock::time_point p) {
    return std::chrono::duration<double>(Clock::now() - p).count();
}
