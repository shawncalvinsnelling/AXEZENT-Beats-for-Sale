# AXEZENT — Press Play Without Public MP3 Links

## Goal

Run the AXEZENT website yourself. The customer sees **▶ Play**, a beat title, and **Email about $100 ownership**. The site does not expose a clickable `*.mp3` download URL, and it contains no paid-master WAV files.

**Important limit:** Listening requires the browser to receive sound data. No honest web application can prevent a capable visitor from recording or extracting the stream. This is NOT DRM. Watermark/tag, use preview-quality files, and keep sale masters private.

## Your computer: get the 50 Play buttons working

1. On GitHub, open **AXEZENT-Beats-for-Sale → Code → Download ZIP**. Extract the repository.
2. Install **Python 3** on Windows if you don't already have it.
3. Create a folder alongside the extracted repository folder, called exactly:
   
   `AXEZENT_PRIVATE_TAGGED_PREVIEWS`
4. From the previous AXEZENT files you already downloaded, extract all **50 tagged preview MP3s** into that private folder. They must have names such as `AXZ-169-tagged.mp3`, `AXZ-085-tagged.mp3` through the complete 50; **do not upload them to GitHub**. The folder can be elsewhere if you set the `AXEZENT_PREVIEW_DIR` environment variable to its full absolute path.
5. Double-click **`LAUNCH_LOCAL_WINDOWS.bat`** in the extracted project. It runs our own `server/axezent_site.py` server.
6. Open **http://127.0.0.1:8080/**. The website will show 50 active Play buttons if all 50 named preview files are present, or disabled ones for any missing files. When you click Play it streams the tagged MP3 directly into the page. Pause and Play are supported. No Download control is provided.
7. To stop your local website, close its command window or press **Ctrl+C**.

If your ZIP was renamed or unpacked into a different location, set the folder explicitly in PowerShell:
```powershell
$env:AXEZENT_PREVIEW_DIR = "C:\\YourFolder\\AXEZENT_PRIVATE_TAGGED_PREVIEWS"
py server/axezent_site.py
```

## Why GitHub cannot be the entire commercial website

- A GitHub repository README is a document; it cannot execute a custom JavaScript player. A direct `raw.githubusercontent.com` audio link lets visitors receive an MP3 and often offers a Download control.
- GitHub Pages is not permitted for websites primarily operating an online shop or facilitating commercial transactions. See GitHub's **GitHub Pages limits** documentation.
- This repository stores public source code only. The real Play interface runs on your own computer/server. The private audio folder is outside the publicly published source.
- To serve customers worldwide, run this same server on an always-online machine with a public domain name, HTTPS and responsible security administration. Use the supplied `Caddyfile.example` to proxy HTTPS to the local service.

## For the developer

- `GET /api/catalog`: the server checks for each tagged preview file in the private folder and only then announces it as playable.
- `GET /api/preview/AXZ-NNN`: range-enabled inline MP3 streaming. It never serves master WAVs or lists directory files; URL identifiers are allowlisted against the 50-release catalog.
- `GET /`, `GET /assets/app.js`, `GET /assets/styles.css`: public static web application.
- HTTP `Range` supported so visitors can seek. Audio uses `Content-Type: audio/mpeg` and `Content-Disposition: inline` with `Cache-Control: no-store`.
- Any unrecognized URL or private filesystem path returns **404**.
- Payments, copyright contracts and master files are handled manually and are **not accessible** from this player.

## Previously published MP3s

50 MP3 preview files and direct links were removed from the current public repository branch. **Git history or cached copies may still expose those previously public previews**. Removing content from `main` is not a true deletion of past publication. For stronger protection, use *new* tagged previews with different arrangements or watermarks and follow GitHub's documented sensitive-data/history cleanup process if appropriate; history rewrites can disrupt clones and cannot retract copies already saved elsewhere.

## Playback quality

These 50 recordings remain **review sketches**, not validated professional studio masters. A buyer should receive only an approved final recording and a separately reviewed, legally enforceable written agreement clarifying transferable master and composition rights.
