"""CPU executable specification for isolated fixed-width GPU root experiments.
Not a production backend. Overflow means CPU fallback, never truncated arithmetic.
"""
from fractions import Fraction

def check_input(x,bits,width):
    x=Fraction(x)
    if not 0 <= x <= 1 or not 1 <= bits <= 222:
        raise ValueError('prototype supports unit-interval roots, 1..222 bits')
    # Includes final (n+1)**5 certificate even for x=1.
    # n+1 < 2**(bits+1), so this conservative bound covers every product.
    if max(x.numerator.bit_length(), x.denominator.bit_length())+5*(bits+1)>width:
        raise OverflowError('CPU fallback: fixed-width proof failed')
    return x

def finish(x,bits,n):
    target=x.numerator << (5*bits)
    den=x.denominator
    if not den*n**5 <= target < den*(n+1)**5:
        raise ArithmeticError('bad root candidate; CPU fallback')
    lo=Fraction(n,1<<bits)
    return lo, lo if den*n**5 == target else Fraction(n+1,1<<bits)

def division_free_bracket(x,bits=222,width=2048):
    """cuPQC-compatible candidate: shifts, products, comparisons; no division.
    Portable correctness baseline, not a performance prediction.
    """
    x=check_input(x,bits,width)
    if x==1:return (Fraction(1),Fraction(1))
    target=x.numerator << (5*bits)
    n=0
    for bit in range(bits-1,-1,-1):
        trial=n | (1<<bit)
        if x.denominator*trial**5 <= target:n=trial
    return finish(x,bits,n)

def newton_bracket(x,bits=222,width=2048):
    """CGBN candidate: wide division then descending integer fifth-root Newton.
    Integer Newton from an upper bound cannot undershoot floor root; termination
    occurs at floor root, including perfect powers. Final inequalities certify it.
    """
    x=check_input(x,bits,width)
    target=(x.numerator << (5*bits))//x.denominator
    if target==0:return finish(x,bits,0)
    n=1<<((target.bit_length()+4)//5)
    for iterations in range(512):
        nxt=(4*n+target//n**4)//5
        if nxt>=n:return finish(x,bits,n)
        n=nxt
    raise ArithmeticError('iteration guard: CPU fallback')
