# AXEZENT — Musical-production audit, V3 review masters (2026-11-07)

Status: **PRODUCTION QUALITY OPEN; objective playback and loudness checks PASS.**

This is a musical QA document, not a claim that all beats are studio-ready, historically recovered, market-validated, or $100 rights-clear exclusive masters.

## What was checked

- 50 archived V3 stereo review MP3s and their 50 detailed arrangement blueprints.
- Actual `scripts/render_arranged_review_audio.py` source and its drum, bass, MIDI, melodic and soundbank choices.
- The independent 50-track EBU R128 report, with average -15.78 LUFS, individual range -18.6 to -14 LUFS and maximum true peak -0.9 dBFS (verified by GitHub Actions run 42442358360).
- 18 seconds of each source MP3 beginning at 20 seconds, sampled at 12kHz; 47 log-spaced frequency bands and normalized spectrum comparison. This measures **frequency-balance similarity**, not musical plagiarism or objective artistic quality.
- Existing backups V1, V2 and V3; source audio/arrangement comparison for AXZ-105 Omaha and AXZ-161 South Dakota.
- Historic regional production research from Berklee, University of Houston, Georgia Public Broadcasting, Tulane Music Rising, NPR, The Wire, peer-reviewed Memphis scholarship, and the 2018 study of 665 listeners' groove responses.

## Significant verified missing ingredients

1. The existing source generator cycles through a common **General MIDI sampled-instrument library**, 10 kick pockets, 10 drum-voice maps, 10 hi-hat patterns, 10 chord progressions and 10 melodic seeds. Its 50 files are technically different but **not guaranteed to sound distinct or professionally compelling**.
2. The source has only four programmed pitched GM channels and GM percussion. It has **no separately processed modern tuned 808 track versus kick, snare/clap, hats, chords and lead stems** with individual mixing.
3. Section labels and timecodes vary, but most musical sections repeat inherited voicings and rhythmic logic. Actual production requires dynamics, fills, instrumental subtraction, lyric-flow space, hook countermelodies and purposeful final transitions.
4. The locally measured **median pairwise frequency-balance cosine similarity was 0.732**, with **10 of 1,225 track pairs above 0.95**. These values are diagnostic and do not establish duplicated musical content. Pairs that should get producer comparison include:
   - Church Bells and 808s / Small State, Big Motion (0.982)
   - Flight Mode / Salt in the Wound (0.981)
   - Queen City Pressure / Can't Count Me Out (0.975)
   - Ice in My Veins / Small City Giants (0.969)
   - Desert Diamond / Clockwork Hustle (0.966)
5. Deep bass masking remains a problem even at correct LUFS. One 18-second sample of **Rain Can't Wash It** had about **84.3%** measured FFT-band energy below 250Hz, versus **80.4%** for **Overtime**. This is not the same measurement as LUFS or perceptual loudness and should be confirmed by listening on multiple playback systems.
6. A full historical review of every rapper's entire album/lyric catalog in each city is **not verified**. Regional sound research cannot substitute for permission-cleared, representative listening and recorded flow/cadence analysis.

## Protected music versions

- Omaha, AXZ-105: V1 had **56 bars, short-intro first**. V2/V3 have **48 bars, verse first**. Keep both forms before making a creative decision.
- South Dakota, AXZ-161: The V1/V2/V3 **50-bar structure is unchanged**, and the owner specifically likes this track. Preserve the approved listening version and do not overwrite it as part of broad experiments.
- The complete V1, V2, V3 review archives are separate. The older private NODESS audio is **still not verified or recovered**.

## V4 auditions — not live-site replacements

Three independently generated alternate DRUM + 808 candidate mixes were produced off-site, based on the preserved V3 review bed:

- AXZ-037 — Right Now, Atlanta: original generated kick transients, tuned sustained 808, clap and faster hats, sectional drops.
- AXZ-081 — Overtime, Boston: deeper head-nod kick, snare ghost notes and a different bass pulse.
- AXZ-145 — Rain Can't Wash It, Portland: atmospheric, slower half-time percussion and a controlled lower-end foundation.

The first V4 experiment proved too bass-heavy on a frequency audit; the sub layer was **rebalanced before packaging**. The three updated audition MP3s measure roughly **-14.7 to -14.8 LUFS** with true peaks at or below **-1.4 dBFS**, but remain **subjectively unapproved review mixes**. They were intentionally **not deployed over the 50 currently live tracks**. The personal comparison bundle contains both V3 and V4 files, full source code and measurements.

## Owner approval gates before calling any beat finished

- Unique hook melody, harmony, sound palette and bass contour (not merely unique SHA256).
- Audible but controlled kick/snare/hat/808 separation, mono-safe sub, earbuds/phone/car/truck tests.
- Rap cadence room and clear contrast of verse, bridge, hook and outro; effective first 5-10 seconds.
- Producer-led blind comparison against representative regional references; original compositions, no copying of masters or lyrics.
- Individual multi-stem export, sample/SoundFont licensing verification, written exclusive rights transfer only after review.

## Regional and psychological references

- Berklee hip-hop production dimensions: https://www.berklee.edu/berklee-now/news/essential-features-of-hip-hop-production-tempo-instrumentation-rhythmic-feel-and-sonic-density
- Houston archive: https://www.uh.edu/news-events/stories/2012/august/08282012uhmdjscrew.php
- Detroit: https://www.wmuk.org/npr-news/npr-news/2023-07-27/how-detroit-and-flint-became-havens-for-rap-dark-horses
- Atlanta: https://www.gpb.org/news/2023/07/19/how-atlanta-became-the-center-of-the-rap-universe
- New Orleans bounce: https://musicrising.tulane.edu/discover/themes/bounce/
- Memphis scholar article: https://doi.org/10.1080/03007766.2023.2282883
- West Coast G-funk interview: https://www.thewire.co.uk/in-writing/the-portal/xl-middleton-guide-tog-funk
- Groove psychology (665 participants): https://pmc.ncbi.nlm.nih.gov/articles/PMC6025871/

**Next gate:** listen and compare the V4 candidates to the preserved V3 originals, reject any that do not materially improve the user-perceived sound; then remake only approved tracks with a genuinely separate multitrack instrument/drum workflow.
