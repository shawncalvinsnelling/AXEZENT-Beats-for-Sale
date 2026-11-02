#!/usr/bin/env python3
"""Publish an AXEZENT GitHub one-click website link ONLY after it is genuinely live.

Run through the GitHub Actions 'Activate public AXEZENT music site' workflow
after independently hosting the site and loading the 50 private preview MP3s.

The storefront stays separate from GitHub's README; no scripts or audio files
are embedded in GitHub's code viewer. The website must answer live HTTP checks.
"""
import argparse
import ipaddress
import json
import re
import socket
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
README=ROOT/"README.md"
BEGIN="<!-- PLAYER_LINK_START -->"
END="<!-- PLAYER_LINK_END -->"
USER_AGENT="AXEZENT-public-player-launch-verifier/1.0"

def validate_url(url):
    url=url.strip().rstrip("/")
    p=urlparse(url)
    if p.scheme!="https" or not p.hostname or p.username or p.password or p.query or p.fragment:
        raise ValueError("A real HTTPS public website URL is required.")
    if p.path not in ("", "/"):
        raise ValueError("Use the site homepage, without a file path.")
    if p.port not in (None,443):
        raise ValueError("Use standard HTTPS port 443.")
    host=p.hostname.lower()
    if host=="localhost" or "." not in host or host.endswith((".local",".internal",".test",".invalid",".example")):
        raise ValueError("Website must have a real public hostname.")
    try:
        ipaddress.ip_address(host)
        raise ValueError("Use a public DNS hostname rather than a literal IP address.")
    except ValueError as exc:
        if "literal IP address" in str(exc):
            raise
    return "https://"+host

def get(url,headers=None,max_read=140_000):
    req=urllib.request.Request(url,headers={"User-Agent":USER_AGENT,**(headers or {})})
    # Domain checked again for redirects, to avoid silently activating a different site.
    opener=urllib.request.build_opener(urllib.request.HTTPSHandler())
    with opener.open(req,timeout=12) as response:
        if urlparse(response.geturl()).hostname!=urlparse(url).hostname:
            raise RuntimeError("Unexpected hostname redirect; verify website and DNS.")
        data=response.read(max_read+1)
        if len(data)>max_read:
            raise RuntimeError("Response larger than expected: "+url)
        return response.status,response.headers,data

def verify_live_player(base):
    status,headers,html=get(base+"/",max_read=250_000)
    if status!=200 or b'id="playerDialog"' not in html or b'id="musicSeek"' not in html:
        raise RuntimeError("Live website must show the actual popup player with seek controls.")
    if b'id="musicPlay"' not in html or b'id="musicStop"' not in html or b'id="closePlayer"' not in html:
        raise RuntimeError("Live website lacks required Play, Stop, or Close controls.")

    status,headers,raw=get(base+"/api/catalog",max_read=200_000)
    if status!=200 or "application/json" not in headers.get("Content-Type",""):
        raise RuntimeError("Live catalog API is unavailable.")
    catalog=json.loads(raw)
    if not isinstance(catalog,list) or len(catalog)!=200:
        raise RuntimeError("Expected all 200 catalog records.")
    first50=[b for b in catalog if isinstance(b.get("releaseRank"),int) and 1<=b["releaseRank"]<=50]
    if len(first50)!=50 or len({b["id"] for b in first50})!=50:
        raise RuntimeError("Expected 50 uniquely identifiable first-release beats.")
    failures=[b["id"] for b in first50 if b.get("status")!="preview_ready" or
              b.get("previewUrl")!="/api/preview/"+b["id"]]
    if failures:
        raise RuntimeError(f"{len(failures)}/50 tracks not ready for playback (first: {failures[:3]}).")

    for beat in (min(first50,key=lambda b:b["releaseRank"]),max(first50,key=lambda b:b["releaseRank"])):
        response=get(base+beat["previewUrl"],{"Range":"bytes=0-15"},max_read=32)
        status,headers,data=response
        if status!=206 or headers.get("Content-Type","").split(";")[0]!="audio/mpeg" or len(data)!=16:
            raise RuntimeError("Audio range streaming failed: "+beat["id"])
        if not (data.startswith(b"ID3") or data[:2] in (b"\xff\xfb",b"\xff\xf3",b"\xff\xf2")):
            raise RuntimeError("Preview stream is not MP3-encoded: "+beat["id"])
    return len(first50)

def publish_link(base):
    text=README.read_text("utf-8")
    if text.count(BEGIN)!=1 or text.count(END)!=1:
        raise RuntimeError("Missing or duplicated README player launch markers.")
    start=text.index(BEGIN)+len(BEGIN)
    finish=text.index(END)
    link="\n**[▶ OPEN AXEZENT MUSIC PLAYER — LISTEN TO ALL 50 BEATS]("+base+"/)**\n\n"
    link+="Click once to open the professional music page. Choose a title, then Play / Pause / Stop / Seek / Exit. No visitor installation or download required.\n"
    updated=text[:start]+link+text[finish:]
    updated=updated.replace(
        "**Online listening status: Player built · Public website not launched yet.**",
        "**Online listening status: Live website link verified.**"
    )
    updated=updated.replace(
        "A working customer-facing link will appear here **only after the owner-controlled server is online and verified**.",
        "Use the live website link at the top of this page to hear the music."
    )
    if updated!=text:
        README.write_text(updated,"utf-8")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--url",required=True,help="Real public HTTPS domain of the running owner-hosted AXEZENT player")
    a=parser.parse_args()
    base=validate_url(a.url)
    ready=verify_live_player(base)
    assert ready==50
    publish_link(base)
    print("PASS: public HTTPS music site verified; 50 preview URLs ready; README one-click player link enabled: "+base)

if __name__=="__main__":
    main()
