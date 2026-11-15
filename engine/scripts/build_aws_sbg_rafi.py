import argparse
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

SCRIPTS = {
    "en": {
        "language": "English",
        "prefix": "aws_sbg_rafi_en",
        "lines": [
            {
                "tts_text": "Everyone at Daffodil wants cloud skills, but watching ten hour tutorials alone gets you nowhere.",
                "caption_text": "Everyone at Daffodil wants cloud skills, but solo tutorials get you nowhere.",
            },
            {
                "tts_text": "That is why the official A W S Student Builder Group is now live at Daffodil International University.",
                "caption_text": "That is why AWS Student Builder Group is now live at DIU!",
            },
            {
                "tts_text": "Forget boring slideshows. Inside S B G D I U, you deploy real cloud servers, databases, and serverless apps.",
                "caption_text": "Forget boring slides. Deploy real cloud servers, databases, and serverless apps.",
            },
            {
                "tts_text": "Even if you have never opened the A W S console, senior builders mentor you through hands on labs and hackathons.",
                "caption_text": "Never touched AWS? Senior builders mentor you in hands-on labs & hackathons.",
            },
            {
                "tts_text": "You build production projects, earn A W S certifications, and stand out before you even graduate.",
                "caption_text": "Build production projects, earn AWS certifications, and stand out before graduating.",
            },
            {
                "tts_text": "Ready to build for real? Follow A W S S B G D I U and grab your seat at the next meetup!",
                "caption_text": "Ready to build? Follow AWS SBG DIU and grab your meetup seat!",
            },
        ],
    },
    "bn": {
        "language": "Bengali",
        "prefix": "aws_sbg_rafi_bn",
        "lines": [
            {
                "tts_text": "ভাই, শুধু ইউটিউব টিউটোরিয়াল দেখে কি আসলেই ক্লাউড ইঞ্জিনিয়ার হওয়া যায়?",
                "caption_text": "ভাই, শুধু YouTube টিউটোরিয়াল দেখে কি আসলেই Cloud Engineer হওয়া যায়?",
            },
            {
                "tts_text": "একদমই না! আর সেজন্যই ড্যাফোডিলে এখন অফিশিয়ালি শুরু হয়েছে এ-ডব্লিউ-এস স্টুডেন্ট বিল্ডার গ্রুপ।",
                "caption_text": "একদমই না! সেজন্যই DIU-তে শুরু হয়েছে অফিশিয়াল AWS Student Builder Group!",
            },
            {
                "tts_text": "এখানে কোনো বোরিং স্লাইড না, আমরা সরাসরি লাইভ ক্লাউড সার্ভার, ডেটাবেস আর রিয়েল প্রজেক্ট ডিপ্লয় করি।",
                "caption_text": "কোনো বোরিং স্লাইড না—সরাসরি লাইভ Cloud সার্ভার, Database আর রিয়েল প্রজেক্ট ডিপ্লয়!",
            },
            {
                "tts_text": "আগে কখনো এ-ডব্লিউ-এস না ছুঁয়ে থাকলেও কোনো টেনশন নাই, ক্যাম্পাসের সিনিয়র বিল্ডাররা হাতে-কলমে শেখাবে।",
                "caption_text": "আগে AWS না ছুঁয়ে থাকলেও টেনশন নাই—সিনিয়র বিল্ডাররা হাতে-কলমে শেখাবে!",
            },
            {
                "tts_text": "ল্যাব সেশন, হ্যাকাথন আর এ-ডব্লিউ-এস সার্টিফিকেশন, সব মিলে গ্র্যাজুয়েশনের আগেই সিভি হবে প্রো লেভেলের!",
                "caption_text": "ল্যাব, হ্যাকাথন আর AWS Certification—গ্র্যাজুয়েশনের আগেই হবে Pro-লেভেল CV!",
            },
            {
                "tts_text": "তাই আর দেরি কেন? এ-ডব্লিউ-এস এস-বি-জি ডি-আই-ইউ পেজ ফলো করো, আর নেক্সট মিটআপে সিট বুক করে ফেলো!",
                "caption_text": "দেরি কেন? AWS SBG DIU ফলো করো আর Next Meetup-এ সিট বুক করো!",
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", choices=["en", "bn", "all"], default="all")
    args = parser.parse_args()

    if not torch.backends.mps.is_available():
        raise RuntimeError(
            "Apple Silicon MPS GPU is not available (e.g. blocked by sandbox). "
            "Run with GPU access enabled so OmniVoice runs on MPS instead of CPU."
        )
    device = "mps"
    local_model_dir = snapshot_download("k2-fsa/OmniVoice", local_files_only=True)
    print(f"Loading local OmniVoice from {local_model_dir} on {device}...")
    model = OmniVoice.from_pretrained(
        local_model_dir,
        device_map=device,
        dtype=torch.float32,
        load_asr=False,
    )

    print("Building Rafi voice clone prompt...")
    rafi_prompt = model.create_voice_clone_prompt(ref_audio=RAFI_REF, ref_text=RAFI_REF_TEXT)

    for lang_key, cfg in SCRIPTS.items():
        if args.lang != "all" and lang_key != args.lang:
            continue
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
            print(f"[{lang_key}] Synthesizing Rafi line {idx + 1}/{len(lines)} on {device}...")
            audios = model.generate(
                text=line["tts_text"],
                language=cfg["language"],
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

        # 3 words per group so bigger captions fit cleanly on 1080px width!
        group_id = 0
        in_group = 0
        prev_line = -1
        for w in all_words:
            if w["line_idx"] != prev_line or in_group >= 3:
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
