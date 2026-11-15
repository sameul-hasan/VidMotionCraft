import json
import os
import subprocess
import soundfile as sf
import torch
from huggingface_hub import snapshot_download
from omnivoice import OmniVoice

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "../assets/audio")
RAFI_REF = os.path.join(os.path.dirname(__file__), "../assets/voices/native_rafi_ref.wav")
RAFI_REF_TEXT = (
    "ভাই এমন দুইটি গিটহাব রিপোজিটরি পেয়েছি যেগুলো তোমার অনেক কাজ সহজ করে দিবে "
    "এবং হাজার ডলারের পেইড সফটওয়্যারের বিকল্প হতে পারে। এমন আরও টেক আপডেট পেতে পেজটি ফলো করে রাখো।"
)
os.makedirs(AUDIO_DIR, exist_ok=True)

PARTS = {
    1: {
        "prefix": "story_part1_en",
        "lines": [
            {
                "tts_text": "Five days ago, I unlocked Antigravity for just five dollars a month using the student offer.",
                "caption_text": "5 days ago, I unlocked Antigravity for just $5/mo using the Student Offer.",
            },
            {
                "tts_text": "Normally it costs twenty dollars, so that is seventy five percent off with a student email.",
                "caption_text": "Normally $20/mo—that is 75% off with a verified student email.",
            },
            {
                "tts_text": "I wanted to test if one five dollar AI workspace could replace an entire production studio.",
                "caption_text": "I wanted to test if one $5 AI workspace could replace a full studio.",
            },
            {
                "tts_text": "On day one, I typed a single prompt, and Antigravity built a 3D motion graphics engine from scratch.",
                "caption_text": "On Day 1, one prompt built a 3D motion-graphics engine from scratch.",
            },
            {
                "tts_text": "No After Effects, no templates, just HTML, GSAP, and Chrome rendering full 1080p reels.",
                "caption_text": "No After Effects, no templates—just HTML, GSAP, and Chrome rendering 1080p reels.",
            },
            {
                "tts_text": "That was only day one. Follow for part two to see what we built next.",
                "caption_text": "That was only Day 1. Follow for Part 2 to see what we built next.",
            },
        ],
    },
    2: {
        "prefix": "story_part2_en",
        "lines": [
            {
                "tts_text": "Day two of building everything with the five dollar Antigravity student offer.",
                "caption_text": "Day 2 of building everything with the $5 Antigravity Student Offer.",
            },
            {
                "tts_text": "Instead of guessing edits, I gave Antigravity real viral reels to analyze.",
                "caption_text": "Instead of guessing edits, I gave Antigravity real viral reels to analyze.",
            },
            {
                "tts_text": "Using y t d l p and f f probe, it measured pacing, color tone, and scene cuts automatically.",
                "caption_text": "Using yt-dlp and ffprobe, it measured pacing, color tone, and scene cuts.",
            },
            {
                "tts_text": "Then it pulled official tech logos, layered real sound effects, and shipped our Aayojon 3D product reels.",
                "caption_text": "Then it pulled official logos, layered real SFX, and shipped Aayojon 3D reels.",
            },
            {
                "tts_text": "We even generated a full behind the scenes breakdown showing the exact code and timeline.",
                "caption_text": "We even generated a full behind-the-scenes breakdown with code and timelines.",
            },
            {
                "tts_text": "Next up in part three: how we took this engine live for an entire university tech event.",
                "caption_text": "Next in Part 3: taking this engine live for a university tech event.",
            },
        ],
    },
    3: {
        "prefix": "story_part3_en",
        "lines": [
            {
                "tts_text": "Day three and four: could this five dollar AI setup handle real client and community promos?",
                "caption_text": "Days 3 & 4: could this $5 AI setup handle real community promos?",
            },
            {
                "tts_text": "We had an upcoming A W S Student Build and Grow event at Daffodil International University.",
                "caption_text": "We had an upcoming AWS Student Build & Grow event at DIU.",
            },
            {
                "tts_text": "Antigravity gathered the official A W S and club badges, built 3D perspective cards, and synced every beat.",
                "caption_text": "Antigravity pulled official AWS & club badges, built 3D cards, and synced every beat.",
            },
            {
                "tts_text": "Every single transition, sound hit, and word-by-word caption was compiled into code in minutes.",
                "caption_text": "Every transition, sound hit, and word-by-word caption was compiled in minutes.",
            },
            {
                "tts_text": "What usually takes a motion designer days of keyframing became a repeatable automated workflow.",
                "caption_text": "Days of manual keyframing became a repeatable automated workflow.",
            },
            {
                "tts_text": "But there was still one paid bottleneck left: voiceovers. That changed on day five.",
                "caption_text": "One paid bottleneck remained: voiceovers. That changed on Day 5.",
            },
        ],
    },
    4: {
        "prefix": "story_part4_en",
        "lines": [
            {
                "tts_text": "Day five was the biggest breakthrough of the whole week: zero cloud fees for voice.",
                "caption_text": "Day 5 was the biggest breakthrough: zero cloud fees for voiceovers.",
            },
            {
                "tts_text": "First we paired Handy, a free offline speech to text app, to dictate scripts three times faster.",
                "caption_text": "First we paired Handy, an offline speech-to-text app, to dictate 3× faster.",
            },
            {
                "tts_text": "Then we set up OmniVoice locally on Mac to clone voices from just ten second clips.",
                "caption_text": "Then we ran OmniVoice locally on Mac to clone voices from 10s clips.",
            },
            {
                "tts_text": "In fact, the voice you are listening to right now is my own ten second clone speaking English.",
                "caption_text": "In fact, this voice right now is my own 10s clone speaking English.",
            },
            {
                "tts_text": "Same voice model, both English and Bangla, running 100 percent offline with zero monthly API bills.",
                "caption_text": "Same model, English & Bangla, running 100% offline with zero monthly bills.",
            },
            {
                "tts_text": "In the final part five, I will show you the full five day blueprint so you can build this too.",
                "caption_text": "In Part 5, I will share the full 5-day blueprint so you can build this too.",
            },
        ],
    },
    5: {
        "prefix": "story_part5_en",
        "lines": [
            {
                "tts_text": "Five days, one five dollar Antigravity student plan, and here is everything we built.",
                "caption_text": "5 days, one $5 Antigravity Student plan—here is everything we built.",
            },
            {
                "tts_text": "A 3D HyperFrames animation engine, automated viral reference analysis, and real layered sound design.",
                "caption_text": "A 3D HyperFrames engine, automated reference analysis, and layered sound design.",
            },
            {
                "tts_text": "Product launch reels, university event promos, and local offline voice cloning in two languages.",
                "caption_text": "Product reels, university event promos, and offline voice cloning in 2 languages.",
            },
            {
                "tts_text": "All orchestrated inside one AI workspace for less than the price of a single coffee.",
                "caption_text": "All orchestrated in one AI workspace for less than a single coffee.",
            },
            {
                "tts_text": "If you are a student, do not sleep on the five dollar Antigravity offer.",
                "caption_text": "If you are a student, do not sleep on the $5 Antigravity offer.",
            },
            {
                "tts_text": "Comment STUDENT below and I will send you our complete workflow and setup guide.",
                "caption_text": "Comment STUDENT below and I will send you our complete workflow & guide.",
            },
        ],
    },
}


def get_duration(path: str) -> float:
    out = subprocess.check_output(
        [
            "/opt/homebrew/bin/ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            path,
        ],
        text=True,
    ).strip()
    return float(out)


def align_line_words(text: str, line_idx: int, offset: float, dur: float):
    tokens = text.split()
    weights = [max(2, len(t.strip(".,!?;:\"'—"))) for t in tokens]
    total_w = sum(weights) or 1
    pad_start = min(0.05, dur * 0.03)
    usable = max(0.2, dur - pad_start * 2)
    cur = offset + pad_start
    result = []
    for tok, w in zip(tokens, weights):
        wdur = usable * (w / total_w)
        result.append(
            {
                "word": tok,
                "start": round(cur, 3),
                "end": round(cur + wdur, 3),
                "speaker": "Rafi",
                "line_idx": line_idx,
            }
        )
        cur += wdur
    return result


def main():
    local_model_dir = snapshot_download("k2-fsa/OmniVoice", local_files_only=True)
    if not torch.backends.mps.is_available():
        raise RuntimeError(
            "Apple Silicon MPS GPU is not available (e.g. blocked by sandbox). "
            "Run with GPU access enabled so OmniVoice runs on MPS instead of CPU."
        )
    device = "mps"
    print(f"Loading local OmniVoice from {local_model_dir} on {device}...")
    model = OmniVoice.from_pretrained(
        local_model_dir,
        device_map=device,
        dtype=torch.float32,
        load_asr=False,
    )

    print("Building Rafi voice clone prompt...")
    rafi_prompt = model.create_voice_clone_prompt(ref_audio=RAFI_REF, ref_text=RAFI_REF_TEXT)

    for part_num, cfg in PARTS.items():
        prefix = cfg["prefix"]
        lines = cfg["lines"]
        tmp_files = []
        all_words = []
        spans = []
        current_offset = 0.0
        gap = 0.16

        for idx, line in enumerate(lines):
            part_wav = os.path.join(AUDIO_DIR, f"_tmp_{prefix}_{idx}.wav")
            tmp_files.append(part_wav)
            print(f"[Part {part_num}] Synthesizing Rafi line {idx + 1}/{len(lines)}...")
            audios = model.generate(
                text=line["tts_text"],
                language="English",
                voice_clone_prompt=rafi_prompt,
                speed=1.05,
                denoise=True,
            )
            sf.write(part_wav, audios[0], model.sampling_rate)
            dur = get_duration(part_wav)

            line_words = align_line_words(line["caption_text"], idx, current_offset, dur)
            all_words.extend(line_words)
            spans.append(
                {
                    "idx": idx,
                    "speaker": "Rafi",
                    "start": round(current_offset, 3),
                    "end": round(current_offset + dur, 3),
                    "text": line["caption_text"],
                }
            )
            current_offset += dur + gap

        group_id = 0
        in_group = 0
        prev_line = -1
        for w in all_words:
            if w["line_idx"] != prev_line or in_group >= 4:
                if prev_line != -1:
                    group_id += 1
                in_group = 0
                prev_line = w["line_idx"]
            w["group"] = group_id
            in_group += 1

        concat_list = os.path.join(AUDIO_DIR, f"_tmp_{prefix}_list.txt")
        sil_wav = os.path.join(AUDIO_DIR, f"_tmp_{prefix}_sil.wav")
        subprocess.run(
            [
                "/opt/homebrew/bin/ffmpeg",
                "-y",
                "-f",
                "lavfi",
                "-i",
                f"anullsrc=r={model.sampling_rate}:cl=mono",
                "-t",
                str(gap),
                sil_wav,
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        with open(concat_list, "w", encoding="utf-8") as f:
            for i, p in enumerate(tmp_files):
                f.write(f"file '{os.path.abspath(p)}'\n")
                if i < len(tmp_files) - 1:
                    f.write(f"file '{os.path.abspath(sil_wav)}'\n")

        out_mp3 = os.path.join(AUDIO_DIR, f"{prefix}.mp3")
        subprocess.run(
            [
                "/opt/homebrew/bin/ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                concat_list,
                "-af",
                "aresample=44100,loudnorm=I=-16:TP=-1.5:LRA=11",
                "-c:a",
                "libmp3lame",
                "-b:a",
                "192k",
                out_mp3,
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        for p in tmp_files + [sil_wav, concat_list]:
            if os.path.exists(p):
                os.remove(p)

        out_ts = os.path.join(AUDIO_DIR, f"{prefix}.timestamps.json")
        out_spans = os.path.join(AUDIO_DIR, f"{prefix}.spans.json")
        with open(out_ts, "w", encoding="utf-8") as f:
            json.dump(all_words, f, ensure_ascii=False, indent=2)
        with open(out_spans, "w", encoding="utf-8") as f:
            json.dump(spans, f, ensure_ascii=False, indent=2)

        total_dur = get_duration(out_mp3)
        print(f"Done {prefix}.mp3: {total_dur:.2f}s | {len(all_words)} words | {group_id + 1} groups")


if __name__ == "__main__":
    main()
