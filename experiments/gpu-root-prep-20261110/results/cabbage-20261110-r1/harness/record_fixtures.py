import json,runpy,sys
from pathlib import Path
p=Path(sys.argv[1]);sys.path.insert(0,str(p.parent));count=sys.argv[2];out=Path(sys.argv[3]);sys.argv=[str(p),'--count',count,'--output',str(out)]
g=runpy.run_path(str(p),run_name='__main__');rejected=[]
for x,b in g['cases']:
 try:g['check_input'](x,b,2048)
 except OverflowError as e:rejected.append(dict(numerator=str(x.numerator),denominator=str(x.denominator),bits=b,required_bits=max(x.numerator.bit_length(),x.denominator.bit_length())+5*(b+1),reason=str(e)))
(out/'unsupported-cases.json').write_text(json.dumps(rejected,indent=2)+'\n')
