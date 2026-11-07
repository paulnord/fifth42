"""Exact cube coefficient enclosure, compatible with the existing symmetric J packet.

Only valid physical points in [-1,1]^3 need coverage. This intentionally does
not preserve the larger enclosing sphere's false candidates. No float is used.
The caller must preserve B=U*A and det(U)=+/-1 certificates.
"""
from fractions import Fraction
from math import isqrt

def inverse_exact(matrix):
    a=[[Fraction(x) if isinstance(x,int) else x for x in row] for row in matrix]
    if len(a)!=3 or any(len(row)!=3 for row in a):
        raise ValueError('Expected a 3 by 3 matrix')
    d=(a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
       -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
       +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))
    if not d:raise ValueError('Singular lattice basis')
    result=[[(a[(j+1)%3][(i+1)%3]*a[(j+2)%3][(i+2)%3]
              -a[(j+1)%3][(i+2)%3]*a[(j+2)%3][(i+1)%3])/d
             for j in range(3)] for i in range(3)]
    if any(sum(a[i][k]*result[k][j] for k in range(3))!=int(i==j)
           for i in range(3) for j in range(3)):
        raise ValueError('Exact inverse certificate failed')
    return result

def coefficient_bounds_cube(b):
    inv=inverse_exact(b)
    values=[sum(abs(inv[i][j]) for i in range(3)) for j in range(3)]
    return tuple(int(value.numerator//value.denominator) for value in values)

def coefficient_bounds_sphere(b):
    inv=inverse_exact(b)
    result=[]
    for j in range(3):
        value=3*sum(inv[i][j]**2 for i in range(3))
        k=isqrt(int(value.numerator//value.denominator))
        result.append(k+int(k*k<value))
    return tuple(result)

def certify_cube_bounds(b,j):
    if tuple(j)!=coefficient_bounds_cube(b):
        raise ValueError('Cube coefficient enclosure mismatch')
    return True
