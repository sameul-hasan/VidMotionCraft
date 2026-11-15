#!/usr/bin/env python3
"""Extract word-level timestamps using faster-whisper for HyperFrames captions."""

import argparse
import json
import subprocess
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel


def load_audio_16k(audio_path: Path) -> np.ndarray:
    """Decode any audio file to 16kHz mono float32 PCM using ffmpeg."""
    cmd = [
        "/opt/homebrew/bin/ffmpeg",
        "-nostdin",
        "-threads", "0",
        "-i", str(audio_path),
        "-f", "f32le",
        "-ac", "1",
        "-acodec", "pcm_f32le",
        "-ar", "16000",
        "-",
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return np.frombuffer(proc.stdout, dtype=np.float32)


def align_audio(
    audio_path: Path,
    out_json: Path,
    model_size: str = "small",
    language: str | None = None,
    group_size: int = 7,
    accent_words: set[str] | None = None,
) -> None:
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    audio_np = load_audio_16k(audio_path)
    segments, info = model.transcribe(
        audio_np,
        language=language,
        word_timestamps=True,
        vad_filter=False,
    )
    print(f"Detected language: {info.language} (p={info.language_probability:.2f})")

    accent_lower = {w.lower() for w in (accent_words or set())}
    words = []
    idx = 0
    for seg in segments:
        if not seg.words:
            continue
        for w in seg.words:
            token = w.word.strip()
            if not token:
                continue
            clean = token.strip(".,!?;:\"'।")
            entry = {
                "w": token,
                "s": round(float(w.start), 4),
                "e": round(float(w.end), 4),
                "g": idx // group_size,
            }
            if clean.lower() in accent_lower:
                entry["accent"] = True
            words.append(entry)
            idx += 1

    out_json.write_text(json.dumps(words, ensure_ascii=False), encoding="utf-8")
    print(f"Saved {len(words)} Whisper-aligned words -> {out_json}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Whisper word-level alignment for HyperFrames")
    parser.add_argument("audio", type=Path, help="Input MP3/WAV file")
    parser.add_argument("--out", type=Path, required=True, help="Output JSON path")
    parser.add_argument("--model", default="small", help="Whisper model size (tiny, base, small, medium)")
    parser.add_argument("--lang", default=None, help="Language code (e.g. en, bn)")
    parser.add_argument("--group-size", type=int, default=7, help="Words per caption group")
    parser.add_argument("--accent", default="", help="Comma-separated accent words")
    args = parser.parse_args()

    accents = {w.strip() for w in args.accent.split(",") if w.strip()}
    align_audio(args.audio, args.out, args.model, args.lang, args.group_size, accents)


if __name__ == "__main__":
    main()
