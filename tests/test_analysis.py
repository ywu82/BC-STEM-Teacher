import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from analyze_results import validate_and_analyze,interactive_radar,svg_radar,teacher_report
class TestAnalysis(unittest.TestCase):
 def setUp(self):
  self.items=[{'item_id':'D1','assessment_type':'diagnostic','objective_id':'O1','max_points':'2'}, {'item_id':'Q1','assessment_type':'quiz','objective_id':'O1','max_points':'4'}]
  self.cfg={'threshold':0.7,'objectives':[{'id':'O1','label':'a'}]}
 def test_separate_denominator(self):
  r=validate_and_analyze([{'student_id':'P01','assessment_type':'diagnostic','item_id':'D1','points':'1'},{'student_id':'P01','assessment_type':'quiz','item_id':'Q1','points':'4'}],self.items,self.cfg)
  self.assertEqual(r['objectives']['O1']['by_assessment']['diagnostic']['observed_percent'],50)
  self.assertEqual(r['objectives']['O1']['by_assessment']['quiz']['observed_percent'],100)
  self.assertFalse(r['growth_comparable'])
 def test_summary_statistics_use_complete_responses(self):
  rows=[
   {'student_id':'P01','assessment_type':'diagnostic','item_id':'D1','points':'1'},
   {'student_id':'P02','assessment_type':'diagnostic','item_id':'D1','points':'2'},
  ]
  r=validate_and_analyze(rows,[self.items[0]],self.cfg);s=r['assessments']['diagnostic']
  self.assertEqual(s['highest_percent'],100)
  self.assertEqual(s['lowest_percent'],50)
  self.assertEqual(s['mean_percent'],75)
  self.assertEqual(s['median_percent'],75)
 def test_teaching_recommendations_are_evidence_linked(self):
  r=validate_and_analyze([{'student_id':'P01','assessment_type':'diagnostic','item_id':'D1','points':'1'}],[self.items[0]],self.cfg)
  recommendation=' '.join(r['teaching_recommendations']['items'])
  self.assertIn('O1',recommendation)
  self.assertIn('50.00%',recommendation)
  self.assertIn('70.00%',recommendation)
 def test_duplicate_rejected(self):
  row={'student_id':'P01','assessment_type':'quiz','item_id':'Q1','points':'3'}
  with self.assertRaisesRegex(ValueError,'duplicate'):validate_and_analyze([row,row],self.items,self.cfg)
 def test_overmax_rejected(self):
  with self.assertRaisesRegex(ValueError,'outside bounds'):validate_and_analyze([{'student_id':'P01','assessment_type':'quiz','item_id':'Q1','points':'5'}],self.items,self.cfg)
 def test_interactive_radar_contains_evidence_without_student_ids(self):
  from tempfile import TemporaryDirectory
  r=validate_and_analyze([{'student_id':'P01','assessment_type':'diagnostic','item_id':'D1','points':'1'},{'student_id':'P01','assessment_type':'quiz','item_id':'Q1','points':'4'}],self.items,self.cfg)
  with TemporaryDirectory() as d:
   p=Path(d)/'objective_radar.html';interactive_radar(r,p);content=p.read_text(encoding='utf-8')
   self.assertIn('Interactive objective attainment radar',content)
   self.assertIn('Meeting target',content)
   self.assertNotIn('P01',content)
   s=Path(d)/'objective_radar.svg';svg_radar(r,s);svg=s.read_text(encoding='utf-8')
   self.assertIn('Objective attainment radar',svg)
   self.assertNotIn('P01',svg)
 def test_teacher_report_is_single_teacher_facing_entry(self):
  from tempfile import TemporaryDirectory
  cfg={**self.cfg,'course':'Demo course','data_provenance':'SYNTHETIC / DEMO','curriculum_status':'PROVISIONAL'}
  r=validate_and_analyze([{'student_id':'P01','assessment_type':'diagnostic','item_id':'D1','points':'1'}],[self.items[0]],cfg)
  with TemporaryDirectory() as d:
   p=Path(d)/'teacher_report.html';teacher_report(r,p);content=p.read_text(encoding='utf-8')
   self.assertIn('Student Learning Evidence Report',content)
   self.assertIn('SYNTHETIC / DEMO',content)
   self.assertIn('Assessment summary',content)
   self.assertIn('Recommended next teaching moves',content)
   self.assertNotIn('P01',content)
 def test_provenance_is_preserved_from_config(self):
  cfg={**self.cfg,'data_provenance':'SYNTHETIC / DEMO'}
  r=validate_and_analyze([],self.items,cfg)
  self.assertEqual(r['synthetic_or_real'],'SYNTHETIC / DEMO')
if __name__=='__main__':unittest.main()
