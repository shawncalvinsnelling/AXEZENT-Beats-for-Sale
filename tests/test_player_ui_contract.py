"""Guard against accidentally breaking the one-click AXEZENT beat player.

This checks source wiring and access patterns. Actual listening still requires
a running streaming server with a valid private tagged MP3 and a web browser.
"""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Elements(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags={}
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if "id" in a:
            if a["id"] in self.tags:
                raise AssertionError("Duplicate HTML id: "+a["id"])
            self.tags[a["id"]]=(tag,a)

class PopupPlayerContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        html=(ROOT/"index.html").read_text("utf-8")
        cls.js=(ROOT/"assets"/"app.js").read_text("utf-8")
        cls.html=html
        cls.dom=Elements()
        cls.dom.feed(html)

    def test_popup_and_controls_exist(self):
        expected={
          "playerDialog":"dialog",
          "closePlayer":"button",
          "musicTitle":"h2",
          "musicPlay":"button",
          "musicPause":"button",
          "musicStop":"button",
          "musicSeek":"input",
          "musicTime":"span",
          "musicDuration":"span",
          "musicInquiry":"a",
          "player":"audio",
        }
        for id,tag in expected.items():
            with self.subTest(id=id):
                self.assertIn(id,self.dom.tags)
                self.assertEqual(self.dom.tags[id][0],tag)
        attrs=self.dom.tags["musicSeek"][1]
        self.assertEqual(attrs.get("type"),"range")
        self.assertEqual(attrs.get("min"),"0")
        self.assertEqual(attrs.get("max"),"100")
        self.assertEqual(self.dom.tags["player"][1].get("controls"),None)

    def test_popup_is_wired_to_real_play_pause_stop_seek_exit(self):
        js=self.js
        for code in (
            'function openPlayer(beat)',
            'musicDialog.showModal()',
            'player.play()',
            'musicPause.addEventListener("click"',
            'musicStop.addEventListener("click",stopPlayback)',
            'musicSeek.addEventListener("input"',
            'player.currentTime=target',
            'player.currentTime=0',
            '$("closePlayer").addEventListener("click",closePlayer)',
            'musicDialog.addEventListener("cancel"',
            'player.removeAttribute("src")',
        ):
            with self.subTest(check=code):
                self.assertIn(code,js)

    def test_audio_uses_server_not_download_links(self):
        self.assertIn('fetch("/api/catalog"',self.js)
        self.assertIn('^\\/api\\/preview\\/AXZ-',self.js)
        self.assertNotIn('download-button',self.js)
        self.assertNotIn('raw.githubusercontent.com/',self.html)
        self.assertNotIn('<a href="previews/',self.html)

if __name__=="__main__":
    unittest.main()
