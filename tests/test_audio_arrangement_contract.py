"""Only proves the arrangement contract and preview synthesizer diversity mapping.
No algorithm can certify a human listener will like the finished beat.
"""
import ast
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from arrangement_spec import SECTIONS, TOTAL_BARS, section_for_bar, hook_ranges

class AudioArrangementContract(unittest.TestCase):
    def test_full_48_bar_structure(self):
        self.assertEqual([name for name,_,_ in SECTIONS],
           ["intro","hook","verse","hook","outro"])
        self.assertEqual([end-start for _,start,end in SECTIONS],[4,8,24,8,4])
        self.assertEqual(TOTAL_BARS,48)
        self.assertEqual([section_for_bar(i) for i in (0,4,12,36,44)],
           ["intro","hook","verse","hook","outro"])
        self.assertEqual(hook_ranges(),((4,12),(36,44)))

    def test_profile_timbre_pairs_not_one_keyboard(self):
        module=ast.parse((ROOT/"scripts"/"render_previews.py").read_text("utf-8"))
        defs={}
        for node in module.body:
            if isinstance(node,ast.Assign):
                for target in node.targets:
                    if isinstance(target,ast.Name) and target.id in (
                       "STYLES","VERSE_TIMBRES","HOOK_TIMBRES","PAD_TIMBRES"):
                        defs[target.id]=ast.literal_eval(node.value)
        self.assertEqual(len(defs),4)
        for key in defs:self.assertEqual(len(defs[key]),12)
        self.assertGreaterEqual(len(set(defs["HOOK_TIMBRES"])),9)
        self.assertGreaterEqual(len(set(defs["VERSE_TIMBRES"])),9)
        self.assertGreater(len(set(zip(defs["VERSE_TIMBRES"],defs["HOOK_TIMBRES"]))),10)

if __name__=="__main__":unittest.main()
