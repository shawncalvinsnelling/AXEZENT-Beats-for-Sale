#!/usr/bin/env python3
"""AXEZENT self-hosted listening server.

Runs a *public-facing demo interface* on the owner's machine or behind a HTTPS
reverse proxy. Reads PREVIEW-ONLY, already watermarked MP3s from a private
directory OUTSIDE the public GitHub checkout.

This removes obvious download links. No streaming server can prevent a client
from recording or copying audio they can hear. Never place sale masters here.
"""
import argparse
import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PREVIEW_DIR = ROOT.parent / "AXEZENT_PRIVATE_TAGGED_PREVIEWS"
PUBLIC_PATHS = {
    "/": ROOT / "index.html",
    "/index.html": ROOT / "index.html",
    "/assets/app.js": ROOT / "assets" / "app.js",
    "/assets/styles.css": ROOT / "assets" / "styles.css",
    "/assets/favicon.svg": ROOT / "assets" / "favicon.svg",
    "/assets/axezent-brand-banner.svg": ROOT / "assets" / "axezent-brand-banner.svg",
}
MP3_MAX_SIZE = 10 * 1024 * 1024
AUDIO_ID_PREFIX = "/api/preview/"
MIMES = {".html": "text/html; charset=utf-8",
         ".css": "text/css; charset=utf-8",
         ".js": "text/javascript; charset=utf-8",
         ".svg": "image/svg+xml"}

def load_catalog():
    data = json.loads((ROOT / "data" / "catalog.json").read_text("utf-8"))
    if not isinstance(data, list) or len(data) != 200:
        raise ValueError("Catalog is incomplete")
    return data

def safe_preview_file(track_id, folder):
    # Never interpolate user path contents or accept arbitrary names.
    if len(track_id) != 7 or not track_id.startswith("AXZ-") or not track_id[4:].isdigit():
        return None
    file = folder / (track_id + "-tagged.mp3")
    try:
        if file.is_symlink() or not file.is_file():
            return None
        if not 100_000 <= file.stat().st_size <= MP3_MAX_SIZE:
            return None
        if file.resolve().parent != folder.resolve():
            return None
        return file
    except OSError:
        return None

def make_handler(preview_folder):
    catalog = load_catalog()
    published = {b["id"] for b in catalog if isinstance(b.get("releaseRank"), int) and
                 1 <= b["releaseRank"] <= 50}
    assert len(published) == 50

    class SiteHandler(BaseHTTPRequestHandler):
        server_version = "AXEZENT-Player/1.0"

        def send_security_headers(self):
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
            self.send_header("X-Frame-Options", "DENY")
            self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
            self.send_header(
                "Content-Security-Policy",
                "default-src 'self'; connect-src 'self'; script-src 'self'; "
                "style-src 'self'; img-src 'self' data:; media-src 'self'; "
                "font-src 'self'; object-src 'none'; base-uri 'self'; "
                "frame-ancestors 'none'; form-action 'self'"
            )

        def send_simple(self, status, body, content_type="text/plain; charset=utf-8", send_body=True):
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.send_security_headers()
            self.end_headers()
            if send_body:
                self.wfile.write(body)

        def do_POST(self):
            self.send_simple(405, b"No checkout is enabled")

        def do_HEAD(self):
            self.route(send_body=False)

        def do_GET(self):
            self.route(send_body=True)

        def route(self, send_body):
            path = urlsplit(self.path).path
            if path == "/api/catalog":
                result = []
                for item in catalog:
                    beat = dict(item)
                    file = safe_preview_file(beat["id"], preview_folder) if beat["id"] in published else None
                    if file is not None:
                        beat["status"] = "preview_ready"
                        beat["previewUrl"] = AUDIO_ID_PREFIX + beat["id"]
                    elif beat["id"] in published:
                        beat["status"] = "mix_review"
                        beat["previewUrl"] = None
                    # Payment always requires a manual rights inquiry.
                    beat["buyEnabled"] = False
                    beat["downloadEnabled"] = False
                    result.append(beat)
                blob = json.dumps(result, ensure_ascii=False).encode("utf-8")
                self.send_simple(200, blob, "application/json; charset=utf-8", send_body)
                return

            if path.startswith(AUDIO_ID_PREFIX):
                track_id = path[len(AUDIO_ID_PREFIX):]
                if track_id not in published:
                    self.send_simple(404, b"Preview unavailable", send_body=send_body)
                    return
                file = safe_preview_file(track_id, preview_folder)
                if file is None:
                    self.send_simple(404, b"Preview unavailable", send_body=send_body)
                    return
                try:
                    self.stream_audio(file, send_body)
                except (BrokenPipeError, ConnectionResetError):
                    pass
                return

            # Explicit allowlist: never serve .git, private folders, scripts, WAV,
            # database, keys, or arbitrary files on disk.
            file = PUBLIC_PATHS.get(path)
            if file is None or not file.is_file():
                self.send_simple(404, b"Not found", send_body=send_body)
                return
            blob = file.read_bytes()
            self.send_simple(200, blob, MIMES.get(file.suffix, "application/octet-stream"), send_body)

        def stream_audio(self, file, send_body):
            size = file.stat().st_size
            start, stop = 0, size - 1
            partial = False
            request_range = self.headers.get("Range", "")
            if request_range:
                import re
                match = re.fullmatch(r"bytes=(\d*)-(\d*)", request_range.strip())
                if not match or (not match.group(1) and not match.group(2)):
                    self.invalid_range(size, send_body)
                    return
                first, last = match.groups()
                if not first:
                    suffix = int(last)
                    if suffix <= 0:
                        self.invalid_range(size, send_body)
                        return
                    start = max(0, size - suffix)
                else:
                    start = int(first)
                    stop = int(last) if last else stop
                if start >= size or stop < start:
                    self.invalid_range(size, send_body)
                    return
                stop = min(stop, size - 1)
                partial = True
            remaining = stop - start + 1
            self.send_response(206 if partial else 200)
            self.send_header("Content-Type", "audio/mpeg")
            self.send_header("Content-Disposition", "inline")
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Cache-Control", "private, no-store, max-age=0")
            self.send_header("Content-Length", str(remaining))
            if partial:
                self.send_header("Content-Range", f"bytes {start}-{stop}/{size}")
            self.send_security_headers()
            self.end_headers()
            if not send_body:
                return
            with file.open("rb") as fp:
                fp.seek(start)
                while remaining:
                    chunk = fp.read(min(64 * 1024, remaining))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    remaining -= len(chunk)

        def invalid_range(self, size, send_body):
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.send_header("Content-Length", "0")
            self.send_security_headers()
            self.end_headers()

    return SiteHandler

def main():
    parser = argparse.ArgumentParser(description="Serve AXEZENT's private-preview music player")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--preview-dir", default=os.getenv("AXEZENT_PREVIEW_DIR", str(DEFAULT_PREVIEW_DIR)))
    args = parser.parse_args()
    folder = Path(args.preview_dir).resolve()
    folder.mkdir(parents=True, exist_ok=True)
    if folder == ROOT or ROOT in folder.parents:
        raise SystemExit("Preview directory MUST be outside the public GitHub repository")
    print("AXEZENT private preview server listening on http://%s:%d" % (args.host,args.port), flush=True)
    print("Private tagged MP3 folder:", folder, flush=True)
    print("Found %d of 50 tagged MP3 previews" % sum(
        safe_preview_file(b["id"], folder) is not None for b in load_catalog() if b.get("releaseRank")), flush=True)
    ThreadingHTTPServer((args.host, args.port), make_handler(folder)).serve_forever()

if __name__ == "__main__":
    main()
