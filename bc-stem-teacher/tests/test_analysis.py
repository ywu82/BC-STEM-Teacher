import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from analyze_results import validate_and_analyze
class TestAnalysis(unittest.TestCase):
 def setUp(self):
  self.items=[{'item_id':'D1','assessment_type':'diagnostic','objective_id':'O1','max_points':'2'}, {'item_id':'Q1','assessment_type':'quiz','objective_id':'O1','max_points':'4'}]
  self.cfg={'threshold':0.7,'objectives':[{'id':'O1','label':'a'}]}
 def test_separate_denominator(self):
  r=validate_and_analyze([{'student_id':'P01','assessment_type':'diagnostic','item_id':'D1','points':'1'},{'student_id':'P01','assessment_type':'quiz','item_id':'Q1','points':'4'}],self.items,self.cfg)
  self.assertEqual(r['objectives']['O1']['by_assessment']['diagnostic']['observed_percent'],50)
  self.assertEqual(r['objectives']['O1']['by_assessment']['quiz']['observed_percent'],100)
  self.assertFalse(r['growth_comparable'])
 def test_duplicate_rejected(self):
  row={'student_id':'P01','assessment_type':'quiz','item_id':'Q1','points':'3'}
  with self.assertRaisesRegex(ValueError,'duplicate'):validate_and_analyze([row,row],self.items,self.cfg)
 def test_overmax_rejected(self):
  with self.assertRaisesRegex(ValueError,'outside bounds'):validate_and_analyze([{'student_id':'P01','assessment_type':'quiz','item_id':'Q1','points':'5'}],self.items,self.cfg)
if __name__=='__main__':unittest.main()
