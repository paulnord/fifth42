"""Experimental exact precision choice for the existing quintic tangent patches.

No runtime monkey-patching or active-run modification. Import and call explicitly.
Works with fractions.Fraction or gmpy2.mpq through the passed engine's Q.
"""

def geometry_bits(engine, cmin, cmax, left, right, cap, *, margin_bits=16):
    """Choose root-enclosure bits from exact patch size, not fifth-power size.

    All choices still use the original outward-bound make_patch. The margin is
    an efficiency bound on rounding broadening, not a correctness assumption.
    Fallback preserves the former high-range precision outside this policy's
    proved ratio domain. Result is a multiple of eight, at least 48 bits.
    """
    Q=engine.Q
    left,right=Q(left),Q(right)
    if not (1<=cmin<=cmax and 0<=left<right<1 and cap>=0):
        raise ValueError('Invalid patch inputs')
    if type(margin_bits) is not int or not 0<=margin_bits<=128:
        raise ValueError('Invalid precision margin')
    baseline=max(48,5*cmax.bit_length()+32)
    if right>Q(9,10):
        return baseline
    h=(right-left)/2
    eta=Q(cap,cmin**5)
    # Conservative lower bound for curvature plus residual terms in make_patch:
    # vlo,vmin<=1 imply 2*r^3*h^2/vlo^9 + eta/(5*vmin^4) >= lower.
    lower=2*right**3*h*h+eta/5
    # Since p<=.9, root(1-p^5)>.5. For bits>=48, qlo>=.5.
    # Root interval width<=2^-bits; derivative of t^-4 on [.5,1]
    # has magnitude<=128. Root+slope rounding <= (1/2+64*h)*2^-bits.
    coefficient=Q(1,2)+64*h
    bits=48
    while coefficient*(1<<margin_bits)>lower*(1<<bits):
        bits+=8
        if bits>=baseline:
            return baseline
    return bits

def make_patch(engine, cmin,cmax,left,right,cap,*,margin_bits=16):
    bits=geometry_bits(engine,cmin,cmax,left,right,cap,margin_bits=margin_bits)
    return engine.make_patch(cmin,cmax,left,right,cap,bits),bits
