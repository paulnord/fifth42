import ctypes,unittest
from array import array
import numpy as np
import candidate_reduction as c
class FlatBufferTests(unittest.TestCase):
 def test_shared_numpy_buffer_is_zero_copy(self):
  source=np.zeros((2,18),dtype=np.float64);data,owner=c.flat_buffer(source,2,10)
  source[1,3]=42;self.assertEqual(data[21],42)
  data[0]=17;self.assertEqual(source[0,0],17)
 def test_capacity_shape_dtype_and_strides_rejected(self):
  cases=[(np.zeros(18),0),(np.zeros(18),True),(np.zeros(18),11),(np.zeros(17),1),(np.zeros(18,dtype=np.int64),1),(np.zeros(36)[::2],1)]
  for values,count in cases:
   with self.subTest(count=count,dtype=str(values.dtype)):
    with self.assertRaises(ValueError):c.flat_buffer(values,count,10)
 def test_ctypes_and_list_paths(self):
  x=(ctypes.c_double*18)(*range(18));data,owner=c.flat_buffer(x,1,10);self.assertEqual(data[17],17)
  data,owner=c.flat_buffer(list(range(18)),1,10);self.assertEqual(data[17],17)
 def test_readonly_float_buffer_copies_safely(self):
  x=memoryview(array('d',range(18))).toreadonly();data,owner=c.flat_buffer(x,1,10);self.assertEqual(data[17],17)
 def test_raw_output_dtype_offsets(self):
  self.assertEqual((ctypes.sizeof(c.Output),c.Output.status.offset,c.Output.steps.offset),(80,72,76))
if __name__=='__main__':unittest.main(verbosity=2)
