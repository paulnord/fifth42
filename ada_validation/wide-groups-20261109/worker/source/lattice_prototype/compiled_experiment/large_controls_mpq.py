"""Two published fixture-selected patches, never complete large-shell searches."""
import hashlib
import json
import benchmark_mpq as exp


def main():
    rows=[]
    engines={kind:exp.engine(kind) for kind in ('fraction','mpq')}
    for a,b,c in [(13852184,27401825,27580409),(21137517920,21483066250,24482314857)]:
        geometries=[]
        results={}
        times={}
        residual=a**5+b**5-c**5
        for kind,(l,f) in engines.items():
            C=1<<(c.bit_length()-1)
            D=2*C-1
            count=l.ceil(l.Q(9*C,20))
            i=l.floor(l.Q(a,c)*10*count/9)
            p=l.make_patch(C,D,l.Q(9*i,10*count),l.Q(9*(i+1),10*count),5*D*D,bits=160)
            basis=p.basis()
            reduced,u=l.reduce_basis(basis,'fpylll')
            mu,norms=l.gram_schmidt(reduced)
            geometries.append(exp.normalize([vars(p),basis,reduced,u,mu,norms]))
            result=f.search_patch(p,[residual],mode='prune',backend='fpylll')
            assert (a,b,c,residual) in set(map(tuple,result['hits']))
            assert result['complete']
            times[kind]=result['stats']['seconds']
            results[kind]=exp.comparable(result)
        assert geometries[0]==geometries[1]
        assert results['fraction']==results['mpq']
        rows.append(dict(triple=[a,b,c],residual=residual,mode='prune',times=times,exact_geometry_equal=True,all_results_and_counters_equal=True,hit_found=True,geometry_sha256=hashlib.sha256(json.dumps(geometries[0],sort_keys=True).encode()).hexdigest(),coverage='fixture-selected single patch only, NOT full shell',result=results['mpq']))
    (exp.ROOT/'results/compiled-mpq-large-controls.json').write_text(json.dumps(rows,indent=2))
    for row in rows:
        print(row['triple'],row['times'],'exact geometry, counters and hit verified')

if __name__=='__main__':
    main()
