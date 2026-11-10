#pragma once
#include "search_common.hpp"
#include "row_search.hpp"

struct TuningOptions {
    Options search;
    Variant variant = Variant::highword;
    int block_size = 128;
};
inline TuningOptions tuning_options(int argc, char** argv) {
    TuningOptions o;
    std::vector<char*> rest{argv[0]};
    for (int i = 1; i < argc; i += 2) {
        if (i+1 == argc) throw std::runtime_error("missing option value");
        const std::string k = argv[i], v = argv[i+1];
        if (k == "--variant") {
            if (v == "baseline") o.variant = Variant::baseline;
            else if (v == "cached") o.variant = Variant::cached;
            else if (v == "pruned") o.variant = Variant::pruned;
            else if (v == "highword") o.variant = Variant::highword;
            else throw std::runtime_error("invalid variant");
        } else if (k == "--block-size") {
            const auto n = parse_integer(v);
            if (n != 64 && n != 128 && n != 256 && n != 512)
                throw std::runtime_error("block size must be 64,128,256,512");
            o.block_size = static_cast<int>(n);
        } else { rest.push_back(argv[i]); rest.push_back(argv[i+1]); }
    }
    o.search = parse_options(static_cast<int>(rest.size()),rest.data());
    check_rows(o.search);
    return o;
}
