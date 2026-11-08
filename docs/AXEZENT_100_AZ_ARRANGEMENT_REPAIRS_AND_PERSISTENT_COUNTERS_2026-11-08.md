# AXEZENT 100 — A–Z selective beat repair, custom timbres and live listener counters

**Owner:** Dr. Shawn Calvin Snelling · **Date:** 2026-11-08
**Website:** https://shawncalvinsnelling.github.io/AXEZENT-Beats-for-Sale/

## Verified scope and production boundaries

All 100 city source MIDI grids were rebuilt, checked for stuck/unpaired notes, interval/key/section integrity, sparse lead/counter vocal pickup windows, and consistency with the original 4/4 section plans. **32 of 100** were identified for deliberate original arrangement revisions. **68** were deliberately not rearranged. The reviewed 32 consist of union of weak hook density, high spectral similarity to another song, and known mono/stereo compatibility issues.

**14 weak-hook targets:** AXZ-021 (#7), AXZ-185 (#16), AXZ-181 (#18), AXZ-001 (#21), AXZ-089 (#25), AXZ-013 (#30), AXZ-189 (#37), AXZ-005 (#42), AXZ-073 (#43), AXZ-101 (#44), AXZ-172 (#58), AXZ-070 (#60), AXZ-187 (#82), AXZ-110 (#92).

**10 observed highest-frequency-similarity pairs:** AXZ-129/AXZ-193, AXZ-169/AXZ-186, AXZ-125/AXZ-161, AXZ-033/AXZ-133, AXZ-157/AXZ-090, AXZ-169/AXZ-015, AXZ-089/AXZ-015, AXZ-173/AXZ-083, AXZ-081/AXZ-025, AXZ-077/AXZ-119. High cosine similarity is a *review prioritizer*, not evidence of musical copying.

**Phase/mono priority:** AXZ-172, AXZ-010, AXZ-110. **Quiet hook priority:** AXZ-187. Exact membership is maintained by `scripts/music_a_z_enhance.py`, not by this manually written report.

### What the original A–Z arrangement renderer does

1. Adds a track-ID-keyed alternative sound palette for lead and counter instruments, selecting from 36 lead programs and 27 answering timbres (0-based General MIDI patches).
2. Creates new short, musical, pitch-class-appropriate hook response notes for the 14 low-contrast songs, with variation on successive four- and eight-bar phrases.
3. Adds deliberately restrained verse pickup fills in the latter half of the bar, without consuming the first two beats needed for a rapper's lead vocal.
4. Adds some bridge/breakdown accents and ghost drum detail so not every four-bar block is a static duplicate.
5. For the selected 32 revisions only, overlays an **original sound-generator layer** based on harmonic partials, lightly detuned musical pitches, and frequency modulation. It uses no outside copyrighted sound clips and is constructed from a mathematical oscillator and envelope. It mostly plays during hooks/intros/bridges, rather than cluttering the rap verse.
6. Adjusts stereo side energy **only** for the three documented phase-risk songs; lifts the repeated hook of AXZ-187 across its actual section windows. Every render is subjected to FFT stereo/mono diagnostic and integrated loudness/true-peak checks.

A basic timbre is:
`y(t) = A(t) * sum(a[k] * sin(2*pi*k*f*t + beta*sin(2*pi*f*t/r)))`;
the selected harmonic ratios, envelope and detuning differ by song identity. **No established neuroscience supports a universal "frequency that forces people to dance"**; musical groove, syncopation, anticipation and song-writing drive the intended experience. These experimental generated layers are not guaranteed radio-quality.

### Automated evidence before release

- Full 100-original MIDI integrity and A–Z edit test: **PASS**; **32 enhanced**, **68 unchanged**, **14 weak hooks strengthened**.
- Counter behavior simulated without inflating real counts: **PASS**; one website visit per browser session, one successful first playback per beat per session, not Pause/Resume.
- New audio sample testing: **PASS** for selected Original Collection One and Collection Two review mixes; no hard mono, true-peak, or missing-media failure in sample.
- AXZ-185 (Rain on the Dashboard): newly rendered hook minus verse **+0.34 dB**; mono verse/hook **0.9951/0.9844**.
- AXZ-172 (Alamo After Hours): newly rendered hook minus verse **+3.61 dB**; mono verse/hook **0.9805/0.9593**.
- AXZ-187 (From Ash to Gold): newly rendered hook minus verse **+0.03 dB**; mono verse/hook **0.9961/0.9850**.
- AXZ-010 (Too Hot to Fold): newly rendered hook minus verse **+3.58 dB**; mono verse/hook **0.9900/0.9909**.
- Independent public-customer audio QA after deployment remains required for all 100 actual published MP3s.

**No live audio should be described as 10/10 or artist-approved solely from the automated tests.** The selected previews are still General MIDI/FluidSynth based with an original synthesized overlay and automated mixed mastering, not captured professional studio stems.

## Listening and visit counters on the static Pages site

- Browser stores a session flag, not a cross-site identity; each genuine browser session may add **one** cumulative site visit.
- `<audio>` event `playing` counts the first successfully started play **per beat per browser session**. Pausing/continuing/repeat/reopening does not multiply the same song's count.
- Each card displays **Plays: N** and the player dialog displays that beat's count; the footer shows **Website visits: N**.
- Counter data resides with independent public service `https://countapi.mileshilliard.com/`, not in GitHub source or a credential. All requests use `no-referrer`. No IP address, identity, email or secret token is deliberately sent from the JavaScript.
- These are **play-session estimates**, not a measurement of unique people. Public counter keys can be incremented artificially; the outside provider may have outages, change terms, or lose historical state. The display shows unavailable rather than fabricating success. A guaranteed permanent/fraud-controlled counter requires a separately controlled database or backend.

## Public GitHub music-protection improvement

The upgraded deployment renders all new 50 audio mixes inside **one** ephemeral GitHub Pages deployment job, with no intermediate public Actions audio ZIP batches. The previously approved live MP3 file is downloaded and preserved byte-for-byte for every First Collection song **outside the selected revision list**. The revised original-collection tracks are regenerated only in the deploy workspace. GitHub Pages still needs a temporary website deployment artifact; the repository's existing successful artifact-cleanup workflow deletes it after deployment. **Nothing can technically prevent a visitor copying full MP3 previews served through public GitHub Pages.** Never put private masters, stem multitracks, or buyer deliverables into that site or its public repository.

## Review before sales

Recommended owner review: audition the 32 changed songs, with special attention to drums/bass pocket, regional authenticity, whether the mathematically synthesized lead fits the song, live-vocal verse intelligibility, and mobile/mono/car translation. Recoverable previous public versions can be retained privately if previously saved; GitHub Pages itself is not a substitute for a private backup. Terms for a beat's exclusive copyright transfer require an individual written agreement.

**Code and test evidence:** `scripts/music_a_z_enhance.py`, `scripts/axezent_spectral_timbres.py`, `scripts/render_priority_review_audio.py`, `tests/test_music_a_z_enhance.py`, `tests/test_public_counters.mjs`, `pages-showcase/counters.js`, and the A–Z release-gate GitHub Actions workflow.
