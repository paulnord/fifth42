from fractions import Fraction as Q
from prototype import check_input,finish,newton_bracket,division_free_bracket
count=0
for d in range(1,101):
 for n in range(d+1):
  for b in range(1,9):
   x=Q(n,d);a=newton_bracket(x,b);assert a==division_free_bracket(x,b)
   k=a[0].numerator*(1<<b)//a[0].denominator
   for wrong in [k-1,k+1]:
    try:finish(x,b,wrong)
    except ArithmeticError:pass
    else:raise AssertionError('bad candidate accepted')
   count+=1
for b in [1,88,176,222]:
 x=Q(1,3);width=2+5*(b+1);check_input(x,b,width)
 try:check_input(x,b,width-1)
 except OverflowError:pass
 else:raise AssertionError('width guard failed')
print('PASS:',count,'exact root comparisons, malformed certificates and width guards')
