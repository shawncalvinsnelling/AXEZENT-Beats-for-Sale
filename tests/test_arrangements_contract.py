"""Integrity checks for 50 proposed song-specific 4/4 AXEZENT arrangements."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ARRANGEMENTS=json.loads((ROOT/"data"/"arrangements.json").read_text("utf-8"))
CATALOG=json.loads((ROOT/"data"/"catalog.json").read_text("utf-8"))
FEATURED=sorted((b for b in CATALOG if isinstance(b.get("releaseRank"),int) and
                 1<=b["releaseRank"]<=50),key=lambda b:b["releaseRank"])

class ArrangementContractTests(unittest.TestCase):
    def test_50_one_to_one(self):
        self.assertEqual(50,len(FEATURED))
        self.assertEqual({b["id"] for b in FEATURED},set(ARRANGEMENTS))
        self.assertEqual(50,len({ARRANGEMENTS[b["id"]]["releaseRank"] for b in FEATURED}))

    def test_contiguous_bars_and_times(self):
        for beat in FEATURED:
            with self.subTest(track=beat["id"]):
                spec=ARRANGEMENTS[beat["id"]]
                self.assertEqual(beat["bpm"],spec["bpm"])
                self.assertEqual(beat["key"],spec["key"])
                self.assertEqual(beat["releaseRank"],spec["releaseRank"])
                self.assertFalse(spec["recordingVerified"])
                self.assertEqual("proposed_not_audio_verified",spec["arrangementStatus"])
                bar=0;intros=0;outros=0;verses=0
                for segment in spec["sections"]:
                    self.assertEqual(bar,segment["startBar"])
                    self.assertEqual(segment["endBar"],bar+segment["bars"])
                    self.assertGreaterEqual(segment["bars"],2)
                    self.assertAlmostEqual(segment["startSeconds"],bar*240/beat["bpm"],delta=.005)
                    self.assertAlmostEqual(segment["endSeconds"],segment["endBar"]*240/beat["bpm"],delta=.005)
                    intros+=segment["kind"]=="intro"
                    outros+=segment["kind"]=="outro"
                    verses+=segment["kind"]=="verse"
                    bar=segment["endBar"]
                self.assertLessEqual(intros,1)
                self.assertEqual(1,outros)
                self.assertTrue(spec["sections"][-1]["kind"]=="outro")
                self.assertGreaterEqual(verses,2)
                self.assertLessEqual(verses,4)
                self.assertEqual(bar,spec["totalBars"])
                self.assertAlmostEqual(spec["durationSeconds"],bar*240/beat["bpm"],delta=.005)

    def test_varied_openings_and_palettes(self):
        self.assertGreaterEqual(len({ARRANGEMENTS[b["id"]]["form"] for b in FEATURED}),3)
        self.assertEqual(50,len({ARRANGEMENTS[b["id"]]["soundPalette"] for b in FEATURED}))
        signatures={tuple((s["kind"],s["bars"]) for s in ARRANGEMENTS[b["id"]]["sections"]) for b in FEATURED}
        self.assertEqual(50,len(signatures),"Each of the 50 regional song structures must be different")
        for beat in FEATURED:
            parts=ARRANGEMENTS[beat["id"]]["sections"]
            self.assertTrue(all(parts[i]["kind"]!=parts[i-1]["kind"] for i in range(1,len(parts))),
                "Unintentional back-to-back repeated sections in "+beat["id"])
        self.assertGreaterEqual(len({ARRANGEMENTS[b["id"]]["form"] for b in FEATURED}),3)

    def test_verse_bar_instrumentation_and_focus_identity(self):
        """Check every generated verse bar, not only printed JSON contracts."""
        import tempfile
        from scripts.render_arranged_review_audio import Arrangement, TICKS_BAR
        focus={"AXZ-049","AXZ-125","AXZ-117","AXZ-001","AXZ-021","AXZ-185"}
        signatures=set()
        with tempfile.TemporaryDirectory() as folder:
            for beat in FEATURED:
                with self.subTest(beat=beat["id"]):
                    arranger=Arrangement(beat,ARRANGEMENTS[beat["id"]])
                    arranger.build_midi(Path(folder)/"contract.mid")
                    verse_count=0
                    for part in ARRANGEMENTS[beat["id"]]["sections"]:
                        if part["kind"]!="verse":
                            continue
                        for bar in range(part["startBar"],part["endBar"]):
                            start=bar*TICKS_BAR
                            counter=[
                                (tick-start,msg.note)
                                for tick,_,msg in arranger.events
                                if msg.type=="note_on" and msg.velocity and
                                   msg.channel==3 and start<=tick<start+TICKS_BAR
                            ]
                            self.assertGreaterEqual(len(counter),2,
                                f"Unscored counter-melody in {beat['id']} bar {bar}")
                            self.assertLessEqual(len(counter),3,
                                f"Counter-melody overcrowds verse in {beat['id']} bar {bar}")
                            if beat["id"] in focus and verse_count==0:
                                signatures.add((beat["id"],tuple(counter)))
                            verse_count+=1
                    self.assertGreaterEqual(verse_count,8)
        self.assertEqual(6,len(signatures))

    def test_palette_instruments_and_city_grooves(self):
        from scripts.render_arranged_review_audio import VOICES, Arrangement, GROOVE_FAMILIES
        self.assertEqual(50,len(VOICES))
        self.assertEqual(50,len(set(VOICES)), "No repeated four-part sonic palette")
        self.assertGreaterEqual(len({v[2] for v in VOICES}),8,
                                "Bass families must include acoustic, electric and synth")
        self.assertGreaterEqual(len({v[0] for v in VOICES}),20)
        observed=set()
        for beat in FEATURED:
            plan=ARRANGEMENTS[beat["id"]]
            arranger=Arrangement(beat,plan)
            observed.add(arranger.groove)
            self.assertEqual(VOICES[beat["releaseRank"]-1],arranger.instruments)
            if "drill" in plan["signature"].lower():
                self.assertEqual("drill",arranger.groove)
        self.assertTrue(set(GROOVE_FAMILIES).issubset(observed))

    def test_rap_space_and_hook_separation(self):
        from scripts.render_arranged_review_audio import Arrangement, TICKS_BAR
        with __import__("tempfile").TemporaryDirectory() as folder:
            for beat in FEATURED:
                with self.subTest(id=beat["id"]):
                    arranger=Arrangement(beat,ARRANGEMENTS[beat["id"]])
                    arranger.build_midi(Path(folder)/"check.mid")
                    kinds={k:next((s for s in ARRANGEMENTS[beat["id"]]["sections"]
                                  if s["kind"]==k),None) for k in ("verse","hook")}
                    self.assertTrue(kinds["verse"] and kinds["hook"])
                    def lead_notes(kind):
                        bar=kinds[kind]["startBar"]
                        return [(t-bar*TICKS_BAR,m.velocity) for t,_,m in arranger.events
                                if m.type=="note_on" and m.velocity
                                and m.channel==1 and bar*TICKS_BAR<=t<(bar+1)*TICKS_BAR]
                    verse=lead_notes("verse")
                    hook=lead_notes("hook")
                    self.assertLessEqual(len(verse),2, "Opening of verse too busy")
                    self.assertTrue(all(t>=2*480 for t,_ in verse),
                                    "Verse pickup must leave first half-bar clear")
                    self.assertGreaterEqual(len(hook),4,"Hooks should have a main phrase")
                    self.assertGreater(sum(v for _,v in hook)/len(hook),
                                       sum(v for _,v in verse)/len(verse))

if __name__=="__main__":unittest.main()
