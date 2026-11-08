# AXEZENT — Four-Track Mix A/B: Do Not Publish Unverified Changes

**2026-11-08 · No published audio modified.**

## Independent evidence

- [All 100 original MIDI-structure/rap-space audit: PASS](https://github.com/shawncalvinsnelling/AXEZENT-Beats-for-Sale/actions/runs/42465411663)
- [All 100 existing public MP3 quality diagnostics: PASS, four producer review flags](https://github.com/shawncalvinsnelling/AXEZENT-Beats-for-Sale/actions/runs/42463896348)
- [Four-track test-only A/B candidate audio run: acceptance FAILED intentionally](https://github.com/shawncalvinsnelling/AXEZENT-Beats-for-Sale/actions/runs/42465799863)

A change to four Collection Two tracks was staged and tested privately in branch `100-beat-four-mix-ab-review-20261108`. It used the existing source and same PCM/MP3 chain to compare a regenerated no-change baseline against two proposed tweaks. No A/B audio was sent to the public storefront. The website and published first 50 and next 50 beats retain their previously tested versions.

| Beat | Before → test candidate | Decision |
|---|---|---|
| AXZ-172 — Alamo After Hours (San Antonio), rank 58 | Min mono retention 0.3565 → 0.3588; min stereo correlation −0.7458 → −0.7426 | Too little phase/mono improvement; candidate remains incompatible |
| AXZ-010 — Too Hot to Fold (Tucson), rank 83 | Min mono retention 0.3563 → 0.3575; min stereo correlation −0.7463 → −0.7445 | Too little improvement; do not publish |
| AXZ-187 — From Ash to Gold (Spokane), rank 82 | Hook-versus-verse excerpt −2.17 → −1.85 dB | Measurably stronger but still 1.85 dB below verse; not a producer sign-off |
| AXZ-110 — High Stakes, Quiet Moves (Reno), rank 92 | Hook-versus-verse −0.25 → −0.03 dB, but min stereo correlation −0.3988 → −0.4069 | Slight gain in hook contrast, worse mono/stereo result; do not publish |

**A/B controls:** The baseline and candidate were freshly rendered in the same test environment. A new rendering is not necessarily byte-identical or spectrally identical to a previously published website MP3. These A/B numbers compare fresh render to fresh candidate, not directly to the live published MP3. The independent published-audio report has its own actual live-file metrics. Until the public MP3s are explicitly included in a level-matched controlled comparison, these differences **cannot** be portrayed as improvements to the user's published product.

**Exit criteria:** Four test cases attempted; two had a qualifying improvement on the intended metric, only one passed the complete safety criterion. Acceptance rule required all four to improve without other technical regressions. Result: **fail-closed, no release**.

## Practical path to radio-ready versions

1. Create separate kick/snare/hat/bass/harmony/lead stems using licensed, higher-quality sample and instrument sources instead of relying only on the current General MIDI SoundFont.
2. Test with an actual recorded rap verse and repeated hook, not MIDI note sparsity alone, especially where the chord/lead fundamentals conflict with vocal intelligibility.
3. Use digital-signal measurements *with* listening: short-term/section loudness; sample and true peak; low-bass phase and mono retention; dynamic masking from 150 Hz to 4 kHz; section-to-section impact; and deliberately limited stereo expansion.
4. Work from the source stems before mastering. Avoid forcing every beat to the same loudness or adding unproven 'nanogap' processing.
5. A/B with gain matched and listener-blind evaluations, then release only if the preferred version survives headphone, car/truck, phone, mono and club-system translation tests.

**Verdict:** 100 public beats remain technically playable with the existing strong tests and no hard failures, but there is no justified claim that they are master-perfect, radio-certified, or commercially guaranteed hits. The attempt to improve these four beats was evaluated and safely withheld.
