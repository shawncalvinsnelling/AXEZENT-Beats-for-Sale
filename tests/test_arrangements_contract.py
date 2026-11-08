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
                            self.assertLessEqual(len(counter),2,
                                f"Counter melody overcrowds {beat['id']} verse bar {bar}")
                            if verse_count%4==0:
                                self.assertEqual(0,len(counter),
                                    "First bar of four-bar vocal phrase must be clear")
                            elif verse_count%4 in (1,2):
                                self.assertEqual(1,len(counter))
                            if beat["id"] in focus and verse_count==3:
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
                    self.assertGreaterEqual(len(hook),3,"Sparse genres may use a memorable three-note hook")
                    self.assertGreater(sum(v for _,v in hook)/len(hook),
                                       sum(v for _,v in verse)/len(verse))

    def test_repeated_hooks_return_to_same_harmonic_melodic_grid(self):
        """For every song, first two bars of each hook must be identical on
        chord, lead, bass and hook response piano-roll lanes."""
        from scripts.render_arranged_review_audio import Arrangement,TICKS_BAR
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmp:
            for beat in FEATURED:
                with self.subTest(id=beat["id"]):
                    plan=ARRANGEMENTS[beat["id"]]
                    arranger=Arrangement(beat,plan)
                    arranger.build_midi(Path(tmp)/"hook.mid")
                    sig=[]
                    for sec in plan["sections"]:
                        if sec["kind"]!="hook":
                            continue
                        first=sec["startBar"]*TICKS_BAR
                        sig.append(tuple(sorted(
                            (tick-first,msg.channel,msg.note)
                            for tick,_,msg in arranger.events
                            if msg.type=="note_on" and msg.velocity>0 and
                            msg.channel in (0,1,2,3) and first<=tick<first+2*TICKS_BAR
                        )))
                    self.assertGreaterEqual(len(sig),2)
                    self.assertTrue(all(x==sig[0] for x in sig[1:]),
                                    "Returning hook must recover its first harmony and lead")

    def test_rap_verse_is_sparser_than_hook(self):
        from scripts.render_arranged_review_audio import Arrangement,TICKS_BAR
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmp:
            for beat in FEATURED:
                with self.subTest(id=beat["id"]):
                    plan=ARRANGEMENTS[beat["id"]]
                    a=Arrangement(beat,plan)
                    a.build_midi(Path(tmp)/"density.mid")
                    by_section={}
                    for sec in plan["sections"]:
                        if sec["kind"] not in ("hook","verse"):
                            continue
                        counts=[]
                        for bar in range(sec["startBar"],sec["endBar"]):
                            counts.append(sum(1 for t,_,m in a.events
                                if m.type=="note_on" and m.velocity and m.channel in (0,1,2,3)
                                and bar*TICKS_BAR<=t<(bar+1)*TICKS_BAR))
                        by_section.setdefault(sec["kind"],[]).extend(counts)
                    verse=sum(by_section["verse"])/len(by_section["verse"])
                    hook=sum(by_section["hook"])/len(by_section["hook"])
                    self.assertLess(verse,hook,f"{beat['id']} vocal verse is too busy")
                    self.assertLessEqual(verse,8.5,
                        f"{beat['id']} verse contains more than 8.5 pitched attacks/bar")

    def test_pitched_notes_terminate_within_their_bar(self):
        from scripts.render_arranged_review_audio import Arrangement,TICKS_BAR
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmp:
            for beat in FEATURED:
                with self.subTest(id=beat["id"]):
                    a=Arrangement(beat,ARRANGEMENTS[beat["id"]])
                    a.build_midi(Path(tmp)/"chord_change.mid")
                    start={}
                    for tick,_,m in sorted(a.events,key=lambda e:(e[0],e[1])):
                        if m.channel not in (0,1,2,3):
                            continue
                        k=(m.channel,m.note)
                        if m.type=="note_on" and m.velocity:
                            start.setdefault(k,[]).append(tick)
                        elif m.type=="note_off":
                            if start.get(k):
                                s=start[k].pop(0)
                                self.assertEqual(s//TICKS_BAR,tick//TICKS_BAR,
                                    "Unintentional pitch held into next chord")

    def test_hooks_do_not_share_one_uniform_note_density(self):
        """Historic 50 tracks all had exactly 13.25 pitched notes per hook bar.
        Different groove families should have purposeful density budgets."""
        from scripts.render_arranged_review_audio import Arrangement,TICKS_BAR
        from tempfile import TemporaryDirectory
        densities={}
        with TemporaryDirectory() as tmp:
            for beat in FEATURED:
                plan=ARRANGEMENTS[beat["id"]]
                a=Arrangement(beat,plan)
                a.build_midi(Path(tmp)/"density-budgets.mid")
                hook=next(s for s in plan["sections"] if s["kind"]=="hook")
                start=hook["startBar"]*TICKS_BAR
                end=hook["endBar"]*TICKS_BAR
                n=sum(1 for t,_,m in a.events if m.type=="note_on" and m.velocity
                      and m.channel!=9 and start<=t<end)
                d=n/hook["bars"]
                densities.setdefault(a.groove,[]).append(d)
                self.assertLessEqual(d,12.5,f"{beat['id']} hook overbuilt")
            means={k:sum(v)/len(v) for k,v in densities.items()}
            self.assertGreaterEqual(len(set(round(x,1) for x in means.values())),4,
                "All hooks are still stamped from the same pitched-note template")
            self.assertLess(means["drill"],means["club"])
            self.assertLess(means["ambient"],means["bounce"])

if __name__=="__main__":unittest.main()
