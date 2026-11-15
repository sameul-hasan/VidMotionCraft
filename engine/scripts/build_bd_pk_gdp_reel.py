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
        "speaker": "Bangladesh",
        "voice": "Rafi",
        "chapter": "1971: FREEDOM & INDEPENDENCE",
        "tts_text": "In nineteen seventy one, Bangladesh won its freedom from Pakistan after a brutal liberation war.",
        "caption_text": "In 1971, Bangladesh won its freedom from Pakistan after a brutal war.",
    },
    {
        "speaker": "Pakistan",
        "voice": "Sara",
        "chapter": "1971: WAR-TORN START",
        "tts_text": "Back then, my economy was ten point seven billion dollars, while you started war torn at just nine billion.",
        "caption_text": "Back then, my GDP was $10.7B, while you started war-torn at $9B.",
    },
    {
        "speaker": "Pakistan",
        "voice": "Sara",
        "chapter": "2000: PAKISTAN LEADS 2X",
        "tts_text": "By two thousand, I reached ninety nine point five billion dollars, nearly double your fifty four point seven billion!",
        "caption_text": "By 2000, I hit $99.5B—nearly double your $54.7B!",
    },
    {
        "speaker": "Bangladesh",
        "voice": "Rafi",
        "chapter": "WHAT CHANGED IN DHAKA?",
        "tts_text": "Instead of giving up, I built a global garment export engine, scaled microfinance, and empowered women workers.",
        "caption_text": "So I built global garment exports, microfinance, and empowered women workers.",
    },
    {
        "speaker": "Pakistan",
        "voice": "Sara",
        "chapter": "2020: THE CROSSOVER",
        "tts_text": "Wait, in twenty twenty, how did a country that broke away from me actually overtake my G D P?!",
        "caption_text": "Wait—in 2020, how did you actually overtake my GDP?!",
    },
    {
        "speaker": "Bangladesh",
        "voice": "Rafi",
        "chapter": "2020–2025: PULLING AHEAD",
        "tts_text": "By twenty twenty five, my economy hit four hundred fifty six billion dollars, while you stood at four hundred seven billion.",
        "caption_text": "By 2025, I reached $456B, while you stood at $407B.",
    },
    {
        "speaker": "Bangladesh",
        "voice": "Rafi",
        "chapter": "2026: PER CAPITA GAP",
        "tts_text": "And per person in twenty twenty six, I average two thousand eight hundred ninety dollars, versus around one thousand seven hundred for you.",
        "caption_text": "And per person in 2026, I'm ~$2,890 vs ~$1,700 for you.",
    },
    {
        "speaker": "Pakistan",
        "voice": "Sara",
        "chapter": "THE 2026 REALITY CHECK",
        "tts_text": "Even the I M F projects you at five hundred six billion in twenty twenty six, while I am near four hundred fifty one billion.",
        "caption_text": "IMF projects you at $506B in 2026, while I'm near $451B.",
    },
    {
        "speaker": "Bangladesh",
        "voice": "Rafi",
        "chapter": "1971 → 2026 LESSON",
        "tts_text": "From a war torn nation in nineteen seventy one to five hundred billion plus. Follow for more data stories!",
        "caption_text": "From war-torn in 1971 to $500B+ in 2026. Follow for more!",
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

    print("Building Rafi (Bangladesh) & Sara (Pakistan) voice clone prompts...")
    clone_prompts = {
        "Rafi": model.create_voice_clone_prompt(ref_audio=RAFI_REF, ref_text=RAFI_REF_TEXT),
        "Sara": model.create_voice_clone_prompt(ref_audio=SARA_REF, ref_text=SARA_REF_TEXT),
    }

    prefix = "bd_pk_gdp_en"
    tmp_files = []
    all_words = []
    spans = []
    current_offset = 0.0
    gap = 0.16

    for idx, line in enumerate(LINES):
        part_wav = os.path.join(AUDIO_DIR, f"_tmp_{prefix}_{idx}.wav")
        tmp_files.append(part_wav)
        print(f"[{prefix}] Synthesizing line {idx + 1}/{len(LINES)} ({line['speaker']} / {line['voice']}) on {device}...")
        audios = model.generate(
            text=line["tts_text"],
            language="English",
            voice_clone_prompt=clone_prompts[line["voice"]],
            speed=1.06,
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
                "chapter": line["chapter"],
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
