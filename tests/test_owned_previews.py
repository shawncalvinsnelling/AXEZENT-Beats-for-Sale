"""Owner-hosting checklist: 50 private preview files are required before launching."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("owned_preflight",ROOT/"scripts"/"check_owned_preview_library.py")
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class OwnerAudioPreflightTests(unittest.TestCase):
    def test_private_folder_requires_fifty_recordings(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp)
            ready,missing=module.scan(d)
            self.assertEqual(len(ready),0)
            self.assertEqual(len(missing),50)
            catalog=json.loads((ROOT/"data"/"catalog.json").read_text("utf-8"))
            first=[x for x in catalog if isinstance(x.get("releaseRank"),int)]
            self.assertEqual(len(first),50)
            for item in first:
                (d/(item["id"]+"-tagged.mp3")).write_bytes(b"ID3"+bytes(100_001))
            ready,missing=module.scan(d)
            self.assertEqual(len(ready),50)
            self.assertEqual(len(missing),0)
            firstfile=d/(first[0]["id"]+"-tagged.mp3")
            firstfile.write_bytes(b"WAV"+bytes(100_001))
            ready,missing=module.scan(d)
            self.assertEqual(len(ready),49)
            self.assertEqual(missing,[first[0]["id"]])

    def test_launch_uses_private_folder_not_public_audio_directory(self):
        batch=(ROOT/"deploy"/"START_AXEZENT_ON_MY_WINDOWS_PC.bat").read_text("utf-8")
        self.assertIn('AXEZENT_PRIVATE_TAGGED_PREVIEWS',batch)
        self.assertIn("check_owned_preview_library.py",batch)
        self.assertIn("--host 127.0.0.1",batch)
        self.assertNotIn("0.0.0.0",batch)
        self.assertNotIn("previews\\",batch)

if __name__=="__main__":
    unittest.main()
