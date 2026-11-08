#!/usr/bin/env python3
"""AXEZENT independent musical signal diagnostic, after public deployment.

Measurements are objective playback diagnostics, NOT a 10/10 producer sign-off.
Inspects the actual decoded, customer-accessible 100 MP3s at multiple musical
sections. Does not use restricted originals, fingerprints of commercial music,
or make claims of hypnotic or guaranteed commercial outcomes.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import math
import subprocess
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_RATE = 22050
WINDOW = 4096
HOP = 2048
SPECTRAL_EDGES = np.geomspace(25.0, 10000.0, 49)
FREQS = np.fft.rfftfreq(WINDOW, 1.0 / SAMPLE_RATE)
FREQ_MASK = FREQS >= 25.0


def decode_excerpt(path: Path, midpoint: float, duration: float = 6.0) -> np.ndarray:
    start = max(0, midpoint - duration / 2)
    data = subprocess.check_output([
        "ffmpeg", "-hide_banner", "-nostdin", "-loglevel", "error",
        "-ss", f"{start:.3f}", "-t", f"{duration:.3f}", "-i", str(path),
        "-vn", "-ar", str(SAMPLE_RATE), "-ac", "2",
        "-f", "f32le", "-acodec", "pcm_f32le", "pipe:1"
    ], stderr=subprocess.PIPE)
    samples = np.frombuffer(data, dtype="<f4")
    if samples.size < SAMPLE_RATE * 3 * 2 or samples.size % 2:
        raise ValueError(f"Unusable decoded excerpt in {path}")
    result = samples.reshape(-1, 2)
    if not np.isfinite(result).all():
        raise ValueError(f"Invalid decoded floating-point sample in {path}")
    return result


def inspect_excerpt(samples: np.ndarray) -> dict:
    left, right = samples[:, 0], samples[:, 1]
    mono = (left + right) * 0.5
    side = (left - right) * 0.5
    l2 = float(np.mean(left ** 2))
    r2 = float(np.mean(right ** 2))
    mono_rms = float(np.sqrt(np.mean(mono ** 2)))
    stereo_rms = float(np.sqrt((l2 + r2) * 0.5))
    if stereo_rms < 1e-7:
        raise ValueError("A main musical section is effectively silent")
    corr = float(np.corrcoef(left, right)[0, 1]) if min(l2, r2) > 1e-12 else 1.0
    if not math.isfinite(corr):
        corr = 1.0
    frames = np.lib.stride_tricks.sliding_window_view(mono, WINDOW)[::HOP]
    window = np.hanning(WINDOW).astype(np.float32)
    power = np.mean(np.abs(np.fft.rfft(frames * window, axis=1)) ** 2, axis=0)
    valid_total = max(float(power[FREQ_MASK].sum()), 1e-15)
    energy = np.array([
        float(power[(FREQS >= lo) & (FREQS < hi)].sum()) / valid_total
        for lo, hi in zip(SPECTRAL_EDGES[:-1], SPECTRAL_EDGES[1:])
    ], dtype=np.float64)
    low = float(power[(FREQS >= 25) & (FREQS < 250)].sum()) / valid_total
    deep = float(power[(FREQS >= 25) & (FREQS < 110)].sum()) / valid_total
    presence = float(power[(FREQS >= 2000) & (FREQS < 9000)].sum()) / valid_total
    block = len(mono) // 551
    envelope = np.sqrt(np.mean(mono[:block * 551].reshape(block, 551) ** 2, axis=1))
    dynamic_pulse = float(np.percentile(envelope, 90) /
                          max(float(np.percentile(envelope, 25)), 1e-7))
    features = np.sqrt(energy)
    features = features / max(float(np.linalg.norm(features)), 1e-12)
    return {
        "rmsDbfs": round(20 * math.log10(max(stereo_rms, 1e-12)), 2),
        "stereoCorrelation": round(corr, 4),
        "monoRetention": round(mono_rms / stereo_rms, 4),
        "sideToMid": round(float(np.sqrt(np.mean(side ** 2))) /
                           max(mono_rms, 1e-12), 4),
        "below110HzEnergyShare": round(deep, 4),
        "below250HzEnergyShare": round(low, 4),
        "presence2to9kEnergyShare": round(presence, 4),
        "rhythmicPulseP90overP25": round(dynamic_pulse, 3),
        "nearFullScaleSampleFraction": round(float(np.mean(np.abs(samples) > .995)), 7),
        "spectrum": features.tolist(),
    }


def one(beat: dict, plan: dict, directory: Path) -> dict:
    ident = beat["id"]
    path = directory / (ident + "-review.mp3")
    if not path.is_file():
        raise ValueError("Missing published review mix " + ident)
    sections = plan["sections"]
    verse = next(s for s in sections if s["kind"] == "verse")
    hook = next(s for s in sections if s["kind"] == "hook")
    duration = float(plan["durationSeconds"])
    timings = {
        "opening": 3.0,
        "verse": (verse["startSeconds"] + verse["endSeconds"]) * 0.5,
        "hook": (hook["startSeconds"] + hook["endSeconds"]) * 0.5,
        "ending": max(3.0, duration - 5.0),
    }
    snippets = {name: inspect_excerpt(decode_excerpt(path, seconds))
                for name, seconds in timings.items()}
    review = []
    hard = []
    musical = [snippets["verse"], snippets["hook"]]
    if any(x["monoRetention"] < .35 for x in musical):
        hard.append("Severe stereo-to-mono cancellation")
    elif any(x["monoRetention"] < .75 for x in musical):
        review.append("Verify stereo-to-mono translation on real speakers")
    if any(x["stereoCorrelation"] < -.25 for x in musical):
        hard.append("Inverted stereo phase risk")
    elif any(x["stereoCorrelation"] < 0 for x in musical):
        review.append("Negative stereo correlation in a musical section")
    if any(x["nearFullScaleSampleFraction"] > .0001 for x in musical):
        hard.append("Clipped decoder samples")
    if any(x["below250HzEnergyShare"] > .90 for x in musical):
        review.append("Sub/bass may mask musical detail; inspect kick-bass balance")
    if snippets["hook"]["rmsDbfs"] < snippets["verse"]["rmsDbfs"] - 1:
        review.append("Hook excerpt substantially quieter than verse excerpt")
    if all(x["rhythmicPulseP90overP25"] < 1.08 for x in musical):
        review.append("Low short-term pulse contrast; check transients and groove")
    verse_feature = np.array(snippets["verse"].pop("spectrum"))
    hook_feature = np.array(snippets["hook"].pop("spectrum"))
    for key in ("opening", "ending"):
        snippets[key].pop("spectrum")
    composite = np.concatenate([verse_feature, hook_feature])
    composite /= max(float(np.linalg.norm(composite)), 1e-12)
    return {
        "id": ident, "rank": beat["releaseRank"], "title": beat["title"],
        "city": beat["city"], "bpm": beat["bpm"],
        "hookMinusVerseDb": round(snippets["hook"]["rmsDbfs"] -
                                 snippets["verse"]["rmsDbfs"], 2),
        "excerpts": snippets, "hardFailures": hard, "producerReviewFlags": review,
        "feature": composite.tolist(),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def main() -> int:
    arg = argparse.ArgumentParser()
    arg.add_argument("--audio-dir", type=Path, required=True)
    arg.add_argument("--report", type=Path, required=True)
    arg.add_argument("--catalog",type=Path,default=ROOT/"data/catalog.json")
    arg.add_argument("--arrangements",type=Path,default=ROOT/"data/arrangements.json")
    opts = arg.parse_args()
    catalog = json.loads(opts.catalog.read_text("utf-8"))
    arrangements = json.loads(opts.arrangements.read_text("utf-8"))
    songs = sorted((b for b in catalog if isinstance(b.get("releaseRank"), int)
                    and 1 <= b["releaseRank"] <= 100), key=lambda b: b["releaseRank"])
    if len(songs) != 100:
        raise ValueError("Expected precisely the 100 published arrangements")
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda b: one(b, arrangements[b["id"]], opts.audio_dir),
                                songs))
    identities = [x["sha256"] for x in results]
    if len(set(identities)) != 100:
        raise ValueError("Public audio files were duplicated")
    similar = []
    for index, left in enumerate(results):
        aa = np.array(left["feature"])
        for right in results[index+1:]:
            bb = np.array(right["feature"])
            similarity = float(np.dot(aa, bb))
            similar.append({
                "a": left["id"], "b": right["id"],
                "cosine": round(similarity, 4),
            })
    similar.sort(key=lambda x: x["cosine"], reverse=True)
    for result in results:
        result.pop("feature")
    hard = [{"id": x["id"], "failures": x["hardFailures"]} for x in results
            if x["hardFailures"]]
    flagged = [{"id": x["id"], "flags": x["producerReviewFlags"]} for x in results
               if x["producerReviewFlags"]]
    summary = {
        "tracksAudited": len(results), "differentAudioFiles": len(set(identities)),
        "hardFailureCount": len(hard),
        "producerReviewTrackCount": len(flagged),
        "minimumMonoRetention": min(
            min(x["excerpts"][k]["monoRetention"] for k in ("hook", "verse"))
            for x in results),
        "maximumSub250EnergyShare": max(
            max(x["excerpts"][k]["below250HzEnergyShare"] for k in ("hook", "verse"))
            for x in results),
        "highestSpectralSimilarity": similar[0],
        "independentOfExistingLufsPeakAudit": True,
        "qualityClaim": "Signal diagnostics only; no objective guarantee of musical quality, sample rights, or hit status",
    }
    opts.report.parent.mkdir(parents=True, exist_ok=True)
    opts.report.write_text(json.dumps({
        "summary": summary, "hardFailures": hard,
        "producerReview": flagged, "closestSpectralPairs": similar[:30],
        "tracks": results
    }, indent=2) + "\n", encoding="utf-8")
    print("AUDIO_DEPTH_SUMMARY:", json.dumps(summary), flush=True)
    for result in results:
        print("AUDIO_DEPTH_TRACK:", json.dumps({
            "rank": result["rank"], "id": result["id"],
            "hookMinusVerseDb": result["hookMinusVerseDb"],
            "verseMonoRetention": result["excerpts"]["verse"]["monoRetention"],
            "verseLowEndShare": result["excerpts"]["verse"]["below250HzEnergyShare"],
            "reviewFlags": result["producerReviewFlags"],
        }), flush=True)
    if hard:
        raise ValueError(f"Independent signal-level QA failed: {len(hard)} tracks")
    print("PASS: all 100 published tracks passed hard phase/mono/clipping diagnostic.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
