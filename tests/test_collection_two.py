"""Collection Two: evidence that 100 playable regions are planned, without mutating original 50."""
from __future__ import annotations
import json
import unittest
from pathlib import Path
from scripts.collection_two import ROOT,load_collection_two,make_collection_two_catalog
from scripts.render_collection_two_review_audio import CollectionTwoArrangement,region_groove

class NewFiftyContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original_catalog=json.loads((ROOT/"data"/"catalog.json").read_text("utf-8"))
        cls.original_arr=json.loads((ROOT/"data"/"arrangements.json").read_text("utf-8"))
        cls.new=load_collection_two()
        cls.catalog,cls.plans=make_collection_two_catalog(cls.original_catalog,cls.original_arr)

    def test_first_fifty_unchanged(self):
        self.assertEqual(50,len(self.original_arr))
        first_ids={x["id"] for x in self.original_catalog if isinstance(x.get("releaseRank"),int)}
        self.assertEqual(50,len(first_ids))
        for ident in first_ids:
            self.assertEqual(self.plans[ident],self.original_arr[ident])

    def test_100_distinct_cities_and_track_ids(self):
        shown=sorted((b for b in self.catalog if isinstance(b.get("releaseRank"),int)),
                     key=lambda b:b["releaseRank"])
        self.assertEqual(list(range(1,101)),[s["releaseRank"] for s in shown])
        self.assertEqual(100,len(set(s["id"] for s in shown)))
        self.assertEqual(100,len(set((s["city"],s["state"]) for s in shown)))
        self.assertEqual(200,len(self.catalog))
        self.assertEqual(100,len(self.plans))

    def test_50_original_city_forms_bpm_keys_and_programs(self):
        self.assertEqual(50,len(self.new))
        self.assertGreaterEqual(len({tuple(x["form"]) for x in self.new}),20)
        self.assertGreaterEqual(len({tuple(x["gmPrograms"]) for x in self.new}),35)
        self.assertEqual(7,len({region_groove(x["groove"]) for x in self.new}))
        for x in self.new:
            with self.subTest(id=x["id"]):
                b=next(z for z in self.catalog if z["id"]==x["id"])
                spec=self.plans[x["id"]]
                self.assertEqual(x["bpm"],b["bpm"])
                self.assertEqual(x["key"],b["key"])
                self.assertEqual(x["releaseRank"],b["releaseRank"])
                self.assertEqual(x["gmPrograms"],list(x["gmPrograms"]))
                self.assertEqual(spec["totalBars"],sum(int(n) for k,n in x["form"]))
                self.assertEqual(spec["sections"][-1]["kind"],"outro")
                self.assertAlmostEqual(spec["durationSeconds"],
                    240*spec["totalBars"]/x["bpm"],delta=0.005)
                for s in spec["sections"]:
                    self.assertAlmostEqual(s["endSeconds"]-s["startSeconds"],
                        240*s["bars"]/x["bpm"],delta=0.005)

    def test_new_midi_real_notes_and_variation(self):
        import tempfile
        from pathlib import Path
        voices=set()
        sigs=set()
        from scripts.render_arranged_review_audio import TICKS_BAR
        with tempfile.TemporaryDirectory() as tmp:
            for bp in self.new:
                beat=next(x for x in self.catalog if x["id"]==bp["id"])
                spec=self.plans[bp["id"]]
                a=CollectionTwoArrangement(beat,spec,bp)
                voices.add(a.instruments)
                count=a.build_midi(Path(tmp)/"new.mid")
                self.assertGreater(count,400)
                hooks=[p for p in spec["sections"] if p["kind"]=="hook"]
                self.assertGreaterEqual(len(hooks),2)
                sig=[]
                for sec in hooks:
                    t0=sec["startBar"]*TICKS_BAR
                    s=tuple(sorted((tick-t0,m.channel,m.note) for tick,_,m in a.events
                        if m.type=="note_on" and m.velocity and m.channel in (0,1,2,3)
                        and t0<=tick<t0+2*TICKS_BAR))
                    sig.append(s)
                self.assertEqual(len(set(sig)),1,"Returning chorus must be recognizable")
                sigs.add(sig[0])
        self.assertEqual(50,len(sigs))
        self.assertGreaterEqual(len(voices),35)

if __name__=="__main__":
    unittest.main()
