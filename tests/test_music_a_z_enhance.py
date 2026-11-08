"""Selective A–Z MIDI upgrade structural regression across all 100 city beats."""
import collections
import json
import tempfile
import unittest
from pathlib import Path
import mido
from scripts.collection_two import ROOT,load_collection_two,make_collection_two_catalog
from scripts.music_a_z_enhance import PRIORITY_IDS,WEAK_HOOK_IDS,enhance_midi
from scripts.render_arranged_review_audio import Arrangement,TICKS_BAR
from scripts.render_collection_two_review_audio import CollectionTwoArrangement

def count(notes,part,channels):
    first=part["startBar"]*TICKS_BAR
    end=part["endBar"]*TICKS_BAR
    return sum(first<=n[0]<end and n[1] in channels for n in notes)/part["bars"]

def note_ons(mf):
    tick=0
    result=[]
    for m in mf.tracks[-1]:
        tick+=m.time
        if m.type=="note_on" and m.velocity:
            result.append((tick,m.channel,m.note))
    return result

def note_integrity(mf,plan):
    tick=0;active=collections.Counter()
    for msg in mf.tracks[-1]:
        tick+=msg.time
        if msg.type=="note_on" and msg.velocity:
            active[(msg.channel,msg.note)]+=1
        elif msg.type=="note_off" or msg.type=="note_on" and not msg.velocity:
            key=(msg.channel,msg.note)
            assert active[key]>0,(tick,key)
            active[key]-=1
        assert tick<=TICKS_BAR*plan["totalBars"],tick
    assert not any(active.values()),active

class TestMusicUpgrade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        old=json.loads((ROOT/"data/catalog.json").read_text())
        plans=json.loads((ROOT/"data/arrangements.json").read_text())
        cls.catalog,cls.plans=make_collection_two_catalog(old,plans)
        cls.beats=sorted([b for b in cls.catalog if isinstance(b.get("releaseRank"),int)],
                         key=lambda b:b["releaseRank"])
        cls.bp={b["id"]:b for b in load_collection_two()}

    def test_100_city_priority_integrity_and_hook_contrast(self):
        self.assertEqual(len(self.beats),100)
        known={b["id"] for b in self.beats}
        self.assertTrue(PRIORITY_IDS<=known)
        self.assertEqual(len(WEAK_HOOK_IDS),14)
        with tempfile.TemporaryDirectory() as temp:
            dest=Path(temp)/"a_z_review.mid"
            reviewed=0
            for beat in self.beats:
                plan=self.plans[beat["id"]]
                arr=(Arrangement(beat,plan) if beat["releaseRank"]<=50 else
                     CollectionTwoArrangement(beat,plan,self.bp[beat["id"]]))
                arr.build_midi(dest)
                old=mido.MidiFile(dest)
                old_notes=note_ons(old)
                old_hooks=[s for s in plan["sections"] if s["kind"]=="hook"]
                old_verses=[s for s in plan["sections"] if s["kind"]=="verse"]
                previous=count(old_notes,old_hooks[0],(0,1,2,3))
                stats=enhance_midi(dest,beat,plan)
                next_midi=mido.MidiFile(dest)
                note_integrity(next_midi,plan)
                after=note_ons(next_midi)
                if beat["id"] in PRIORITY_IDS:
                    reviewed+=1
                    self.assertTrue(stats["enhanced"])
                    self.assertGreater(len(after),len(old_notes))
                    if beat["id"] in WEAK_HOOK_IDS:
                        now=count(after,old_hooks[0],(0,1,2,3))
                        self.assertGreaterEqual(now-previous,1.7,beat["id"])
                    for v in old_verses:
                        # New lead/counter still respects open first half of verse.
                        from_start=v["startBar"]*TICKS_BAR
                        to_end=v["endBar"]*TICKS_BAR
                        added={(tick,ch,n) for tick,ch,n in after}-set(old_notes)
                        self.assertFalse(any(from_start<=t<to_end and
                            (t%TICKS_BAR)<2*480 and ch in (1,3)
                            for t,ch,n in added),beat["id"])
                else:
                    self.assertEqual(old_notes,after,beat["id"])
            self.assertGreaterEqual(reviewed,25)
            print("PASS: instrumental arrangements verified")
