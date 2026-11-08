"""Fail-closed tests for connecting the original AXEZENT audio without new synthesis."""
import io
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.connect_original_previews import (
    CATALOG, check_stream, featured_tracks, validate_base_url
)

class AudioConnectorTests(unittest.TestCase):
    def test_catalog_contains_50_unique_featured_ids(self):
        beats = featured_tracks(CATALOG)
        self.assertEqual(50,len(beats))
        self.assertEqual(1,beats[0]["releaseRank"])
        self.assertEqual(50,beats[-1]["releaseRank"])
        self.assertEqual(50,len({b["id"] for b in beats}))

    def test_public_https_source_only(self):
        self.assertEqual("https://music.example.org",validate_base_url("https://music.example.org/"))
        self.assertEqual("https://music.example.org:443",validate_base_url("https://music.example.org:443"))
        for bad in (
            "http://music.example.org", "https://127.0.0.1",
            "https://192.168.1.1", "https://localhost:8443",
            "https://vault.axezent.chatgpt.site", "https://music.example.org/path",
            "https://a:b@music.example.org", "https://music.example.org/?token=private",
        ):
            with self.subTest(url=bad),self.assertRaises(ValueError):
                validate_base_url(bad)

    def test_range_stream_accepts_valid_mp3_header(self):
        class FakeResponse:
            status=206
            headers={"Content-Range":"bytes 0-31/1371200"}
            def __enter__(self): return self
            def __exit__(self,*args): return False
            def read(self,n): return b"ID3" + bytes(n-3)
        with patch("urllib.request.urlopen",return_value=FakeResponse()):
            check_stream("https://music.example.org/api/preview/AXZ-169",timeout=1)

    def test_non_range_host_rejected(self):
        class FakeResponse:
            status=200
            headers={}
            def __enter__(self): return self
            def __exit__(self,*args): return False
            def read(self,n): return b"ID3" + bytes(n-3)
        with patch("urllib.request.urlopen",return_value=FakeResponse()):
            with self.assertRaises(ValueError):
                check_stream("https://music.example.org/api/preview/AXZ-169",timeout=1)

    def test_non_audio_response_rejected(self):
        class FakeResponse:
            status=206
            headers={"Content-Range":"bytes 0-31/1000000"}
            def __enter__(self): return self
            def __exit__(self,*args): return False
            def read(self,n): return b"<html>" + bytes(n-6)
        with patch("urllib.request.urlopen",return_value=FakeResponse()):
            with self.assertRaises(ValueError):
                check_stream("https://music.example.org/api/preview/AXZ-169",timeout=1)

if __name__=="__main__":
    unittest.main()
