#!/usr/bin/env python3
"""real-sfx: Resolve real SFX cues for HyperFrames compositions using Openverse + earshot."""

import argparse
import json
import subprocess
from pathlib import Path
from openverse_sfx import REAL_SFX_DIR, download_and_normalize, search_openverse

ENGINE_DIR = Path(__file__).resolve().parent.parent
STARTER_PACK = {
    "whoosh": "whoosh",
    "pop": "pop",
    "chime": "chime",
    "click": "click",
    "riser": "riser",
}


def ensure_sfx(name: str, query: str) -> Path:
    wav_path = REAL_SFX_DIR / f"{name}.wav"
    if wav_path.exists():
        return wav_path
    results = search_openverse(query, page_size=5)
    # Prefer short SFX (< 4s) if duration metadata is present
    short = [r for r in results if isinstance(r.get("duration"), (int, float)) and r["duration"] <= 4000]
    chosen = (short or results)[0]
    return download_and_normalize(chosen, name, max_duration=3.0)


def cmd_fetch_pack() -> None:
    for name, query in STARTER_PACK.items():
        path = ensure_sfx(name, query)
        print(f"[real-sfx] ready: {path.relative_to(ENGINE_DIR)}")


def cmd_cues(cues_file: Path) -> None:
    cues = json.loads(cues_file.read_text(encoding="utf-8"))
    for idx, cue in enumerate(cues):
        sfx_name = cue["sfx"]
        query = cue.get("query", sfx_name)
        path = ensure_sfx(sfx_name, query)
        rel = path.relative_to(ENGINE_DIR).as_posix()
        cue_id = cue.get("id", f"real-sfx-{idx}")
        start = cue["start"]
        vol = cue.get("volume", 0.35)
        print(f'<audio id="{cue_id}" src="{rel}" data-start="{start}" volume="{vol}"></audio>')


def cmd_inspect(wav_path: Path) -> None:
    earshot_bin = ENGINE_DIR / ".venv" / "bin" / "earshot"
    subprocess.run([str(earshot_bin), "measure", str(wav_path)], check=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="real-sfx pipeline for HyperFrames")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("fetch-pack", help="Download starter real SFX pack from Openverse")
    p_cues = sub.add_parser("cues", help="Resolve JSON cue list to HyperFrames <audio> tags")
    p_cues.add_argument("cues_json", type=Path)
    p_ins = sub.add_parser("inspect", help="Inspect an SFX file using earshot")
    p_ins.add_argument("wav_path", type=Path)
    args = parser.parse_args()

    if args.cmd == "fetch-pack":
        cmd_fetch_pack()
    elif args.cmd == "cues":
        cmd_cues(args.cues_json)
    elif args.cmd == "inspect":
        cmd_inspect(args.wav_path)


if __name__ == "__main__":
    main()
