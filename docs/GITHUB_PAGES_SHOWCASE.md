# AXEZENT GitHub Pages: 50 full-length NEW review tracks — source and verification

**Live public showcase**: https://shawncalvinsnelling.github.io/AXEZENT-Beats-for-Sale/

**Deployment verified**: https://github.com/shawncalvinsnelling/AXEZENT-Beats-for-Sale/actions/runs/42438813265

**50-file live HTTPS check passed**: https://github.com/shawncalvinsnelling/AXEZENT-Beats-for-Sale/actions/runs/42439024120

## The 50 arrangements

All 50 featured songs have individually curated, deterministic, track-ID-linked arrangement plans under `data/arrangements.json`. Section entries specify label, type, number of bars, starting and ending bar indices, and calculated start/end seconds at the published BPM in 4/4. The range includes hook-first, verse-first and short-intro structures, several verse and hook counts, optional bridges and 4-verse arrangements. These are **creative plans**, not statistical findings proving that every artist in a city uses a particular bar count. The unit tests are in `tests/test_arrangements_contract.py`.

The Details popup fetches these 50 plans and displays per-track section timings. The main homepage has been updated to refer to the customer's next **song** rather than next record.

## What the live audio is — and is not

The 50 playable MP3s are **new synthetic sampled-instrument review mixes generated in this repo**, not the source recordings from the earlier private ChatGPT-hosted listening site. The audio renderer is `scripts/render_arranged_review_audio.py`, based on FluidR3 GM sampled instrument patches, ten percussion families, multiple rhythmic pockets, per-track instrument choices, melodic variations and each song's exact bar map. This design aims to improve timbral and structural variety, but cannot replace a producer's actual listening, musical revision, mix engineering and mastering.

The output audio is 128-kbit/s stereo MP3 for browser audition, not the paid studio master. New files are generated in GitHub Actions' temporary runners, grouped into five ten-track artifact batches and combined only into the GitHub Pages site deployment package. This does not write MP3 files into the source Git repository. We do not upload private source masters, WAV files, MIDI or session files to the live website.

**All 50** tracks passed source generation checks for track identity, duration matching, MP3 codec, stereo channels, length, file size and nonduplicate hashes; the published live site was separately checked for 50 HTTP 200 audio HEAD responses plus actual 206 partial-content MP3 requests.

The full-length web MP3s **are capturable and copyable**. A missing Download button is not DRM. Do not claim the $100 masters are secure simply because website users can only press Play. The paid mastered deliverable must be retained separately and delivered under a written rights-transfer contract.

## Recovering the earlier original recordings

Earlier ChatGPT work referenced these owner-held archives:

- `AXEZENT_50_Beats_Ready_To_Listen_Offline_Package.zip`
- `AXEZENT_NODESS_50_TAGGED_WEB_PREVIEWS_UPLOAD.zip`
- `AXEZENT_NODESS_V2_PRIVATE_Volume_01_01-10.zip` plus additional volumes

These names are references only; the files were not available in the current GitHub repository. **Do not claim the new MIDI/SoundFont mixes reproduce them.** For archival reconciliation, recover the actual files, map by stable IDs (for example AXZ-169, AXZ-085), compare SHA-256, durations and audible content, and keep unreleased masters outside public web hosting.

## How to use the website

1. Open https://shawncalvinsnelling.github.io/AXEZENT-Beats-for-Sale/
2. Hard refresh (Ctrl+F5) if an old version is cached.
3. Choose All regional collections, Midwest or another region. Search by city or title.
4. Press **Play** next to a beat. The popup starts that full-length *new review recording*.
5. Use Pause, Play, Stop, Repeat or drag the timeline to seek. Exit closes and stops the music.
6. Open **Details** on any beat for title, city, BPM, key, full structure, section bar counts and calculated start/end times.
7. Use the $100 exclusive instrumental information as a proposed offer; no payment or rights transfer occurs through GitHub Pages.

## Commercial and licensing constraints

GitHub Pages is a static showcase host, and GitHub's own rules prohibit using Pages as a primary e-commerce or online-business website. The public GitHub site therefore has no card collection, paid checkout, protected files or automatically granted intellectual-property rights. Use an independent public HTTPS server for the commercial store and rights-controlled delivery.

The SoundFont used in the workflow is `FluidR3_GM.sf2` by Frank Wen, distributed under MIT terms; verify and retain its full applicable license notice when distributing derived assets or components where required. It is a sampled instrument source, so sound design is not the same as wholly independent recordings of all underlying instruments. Verify commercial licensing and originality before any exclusive rights representation. The `fluidsynth` application and `ffmpeg` are installed in the build runner, not bundled into the visitor website.

## Next release-quality work

The 50 render passes prove **software-generated listening playback**, not excellence of the audio. Producer signoff must separately assess: distinctive drum kits (especially closed hats versus shakers/rims), strong and controlled kick/808 dynamics, motif identity, arrangement contrast, drum fills, clipping and peak/loudness, translation on headphones and truck speakers, correct sample rights, and exact preview/master lineage. Only then is a beat a sale-ready finished asset.
