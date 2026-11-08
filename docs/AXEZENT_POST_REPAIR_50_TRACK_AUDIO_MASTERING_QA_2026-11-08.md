# AXEZENT — Final published-audio check after 50-song piano-roll repair

**Checked:** 2026-11-08. **Actual customer-facing site:** https://shawncalvinsnelling.github.io/AXEZENT-Beats-for-Sale/ 

**Reproducible GitHub evidence:**
- [Passing full 50-song public-audio + deeper phase/FFT quality run](https://github.com/shawncalvinsnelling/AXEZENT-Beats-for-Sale/actions/runs/42459506584)
- [Passing final website / mobile browser audit](https://github.com/shawncalvinsnelling/AXEZENT-Beats-for-Sale/actions/runs/42459506632)
- [Passing final 50-song rebuild/deployment](https://github.com/shawncalvinsnelling/AXEZENT-Beats-for-Sale/actions/runs/42459316578)
- [50 real piano-roll diagrams and exact note-pattern tests](https://github.com/shawncalvinsnelling/AXEZENT-Beats-for-Sale/actions/runs/42459316514)
- [Regional/reference production analysis and note-by-note MIDI matrix](AXEZENT_50_PIANO_ROLL_REGIONAL_ERROR_AUDIT_2026-11-08.md)

## What was actually verified

- **50/50** live website review files downloaded from the customer-facing endpoints; codec, sample rate, sample duration, unique SHA256, true peak and EBU R128 band checks: **0 failed checks**.
- Average integrated loudness **-15.7 LUFS**, minimum **-17.5**, maximum **-14.3**; highest measured true peak **-1 dBFS**.
- Independent decoded 4-section signal audit: **50/50**, **50 unique MP3s**, **0 hard failures**, **0 threshold-based producer-review flags**, minimum measured mono RMS retention **0.7549**, highest sub-250Hz FFT energy share **81.8%**.
- Live website UI, 50 buttons and audio decoding verified by Chromium automated checks; artifact protection succeeded.
- All 50 source MIDI grids passed the harmonic return, note-length boundary, scale and verse-density assertions.

## Remaining artist-review observations (not file failures)

- **Rain on the Dashboard (AXZ-185, Seattle)**: the first hook excerpt measured **-0.26 dB** relative to the first verse. It improved from **-0.63 dB** before the selective hook accent but remains slightly quieter: stylistically defensible for downtempo, still worth hearing in a vocal test.
- **Crown of the South (AXZ-181, Richmond)**: hook excerpt changed from **-0.27 dB** to **0.38 dB** after its targeted hook accent; no hard audio failure.
- **Queen City Pressure (Charlotte, AXZ-129)** and **Cold City Pressure (Milwaukee, AXZ-193)** remain spectrally similar (cosine **0.9798** in a limited RMS-normalized 48-band hook-and-verse comparison). A different Milwaukee MIDI voice was tried, but the cosine was not reduced. Similar power spectra are **not** proof of the same melody, groove or song. **Do not over-tune patches to chase this one metric.** This is a candidate for producer judgment only.
- All review recordings use a General MIDI SoundFont, FluidSynth and a stereo FFmpeg mastering chain; **these are not the original private masters, high-end individually mixed stems, certified sample-clear recordings, or proven chart hits**. A reference study of hip-hop subgenres informed the arrangement decisions, but **commercial CD audio or a licensed per-city hit-MIDI dataset was not analyzed**. No objective numerical average of million-dollar commercial songs has been claimed.

## Final 50-track objective measurements

*Hook lift*: first-hook versus first-verse excerpt RMS dB. *Mono*: verse mono retained RMS ratio. *Sub250*: FFT share (25–250 Hz) in verse excerpt; cannot alone diagnose kick/bass masking or bass quality.

| # | Track | ID | LUFS | True peak dBFS | Hook lift dB | Mono ratio | Sub250 |
|---:|---|---|---:|---:|---:|---:|---:|
| 01 | Diamond in the Dirt | AXZ-169 | -15.4 | -2.0 | 3.92 | 0.972 | 81.8% |
| 02 | Motor City Money | AXZ-085 | -16.6 | -2.0 | 0.50 | 0.926 | 70.0% |
| 03 | Borough Crown | AXZ-125 | -15.2 | -2.5 | 2.40 | 0.979 | 61.5% |
| 04 | Out the Frame | AXZ-017 | -16.4 | -1.6 | 4.80 | 0.973 | 47.6% |
| 05 | Right Now | AXZ-037 | -15.1 | -1.9 | 3.36 | 0.990 | 74.8% |
| 06 | Heartbreak in the Trunk | AXZ-166 | -15.6 | -1.1 | 1.70 | 0.932 | 62.9% |
| 07 | Mile High Motion | AXZ-021 | -16.2 | -1.8 | 0.86 | 0.994 | 62.1% |
| 08 | Gold on the Water | AXZ-033 | -14.8 | -2.5 | 2.01 | 0.986 | 73.3% |
| 09 | City Made Me | AXZ-049 | -14.3 | -1.5 | 1.15 | 0.981 | 54.4% |
| 10 | Second Line Money | AXZ-069 | -15.8 | -1.3 | 2.24 | 0.997 | 31.6% |
| 11 | Queen City Pressure | AXZ-129 | -15.3 | -2.2 | 3.12 | 0.991 | 60.2% |
| 12 | Brick City Armor | AXZ-117 | -16.2 | -2.0 | 1.18 | 0.934 | 50.5% |
| 13 | Heart of Steel | AXZ-137 | -16.1 | -2.0 | 3.85 | 0.919 | 62.5% |
| 14 | Broad Street Hunger | AXZ-149 | -17.4 | -1.6 | 1.24 | 0.994 | 54.0% |
| 15 | Gateway to Gold | AXZ-097 | -15.5 | -2.0 | 4.02 | 0.990 | 56.8% |
| 16 | Rain on the Dashboard | AXZ-185 | -14.3 | -2.0 | -0.26 | 0.995 | 45.3% |
| 17 | Ain't No Easy Way | AXZ-077 | -15.4 | -2.1 | 2.54 | 0.985 | 75.4% |
| 18 | Crown of the South | AXZ-181 | -17.0 | -2.3 | 0.38 | 0.934 | 65.9% |
| 19 | Church Bells and 808s | AXZ-142 | -14.6 | -1.7 | 1.59 | 0.989 | 80.5% |
| 20 | Desert Diamond | AXZ-009 | -16.5 | -1.8 | 1.54 | 0.996 | 63.0% |
| 21 | Heavy Is the Crown | AXZ-001 | -14.9 | -2.2 | 1.52 | 0.986 | 41.2% |
| 22 | Porchlight Prophecy | AXZ-093 | -15.5 | -2.5 | 1.53 | 0.998 | 30.5% |
| 23 | Sweetgrass and Gold | AXZ-157 | -15.9 | -2.4 | 3.59 | 0.995 | 44.1% |
| 24 | Cold City Pressure | AXZ-193 | -14.6 | -1.9 | 0.89 | 0.986 | 58.0% |
| 25 | Ice in My Veins | AXZ-089 | -15.5 | -1.7 | 0.05 | 0.991 | 70.3% |
| 26 | Steel in My Chest | AXZ-054 | -16.5 | -1.0 | 1.39 | 0.928 | 57.8% |
| 27 | Overtime | AXZ-081 | -17.5 | -1.6 | 3.10 | 0.992 | 69.5% |
| 28 | Luck Ain't the Plan | AXZ-109 | -16.3 | -2.0 | 2.37 | 0.989 | 56.1% |
| 29 | Rain Can't Wash It | AXZ-145 | -14.8 | -1.6 | 1.67 | 0.995 | 57.6% |
| 30 | Still Solid | AXZ-013 | -15.7 | -1.9 | 0.69 | 0.988 | 38.9% |
| 31 | Derby Dream | AXZ-065 | -17.3 | -1.6 | 3.15 | 0.951 | 61.8% |
| 32 | Flight Mode | AXZ-061 | -15.5 | -2.2 | 3.25 | 0.856 | 53.7% |
| 33 | Nothing Left to Prove | AXZ-105 | -15.6 | -2.3 | 2.38 | 0.993 | 32.2% |
| 34 | Numbers Never Lie | AXZ-057 | -16.0 | -1.7 | 1.45 | 0.997 | 33.7% |
| 35 | Clockwork Hustle | AXZ-025 | -16.1 | -1.5 | 3.44 | 0.994 | 78.2% |
| 36 | Small State, Big Motion | AXZ-029 | -16.6 | -1.4 | 0.48 | 0.920 | 66.0% |
| 37 | Coal Dust Diamonds | AXZ-189 | -15.8 | -1.3 | 0.07 | 0.995 | 48.7% |
| 38 | Salt in the Wound | AXZ-173 | -14.7 | -2.1 | 0.67 | 0.998 | 52.4% |
| 39 | Can't Count Me Out | AXZ-045 | -15.6 | -1.8 | 2.93 | 0.956 | 34.1% |
| 40 | Dust and Diamonds | AXZ-121 | -14.6 | -2.0 | 1.05 | 0.987 | 45.4% |
| 41 | Island Time Money | AXZ-041 | -15.9 | -1.6 | 3.48 | 0.994 | 49.4% |
| 42 | Cold World Code | AXZ-005 | -14.5 | -2.1 | 1.86 | 0.988 | 30.6% |
| 43 | Ocean in the Rearview | AXZ-073 | -15.6 | -2.3 | 2.98 | 0.993 | 80.2% |
| 44 | Wide Open Vault | AXZ-101 | -16.0 | -1.8 | 1.09 | 0.994 | 64.7% |
| 45 | Cold Cash Season | AXZ-133 | -14.5 | -3.0 | 1.37 | 0.984 | 72.7% |
| 46 | Flatland Famous | AXZ-161 | -14.3 | -1.5 | 1.01 | 0.964 | 47.0% |
| 47 | Wide Open | AXZ-197 | -15.8 | -1.7 | 3.21 | 0.996 | 20.7% |
| 48 | Green Mountain Gold | AXZ-177 | -15.4 | -1.3 | 1.94 | 0.994 | 48.0% |
| 49 | Granite Heart | AXZ-113 | -17.0 | -1.3 | 1.61 | 0.939 | 59.3% |
| 50 | Small City Giants | AXZ-153 | -17.5 | -1.5 | 1.95 | 0.930 | 61.0% |

**Signoff policy:** Objective technical QA passed. Producer/artistic approval remains open. Do not claim every track is a 10/10 millionaire hit or sell a certified final studio master based only on these measurements.
