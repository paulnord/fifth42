import copy,unittest
import controller
class ControlTests(unittest.TestCase):
 def test_allocations_stay_in_unreserved_cells(self):
  claims=[dict(first=500000000,last=11250000001)]
  self.assertEqual(controller.available_interval(claims),(1,500000000))
  self.assertIsNone(controller.available_interval([dict(first=1,last=11250000001)]))
  self.assertEqual(controller.available_interval([dict(first=100,last=11250000001)]),(1,100))
 def test_only_expected_clean_stops_roll_over(self):
  cp=dict(next_patch=10,window=dict(last=20))
  self.assertEqual(controller.next_action(cp,dict(reason='Local journal byte cap reached',error=None),0),'rotate')
  for reason in ['Stop requested','Running CPU load budget exceeded','Storage free reserve reached']:
   self.assertEqual(controller.next_action(cp,dict(reason=reason,error=None),0),'stop')
  self.assertEqual(controller.next_action(cp,dict(reason='Local journal byte cap reached',error='bad'),0),'stop')
  cp['next_patch']=20
  self.assertEqual(controller.next_action(cp,dict(reason='Selected remaining shell endpoint reached',error=None),0),'next_reservation')
  self.assertEqual(controller.next_action(cp,dict(reason=None,error=None),controller.DEADLINE-10),'stop')
if __name__=='__main__':unittest.main(verbosity=2)
