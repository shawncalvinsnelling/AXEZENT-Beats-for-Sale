# AXEZENT — GitHub website and original audio restoration

## Public GitHub HTTPS site
https://shawncalvinsnelling.github.io/AXEZENT-Beats-for-Sale/

The GitHub Pages website displays the original AXEZENT catalog layout, search/filtering and popup player, but **GitHub Pages is not the private listening server or commercial storefront**. Buyers do not need ChatGPT accounts to open the public GitHub site.

The 30-second automatically synthesized excerpts deployed on November 7, 2026 did not match the full-length private recordings. **That substitute audio pipeline was removed on November 7.** The public website no longer claims those clips are the authentic original beats. Never synthesize, replace, shorten, or re-master the source recordings solely to populate the GitHub website without owner review.

## Source media needed for the original 50 recordings

The public repository contains only catalog metadata, frontend code and a self-hosted streaming server. It contains no original MP3/WAV content or GitHub music releases.

Earlier ChatGPT work referenced the following possible owner-held source archives:

- `AXEZENT_50_Beats_Ready_To_Listen_Offline_Package.zip` — reported as a full-length listening archive.
- `AXEZENT_NODESS_50_TAGGED_WEB_PREVIEWS_UPLOAD.zip` — a separate tagged preview package.
- `AXEZENT_NODESS_V2_PRIVATE_Volume_01_01-10.zip` and associated volumes 2–5.

**Do not assume these files are identical, have approved sound quality, or contain the exact mixes from the original private site without comparing them.** Archives referred to in a previous chat are not automatically recoverable in a new chat; the files must be provided again if they are not accessible.

To preserve exact audio, match the original files by stable track ID (`AXZ-169`, `AXZ-085`, etc.), duration, SHA-256 hash, and a listening comparison before publication. Check at least `AXZ-169 — Diamond in the Dirt`, `AXZ-085 — Motor City Money`, and the Omaha recording actually intended by the owner.

## Playback architecture — no ChatGPT dependency

1. Keep the original full-quality masters and session stems private. Store owner-approved, full-length tagged listening versions in a separate folder `AXEZENT_PRIVATE_TAGGED_PREVIEWS`.
2. The existing original `server/axezent_site.py` uses `/api/catalog` and `/api/preview/AXZ-NNN` and supports HTTP range requests for seeking. The Windows/local and Docker/Caddy self-hosting instructions are in `docs/PRIVATE_STREAMING_SETUP.md` and `docs/NO_HOSTING_COMPANY_WINDOWS.md`.
3. Publish the audio-streaming server at an owner-controlled public HTTPS domain; it must be genuinely accessible by visitors without ChatGPT login. The static GitHub frontend can then point to per-track HTTPS streaming URLs via `data/public-preview-manifest.json`, using exact stable IDs and only after testing the URLs.
4. The public pages player is configured for Play, Pause, Stop, Seek, Repeat, and Exit when actual audio URLs are available. Test duration and seek on desktop and mobile. This is an interface contract, **not** a claim that all 50 private source recordings are currently hosted.
5. GitHub Pages itself cannot run a private streaming backend, and GitHub prohibits running an e-commerce store primarily directed at commercial transactions on Pages. The $100 exclusive rights process belongs on the separately hosted full website, not the Pages showcase.

**Security truth:** Any sound sent to a browser can be recorded or extracted, even without a Download button. A stream is not DRM. Keep sale masters private; use appropriate tagged listening copies.

## Normal Pages publication (no generated substitute audio)

1. Under repository **Settings → Pages**, keep **Source: GitHub Actions**.
2. The `Deploy AXEZENT artist showcase to GitHub Pages` workflow builds the static site, publishes no MP3s, and verifies the catalog and controls.
3. Open the website and use Ctrl+F5 to refresh if necessary.

## Link tracking

A link opened from ChatGPT may include `?utm_source=chatgpt.com`, which is an optional referral query parameter, not a relocation to ChatGPT hosting. The clean origin is `https://shawncalvinsnelling.github.io`. Copy/paste the canonical link directly if you do not want the tracking query on the address bar.

The original private ChatGPT-hosted site is separate from this GitHub repository; changes to this repository do not rewrite that site.
