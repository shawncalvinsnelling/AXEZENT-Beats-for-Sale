# AXEZENT — One-link public music player on YOUR OWN server

**For visitors:** open one HTTPS address, click a beat, and get our branded popup with **Play, Pause, Stop, drag-to-seek, and Exit**. They never install software or download a ZIP. There is no Download button or publicly listed master file.

**For the owner:** this still requires a real computer/server that stays online. A GitHub README cannot run JavaScript popup players. GitHub's free Pages product also does not permit use as a primarily commercial storefront. The code in this repository is not a substitute for internet-connected hosting.

## Server launch (owner only)

Prerequisites: a computer or server you control, Docker Compose, a domain name you own, working DNS pointed to your server's public address, inbound ports 80 and 443, and your 50 tagged preview MP3s. The MP3s must be previews, not full-quality sale masters.

1. Copy this repository onto the server you control.
2. Beside `compose.yaml`, create a folder `private_previews`. Extract **only 50 tagged MP3 preview files** there; the filenames have the pattern `AXZ-169-tagged.mp3` and so on. **This folder is excluded from Git.**
3. Copy `.env.example` to `.env` and edit `AXEZENT_DOMAIN=beats.example.com` to your actual domain.
4. On that server, run **`bash deploy/launch-on-own-server.sh`**. This verifies the real domain is configured, checks all 50 private preview MP3s exist and are formatted plausibly, then starts our Docker-based API and website. HTTPS certificates can be issued once DNS, ports 80/443, and network reachability are configured.
5. Open `https://YOUR-DOMAIN/` **from a phone on mobile data**. Click `Listen to Diamond in the Dirt`; its popup should open, Play should start audio, Pause should pause, Stop should reset to 0:00, the timeline should seek, and X should exit. Repeat for the remaining 49.
6. Add your verified HTTPS URL to the repository's **About → Website** field. Put the same actual URL in `README.md` so GitHub visitors have **one click** to the live player.

### Diagnostics

- `docker compose ps` — both `player` and `https` services should be healthy/running.
- `docker compose logs --tail 100 player` — inspect the server's startup and audio errors.
- `docker compose logs --tail 100 https` — inspect domain/DNS/certificate errors.
- `curl https://YOUR-DOMAIN/api/ready` — must return 200 JSON with `websiteReady:true` and `playableBeats:50` before any GitHub launch link is enabled. `/api/catalog` returns all 200 catalog records, including the first 50 playable previews.
- No private audio/master files belong in the GitHub repository, the web public root, or a public download directory.

### What "no downloads" means

The popup does **not** provide a download link. The streaming server serves only allowlisted tagged compressed MP3 previews and implements byte-range seeking; it never provides full-quality master WAVs. **No public audio streaming system can guarantee that visitors cannot capture or save the sound they can hear.** Use distinctive short or watermarked previews if leakage matters. Do not ever expose sale masters to anonymous web visitors.

### Payment status

The website still has **email-only inquiries** at `axezentai@gmail.com` and a proposed `$100` exclusive-rights offer. No checkout, PayPal payment verification, automatic master delivery, or copyright assignment is active. Confirm ownership and use a legally appropriate signed agreement before accepting money.

The site has been automated and code-tested, but **it is not publicly online until these owner-side hosting steps are complete**.
