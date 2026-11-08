# AXEZENT — All 50 published beats: independent A–Z audio QA

**Date:** 2026-11-08. **Scope:** the live 50 *new synthetic review MP3s* at https://shawncalvinsnelling.github.io/AXEZENT-Beats-for-Sale/ (not the owner's private originals or lossless paid masters).

## Verifiable verdict

- **50/50** separate, customer-accessible stereo MP3 files were downloaded from the live website and passed codec, 44.1 kHz, duration, SHA uniqueness, EBU R128 loudness, decoded true peak and minimum loudness-range checks.
- **50/50** then passed a second independent 4-section waveform audit covering stereo correlation, mono retention, near-full-scale clipping, FFT frequency balance, short-time pulse contrast, and first-hook/first-verse loudness. **Hard failures: 0.** **Algorithmic producer-review flags: 0** under the published diagnostic criteria.
- Mastering QA mean **-15.42 LUFS** (range **-17.4…-13.7 LUFS**), worst decoded true peak **-1.1 dBFS**.
- Minimum measured stereo-to-mono retained RMS over sampled hook/verse excerpts **0.7801**; greatest sub-250 Hz energy share **83.7%**. High bass share is **not** automatically good or bad: compare kick, 808 and vocals on multiple speakers.
- Highest multi-band hook-and-verse spectral-feature cosine among 1,225 track pairs: **0.9371** (Overtime / Clockwork Hustle). Frequency similarity is **not** a musical duplication or quality score.
- Current source includes 50 curated unique four-patch instrumental combinations, 8 bass patches, seven groove families, vocal-oriented verse space and differentiated hooks. Mathematical and catalog MIDI regression tests passed on commit `b9a149fcdcf78c99c68541ffaf40dab892e0e54d`.
- Live desktop/mobile browser check passed 50 playable buttons, mobile responsiveness, real audio decoding, and no JS errors.

**Evidence:** [50-track complete audio QA run](https://github.com/shawncalvinsnelling/AXEZENT-Beats-for-Sale/actions/runs/42457129189) · [browser QA](https://github.com/shawncalvinsnelling/AXEZENT-Beats-for-Sale/actions/runs/42457129155) · [public deploy](https://github.com/shawncalvinsnelling/AXEZENT-Beats-for-Sale/actions/runs/42456951527).

## Track-by-track verified measurements

*Hook lift* = first-hook excerpt RMS minus first-verse excerpt RMS; positive means the tested hook is stronger. *Mono retention* = mono RMS divided by average-channel RMS, sampled in the verse. *Low-250* = fraction of FFT spectral energy from 25–250 Hz in the verse excerpt, **not** a subjective bass rating.

| # | Title (ID) | LUFS | Peak dBFS | Hook lift dB | Verse mono retention | Verse low-250 |
|---:|---|---:|---:|---:|---:|---:|
| 01 | Diamond in the Dirt (AXZ-169) | -15.1 | -2.0 | 3.87 | 0.945 | 78.4% |
| 02 | Motor City Money (AXZ-085) | -16.1 | -2.1 | 1.39 | 0.929 | 64.5% |
| 03 | Borough Crown (AXZ-125) | -15.0 | -2.4 | 3.75 | 0.967 | 62.3% |
| 04 | Out the Frame (AXZ-017) | -16.2 | -1.8 | 3.84 | 0.933 | 39.9% |
| 05 | Right Now (AXZ-037) | -15.1 | -2.1 | 3.68 | 0.988 | 83.7% |
| 06 | Heartbreak in the Trunk (AXZ-166) | -15.2 | -1.4 | 1.15 | 0.934 | 51.6% |
| 07 | Mile High Motion (AXZ-021) | -15.6 | -1.7 | 4.62 | 0.976 | 59.1% |
| 08 | Gold on the Water (AXZ-033) | -14.9 | -2.4 | 2.88 | 0.978 | 63.0% |
| 09 | City Made Me (AXZ-049) | -14.2 | -1.6 | 1.94 | 0.961 | 56.8% |
| 10 | Second Line Money (AXZ-069) | -15.6 | -1.8 | 4.03 | 0.995 | 34.6% |
| 11 | Queen City Pressure (AXZ-129) | -15.3 | -2.0 | 3.57 | 0.989 | 83.4% |
| 12 | Brick City Armor (AXZ-117) | -15.8 | -2.1 | 0.98 | 0.924 | 45.4% |
| 13 | Heart of Steel (AXZ-137) | -15.9 | -2.3 | 4.16 | 0.911 | 60.1% |
| 14 | Broad Street Hunger (AXZ-149) | -17.1 | -1.7 | 2.09 | 0.993 | 44.7% |
| 15 | Gateway to Gold (AXZ-097) | -15.3 | -2.0 | 4.26 | 0.977 | 50.2% |
| 16 | Rain on the Dashboard (AXZ-185) | -13.9 | -1.8 | 0.74 | 0.994 | 50.4% |
| 17 | Ain't No Easy Way (AXZ-077) | -15.2 | -1.8 | 2.23 | 0.982 | 55.8% |
| 18 | Crown of the South (AXZ-181) | -16.4 | -2.2 | 2.79 | 0.930 | 68.3% |
| 19 | Church Bells and 808s (AXZ-142) | -14.4 | -1.5 | 1.35 | 0.986 | 70.8% |
| 20 | Desert Diamond (AXZ-009) | -16.0 | -1.7 | 2.44 | 0.989 | 52.4% |
| 21 | Heavy Is the Crown (AXZ-001) | -14.3 | -2.3 | 2.85 | 0.978 | 34.8% |
| 22 | Porchlight Prophecy (AXZ-093) | -15.3 | -2.2 | 3.53 | 0.993 | 48.5% |
| 23 | Sweetgrass and Gold (AXZ-157) | -15.7 | -2.1 | 3.19 | 0.991 | 51.6% |
| 24 | Cold City Pressure (AXZ-193) | -14.4 | -1.9 | 0.88 | 0.983 | 55.9% |
| 25 | Ice in My Veins (AXZ-089) | -15.4 | -2.3 | 2.61 | 0.957 | 59.8% |
| 26 | Steel in My Chest (AXZ-054) | -16.5 | -1.1 | 1.46 | 0.909 | 60.1% |
| 27 | Overtime (AXZ-081) | -17.0 | -1.7 | 3.88 | 0.989 | 62.4% |
| 28 | Luck Ain't the Plan (AXZ-109) | -16.2 | -2.0 | 1.90 | 0.980 | 48.4% |
| 29 | Rain Can't Wash It (AXZ-145) | -14.4 | -2.0 | 0.69 | 0.994 | 67.2% |
| 30 | Still Solid (AXZ-013) | -15.4 | -2.1 | 2.81 | 0.977 | 32.1% |
| 31 | Derby Dream (AXZ-065) | -17.1 | -1.6 | 2.33 | 0.951 | 45.9% |
| 32 | Flight Mode (AXZ-061) | -15.2 | -1.8 | 2.72 | 0.785 | 48.5% |
| 33 | Nothing Left to Prove (AXZ-105) | -15.5 | -2.0 | 2.60 | 0.992 | 32.4% |
| 34 | Numbers Never Lie (AXZ-057) | -15.7 | -1.9 | 2.64 | 0.996 | 31.3% |
| 35 | Clockwork Hustle (AXZ-025) | -15.9 | -1.9 | 3.49 | 0.992 | 75.0% |
| 36 | Small State, Big Motion (AXZ-029) | -16.3 | -1.6 | 0.41 | 0.917 | 60.0% |
| 37 | Coal Dust Diamonds (AXZ-189) | -15.3 | -1.8 | 2.62 | 0.991 | 59.2% |
| 38 | Salt in the Wound (AXZ-173) | -14.4 | -2.3 | 0.04 | 0.997 | 39.2% |
| 39 | Can't Count Me Out (AXZ-045) | -15.5 | -2.0 | 2.54 | 0.924 | 29.0% |
| 40 | Dust and Diamonds (AXZ-121) | -14.2 | -2.1 | 2.18 | 0.987 | 46.6% |
| 41 | Island Time Money (AXZ-041) | -16.0 | -1.7 | 1.93 | 0.993 | 44.9% |
| 42 | Cold World Code (AXZ-005) | -13.7 | -2.0 | 2.47 | 0.976 | 24.4% |
| 43 | Ocean in the Rearview (AXZ-073) | -14.7 | -2.2 | 3.32 | 0.989 | 60.6% |
| 44 | Wide Open Vault (AXZ-101) | -15.2 | -1.7 | 3.92 | 0.984 | 39.6% |
| 45 | Cold Cash Season (AXZ-133) | -14.6 | -3.3 | 0.90 | 0.981 | 71.5% |
| 46 | Flatland Famous (AXZ-161) | -13.9 | -1.9 | 2.00 | 0.942 | 43.4% |
| 47 | Wide Open (AXZ-197) | -15.6 | -1.7 | 5.00 | 0.992 | 36.4% |
| 48 | Green Mountain Gold (AXZ-177) | -15.2 | -1.8 | 2.05 | 0.992 | 46.8% |
| 49 | Granite Heart (AXZ-113) | -16.8 | -1.6 | 2.12 | 0.936 | 71.2% |
| 50 | Small City Giants (AXZ-153) | -17.4 | -1.8 | 2.44 | 0.924 | 58.0% |

## Listening decisions that are not automatable

**Seven deliberately flagged here for producer listening, not technical failures:** relatively subtle measured first-hook level lift (<1 dB): Salt in the Wound (AXZ-173, +0.04 dB); Small State, Big Motion (AXZ-029, +0.41 dB); Rain Can't Wash It (AXZ-145, +0.69 dB); Rain on the Dashboard (AXZ-185, +0.74 dB); Cold City Pressure (AXZ-193, +0.88 dB); Cold Cash Season (AXZ-133, +0.90 dB); Brick City Armor (AXZ-117, +0.98 dB). These can be stylistically appropriate for reflective songs, or a cue to strengthen hook instrumentation, but numerical RMS alone cannot decide.

**Highest spectral-resemblance pairs for comparison:** Overtime / Clockwork Hustle (0.9371); Motor City Money / Luck Ain't the Plan (0.8988); Out the Frame / Luck Ain't the Plan (0.8942); Derby Dream / Island Time Money (0.8939); Luck Ain't the Plan / Nothing Left to Prove (0.8931). Do not infer copying or same melodies from these measurements; both style and timbre affect them.

The live MP3s are coded **160 kb/s / 44.1 kHz stereo review audio** made with FluidR3 General MIDI and an FFmpeg EQ/compressor/loudness/limiter chain, not a certified multi-stem professional studio master. We cannot establish $1M hit potential, emotional or hypnotic effects, industry-standard licensing clearance, mono compatibility on every consumer device, or a 10/10 subjective score by software measurement. Audition kick/sub punch, human drum feel, transitions, and vocal room with actual rapping and real speakers before issuing a sale-ready master.

**Reproducibility:** `scripts/audit_loudness.py`, `scripts/audit_audio_depth.py`, `tests/test_arrangements_contract.py`, `.github/workflows/audit-public-audio.yml`. Every audio redeployment triggers the independent public-download QA. The JSON evidence is stored as a 90-day GitHub Actions artifact.

**Publishing policy:** These are audition previews; the owner controls approval and exclusive transfer. No original private stems or paid masters have been authenticated by these tests.
