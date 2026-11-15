import json
import os
import subprocess
import numpy as np
import soundfile as sf
import torch
from huggingface_hub import snapshot_download
from omnivoice import OmniVoice

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "../assets/audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

VOICES = {
    "Rafi": "male, young adult, moderate pitch",
    "Riya": "female, young adult, moderate pitch",
}

SCRIPTS = {
    "en": {
        "language": "English",
        "lines": [
            {
                "speaker": "Rafi",
                "text": "Wait, you are still paying monthly subscriptions just to clone your own voice for reels?",
            },
            {
                "speaker": "Riya",
                "text": "Not anymore. Meet OmniVoice, an open-source voice cloning model from k2-fsa that runs 100 percent locally on your Mac.",
            },
            {
                "speaker": "Rafi",
                "text": "Hold on, how much audio does it actually need to sound like me?",
            },
            {
                "speaker": "Riya",
                "text": "Just a 5 to 15 second mic clip. Load OmniVoice in Python on Apple Silicon MPS, pass your text, and it clones your exact tone.",
            },
            {
                "speaker": "Rafi",
                "text": "And it works across 600 plus languages with zero API limits?",
            },
            {
                "speaker": "Riya",
                "text": "Zero limits and zero cloud uploads. Want the exact Python script to run it on your Mac? Comment OMNI below.",
            },
        ],
    },
    "bn": {
        "language": "Bengali",
        "lines": [
            {
                "speaker": "Rafi",
                "text": "ভাই, তুমি কি এখনো রিলসের ভয়েসওভারের জন্য প্রতি মাসে ডলার দিয়ে এআই সাবস্ক্রিপশন কিনছো?",
            },
            {
                "speaker": "Riya",
                "text": "একদম দরকার নাই। এটা হলো OmniVoice, একটা ওপেন-সোর্স ভয়েস ক্লোনিং মডেল, যা তোমার Mac এই ১০০ পার্সেন্ট অফলাইন রান হয়।",
            },
            {
                "speaker": "Rafi",
                "text": "আমার নিজের ভয়েস ক্লোন করতে কতক্ষণের অডিও ক্লিপ লাগবে?",
            },
            {
                "speaker": "Riya",
                "text": "মাত্র ৫ থেকে ১৫ সেকেন্ডের একটা ক্লিপ! Python এ Apple Silicon MPS দিয়ে OmniVoice রান করলেই তোমার এক্স্যাক্ট টোনে ভয়েস রেডি।",
            },
            {
                "speaker": "Rafi",
                "text": "মানে ৬০০ প্লাস ল্যাঙ্গুয়েজ সাপোর্ট আর কোনো API লিমিট বা প্রাইভেসি রিস্ক নাই?",
            },
            {
                "speaker": "Riya",
                "text": "কোনো লিমিট নাই, সব লোকাল। তোমার Mac এ সেটআপ করার Python স্ক্রিপ্ট লাগলে নিচে OMNI কমেন্ট করো!",
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


def try_load_whisper():
    try:
        from faster_whisper import WhisperModel
        return WhisperModel("small", device="cpu", compute_type="int8", local_files_only=True)
    except Exception as e:
        print(f"Whisper local cache not available ({e}); using proportional line word timing.")
        return None


def align_line_words(whisper_model, wav_path: str, text: str, speaker: str, line_idx: int, offset: float, dur: float, lang_code: str):
    tokens = text.split()
    if whisper_model is not None:
        try:
            segs, _ = whisper_model.transcribe(wav_path, language=lang_code, word_timestamps=True, vad_filter=False)
            w_list = []
            for seg in segs:
                if not seg.words:
                    continue
                for w in seg.words:
                    t = w.word.strip()
                    if t:
                        w_list.append({
                            "word": t,
                            "start": round(float(w.start) + offset, 3),
                            "end": round(float(w.end) + offset, 3),
                            "speaker": speaker,
                            "line_idx": line_idx,
                        })
            if len(w_list) >= max(2, len(tokens) // 2):
                return w_list
        except Exception:
            pass

    # Fallback: weight each word by character length across the synthesized line duration
    weights = [max(2, len(t.strip(".,!?;:\"'।"))) for t in tokens]
    total_w = sum(weights) or 1
    pad_start = min(0.05, dur * 0.03)
    usable = max(0.2, dur - pad_start * 2)
    cur = offset + pad_start
    result = []
    for tok, w in zip(tokens, weights):
        wdur = usable * (w / total_w)
        result.append({
            "word": tok,
            "start": round(cur, 3),
            "end": round(cur + wdur, 3),
            "speaker": speaker,
            "line_idx": line_idx,
        })
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
    whisper_model = try_load_whisper()

    for lang, cfg in SCRIPTS.items():
        prefix = f"omnivoice_{lang}"
        tmp_files = []
        all_words = []
        spans = []
        current_offset = 0.0
        gap = 0.16
        lang_code = "en" if lang == "en" else "bn"

        for idx, line in enumerate(cfg["lines"]):
            part_wav = os.path.join(AUDIO_DIR, f"_tmp_{prefix}_{idx}.wav")
            tmp_files.append(part_wav)
            print(f"[{lang}] Synthesizing line {idx + 1}/{len(cfg['lines'])} ({line['speaker']})...")
            audios = model.generate(
                text=line["text"],
                language=cfg["language"],
                instruct=VOICES[line["speaker"]],
                speed=1.05,
            )
            sf.write(part_wav, audios[0], model.sampling_rate)
            dur = get_duration(part_wav)

            line_words = align_line_words(
                whisper_model, part_wav, line["text"], line["speaker"], idx, current_offset, dur, lang_code
            )
            all_words.extend(line_words)
            spans.append({
                "idx": idx,
                "speaker": line["speaker"],
                "start": round(current_offset, 3),
                "end": round(current_offset + dur, 3),
                "text": line["text"],
            })
            current_offset += dur + gap

        # Assign 4-word caption group IDs
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

        print(f"[{lang}] Built {final_mp3} ({total_dur:.2f}s), {len(all_words)} words, {group_id + 1} groups")


if __name__ == "__main__":
    main()
