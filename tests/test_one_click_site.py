"""Tests for the one-click GitHub-to-website launch verifier."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import activate_one_click_player as gateway

class LaunchTests(unittest.TestCase):
    def test_reject_insecure_or_local_urls(self):
        for bad in ["http://mywebsite.com","http://localhost:8080",
                    "https://127.0.0.1","https://internal.local",
                    "https://fake.example","https://user:pass@website.com",
                    "https://example.com/foo","https://mywebsite.com:8080"]:
            with self.subTest(url=bad):
                with self.assertRaises(ValueError):
                    gateway.validate_url(bad)

    def test_public_hostname_normalization(self):
        self.assertEqual(gateway.validate_url("https://MUSIC.Example.org/"),
                         "https://music.example.org")

    def test_gates_all_fifty_before_enabling_a_link(self):
        tracks=[{"id":f"AXZ-{i:03}", "releaseRank":i,
                 "status":"preview_ready","previewUrl":f"/api/preview/AXZ-{i:03}"} for i in range(1,51)]
        tracks+=[{"id":f"OTHER-{i}", "status":"planned"} for i in range(150)]
        page=b'<html><dialog id="playerDialog"><input id="musicSeek"><button id="musicPlay"></button><button id="musicStop"></button><button id="closePlayer"></button></dialog></html>'
        def get(_url,_headers=None,max_read=140000):
            if _url.endswith("/api/ready"):
                present=sum(b.get("status")=="preview_ready" for b in tracks)
                return 200 if present==50 else 503,{"Content-Type":"application/json"},json.dumps({"websiteReady":present==50,"playableBeats":present}).encode()
            if _url.endswith("/api/catalog"):
                return 200,{"Content-Type":"application/json"},json.dumps(tracks).encode()
            if _url.endswith("/"):
                return 200,{"Content-Type":"text/html"},page
            if "/api/preview/" in _url:
                return 206,{"Content-Type":"audio/mpeg"},b"ID3"+bytes(13)
            raise AssertionError(_url)
        with patch.object(gateway,"get",side_effect=get):
            self.assertEqual(gateway.verify_live_player("https://music.example.org"),50)
        tracks[0]["status"]="mix_review"
        with patch.object(gateway,"get",side_effect=get):
            with self.assertRaisesRegex(RuntimeError,"not ready"):
                gateway.verify_live_player("https://music.example.org")

    def test_only_verified_launch_link_rewrites_readme_area(self):
        with tempfile.TemporaryDirectory() as t:
            target=Path(t)/"README.md"
            target.write_text("before\n"+gateway.BEGIN+"\nPending\n"+gateway.END+"\nafter\n",encoding="utf-8")
            with patch.object(gateway,"README",target):
                gateway.publish_link("https://music.example.org")
            content=target.read_text(encoding="utf-8")
            self.assertIn("[▶ OPEN AXEZENT MUSIC PLAYER — LISTEN TO ALL 50 BEATS](https://music.example.org/)",content)
            self.assertIn("before",content)
            self.assertIn("after",content)
if __name__=="__main__":unittest.main()
