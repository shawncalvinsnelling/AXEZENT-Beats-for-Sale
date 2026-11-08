# AXEZENT — 50-song real piano-roll error audit and regional production comparison

**2026-11-08. Evidence:** [passing all-50 real MIDI piano-roll CI run](https://github.com/shawncalvinsnelling/AXEZENT-Beats-for-Sale/actions/runs/42458834391) (includes 50 printable FL-Studio-style SVG charts and JSON), [live music renderer](../scripts/render_arranged_review_audio.py), [arrangement integrity regression tests](../tests/test_arrangements_contract.py).

**Scope:** These are the original generated note patterns used to create AXEZENT's 50 current *review MP3s*. An SVG showing precisely sequenced MIDI note onsets and durations is analogous to the FL Studio piano-roll view, **not** an actual FL Studio project screenshot. Commercial hit masters, proprietary piano-roll files, and multitrack stems have **not** been downloaded, inspected, or reverse-engineered. Regional research below is a qualitative style comparator, **not** a numerical average across every charting song from a city.

## Actual source error, not a loudness problem

1. **Returning hooks changed chord progressions.** The old renderer selected `progression[(bar//4)%4]` for every melody/chord/bass lane; all 50 tracks had different absolute starting-bar chord indices across returning hooks. That meant the listener could hear a new harmony under an intended repeated chorus. Corrected to `chord_degree(kind,local_bar)` consistently in all three harmonic lanes, verified first two bars match across recurring hooks in **50/50** songs.
2. **Overcrowded rap verses.** Old code placed 2–3 independently sequenced counter-notes in *every* verse bar in addition to bass, lead, chords and drums. Revised to a four-bar response pattern: rest, one answer, one answer, two-note turnaround; sparse/half-time verse chord shells, shorter chord duration and fewer intrusive rolls. Vocal verse mean is now **7.67 pitched attacks per bar**, with greater hook energy.
3. **The hooks were mechanically identical in density.** Prior piano-roll audit: **13.25 pitched attacks/bar in every one of the 50 hooks**. New hooks differ by groove families, ranging from spacious ambient/drill to fuller club/bounce responses; mean **10.2**. Hook A/B contour repeats, instead of an endless melodic run.
4. **Pitch bleed over the bar line.** Some older lead and bass note lengths could overlap the following chord. The renderer now clamps every pitched GM note before the next bar line, avoiding unintended note collisions.
5. **Catalog contradiction on a key:** *Heartbreak in the Trunk* (Memphis, AXZ-166) was described in the arrangement as *minor-key*, but the written and played key was E major. Corrected the catalog and arrangement jointly to **E minor**, without modifying the track's BPM or form.
6. **Drum/hat excess.** Removed twelve-note crash-style hat rolls every fourth verse bar in drill/trap; restrained rolling emphasis is reserved primarily for hooks, allowing a rapper to sit in the groove.

## Independent MIDI verification of the corrected 50 arrangements

- **50/50** checked; **50/50** have the same pitched harmonic/melodic opening on all repeated hooks; **50** different complete pitched-hook MIDI layouts.
- **49** distinct *16th-note-quantized, instrument-role-labeled* first-hook drum patterns across 50 tracks. This correctly ignores tiny random MIDI timing jitter; a shared kick/snare framework is not itself an error.
- **7.67** average pitched attacks per verse bar; **10.2** per hook bar; **0** programmatic harmonic/key/density/return-identity flags.
- The MIDI analyzer checks key pitch classes, onset, length, hook identity, drum-event categories, and pitched/percussive density; 50 original note-roll SVGs available as the action artifact **AXEZENT-50-REAL-MIDI-PIANO-ROLLS**. It does not check musical memorability by ear.

## Regional production research and musical comparison

| Reference tradition | Grounded musical characteristics (not a required city stereotype) | AXEZENT correction / relevant tracks |
|---|---|---|
| Houston chopped-and-screwed / Southern swing | Slow spacious pulse, repeated motifs and room for extended vocals; DJ Screw's slowed and repeated transitions | *Diamond in the Dirt*: preserve repeat identity and restrained replies rather than synthesizer note clutter |
| Detroit/Flint punch-in rap | Short piano/bell loops and strong enough drum grid for conversational phrasing; modern variations can differ from Dilla-era swing | *Motor City Money*: sparse three-note hook and controlled verse density instead of extra counter-lines |
| Chicago / New York drill | Half-time pulse, short melodic motifs, syncopated bass, lean eerie tops; Chicago and Bronx styles are not identical | *City Made Me*, *Borough Crown*, *Brick City Armor*: fewer hook lead notes, simpler chord shells and rap-friendly verses |
| Southern California G-funk | Melodic synth chords, low-register bass, restrained funk groove | *Out the Frame*: keep syncopation and synth colors, avoid constant high keyboard ornamentation |
| Atlanta trap | Half-time snare, 808-centered low end, selected quicker hat figures rather than rolls throughout every verse | *Right Now*: allow hat embellishments in hook, leave main vocal phrases open |
| Memphis tape tradition | Strong snare, repeating high-hat motifs, lower tempos and dark hypnotic lines rather than over-complex counterpoint | *Heartbreak in the Trunk*: resolve minor-key contradiction and reduce competing lead voices |
| New Orleans bounce / second-line influence | Percussion-driven repetition, call-and-response, dance-centered groove | *Second Line Money*: rhythmic call/response remains, with selective chord stabs instead of permanent layered keys |
| East Coast boom-bap | Head-nod backbeat and repeated compact harmonic motifs; rapper remains rhythmically foregrounded | *Broad Street Hunger*, *Overtime* and similar songs: shorter repeated phrases, reduced note density |

**Source-grounded style references** (descriptive genre research, **not** direct transcriptions or averaged commercial-song MIDI): [Berklee—hip-hop tempo, rhythmic feel, sonic density](https://www.berklee.edu/berklee-now/news/essential-features-of-hip-hop-production-tempo-instrumentation-rhythmic-feel-and-sonic-density); [FL Studio official piano-roll manual](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/pianoroll.htm); [University of Houston DJ Screw exhibition](https://exhibits.lib.uh.edu/s/exhibits/page/dj-screw); [Tulane on New Orleans bounce](https://musicrising.tulane.edu/discover/themes/bounce/); [The Wire: XL Middleton on G-funk](https://www.thewire.co.uk/in-writing/the-portal/xl-middleton-guide-tog-funk); [Memphis rap tape sound study](https://doi.org/10.1080/03007766.2023.2282883); [Tracklib: drill structures](https://www.tracklib.com/blog/drill-beat).

## Complete 50-track source-note audit

**Pitched/Drum values** = first full verse and first full hook average MIDI note-on counts per bar. They are not the counts of *simultaneously sounding* voices, actual loudness, rhythmic interest, listening scores, or comparisons to copyrighted recording data.

| # | Track | City | Arrangement groove | Verse pitched/bar | Hook pitched/bar | Verse drums/bar | Hook drums/bar | Returning hook identical |
|---:|---|---|---|---:|---:|---:|---:|:---:|
| 01 | Diamond in the Dirt | Houston | swing | 8.17 | 11.13 | 9.58 | 11.63 | yes |
| 02 | Motor City Money | Detroit | bounce | 8.17 | 11.13 | 12.67 | 14.50 | yes |
| 03 | Borough Crown | Bronx | drill | 7.13 | 8.38 | 8.56 | 11.63 | yes |
| 04 | Out the Frame | Los Angeles | swing | 8.38 | 11.13 | 9.56 | 11.63 | yes |
| 05 | Right Now | Atlanta | trap | 6.88 | 9.63 | 8.63 | 11.75 | yes |
| 06 | Heartbreak in the Trunk | Memphis | bounce | 8.17 | 12.13 | 10.58 | 12.63 | yes |
| 07 | Mile High Motion | Denver | ambient | 7.13 | 7.38 | 7.00 | 7.75 | yes |
| 08 | Gold on the Water | Miami | club | 6.92 | 12.13 | 10.67 | 12.63 | yes |
| 09 | City Made Me | Chicago | drill | 7.13 | 8.38 | 9.50 | 12.38 | yes |
| 10 | Second Line Money | New Orleans | swing | 8.17 | 11.13 | 9.58 | 11.75 | yes |
| 11 | Queen City Pressure | Charlotte | trap | 6.92 | 9.63 | 9.58 | 12.38 | yes |
| 12 | Brick City Armor | Newark | drill | 7.38 | 8.38 | 7.56 | 10.63 | yes |
| 13 | Heart of Steel | Cleveland | bounce | 8.17 | 12.13 | 12.67 | 14.63 | yes |
| 14 | Broad Street Hunger | Philadelphia | boom_bap | 8.38 | 9.63 | 12.00 | 14.25 | yes |
| 15 | Gateway to Gold | St. Louis | club | 6.88 | 12.13 | 9.50 | 11.88 | yes |
| 16 | Rain on the Dashboard | Seattle | ambient | 7.17 | 7.38 | 7.00 | 7.88 | yes |
| 17 | Ain't No Easy Way | Baltimore | club | 6.92 | 12.00 | 9.58 | 11.50 | yes |
| 18 | Crown of the South | Richmond | ambient | 7.13 | 7.38 | 6.94 | 7.75 | yes |
| 19 | Church Bells and 808s | Tulsa | trap | 6.92 | 9.63 | 9.50 | 12.25 | yes |
| 20 | Desert Diamond | Phoenix | bounce | 8.38 | 12.13 | 8.50 | 10.75 | yes |
| 21 | Heavy Is the Crown | Birmingham | ambient | 7.13 | 7.38 | 7.00 | 7.75 | yes |
| 22 | Porchlight Prophecy | Jackson | swing | 8.17 | 11.13 | 9.58 | 11.75 | yes |
| 23 | Sweetgrass and Gold | Charleston | bounce | 8.13 | 12.13 | 6.50 | 8.50 | yes |
| 24 | Cold City Pressure | Milwaukee | trap | 6.92 | 9.63 | 8.67 | 11.50 | yes |
| 25 | Ice in My Veins | Minneapolis | ambient | 6.88 | 7.38 | 6.94 | 7.88 | yes |
| 26 | Steel in My Chest | Gary | bounce | 8.17 | 12.13 | 12.67 | 14.63 | yes |
| 27 | Overtime | Boston | boom_bap | 8.13 | 9.63 | 9.06 | 11.13 | yes |
| 28 | Luck Ain't the Plan | Las Vegas | bounce | 8.38 | 12.13 | 9.88 | 11.75 | yes |
| 29 | Rain Can't Wash It | Portland | bounce | 8.17 | 12.13 | 9.67 | 11.63 | yes |
| 30 | Still Solid | Little Rock | ambient | 7.13 | 7.38 | 7.00 | 7.88 | yes |
| 31 | Derby Dream | Louisville | bounce | 8.13 | 12.13 | 10.56 | 12.63 | yes |
| 32 | Flight Mode | Wichita | bounce | 8.38 | 12.13 | 7.50 | 9.38 | yes |
| 33 | Nothing Left to Prove | Omaha | bounce | 8.13 | 12.13 | 12.56 | 14.63 | yes |
| 34 | Numbers Never Lie | Des Moines | boom_bap | 8.17 | 9.63 | 10.08 | 12.13 | yes |
| 35 | Clockwork Hustle | Hartford | boom_bap | 8.13 | 9.63 | 12.06 | 14.00 | yes |
| 36 | Small State, Big Motion | Wilmington | bounce | 8.17 | 12.13 | 12.58 | 14.63 | yes |
| 37 | Coal Dust Diamonds | Charleston | ambient | 6.88 | 7.38 | 6.88 | 8.00 | yes |
| 38 | Salt in the Wound | Salt Lake City | trap | 6.92 | 9.63 | 7.58 | 10.00 | yes |
| 39 | Can't Count Me Out | Boise | bounce | 8.17 | 12.13 | 11.58 | 13.63 | yes |
| 40 | Dust and Diamonds | Albuquerque | drill | 7.13 | 8.38 | 8.56 | 11.63 | yes |
| 41 | Island Time Money | Honolulu | bounce | 8.17 | 12.13 | 9.67 | 11.38 | yes |
| 42 | Cold World Code | Anchorage | ambient | 7.13 | 7.38 | 7.06 | 7.63 | yes |
| 43 | Ocean in the Rearview | Portland | ambient | 6.88 | 7.38 | 7.13 | 8.00 | yes |
| 44 | Wide Open Vault | Billings | ambient | 7.13 | 7.38 | 7.00 | 8.00 | yes |
| 45 | Cold Cash Season | Fargo | trap | 6.92 | 9.63 | 9.58 | 12.50 | yes |
| 46 | Flatland Famous | Sioux Falls | bounce | 8.38 | 12.13 | 10.44 | 12.75 | yes |
| 47 | Wide Open | Cheyenne | bounce | 8.17 | 12.13 | 9.58 | 11.75 | yes |
| 48 | Green Mountain Gold | Burlington | boom_bap | 8.38 | 9.63 | 8.06 | 10.13 | yes |
| 49 | Granite Heart | Manchester | bounce | 8.15 | 12.13 | 12.45 | 14.63 | yes |
| 50 | Small City Giants | Providence | swing | 8.38 | 11.13 | 9.44 | 11.75 | yes |

## Producer sign-off still requires separate evidence

Different pitch patterns and all-green waveform QA do **not** mean 50 unique million-dollar hit songs. The source renderer uses a GM SoundFont and stereo review MP3 chain—not separate high-quality kick, 808, bass, snare, leads and chord audio stems. Without actual listening/recorded-rap testing and suitable rights-cleared reference files, it would be deceptive to assign a subjective 10/10 score or claim we measured the numerical average of commercial hits.

Producer review should concentrate on kick/bass tone, musical emotion, ear-catching first seconds, local style nuance, and how actual vocals fit each verse. Do not approve or sell a private master solely on note-grid statistics.
