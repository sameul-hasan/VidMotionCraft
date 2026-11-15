import json
import os
import subprocess
import soundfile as sf
import torch
from huggingface_hub import snapshot_download
from omnivoice import OmniVoice

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "../assets/audio")
SIRI_REF = os.path.join(os.path.dirname(__file__), "../assets/voices/native_siri_ref.wav")
os.makedirs(AUDIO_DIR, exist_ok=True)

LINES = [
    {
        "speaker": "Siri",
        "tts_text": "কোনো ভিডিও এডিটর ছাড়াই, শুধু কোড দিয়ে এই পুরো থ্রি-ডি রিলসটা কীভাবে বানানো হয়েছে দেখবে?",
        "caption_text": "কোনো Video Editor ছাড়াই, শুধু Code দিয়ে এই পুরো 3D রিলসটা কীভাবে বানানো হলো?",
    },
    {
        "speaker": "Siri",
        "tts_text": "প্রথমে এ-আই ভাইরাল ভিডিওর পেসিং আর ফ্রেম অ্যানালাইসিস করে একদম নিখুঁত বাংলা স্ক্রিপ্ট লেখে।",
        "caption_text": "প্রথমে AI ভাইরাল ভিডিওর pacing ও frame বিশ্লেষণ করে বাংলা Script লেখে।",
    },
    {
        "speaker": "Siri",
        "tts_text": "এরপর মাত্র দশ সেকেন্ডের একটা অডিও ক্লিপ থেকে সরাসরি আমার ম্যাক-এ অফলাইন বাংলা ভয়েস তৈরি হয়!",
        "caption_text": "এরপর মাত্র 10s অডিও ক্লিপ থেকে সরাসরি Mac-এ offline Bangla voice তৈরি হয়!",
    },
    {
        "speaker": "Siri",
        "tts_text": "তারপর থ্রি-ডি কার্ড, স্মুথ জি-স্যাপ অ্যানিমেশন আর প্রতিটা শব্দের সাথে সিংক করা ক্যাপশন কোড করা হয়।",
        "caption_text": "তারপর 3D কার্ড, smooth GSAP animation আর word-synced caption কোড হয়।",
    },
    {
        "speaker": "Siri",
        "tts_text": "শেষে রিয়েল সাউন্ড ইফেক্টস মিক্স করে একদম ক্রিস্প টেন-এইটি-পি ভিডিও হিসেবে রেন্ডার হয়ে যায়!",
        "caption_text": "শেষে real SFX মিক্স করে একদম crisp 1080p MP4 ভিডিও রেন্ডার হয়ে যায়!",
    },
    {
        "speaker": "Siri",
        "tts_text": "একশো পার্সেন্ট অটোমেটেড এই ভিডিও ইঞ্জিনটা তুমিও চাইলে ব্যবহার করতে পারো, পুরো গাইড পেতে নিচে কোড কমেন্ট করো!",
        "caption_text": "100% Automated এই Video Engine-এর পুরো গাইড পেতে নিচে CODE কমেন্ট করো!",
    },
]


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
                "speaker": "Siri",
                "line_idx": line_idx,
            }
        )
        cur += wdur
    return result


def main():
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
        load_asr=True,
    )

    print("Building Siri voice clone prompt...")
    siri_prompt = model.create_voice_clone_prompt(ref_audio=SIRI_REF)

    prefix = "siri_making_of_bn"
    tmp_files = []
    all_words = []
    spans = []
    current_offset = 0.0
    gap = 0.16

    for idx, line in enumerate(LINES):
        part_wav = os.path.join(AUDIO_DIR, f"_tmp_{prefix}_{idx}.wav")
        tmp_files.append(part_wav)
        print(f"[{prefix}] Synthesizing Siri line {idx + 1}/{len(LINES)} on {device}...")
        audios = model.generate(
            text=line["tts_text"],
            language="Bengali",
            voice_clone_prompt=siri_prompt,
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
                "speaker": "Siri",
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
