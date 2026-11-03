void sparse_gpu_self_test() {
    const std::vector<int> xs{-MAX_BOUND,-70000000,-50000000,-44275339,-35,-1,0,2,35,44275339,50000000,70000000,MAX_BOUND};
    std::vector<I192> powers,goals;
    std::vector<mpz_class> native;
    std::vector<std::uint64_t> lows;
    std::vector<Upper128> highs;
    for(int x:xs) {
        const auto p=fifth(x);const auto g=arbitrary_fifth(x);
        if(arbitrary(p)!=g)throw std::runtime_error("host fifth power/GMP mismatch");
        powers.push_back(p);native.push_back(g);lows.push_back(p.lo);highs.push_back(p.hi);
    }
    for(std::size_t i=0;i<xs.size();++i)for(std::size_t j=i;j<xs.size();++j)
        for(int delta:{-1,0,1})goals.push_back(from_arbitrary(mpz_class(native[i]+native[j])+delta));
    std::vector<int> zs(goals.size());
    std::vector<Hit> expected;
    for(std::size_t r=0;r<goals.size();++r) {
        zs[r]=static_cast<int>(r);
        for(std::size_t i=0;i<xs.size();++i)for(std::size_t j=i;j<xs.size();++j)
            if(mpz_class(native[i]+native[j])==arbitrary(goals[r]))
                expected.push_back({static_cast<int>(i),static_cast<int>(j),static_cast<int>(r)});
    }
    std::sort(expected.begin(),expected.end(),hit_less);
    DeviceBuffer<I192> p(powers.size()),g(goals.size());
    DeviceBuffer<std::uint64_t> lo(lows.size());DeviceBuffer<Upper128> hi(highs.size());
    DeviceBuffer<int> z(zs.size());DeviceBuffer<Hit> hits(65536);
    DeviceBuffer<unsigned long long> count(1),steps(goals.size());
    checked(cudaMemcpy(p.p,powers.data(),powers.size()*sizeof(I192),cudaMemcpyHostToDevice),"sparse powers");
    checked(cudaMemcpy(g.p,goals.data(),goals.size()*sizeof(I192),cudaMemcpyHostToDevice),"sparse goals");
    checked(cudaMemcpy(lo.p,lows.data(),lows.size()*sizeof(lows[0]),cudaMemcpyHostToDevice),"sparse lows");
    checked(cudaMemcpy(hi.p,highs.data(),highs.size()*sizeof(highs[0]),cudaMemcpyHostToDevice),"sparse highs");
    checked(cudaMemcpy(z.p,zs.data(),zs.size()*sizeof(int),cudaMemcpyHostToDevice),"sparse rows");
    const auto n=static_cast<int>(xs.size());const auto rows=static_cast<unsigned>(goals.size());
    for(Variant v:{Variant::baseline,Variant::cached,Variant::pruned,Variant::highword}) {
        checked(cudaMemset(count.p,0,sizeof(unsigned long long)),"sparse clear");
#define SPARSE_LAUNCH(vv) search_rows<vv><<<(rows+127)/128,128>>>(p.p,lo.p,hi.p,n,g.p,z.p,rows,hits.p,count.p,65536,steps.p)
        switch(v) {
            case Variant::baseline:SPARSE_LAUNCH(Variant::baseline);break;
            case Variant::cached:SPARSE_LAUNCH(Variant::cached);break;
            case Variant::pruned:SPARSE_LAUNCH(Variant::pruned);break;
            case Variant::highword:SPARSE_LAUNCH(Variant::highword);break;
        }
#undef SPARSE_LAUNCH
        checked(cudaGetLastError(),"sparse launch");checked(cudaDeviceSynchronize(),"sparse synchronize");
        unsigned long long count_value=0;
        checked(cudaMemcpy(&count_value,count.p,sizeof(count_value),cudaMemcpyDeviceToHost),"sparse count");
        if(count_value!=expected.size())throw std::runtime_error("sparse GPU hit count mismatch");
        std::vector<Hit> actual(static_cast<std::size_t>(count_value));
        checked(cudaMemcpy(actual.data(),hits.p,actual.size()*sizeof(Hit),cudaMemcpyDeviceToHost),"sparse hits");
        std::sort(actual.begin(),actual.end(),hit_less);
        for(std::size_t i=0;i<actual.size();++i)
            if(actual[i].a!=expected[i].a||actual[i].b!=expected[i].b||actual[i].z!=expected[i].z)
                throw std::runtime_error("sparse GPU/GMP pair mismatch");
    }
}
