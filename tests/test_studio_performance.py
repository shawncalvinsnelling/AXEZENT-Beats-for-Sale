"""All-catalog performance compatibility regression."""
import collections
import json
import tempfile
import unittest
from pathlib import Path
import mido
from scripts.collection_two import ROOT,load_collection_two,make_collection_two_catalog
from scripts.render_arranged_review_audio import Arrangement,TICKS_BAR
from scripts.render_collection_two_review_audio import CollectionTwoArrangement
from scripts.music_a_z_enhance import enhance_midi, PRIORITY_IDS
from scripts.studio_performance import refine_midi,PITCH_PROFILES

class StudioPerformance(unittest.TestCase):
 def test_full_catalog(self):
    orig=json.loads((ROOT/"data/catalog.json").read_text())
    specs=json.loads((ROOT/"data/arrangements.json").read_text())
    catalog,plans=make_collection_two_catalog(orig,specs)
    ids={b["id"] for b in catalog if b.get("releaseRank") is not None}
    self.assertTrue(set(PITCH_PROFILES)<=ids)
    bp={x["id"]:x for x in load_collection_two()}
    done={}
    with tempfile.TemporaryDirectory() as tmp:
      path=Path(tmp)/"music.mid"
      for b in sorted((b for b in catalog if isinstance(b.get("releaseRank"),int)),
                      key=lambda b:b["releaseRank"]):
        plan=plans[b["id"]]
        builder=Arrangement(b,plan) if b["releaseRank"]<=50 else CollectionTwoArrangement(b,plan,bp[b["id"]])
        builder.build_midi(path)
        before=path.read_bytes()
        enhanced=enhance_midi(path,b,plan)
        changed=refine_midi(path,b,plan)
        mf=mido.MidiFile(path)
        ticks=0;active=collections.Counter(); count=0
        for msg in mf.tracks[-1]:
          ticks+=msg.time
          self.assertLessEqual(ticks,plan["totalBars"]*TICKS_BAR)
          if msg.type=="note_on" and msg.velocity:
            active[(msg.channel,msg.note)]+=1; count+=1
            if msg.channel in (1,3) and any(
                s["startBar"]*TICKS_BAR<=ticks<s["endBar"]*TICKS_BAR and
                s["kind"]=="verse" for s in plan["sections"]):
              self.assertGreaterEqual(ticks%TICKS_BAR,2*480,
                                      b["id"]+" vocal pickup")
          elif msg.type in ("note_off","note_on") and getattr(msg,"velocity",None)==0:
            key=(msg.channel,msg.note)
            self.assertGreater(active[key],0,b["id"])
            active[key]-=1
        self.assertFalse(any(active.values()),b["id"])
        if b["id"] in PITCH_PROFILES:
          self.assertTrue(changed["processed"])
          self.assertGreater(changed["articulations"],0,b["id"])
          self.assertNotEqual(before,path.read_bytes(),b["id"])
        elif b["id"] not in PRIORITY_IDS:
          self.assertEqual(before,path.read_bytes(),b["id"])
        done[b["id"]]={"notes":count,"polished":changed["processed"]}
    self.assertEqual(len(done),100)
    self.assertEqual(sum(x["polished"] for x in done.values()),4)
    print("PASS: 100 individually checked performances; correct note boundaries and vocal space")
