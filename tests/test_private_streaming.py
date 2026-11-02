"""AXEZENT private-preview server: HTTP integration and path-safety tests."""
import json
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"server"))
from axezent_site import make_handler, safe_preview_file

class PrivateStreamingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.directory=Path(cls.temp.name)
        cls.server=ThreadingHTTPServer(("127.0.0.1",0),make_handler(cls.directory))
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True)
        cls.thread.start()
        cls.origin="http://127.0.0.1:%d"%cls.server.server_address[1]

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.temp.cleanup()

    def url(self,path,headers=None,method="GET"):
        req=urllib.request.Request(self.origin+path,headers=headers or {},method=method)
        return urllib.request.urlopen(req,timeout=5)

    def test_homepage_responds(self):
        with self.url("/") as r:
            self.assertEqual(r.status,200)
            self.assertIn(b"AXEZENT",r.read())

    def test_catalog_has_no_active_audio_when_private_folder_empty(self):
        with self.url("/api/catalog") as r:
            arr=json.load(r)
        self.assertEqual(len(arr),200)
        self.assertEqual(sum(bool(x.get("previewUrl")) for x in arr),0)

    def test_secret_paths_inaccessible(self):
        for path in ("/.git/config","/server/axezent_site.py","/data/catalog.json",
                     "/private/file.wav","/previews/AXZ-169-tagged.mp3",
                     "/api/preview/../../README.md","/api/preview/AXZ-999"):
            with self.subTest(path=path):
                with self.assertRaises(urllib.error.HTTPError) as e:self.url(path)
                self.assertEqual(e.exception.code,404)

    def test_verified_local_audio_becomes_streamable_with_range(self):
        local=self.directory/"AXZ-169-tagged.mp3"
        content=b"ID3"+bytes(110_000)
        local.write_bytes(content)
        try:
            with self.url("/api/catalog") as r:
                arr=json.load(r)
            item=next(x for x in arr if x["id"]=="AXZ-169")
            self.assertEqual(item["status"],"preview_ready")
            self.assertEqual(item["previewUrl"],"/api/preview/AXZ-169")
            self.assertFalse(item["downloadEnabled"])
            with self.url("/api/preview/AXZ-169",headers={"Range":"bytes=5-25"}) as r:
                self.assertEqual(r.status,206)
                self.assertEqual(r.headers.get("Content-Type"),"audio/mpeg")
                self.assertEqual(r.headers.get("Content-Disposition"),"inline")
                self.assertEqual(r.headers.get("Content-Range"),f"bytes 5-25/{len(content)}")
                self.assertEqual(r.read(),content[5:26])
            with self.url("/api/preview/AXZ-169",method="HEAD") as r:
                self.assertEqual(r.status,200)
                self.assertEqual(int(r.headers["Content-Length"]),len(content))
            with self.assertRaises(urllib.error.HTTPError) as e:
                self.url("/api/preview/AXZ-169",headers={"Range":"bytes=9999999-"})
            self.assertEqual(e.exception.code,416)
        finally:
            local.unlink()

if __name__=="__main__":
    unittest.main()
