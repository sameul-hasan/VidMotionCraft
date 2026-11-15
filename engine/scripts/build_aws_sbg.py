#!/usr/bin/env python3
"""Build audio, assets, and HyperFrames composition for AWS SBG DIU reel."""

import asyncio
import json
from pathlib import Path
import edge_tts
from pydub import AudioSegment

ENGINE_DIR = Path(__file__).resolve().parent.parent
AUDIO_DIR = ENGINE_DIR / "assets" / "audio"
LOGOS_DIR = ENGINE_DIR / "assets" / "logos"

DIALOGUE = [
    {
        "speaker": "student",
        "voice": "en-US-BrianMultilingualNeural",
        "text": "Wait, everyone at Daffodil is talking about Cloud, but how do students actually build on AWS without getting lost?",
        "pause_after_ms": 300,
    },
    {
        "speaker": "ai",
        "voice": "en-US-AvaMultilingualNeural",
        "text": "Simple. You join AWS SBG DIU.",
        "pause_after_ms": 350,
    },
    {
        "speaker": "student",
        "voice": "en-US-BrianMultilingualNeural",
        "text": "What is SBG? Just another club with boring slideshows?",
        "pause_after_ms": 300,
    },
    {
        "speaker": "ai",
        "voice": "en-US-AvaMultilingualNeural",
        "text": "Not even close! SBG is Daffodil's official AWS Student Builder Group. We deploy real cloud architecture, run hands-on labs, and host live hackathons.",
        "pause_after_ms": 350,
    },
    {
        "speaker": "student",
        "voice": "en-US-BrianMultilingualNeural",
        "text": "Wait, what if I've never touched an AWS console in my life?",
        "pause_after_ms": 300,
    },
    {
        "speaker": "ai",
        "voice": "en-US-AvaMultilingualNeural",
        "text": "Even better! Senior builders mentor you from zero, help you get AWS certified, and guide you through real production projects.",
        "pause_after_ms": 350,
    },
    {
        "speaker": "student",
        "voice": "en-US-BrianMultilingualNeural",
        "text": "So actual hands-on skills employers look for?",
        "pause_after_ms": 300,
    },
    {
        "speaker": "ai",
        "voice": "en-US-AvaMultilingualNeural",
        "text": "Exactly. Real deployments, real cloud architectures, and a crazy community of builders pushing each other forward.",
        "pause_after_ms": 350,
    },
    {
        "speaker": "student",
        "voice": "en-US-BrianMultilingualNeural",
        "text": "Say no more. How do I join the squad?",
        "pause_after_ms": 300,
    },
    {
        "speaker": "ai",
        "voice": "en-US-AvaMultilingualNeural",
        "text": "Grab your seat right now — the upcoming meetup link is in the comments!",
        "pause_after_ms": 500,
    },
]


async def synthesize_line(index: int, item: dict) -> tuple[Path, list[dict]]:
    tmp_mp3 = AUDIO_DIR / f"_tmp_line_{index}.mp3"
    communicate = edge_tts.Communicate(
        item["text"], voice=item["voice"], boundary="WordBoundary"
    )
    words = []
    with open(tmp_mp3, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                start_sec = chunk["offset"] / 10_000_000
                duration_sec = chunk["duration"] / 10_000_000
                words.append({
                    "word": chunk["text"],
                    "start": round(start_sec, 4),
                    "end": round(start_sec + duration_sec, 4),
                    "speaker": item["speaker"],
                })
    return tmp_mp3, words


async def generate_dialogue():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    LOGOS_DIR.mkdir(parents=True, exist_ok=True)

    master_audio = AudioSegment.silent(duration=100)  # initial 100ms cushion
    current_time_ms = 100
    all_word_timings = []
    line_spans = []

    for i, item in enumerate(DIALOGUE):
        print(f"[{i+1}/{len(DIALOGUE)}] Synthesizing {item['speaker']} ({item['voice']})...")
        tmp_mp3, words = await synthesize_line(i, item)
        seg = AudioSegment.from_file(tmp_mp3, format="mp3")
        seg_duration_ms = len(seg)

        line_start_sec = current_time_ms / 1000.0
        line_end_sec = (current_time_ms + seg_duration_ms) / 1000.0
        line_spans.append({
            "line_index": i,
            "speaker": item["speaker"],
            "text": item["text"],
            "start": round(line_start_sec, 3),
            "end": round(line_end_sec, 3),
        })

        for w in words:
            all_word_timings.append({
                "word": w["word"],
                "start": round(line_start_sec + w["start"], 3),
                "end": round(line_start_sec + w["end"], 3),
                "speaker": w["speaker"],
            })

        master_audio += seg
        current_time_ms += seg_duration_ms

        pause_ms = item["pause_after_ms"]
        master_audio += AudioSegment.silent(duration=pause_ms)
        current_time_ms += pause_ms

        tmp_mp3.unlink(missing_ok=True)

    total_duration_sec = current_time_ms / 1000.0
    out_mp3 = AUDIO_DIR / "aws_sbg_dialogue.mp3"
    out_json = AUDIO_DIR / "aws_sbg_dialogue.timestamps.json"
    out_spans = AUDIO_DIR / "aws_sbg_dialogue.spans.json"

    master_audio.export(out_mp3, format="mp3", bitrate="192k")
    out_json.write_text(json.dumps(all_word_timings, indent=2), encoding="utf-8")
    out_spans.write_text(json.dumps(line_spans, indent=2), encoding="utf-8")

    print(f"Master dialogue saved: {out_mp3} ({total_duration_sec:.2f}s)")
    print(f"Timestamps saved: {out_json} ({len(all_word_timings)} words)")
    print(f"Spans saved: {out_spans} ({len(line_spans)} lines)")
    return total_duration_sec, line_spans, all_word_timings


if __name__ == "__main__":
    asyncio.run(generate_dialogue())
