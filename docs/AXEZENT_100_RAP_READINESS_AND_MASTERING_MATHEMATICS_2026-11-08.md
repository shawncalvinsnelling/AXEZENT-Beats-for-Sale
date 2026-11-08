# AXEZENT — 100 Original City Beats: Rap-Focused Production and Mathematical Mastering Audit

*November 8, 2026 · Full 100-song source-MIDI audit, linked to last verified 100-song public-audio QA.*

## Overall evidence and audit origin

- [Original 100-track generated-note audit (passed)](https://github.com/shawncalvinsnelling/AXEZENT-Beats-for-Sale/actions/runs/42465411663)
- [Independent 100-track decoded MP3 loudness / phase / stereo / FFT audit (passed)](https://github.com/shawncalvinsnelling/AXEZENT-Beats-for-Sale/actions/runs/42463896348)
- [100 playable buttons and accessible desktop/mobile arrangement timeline (passed)](https://github.com/shawncalvinsnelling/AXEZENT-Beats-for-Sale/actions/runs/42463896372)

The analysis re-executed the **actual MIDI arrangement source** for all 100 city tracks, examined 112,154 original note attacks across 6,250 bars, checked individual drum roles, section intervals and the first two beats of every verse bar. **No customer-facing audio was changed during this audit.**

| Mathematical/structural check | Observed result |
|---|---:|
| Songs / cities | 100 / 100 |
| Original first collection / new second collection | 50 / 50 |
| MIDI note attacks inspected | 112,154 |
| Total bars analyzed | 6,250 |
| Distinct first-hook lead+bass+drum patterns | 100 |
| Distinct first-verse lead+bass+drum patterns | 100 |
| Tracks with zero lead/counter-melody in each verse's first two beats | 100/100 |
| Tracks with kick, snare/clap and top percussion on every verse bar | 100/100 |
| Mean pitched notes per verse bar | 7.77 |
| Mean pitched notes per hook bar | 10.47 |
| Average deviation of kick attacks from theoretical 16th-note grid | 4.221 milliseconds RMS |
| Structural MIDI hard failures | 0 |
| MIDI grid review flags under this particular audit | 0 |

**Important nuance:** A unique MIDI hash is evidence of a different *encoded pattern*, not proof of uniquely memorable music. A functioning kick/snare event says a note is programmed, not that its SoundFont timbre is good or that the kick cuts through the bass. The first-two-beats-clear test explicitly covers **lead and counter lines**, not every possible bass/chord accent or an actual recorded vocal performance.

## Published-audio results (independent decoded MP3 analysis)

The **separate public-audio run** inspected the 100 customer-accessible stereo MP3s: all 100 different files passed codec, nominal section-duration, true-peak, integrated loudness and hard phase/clipping checks; mean −15.68 LUFS, loudness range across songs −17.5 to −14.2 LUFS, highest true peak −1.0 dBFS. **Four producer-review flags remain**:

- **AXZ-172 / rank 58 — Alamo After Hours / San Antonio:** negative stereo-correlation / mono compatibility on at least one excerpt.
- **AXZ-010 / rank 83 — Too Hot to Fold / Tucson:** negative stereo-correlation / mono compatibility.
- **AXZ-187 / rank 82 — From Ash to Gold / Spokane:** hook significantly quieter than verse in tested excerpt.
- **AXZ-110 / rank 92 — High Stakes, Quiet Moves / Reno:** hook significantly quieter than verse in tested excerpt.

These are not hard audio failures. A separate, controlled 4-song A/B is required before changing those mixes. Headphone, phone speaker, car/truck, club sub and actual vocal tracking are still necessary.

## Each of the 100 beats — instrument note-grid evidence

Numbers in **Drums/bar** = kick / snare-clap / hat-and-top-percussion note attacks in all verse bars, averaged across the entire verse sections. **Pitched/bar** = verse → hook note attacks (chord + bass + lead + counter). **Grid RMS** = milliseconds between kick onset and nearest strict 16th-note tick. All audio remains subject to human approval.

| # | Track | City | BPM | Groove family | Bars | Drums/bar K/S/H | Pitched/bar verse→hook | Kick grid RMS (ms) | Source-MIDI checks |
|---:|---|---|---:|---|---:|---:|---:|---:|---|
| 1 | Diamond in the Dirt | Houston, Texas | 84 | swing | 60 | 2.75/2.643/4 | 8.143 → 11.125 | 4.527 | Grid pass |
| 2 | Motor City Money | Detroit, Michigan | 101 | bounce | 56 | 2.75/4.708/5 | 8.167 → 11.125 | 4.216 | Grid pass |
| 3 | Borough Crown | Bronx, New York | 142 | drill | 60 | 2.75/1.625/2 | 7.125 → 8.375 | 2.882 | Grid pass |
| 4 | Out the Frame | Los Angeles, California | 96 | swing | 56 | 2.75/2.625/4.031 | 8.375 → 11.125 | 4.219 | Grid pass |
| 5 | Right Now | Atlanta, Georgia | 138 | trap | 80 | 2.75/1.722/3.972 | 6.889 → 9.625 | 2.978 | Grid pass |
| 6 | Heartbreak in the Trunk | Memphis, Tennessee | 101 | bounce | 46 | 2.75/2.417/3.25 | 8.167 → 12.125 | 3.802 | Grid pass |
| 7 | Mile High Motion | Denver, Colorado | 90 | ambient | 68 | 2.25/1.375/2.25 | 7.125 → 7.375 | 4.116 | Grid pass |
| 8 | Gold on the Water | Miami, Florida | 108 | club | 52 | 3.75/2.417/2 | 6.917 → 12.125 | 4.009 | Grid pass |
| 9 | City Made Me | Chicago, Illinois | 144 | drill | 68 | 2.75/1.667/5.028 | 7.139 → 8.375 | 2.933 | Grid pass |
| 10 | Second Line Money | New Orleans, Louisiana | 103 | swing | 58 | 2.75/4.643/2 | 8.286 → 11.125 | 4.236 | Grid pass |
| 11 | Queen City Pressure | Charlotte, North Carolina | 100 | trap | 54 | 2.75/1.393/5.036 | 6.893 → 9.625 | 4.286 | Grid pass |
| 12 | Brick City Armor | Newark, New Jersey | 132 | drill | 52 | 2.75/2.656/2 | 7.375 → 8.375 | 3.159 | Grid pass |
| 13 | Heart of Steel | Cleveland, Ohio | 97 | bounce | 56 | 2.75/2.417/5 | 8.167 → 12.125 | 4.059 | Grid pass |
| 14 | Broad Street Hunger | Philadelphia, Pennsylvania | 96 | boom_bap | 56 | 2.25/2.625/7 | 8.375 → 9.6 | 4.35 | Grid pass |
| 15 | Gateway to Gold | St. Louis, Missouri | 92 | club | 62 | 3.75/2.625/3.031 | 6.875 → 12.125 | 4.413 | Grid pass |
| 16 | Rain on the Dashboard | Seattle, Washington | 89 | ambient | 60 | 2.25/1.417/2 | 7.167 → 7.375 | 4.078 | Grid pass |
| 17 | Ain't No Easy Way | Baltimore, Maryland | 128 | club | 48 | 3.75/2.667/2 | 6.917 → 12.1 | 3.47 | Grid pass |
| 18 | Crown of the South | Richmond, Virginia | 100 | ambient | 56 | 2.25/1.667/2 | 7.125 → 7.375 | 4.186 | Grid pass |
| 19 | Church Bells and 808s | Tulsa, Oklahoma | 98 | trap | 56 | 2.75/1.438/5.219 | 6.906 → 9.625 | 3.844 | Grid pass |
| 20 | Desert Diamond | Phoenix, Arizona | 92 | bounce | 52 | 2.75/3.667/2 | 8.375 → 12.125 | 4.374 | Grid pass |
| 21 | Heavy Is the Crown | Birmingham, Alabama | 78 | ambient | 48 | 2.25/1.375/3.031 | 7.125 → 7.333 | 5.165 | Grid pass |
| 22 | Porchlight Prophecy | Jackson, Mississippi | 74 | swing | 48 | 2.75/4.667/2 | 8.167 → 11.1 | 5.735 | Grid pass |
| 23 | Sweetgrass and Gold | Charleston, South Carolina | 99 | bounce | 52 | 1.75/1.393/2.25 | 8.143 → 12.1 | 3.792 | Grid pass |
| 24 | Cold City Pressure | Milwaukee, Wisconsin | 105 | trap | 58 | 2.75/1.438/4.062 | 6.969 → 9.625 | 3.661 | Grid pass |
| 25 | Ice in My Veins | Minneapolis, Minnesota | 89 | ambient | 60 | 2.25/1.625/3 | 6.875 → 7.375 | 4.806 | Grid pass |
| 26 | Steel in My Chest | Gary, Indiana | 108 | bounce | 54 | 2.75/2.417/5 | 8.167 → 12.125 | 3.746 | Grid pass |
| 27 | Overtime | Boston, Massachusetts | 90 | boom_bap | 44 | 2.25/2.643/2 | 8.143 → 9.583 | 4.535 | Grid pass |
| 28 | Luck Ain't the Plan | Las Vegas, Nevada | 107 | bounce | 76 | 2.75/2.722/2 | 8.306 → 12.125 | 3.814 | Grid pass |
| 29 | Rain Can't Wash It | Portland, Oregon | 83 | bounce | 48 | 2.75/2.417/4.042 | 8.167 → 12.125 | 4.906 | Grid pass |
| 30 | Still Solid | Little Rock, Arkansas | 76 | ambient | 56 | 2.25/2.357/2 | 7.036 → 7.35 | 5.316 | Grid pass |
| 31 | Derby Dream | Louisville, Kentucky | 79 | bounce | 64 | 2.75/2.643/5.036 | 8.143 → 12.107 | 5.068 | Grid pass |
| 32 | Flight Mode | Wichita, Kansas | 102 | bounce | 80 | 2.75/2.667/2 | 8.306 → 12.111 | 3.844 | Grid pass |
| 33 | Nothing Left to Prove | Omaha, Nebraska | 94 | bounce | 48 | 2.75/2.393/5.25 | 8.143 → 12.083 | 4.381 | Grid pass |
| 34 | Numbers Never Lie | Des Moines, Iowa | 85 | boom_bap | 76 | 2.25/2.688/4.969 | 8.219 → 9.611 | 4.699 | Grid pass |
| 35 | Clockwork Hustle | Hartford, Connecticut | 91 | boom_bap | 48 | 2.25/2.643/7.036 | 8.143 → 9.625 | 4.061 | Grid pass |
| 36 | Small State, Big Motion | Wilmington, Delaware | 99 | bounce | 48 | 2.75/2.667/5 | 8.167 → 12.125 | 4.052 | Grid pass |
| 37 | Coal Dust Diamonds | Charleston, West Virginia | 81 | ambient | 88 | 2.25/1.386/2 | 6.886 → 7.361 | 4.921 | Grid pass |
| 38 | Salt in the Wound | Salt Lake City, Utah | 88 | trap | 58 | 2.75/1.667/2 | 6.917 → 9.625 | 4.655 | Grid pass |
| 39 | Can't Count Me Out | Boise, Idaho | 87 | bounce | 56 | 3.75/2.393/5.286 | 8.143 → 12.125 | 4.887 | Grid pass |
| 40 | Dust and Diamonds | Albuquerque, New Mexico | 90 | drill | 52 | 2.75/3.393/2 | 7.036 → 8.375 | 4.679 | Grid pass |
| 41 | Island Time Money | Honolulu, Hawaii | 96 | bounce | 50 | 3.75/1.417/4.25 | 8.167 → 12.1 | 4.684 | Grid pass |
| 42 | Cold World Code | Anchorage, Alaska | 70 | ambient | 56 | 2.25/2.679/2 | 7.036 → 7.35 | 5.657 | Grid pass |
| 43 | Ocean in the Rearview | Portland, Maine | 78 | ambient | 72 | 2.25/1.464/2 | 6.893 → 7.361 | 5.159 | Grid pass |
| 44 | Wide Open Vault | Billings, Montana | 86 | ambient | 84 | 2.25/1.417/3.028 | 7.056 → 7.361 | 4.629 | Grid pass |
| 45 | Cold Cash Season | Fargo, North Dakota | 82 | trap | 52 | 2.75/1.417/5.25 | 6.917 → 9.625 | 5.201 | Grid pass |
| 46 | Flatland Famous | Sioux Falls, South Dakota | 83 | bounce | 50 | 2.75/2.393/3 | 8.286 → 12.125 | 4.914 | Grid pass |
| 47 | Wide Open | Cheyenne, Wyoming | 84 | bounce | 52 | 2.75/2.667/2 | 8.167 → 12.1 | 4.736 | Grid pass |
| 48 | Green Mountain Gold | Burlington, Vermont | 82 | boom_bap | 72 | 2.25/2.417/2.25 | 8.306 → 9.607 | 5.058 | Grid pass |
| 49 | Granite Heart | Manchester, New Hampshire | 86 | bounce | 88 | 2.75/2.4/7.025 | 8.15 → 12.111 | 4.484 | Grid pass |
| 50 | Small City Giants | Providence, Rhode Island | 91 | swing | 56 | 2.75/4.607/2 | 8.286 → 11.125 | 4.521 | Grid pass |
| 51 | 407 After Midnight | Orlando, Florida | 142 | trap | 80 | 2.75/1.361/5.222 | 6.889 → 9.594 | 2.847 | Grid pass |
| 52 | Duval After Dark | Jacksonville, Florida | 146 | drill | 86 | 2.75/3.333/3 | 7.125 → 8.375 | 2.768 | Grid pass |
| 53 | Bayline Bounce | Tampa, Florida | 128 | club | 72 | 3.75/2.643/3 | 6.893 → 12.094 | 3.323 | Grid pass |
| 54 | Side Street Slap | Oakland, California | 102 | bounce | 72 | 2.75/2.65/3 | 8.375 → 12.125 | 3.909 | Grid pass |
| 55 | Shoreline Chrome | Long Beach, California | 94 | swing | 60 | 2.75/2.375/4.031 | 8.125 → 11.125 | 4.694 | Grid pass |
| 56 | Southbound Sunset | San Diego, California | 92 | swing | 60 | 2.75/2.417/2 | 8.167 → 11.125 | 4.257 | Grid pass |
| 57 | North Tollway Nights | Dallas, Texas | 148 | trap | 84 | 2.75/1.6/2 | 6.9 → 9.625 | 2.579 | Grid pass |
| 58 | Alamo After Hours | San Antonio, Texas | 98 | ambient | 60 | 2.25/1.643/2 | 7.036 → 7.375 | 4.338 | Grid pass |
| 59 | Sixth Street Current | Austin, Texas | 109 | swing | 70 | 2.75/2.625/4.031 | 8.125 → 11.125 | 3.666 | Grid pass |
| 60 | Concrete Magnolia | Baton Rouge, Louisiana | 145 | ambient | 84 | 2.25/2.306/2 | 7.056 → 7.35 | 2.783 | Grid pass |
| 61 | Red River Receipts | Shreveport, Louisiana | 106 | bounce | 68 | 2.75/2.375/5 | 8.125 → 12.125 | 3.891 | Grid pass |
| 62 | Bass in My Bones | Nashville, Tennessee | 88 | swing | 50 | 2.75/4.679/2 | 8.286 → 11.125 | 4.642 | Grid pass |
| 63 | Crossroads Calling | Chattanooga, Tennessee | 99 | bounce | 60 | 3.75/1.667/3 | 8.167 → 12.125 | 4.072 | Grid pass |
| 64 | Velvet and Steel | Savannah, Georgia | 82 | trap | 72 | 2.75/1.4/3.025 | 7.125 → 9.625 | 5.038 | Grid pass |
| 65 | Garden City Grind | Augusta, Georgia | 94 | bounce | 60 | 2.75/1.625/3.031 | 8.125 → 12.125 | 4.44 | Grid pass |
| 66 | Steel Survival | Flint, Michigan | 196 | bounce | 112 | 2.75/1.591/3 | 8.318 → 12.107 | 2.093 | Grid pass |
| 67 | West Side Ledger | Grand Rapids, Michigan | 104 | boom_bap | 60 | 2.25/2.643/2 | 8.143 → 9.6 | 4.096 | Grid pass |
| 68 | Sax and Streetlights | Kansas City, Missouri | 150 | bounce | 88 | 3.75/2.6/2 | 8.375 → 12.1 | 2.932 | Grid pass |
| 69 | Indy Fast Lane | Indianapolis, Indiana | 96 | bounce | 70 | 2.75/2.375/7 | 8.125 → 12.125 | 4.387 | Grid pass |
| 70 | Riverfront Royalty | Cincinnati, Ohio | 91 | swing | 56 | 2.75/4.667/2 | 8.167 → 11.125 | 4.555 | Grid pass |
| 71 | Cap City Frequency | Columbus, Ohio | 104 | bounce | 68 | 1.75/1.625/2.969 | 8.125 → 12.125 | 3.579 | Grid pass |
| 72 | Winter Don't Win | Buffalo, New York | 86 | boom_bap | 50 | 2.25/4.357/3 | 8.286 → 9.625 | 4.685 | Grid pass |
| 73 | Concrete at Dawn | Brooklyn, New York | 95 | boom_bap | 60 | 2.25/2.417/2.25 | 8.167 → 9.625 | 4.454 | Grid pass |
| 74 | Queens at Daybreak | Queens, New York | 88 | boom_bap | 72 | 2.25/2.4/3.25 | 8.375 → 9.625 | 4.413 | Grid pass |
| 75 | Steel and Soul | Pittsburgh, Pennsylvania | 93 | swing | 60 | 2.75/2.625/4.031 | 8.125 → 11.125 | 4.591 | Grid pass |
| 76 | Capital on Repeat | Raleigh, North Carolina | 96 | boom_bap | 60 | 2.25/2.667/2 | 8.167 → 9.625 | 4.606 | Grid pass |
| 77 | Tobacco Road Code | Durham, North Carolina | 90 | swing | 52 | 2.75/2.667/2 | 8.167 → 11.125 | 4.435 | Grid pass |
| 78 | Carolina Midnight | Columbia, South Carolina | 99 | trap | 60 | 2.75/1.393/3 | 7.036 → 9.625 | 4.354 | Grid pass |
| 79 | Anchor on My Soul | Norfolk, Virginia | 100 | bounce | 70 | 2.75/2.625/6.969 | 8.125 → 12.125 | 4.328 | Grid pass |
| 80 | Undertow | Virginia Beach, Virginia | 108 | swing | 64 | 2.75/4.643/2 | 8.286 → 11.107 | 3.892 | Grid pass |
| 81 | Portside Echoes | Tacoma, Washington | 91 | boom_bap | 68 | 2.25/2.375/2.969 | 8.125 → 9.625 | 4.257 | Grid pass |
| 82 | From Ash to Gold | Spokane, Washington | 94 | ambient | 54 | 2.25/2.625/2 | 7.125 → 7.375 | 4.521 | Grid pass |
| 83 | Too Hot to Fold | Tucson, Arizona | 101 | bounce | 60 | 2.75/2.667/2 | 8.167 → 12.125 | 4.132 | Grid pass |
| 84 | Thread the Needle | Paterson, New Jersey | 137 | club | 80 | 3.75/2.636/3.977 | 7.068 → 12.107 | 2.996 | Grid pass |
| 85 | Cold Case Heart | New Haven, Connecticut | 90 | boom_bap | 60 | 2.25/2.375/5.25 | 8.125 → 9.625 | 4.708 | Grid pass |
| 86 | Furnace in My Soul | Springfield, Massachusetts | 93 | boom_bap | 60 | 2.25/2.417/2 | 8.167 → 9.625 | 4.387 | Grid pass |
| 87 | Gulf Coast Pressure | Mobile, Alabama | 100 | club | 60 | 3.75/2.643/2 | 6.893 → 12.1 | 4.358 | Grid pass |
| 88 | Every Scar Shines | Hattiesburg, Mississippi | 82 | swing | 60 | 2.75/2.643/2 | 8.286 → 11.125 | 5.326 | Grid pass |
| 89 | Delta Outlast | Pine Bluff, Arkansas | 86 | swing | 70 | 2.75/2.375/4.25 | 8.125 → 11.125 | 4.843 | Grid pass |
| 90 | Blue Notes, Bluegrass | Lexington, Kentucky | 104 | swing | 60 | 2.75/4.458/2 | 8.167 → 11.107 | 3.752 | Grid pass |
| 91 | Red Dirt Runway | Oklahoma City, Oklahoma | 96 | bounce | 68 | 2.75/2.625/4.969 | 8.125 → 12.125 | 4.267 | Grid pass |
| 92 | High Stakes, Quiet Moves | Reno, Nevada | 98 | ambient | 58 | 2.25/2.594/2 | 7.125 → 7.35 | 4.026 | Grid pass |
| 93 | Capital Grind | Lincoln, Nebraska | 91 | bounce | 60 | 2.75/2.417/2 | 8.167 → 12.125 | 4.3 | Grid pass |
| 94 | Saints on the 808 | Saint Paul, Minnesota | 88 | boom_bap | 72 | 2.25/2.65/7 | 8.375 → 9.625 | 4.555 | Grid pass |
| 95 | Never Park It | Madison, Wisconsin | 110 | bounce | 64 | 3.75/2.625/4.031 | 8.125 → 12.107 | 3.853 | Grid pass |
| 96 | Painted in Fire | Santa Fe, New Mexico | 92 | bounce | 60 | 2.75/2.667/3 | 8.167 → 12.125 | 4.26 | Grid pass |
| 97 | Thin Air, Thick Money | Colorado Springs, Colorado | 103 | club | 60 | 3.75/2.393/2.25 | 6.893 → 12.1 | 4.113 | Grid pass |
| 98 | Silver Spring Static | Silver Spring, Maryland | 101 | bounce | 60 | 2.75/2.393/5 | 8.286 → 12.125 | 3.821 | Grid pass |
| 99 | Head Above the Noise | Topeka, Kansas | 98 | boom_bap | 70 | 2.25/2.625/4 | 8.125 → 9.625 | 4.289 | Grid pass |
| 100 | Willamette After Rain | Eugene, Oregon | 84 | bounce | 56 | 2.75/4.375/3 | 8.167 → 12.125 | 4.736 | Grid pass |

## Mathematics: what is genuinely implemented

1. Beat and section clocks are reproducible: for 4/4 music, one bar lasts **240/BPM seconds**. Every section's precise clock is derived from this musical bar grid.
2. At **44,100 samples/second**, an individual sample spans **22.676 microseconds**; this describes digital time resolution, not a claim that all these songs contain a proprietary or psychoactive "nanogap" algorithm.
3. For a 480-tick-per-quarter MIDI grid, an event at tick `t` has musical clock `t × (60/BPM) / 480` seconds; the timing deviation in the above table compares kick attacks with an ideal 16th-note quantization grid. Variation is not automatically a defect—swing and groove often require it.
4. The generated renderer uses four main GM instruments and MIDI channel-10 percussion with deliberate per-region instrument/program choices, velocity variation, section changes and some finite event jitter. It does **not** currently supply independently recorded kick/snare/hat/vocal stems.
5. The streaming review render uses 44.1-kHz stereo, 160-kbps MP3, equalization, compression, loudness normalization, and limiting. The decoded MP3 is what audio QA measured—not the uncompressed multitrack session.

**Earlier AXEZENT conceptual mastering discussions** proposed deliberate low-frequency centering, band-limited upper-frequency widening, millisecond interchannel delays and phrase-based width. A complete formally versioned NODESS/nanogap psychoacoustic source implementation applicable to these exact 100 mixes was **not** found, and those effects are not claimed as active simply because the ideas were discussed. A/B measurements must precede any DSP that risks phase cancellation or weak mono playback.

## Producer verdict: technical competence versus "million-dollar" art

**Verified:** All 100 generated notes/form maps are structurally coherent under the current rules; live full-length MP3 audio plays; loudness and true peak meet stated review thresholds; no noted hard signal failures.

**Not verified:** Human-sounding live performance, natural drum sample selection, vocal masking under a real rapper, mix translation to commercial broadcast chains, music-publishing rights, sample clearance, and commercial appeal. All 100 renders use a **General MIDI SoundFont** that places a practical ceiling on sonic realism and independent stem processing. More compression or unusual frequencies alone cannot prove the sound would be worth more.

**Next artist-grade test:** Have a performer record an eight- or sixteen-bar vocal plus a hook against selected beats; compare version A/B under matched playback loudness on headphones, phone, mono speaker, car/truck system, and larger monitoring system. Compare lyric intelligibility (especially first two beats), memorable four-bar motifs, kick/bass timing, and hook emotional contrast. Use that evidence to decide which beats get replacement samples and a real multitrack session.

### Engineering reference standards and limits

- [EBU R 128 — programme loudness, Loudness Range, true-peak descriptors](https://tech.ebu.ch/publications/r128)
- [EBU R 128 supplement S2 — streaming loudness context](https://tech.ebu.ch/publications/r128s2)
- [Image-Line FL Studio Piano Roll — editable pitch, duration, velocity, pan](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/pianoroll.htm)

**Commercial note:** Selling ownership requires accurate disclosure of the source and written rights terms. Sounding natural is an artistic goal; do not falsely state that software or generative methods were never used if asked directly.
