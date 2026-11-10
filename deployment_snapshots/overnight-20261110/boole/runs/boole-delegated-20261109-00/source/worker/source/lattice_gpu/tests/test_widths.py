import os
from pathlib import Path
import sys
import time
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import scaling_core as core
import packing_opt
import width_benchmark as widths
from engine_session import EngineSession
SOURCE=Path(os.environ.get('SCALING_LATTICE_SOURCE','/home/pnord/fifth42-lattice-optimizations-91bb89b/lattice_prototype'))

class CertifiedWidths(unittest.TestCase):
    @classmethod
    def setUpClass(cls):core.initialize(SOURCE)

    def test_width_grids_cover_every_shell_and_closed_ratio_interval(self):
        q=core.lattice().Q
        for width in widths.WIDTHS:
            specs,direct=core.specs(8000,42,width)
            shells=sorted(set((s[1],s[2]) for s in specs)|set(direct))
            self.assertEqual(shells[0][0],1);self.assertEqual(shells[-1][1],8000)
            for a,b in zip(shells,shells[1:]):self.assertEqual(a[1]+1,b[0])
            for shell in set((s[1],s[2]) for s in specs):
                rows=[s for s in specs if (s[1],s[2])==shell]
                self.assertEqual(q(*rows[0][3]),0);self.assertEqual(q(*rows[-1][4]),q(9,10))
                for a,b in zip(rows,rows[1:]):self.assertEqual(a[4],b[3])

    def test_every_width_matches_nonempty_oracle_with_exact_cpu_streams(self):
        l=core.lattice();expected=l.direct_positive(1,100,lambda c:2951,lambda r,c:abs(r)<=2951)
        self.assertIn((42,71,72,2951),expected)
        with EngineSession([str(ROOT/'bin/scaling_cpu'),'--threads','2'],'emulated',time.monotonic()+30) as session:
            for width in widths.WIDTHS:
                specs,direct=core.specs(100,2951,width);tasks=[core.prepare_task(s) for s in specs]
                plan=packing_opt.assemble(100,2951,specs,direct,tasks,[core.certify_task(t) for t in tasks])
                hits=set(plan.direct_hits)
                for batch in plan.batches:
                    raw,_=session.run(batch.packet);hits|=core.decode_batch(batch,raw,'emulated')
                self.assertEqual(hits,expected)

    def test_trial_orders_always_include_all_widths(self):
        orders=[widths.rotated_widths(r) for r in range(5)]
        for order in orders:self.assertEqual(sorted(order),list(widths.WIDTHS))
        self.assertGreater(len({tuple(order) for order in orders}),2)

if __name__=='__main__':unittest.main()
