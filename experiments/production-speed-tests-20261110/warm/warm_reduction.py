"""Experimental neighboring-basis seed, never enabled in production implicitly.

Row bases: B = V * (S * A), hence U = V*S. Every accepted result is
independently certified against A; invalid seeds/results fall back to cold LLL.
A warm result may differ from the cold basis: compare coverage/hits, NOT U bytes.
"""
from dataclasses import dataclass


def matrix3(m, integers=False):
    return (isinstance(m,(list,tuple)) and len(m)==3 and
            all(isinstance(r,(list,tuple)) and len(r)==3 for r in m) and
            (not integers or all(type(x) is int for r in m for x in r)))


def verify(engine, original, reduced, transform):
    if not matrix3(original) or not matrix3(reduced) or not matrix3(transform, True):
        raise ValueError('bad reduction matrix shape/type')
    if abs(engine.det3(transform)) != 1 or engine.matmul(transform, original) != reduced:
        raise ValueError('exact reduction certificate failed')


@dataclass
class Stats:
    cold: int=0
    warm: int=0
    fallbacks: int=0


class WarmReducer:
    def __init__(self, engine, backend='fpylll', max_seed_bits=64, reducer=None):
        self.engine=engine
        self.backend=backend
        self.max_seed_bits=max_seed_bits
        self.reducer=reducer or engine.reduce_basis
        self.seed=None
        self.stats=Stats()

    def clear(self):
        self.seed=None

    def cold(self, basis):
        b,u=self.reducer(basis,self.backend)
        verify(self.engine,basis,b,u)
        self.stats.cold+=1
        self.seed=[list(row) for row in u]
        return b,u

    def __call__(self,basis,backend=None):
        if backend is not None and backend != self.backend:
            raise ValueError('backend changed during warm reduction')
        if self.seed is None:
            return self.cold(basis)
        try:
            s=self.seed
            if (not matrix3(s,True) or abs(self.engine.det3(s))!=1 or
                any(abs(x).bit_length()>self.max_seed_bits for row in s for x in row)):
                raise ValueError('invalid or oversize seed')
            candidate=self.engine.matmul(s,basis)
            b,v=self.reducer(candidate,self.backend)
            verify(self.engine,candidate,b,v)
            u=self.engine.matmul(v,s)
            verify(self.engine,basis,b,u)
        except Exception:
            # A bad optional optimization must not bypass the cold certificate.
            self.stats.fallbacks+=1
            return self.cold(basis)
        self.stats.warm+=1
        self.seed=[list(row) for row in u]
        return b,u
