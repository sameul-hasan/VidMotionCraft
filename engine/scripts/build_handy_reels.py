import json
import os
import subprocess
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
                "text": "I stopped typing long AI prompts by hand, and it made my workflow three times faster.",
            },
            {
                "speaker": "Riya",
                "text": "That is Handy, a free open-source offline speech to text app for Mac, Windows, and Linux.",
            },
            {
                "speaker": "Rafi",
                "text": "So I do not even have to switch windows or open a browser?",
            },
            {
                "speaker": "Riya",
                "text": "Nope. Press Option plus Space in your editor, notes, or chat. Handy runs Whisper or Parakeet locally and pastes clean text instantly.",
            },
            {
                "speaker": "Rafi",
                "text": "Wait, does it click buttons on my screen too, or just type?",
            },
            {
                "speaker": "Riya",
                "text": "Pure ultra-fast dictation with zero monthly fees. Want the download link and setup guide? Comment HANDY below.",
            },
        ],
    },
    "bn": {
        "language": "Bengali",
        "lines": [
            {
                "speaker": "Rafi",
                "text": "আমি বড় বড় AI প্রম্পট আর স্ক্রিপ্ট হাতে টাইপ করা বন্ধ করে দিয়েছি, ওয়ার্কফ্লো এখন তিন গুণ ফাস্ট!",
            },
            {
                "speaker": "Riya",
                "text": "এটার নাম Handy, একটা ফ্রি ওপেন-সোর্স অফলাইন ভয়েস টু টেক্সট অ্যাপ, যেটা Wispr Flow এর সেরা লোকাল অল্টারনেটিভ।",
            },
            {
                "speaker": "Rafi",
                "text": "মানে আমার কোনো ব্রাউজার বা আলাদা অ্যাপ ওপেন করতে হবে না?",
            },
            {
                "speaker": "Riya",
                "text": "না! এডিটর বা চ্যাটে গিয়ে শুধু Option plus Space চাপো। Handy লোকাল Whisper বা Parakeet মডেল দিয়ে সাথে সাথে টেক্সট পেস্ট করে দিবে।",
            },
            {
                "speaker": "Rafi",
                "text": "আর কোনো অডিও ক্লাউডে আপলোড হয় না, আর মান্থলি সাবস্ক্রিপশনও নাই?",
            },
            {
                "speaker": "Riya",
                "text": "একদম ফ্রি আর প্রাইভেট। Handy এর ডাউনলোড লিংক আর সেটআপ গাইড চাইলে নিচে HANDY কমেন্ট করো!",
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
    except Exception:
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
        prefix = f"handy_{lang}"
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
