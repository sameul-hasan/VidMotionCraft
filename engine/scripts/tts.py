#!/usr/bin/env python3
"""Generate Edge TTS voiceover audio and word-level timing JSON for HyperFrames."""

import argparse
import asyncio
import json
from pathlib import Path
import edge_tts

DEFAULT_VOICE = "en-US-AndrewNeural"
ENGINE_DIR = Path(__file__).resolve().parent.parent
AUDIO_DIR = ENGINE_DIR / "assets" / "audio"


async def synthesize(text: str, voice: str, rate: str, pitch: str, out_prefix: str) -> None:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    mp3_path = AUDIO_DIR / f"{out_prefix}.mp3"
    json_path = AUDIO_DIR / f"{out_prefix}.timestamps.json"

    communicate = edge_tts.Communicate(
        text, voice=voice, rate=rate, pitch=pitch, boundary="WordBoundary"
    )
    word_timings = []

    with open(mp3_path, "wb") as audio_file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                # offset and duration are in 100-nanosecond ticks
                start_sec = chunk["offset"] / 10_000_000
                duration_sec = chunk["duration"] / 10_000_000
                word_timings.append(
                    {
                        "word": chunk["text"],
                        "start": round(start_sec, 4),
                        "end": round(start_sec + duration_sec, 4),
                    }
                )

    json_path.write_text(json.dumps(word_timings, indent=2), encoding="utf-8")
    print(f"Audio saved: {mp3_path}")
    print(f"Timestamps saved: {json_path} ({len(word_timings)} words)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Edge TTS generator for HyperFrames")
    parser.add_argument("text", help="Text to synthesize")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help=f"Edge TTS voice (default: {DEFAULT_VOICE})")
    parser.add_argument("--rate", default="+0%", help="Speech rate, e.g. +10%% or -5%%")
    parser.add_argument("--pitch", default="+0Hz", help="Speech pitch, e.g. +5Hz or -3Hz")
    parser.add_argument("--out", default="voiceover", help="Output filename prefix in assets/audio/")
    args = parser.parse_args()

    asyncio.run(synthesize(args.text, args.voice, args.rate, args.pitch, args.out))


if __name__ == "__main__":
    main()
