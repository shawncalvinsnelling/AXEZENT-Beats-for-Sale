#!/usr/bin/env python3
"""Connect the real AXEZENT public preview server to the GitHub Pages player.

Verifies 50 original tagged MP3 streams without downloading audio into memory.
It NEVER renders, synthesizes, copies, or publishes substitute sound.
The owner must already be serving the authentic tagged MP3s via HTTPS.
"""
from __future__ import annotations
import argparse
import ipaddress
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

CATALOG = Path(__file__).resolve().parents[1] / "data" / "catalog.json"
MANIFEST = Path(__file__).resolve().parents[1] / "data" / "public-preview-manifest.json"

def validate_base_url(base: str) -> str:
    if not isinstance(base, str):
        raise ValueError("The website address must be a string")
    parsed = urlsplit(base.strip().rstrip("/"))
    host = parsed.hostname or ""
    if (parsed.scheme != "https" or not host or parsed.username or
            parsed.password or parsed.query or parsed.fragment or parsed.path not in ("", "/")):
        raise ValueError("Use a public HTTPS origin only, e.g. https://beats.yourdomain.com")
    if host in {"localhost", "127.0.0.1"} or host.endswith((".localhost", ".local", ".chatgpt.site")):
        raise ValueError("This must be an independent, visitor-accessible HTTPS stream host")
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        if not address.is_global:
            raise ValueError("Local, private and reserved IP addresses are not public playback hosts")
    return urlunsplit((parsed.scheme, parsed.netloc, "", "", ""))

def featured_tracks(catalog_path: Path) -> list[dict]:
    tracks = json.loads(catalog_path.read_text(encoding="utf-8"))
    if not isinstance(tracks, list) or len(tracks) != 200:
        raise ValueError("Expected original 200-entry AXEZENT catalog")
    chosen = [b for b in tracks if isinstance(b.get("releaseRank"), int) and
              1 <= b["releaseRank"] <= 50]
    if len(chosen) != 50 or len(set(b["id"] for b in chosen)) != 50:
        raise ValueError("Expected 50 unique featured AXEZENT beats")
    if not all(re.fullmatch(r"AXZ-\d{3}", b["id"]) for b in chosen):
        raise ValueError("Invalid stable AXEZENT track ID")
    return sorted(chosen, key=lambda b: b["releaseRank"])

def check_ready(origin: str, timeout: float) -> None:
    url = origin + "/api/ready"
    request = urllib.request.Request(url, headers={"User-Agent":"AXEZENT-Original-Audio-Verifier/1.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        if response.status != 200:
            raise ValueError("Private preview server is not ready")
        info = json.loads(response.read(4096))
    if info.get("websiteReady") is not True or info.get("playableBeats") != 50 or info.get("expectedBeats") != 50:
        raise ValueError("Original server reports fewer than 50 complete tagged previews")

def check_stream(url: str, timeout: float) -> None:
    # Request a 32-byte Range. Never buffer an entire MP3 or master file.
    request = urllib.request.Request(url, headers={
        "Range":"bytes=0-31",
        "User-Agent":"AXEZENT-Original-Audio-Verifier/1.0"
    })
    with urllib.request.urlopen(request, timeout=timeout) as response:
        if response.status != 206:
            raise ValueError(f"Missing partial-content seeking (206) for {url}")
        if not response.headers.get("Content-Range", "").startswith("bytes 0-31/"):
            raise ValueError(f"Missing correct Content-Range for {url}")
        start = response.read(32)
        if len(start) != 32:
            raise ValueError(f"Short audio response for {url}")
        if not (start.startswith(b"ID3") or (start[0] == 0xFF and (start[1] & 0xE0) == 0xE0)):
            raise ValueError(f"Response is not recognizable MP3 audio for {url}")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--origin", required=True, help="Public HTTPS origin of the original AXEZENT streaming server")
    parser.add_argument("--timeout", type=float, default=8.0)
    parser.add_argument("--publish-manifest", action="store_true", help="Write the 50 verified HTTPS audio URLs into GitHub Pages manifest")
    parser.add_argument("--catalog", type=Path, default=CATALOG)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    args = parser.parse_args()
    base = validate_base_url(args.origin)
    beats = featured_tracks(args.catalog)
    check_ready(base, args.timeout)
    urls = {}
    for i, beat in enumerate(beats, start=1):
        url = f"{base}/api/preview/{beat['id']}"
        check_stream(url, args.timeout)
        urls[beat["id"]] = url
        print(f"VERIFIED {i:02}/50 {beat['id']} — HTTP 206 original preview source", flush=True)
    if args.publish_manifest:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        temporary = args.manifest.with_suffix(args.manifest.suffix + ".tmp")
        temporary.write_text(json.dumps(urls, indent=2)+"\n",encoding="utf-8")
        temporary.replace(args.manifest)
        print(f"READY: wrote all 50 authentic source URLs to {args.manifest}")
    else:
        print("VERIFIED: all 50 audio streams are reachable. No files changed (pass --publish-manifest to connect).")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, urllib.error.URLError, json.JSONDecodeError) as error:
        print(f"NOT READY: {error}",file=sys.stderr)
        sys.exit(1)
