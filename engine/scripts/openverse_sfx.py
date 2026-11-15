#!/usr/bin/env python3
"""Search and download real CC-licensed sound effects via the Openverse API v1."""

import argparse
import json
import subprocess
from pathlib import Path
import requests

OPENVERSE_AUDIO_URL = "https://api.openverse.org/v1/audio/"
ENGINE_DIR = Path(__file__).resolve().parent.parent
REAL_SFX_DIR = ENGINE_DIR / "assets" / "sfx" / "real"
CREDITS_FILE = REAL_SFX_DIR / "credits.json"


def search_openverse(
    query: str,
    page_size: int = 10,
    license_type: str | None = None,
    source: str | None = None,
    category: str | None = None,
) -> list[dict]:
    params = {
        "q": query,
        "page_size": str(page_size),
    }
    if category:
        params["category"] = category
    if license_type:
        params["license_type"] = license_type
    if source:
        params["source"] = source

    resp = requests.get(
        OPENVERSE_AUDIO_URL,
        params=params,
        headers={
            "Accept": "application/json",
            "User-Agent": "video-viral-engine/1.0 (https://github.com/sameul-hasan)",
        },
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json().get("results", [])


def download_and_normalize(item: dict, out_name: str, max_duration: float = 3.5) -> Path:
    REAL_SFX_DIR.mkdir(parents=True, exist_ok=True)
    audio_url = item["url"]
    tmp_raw = REAL_SFX_DIR / f".tmp_{out_name}"
    out_wav = REAL_SFX_DIR / f"{out_name}.wav"

    resp = requests.get(
        audio_url,
        headers={"User-Agent": "video-viral-engine/1.0"},
        timeout=30,
    )
    resp.raise_for_status()
    tmp_raw.write_bytes(resp.content)

    try:
        subprocess.run(
            [
                "/opt/homebrew/bin/ffmpeg",
                "-y",
                "-i", str(tmp_raw),
                "-t", str(max_duration),
                "-ar", "48000",
                "-ac", "2",
                "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                str(out_wav),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    finally:
        if tmp_raw.exists():
            tmp_raw.unlink()

    credits = {}
    if CREDITS_FILE.exists():
        credits = json.loads(CREDITS_FILE.read_text(encoding="utf-8"))
    credits[f"{out_name}.wav"] = {
        "title": item.get("title"),
        "creator": item.get("creator"),
        "license": item.get("license"),
        "license_version": item.get("license_version"),
        "source": item.get("source"),
        "foreign_landing_url": item.get("foreign_landing_url"),
        "url": audio_url,
    }
    CREDITS_FILE.write_text(json.dumps(credits, indent=2), encoding="utf-8")
    return out_wav


def main() -> None:
    parser = argparse.ArgumentParser(description="Openverse API v1 SFX searcher & downloader")
    parser.add_argument("query", help="Search keywords (e.g. 'whoosh', 'ui pop', 'notification chime')")
    parser.add_argument("--limit", type=int, default=8, help="Max results to fetch")
    parser.add_argument("--download", default=None, help="Download & normalize pick to assets/sfx/real/<name>.wav")
    parser.add_argument("--pick", type=int, default=0, help="0-based index of result to download")
    parser.add_argument("--max-dur", type=float, default=3.0, help="Trim downloaded SFX to max seconds")
    parser.add_argument("--license-type", default=None, help="e.g. commercial or modification")
    args = parser.parse_args()

    results = search_openverse(args.query, page_size=args.limit, license_type=args.license_type)
    if not results:
        print(f"No Openverse sound_effect results for: {args.query}")
        return

    for idx, r in enumerate(results):
        dur_ms = r.get("duration")
        dur_s = f"{dur_ms / 1000:.2f}s" if isinstance(dur_ms, (int, float)) else "?"
        print(f"[{idx}] {r.get('title', 'Untitled')} | {dur_s} | {r.get('license')} | {r.get('source')}")

    if args.download:
        chosen = results[min(args.pick, len(results) - 1)]
        wav_path = download_and_normalize(chosen, args.download, max_duration=args.max_dur)
        print(f"Saved real SFX -> {wav_path}")


if __name__ == "__main__":
    main()
