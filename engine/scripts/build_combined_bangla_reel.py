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
SARA_REF = os.path.join(os.path.dirname(__file__), "../assets/voices/native_sara_ref.wav")
SARA_REF_TEXT = (
    "ভালোবাসা মানে নতুন জিনিস কেনা না, ভালোবাসা মানে প্রথম দিনের ছোট্ট জিনিসটার "
    "ভেতরের যত্নটা আগলে রাখা, সেই ভাঙা কাপে চা-টা তো তুমি ভেবেছিলে?"
)
os.makedirs(AUDIO_DIR, exist_ok=True)

LINES = [
    {
        "speaker": "Rafi",
        "tts_text": "কীবোর্ডে টাইপ করা আর পেইড এ-আই ভয়েস, দুটোই এবার ফ্রি-তে রিপ্লেস করো, তাও একশো পার্সেন্ট অফলাইনে!",
        "caption_text": "কীবোর্ডে টাইপ করা আর পেইড AI ভয়েস—দুটোই এবার ফ্রি-তে রিপ্লেস করো, তাও 100% অফলাইনে!",
    },
    {
        "speaker": "Sara",
        "tts_text": "স্টেপ ওয়ান, হ্যান্ডি! অপশন আর স্পেস চেপে মুখে বলো, হুইসপার বা প্যারাকিট লোকালি সাথে সাথে স্ক্রিপ্ট লিখে দিবে।",
        "caption_text": "স্টেপ 1: Handy! Option + Space চেপে মুখে বলো—Whisper বা Parakeet লোকালি সাথে সাথে স্ক্রিপ্ট লিখে দিবে।",
    },
    {
        "speaker": "Rafi",
        "tts_text": "স্ক্রিপ্ট তো রেডি, এবার ভয়েস-ওভার কীভাবে বানাবে?",
        "caption_text": "স্ক্রিপ্ট তো রেডি, এবার ভয়েসওভার কীভাবে বানাবে?",
    },
    {
        "speaker": "Sara",
        "tts_text": "স্টেপ টু, অমনি-ভয়েস! মাত্র দশ সেকেন্ডের তোমার নিজের ভয়েস ক্লিপ দিয়েই পুরো ভিডিওর বাংলা ভয়েস-ওভার বানিয়ে নাও ম্যাক-এ।",
        "caption_text": "স্টেপ 2: OmniVoice! মাত্র 10 সেকেন্ডের তোমার নিজের ভয়েস ক্লিপ দিয়েই পুরো ভিডিওর বাংলা ভয়েসওভার বানিয়ে নাও Mac-এ।",
    },
    {
        "speaker": "Rafi",
        "tts_text": "মানে হ্যান্ডি দিয়ে তিন গুণ ফাস্ট লেখা, আর অমনি-ভয়েস দিয়ে নিজের ভয়েসে রিলস, কোনো ক্লাউড বা মান্থলি ফি ছাড়াই!",
        "caption_text": "মানে Handy দিয়ে 3× ফাস্ট লেখা, আর OmniVoice দিয়ে নিজের ভয়েসে রিলস—কোনো ক্লাউড বা মান্থলি ফি ছাড়াই!",
    },
    {
        "speaker": "Sara",
        "tts_text": "দুটো টুলের সেটআপ গাইড আর পাইথন স্ক্রিপ্ট একসাথে পেতে নিচে লোকাল কমেন্ট করো!",
        "caption_text": "দুটো টুলের সেটআপ গাইড আর Python স্ক্রিপ্ট একসাথে পেতে নিচে LOCAL কমেন্ট করো!",
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


def align_line_words(text: str, speaker: str, line_idx: int, offset: float, dur: float):
    tokens = text.split()
    weights = [max(2, len(t.strip(".,!?;:\"'।—"))) for t in tokens]
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
                "speaker": speaker,
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

    print(f"Building native Bangla voice clone prompts...")
    clone_prompts = {
        "Rafi": model.create_voice_clone_prompt(ref_audio=RAFI_REF, ref_text=RAFI_REF_TEXT),
        "Sara": model.create_voice_clone_prompt(ref_audio=SARA_REF, ref_text=SARA_REF_TEXT),
    }

    prefix = "combined_bn"
    tmp_files = []
    all_words = []
    spans = []
    current_offset = 0.0
    gap = 0.16

    for idx, line in enumerate(LINES):
        part_wav = os.path.join(AUDIO_DIR, f"_tmp_{prefix}_{idx}.wav")
        tmp_files.append(part_wav)
        print(f"[combined_bn] Synthesizing cloned line {idx + 1}/{len(LINES)} ({line['speaker']})...")
        audios = model.generate(
            text=line["tts_text"],
            language="Bengali",
            voice_clone_prompt=clone_prompts[line["speaker"]],
            speed=1.05,
            denoise=True,
        )
        sf.write(part_wav, audios[0], model.sampling_rate)
        dur = get_duration(part_wav)

        line_words = align_line_words(line["caption_text"], line["speaker"], idx, current_offset, dur)
        all_words.extend(line_words)
        spans.append(
            {
                "idx": idx,
                "speaker": line["speaker"],
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
        w["g"] = group_id
        in_group += 1

    silence_wav = os.path.join(AUDIO_DIR, f"_tmp_{prefix}_silence.wav")
    subprocess.run(
        [
            "/opt/homebrew/bin/ffmpeg",
            "-v",
            "error",
            "-f",
            "lavfi",
            "-i",
            f"anullsrc=r={model.sampling_rate}:cl=mono",
            "-t",
            str(gap),
            "-y",
            silence_wav,
        ],
        check=True,
    )

    concat_list = os.path.join(AUDIO_DIR, f"_tmp_{prefix}_concat.txt")
    with open(concat_list, "w") as f:
        for idx, p in enumerate(tmp_files):
            f.write(f"file '{p}'\n")
            if idx < len(tmp_files) - 1:
                f.write(f"file '{silence_wav}'\n")

    final_mp3 = os.path.join(AUDIO_DIR, f"{prefix}.mp3")
    subprocess.run(
        [
            "/opt/homebrew/bin/ffmpeg",
            "-v",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            concat_list,
            "-c:a",
            "libmp3lame",
            "-b:a",
            "192k",
            "-y",
            final_mp3,
        ],
        check=True,
    )

    total_dur = get_duration(final_mp3)
    with open(os.path.join(AUDIO_DIR, f"{prefix}.timestamps.json"), "w") as f:
        json.dump(all_words, f, indent=2, ensure_ascii=False)
    with open(os.path.join(AUDIO_DIR, f"{prefix}.spans.json"), "w") as f:
        json.dump(spans, f, indent=2, ensure_ascii=False)

    for p in tmp_files + [silence_wav, concat_list]:
        if os.path.exists(p):
            os.remove(p)

    print(f"[combined_bn] Built {final_mp3} ({total_dur:.2f}s), {len(all_words)} words, {group_id + 1} groups")


if __name__ == "__main__":
    main()
