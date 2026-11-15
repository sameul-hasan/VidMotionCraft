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
        "tts_text": "Stop typing long prompts by hand and stop paying monthly for AI voiceovers. Replace both 100 percent offline for free.",
        "caption_text": "Stop typing long prompts by hand and stop paying monthly for AI voiceovers—replace both 100% offline for free.",
    },
    {
        "speaker": "Sara",
        "tts_text": "Step one: Handy. Hit Option plus Space and just speak. Whisper or Parakeet transcribes locally and types your script instantly.",
        "caption_text": "Step 1: Handy! Hit Option + Space and speak—Whisper or Parakeet transcribes locally and types your script instantly.",
    },
    {
        "speaker": "Rafi",
        "tts_text": "Okay, the script is ready. What about the voiceover?",
        "caption_text": "Okay, the script is ready. What about the voiceover?",
    },
    {
        "speaker": "Sara",
        "tts_text": "Step two: OmniVoice. Use a 10 second clip of your own voice and generate the entire reel voiceover locally on your Mac.",
        "caption_text": "Step 2: OmniVoice! Use a 10s clip of your own voice and generate the entire reel voiceover locally on your Mac.",
    },
    {
        "speaker": "Rafi",
        "tts_text": "So three times faster writing with Handy, plus my own cloned voice with OmniVoice, with zero cloud uploads or monthly fees.",
        "caption_text": "So 3× faster writing with Handy, plus my own cloned voice with OmniVoice—zero cloud uploads or monthly fees.",
    },
    {
        "speaker": "Sara",
        "tts_text": "Want the setup guide and Python script for both tools? Comment LOCAL below.",
        "caption_text": "Want the setup guide and Python script for both tools? Comment LOCAL below.",
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

    print("Building cross-lingual voice clone prompts for Rafi and Sara...")
    clone_prompts = {
        "Rafi": model.create_voice_clone_prompt(ref_audio=RAFI_REF, ref_text=RAFI_REF_TEXT),
        "Sara": model.create_voice_clone_prompt(ref_audio=SARA_REF, ref_text=SARA_REF_TEXT),
    }

    prefix = "combined_en"
    tmp_files = []
    all_words = []
    spans = []
    current_offset = 0.0
    gap = 0.16

    for idx, line in enumerate(LINES):
        part_wav = os.path.join(AUDIO_DIR, f"_tmp_{prefix}_{idx}.wav")
        tmp_files.append(part_wav)
        print(f"[combined_en] Synthesizing cloned line {idx + 1}/{len(LINES)} ({line['speaker']})...")
        audios = model.generate(
            text=line["tts_text"],
            language="English",
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

    print(f"[combined_en] Built {final_mp3} ({total_dur:.2f}s), {len(all_words)} words, {group_id + 1} groups")


if __name__ == "__main__":
    main()
