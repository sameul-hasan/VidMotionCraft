import json
import os
import subprocess
import soundfile as sf
import torch
from huggingface_hub import snapshot_download
from omnivoice import OmniVoice

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "../assets/audio")
SAKAL_REF = os.path.join(os.path.dirname(__file__), "../assets/voices/native_sakal_ref.wav")
os.makedirs(AUDIO_DIR, exist_ok=True)

LINES = [
    {
        "speaker": "Sakal",
        "tts_text": "In eastern India lies Bihar, sharing borders with Uttar Pradesh to the west, Jharkhand to the south, West Bengal to the east, and Nepal to the north.",
        "caption_text": "In eastern India lies Bihar, sharing borders with Uttar Pradesh, Jharkhand, West Bengal, and Nepal.",
    },
    {
        "speaker": "Sakal",
        "tts_text": "Home to over one hundred and thirty million people, its population is roughly eighty two percent Hindu and seventeen percent Muslim, alongside other communities.",
        "caption_text": "Home to over 130 million people, roughly 82% Hindu and 17% Muslim, alongside other communities.",
    },
    {
        "speaker": "Sakal",
        "tts_text": "With an economy around one hundred and thirty billion dollars, Bihar is famous for over a dozen G-I tagged products, from Madhubani art to Shahi Litchi.",
        "caption_text": "With a $130 Billion GDP, Bihar is famous for GI-tagged Madhubani art and Shahi Litchi.",
    },
    {
        "speaker": "Sakal",
        "tts_text": "From the sub-Himalayan Shiwalik hills to twelve wildlife sanctuaries, its state bird is the House Sparrow.",
        "caption_text": "From the Sub-Himalayan Shiwalik hills to 12 wildlife sanctuaries, its state bird is the House Sparrow.",
    },
    {
        "speaker": "Sakal",
        "tts_text": "Infrastructurally, new expressways and bridges are rapidly connecting every corner of the state.",
        "caption_text": "Infrastructurally, new expressways and bridges are rapidly connecting every corner of Bihar.",
    },
    {
        "speaker": "Sakal",
        "tts_text": "And historically, this is the land of Chanakya, Emperor Ashoka, and ancient Nalanda. Follow for more daily geo stories!",
        "caption_text": "Historically, this is the land of Chanakya, Emperor Ashoka, and Nalanda. Follow for more!",
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
                "speaker": "Sakal",
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

    print("Building Sakal voice clone prompt...")
    sakal_prompt = model.create_voice_clone_prompt(ref_audio=SAKAL_REF)

    prefix = "sakal_bihar_en"
    tmp_files = []
    all_words = []
    spans = []
    current_offset = 0.0
    gap = 0.16

    for idx, line in enumerate(LINES):
        part_wav = os.path.join(AUDIO_DIR, f"_tmp_{prefix}_{idx}.wav")
        tmp_files.append(part_wav)
        print(f"[{prefix}] Synthesizing Sakal line {idx + 1}/{len(LINES)} on {device}...")
        audios = model.generate(
            text=line["tts_text"],
            language="English",
            voice_clone_prompt=sakal_prompt,
        )
        audio_np = audios[0].detach().cpu().numpy() if hasattr(audios[0], "detach") else audios[0]
        audio_np = audio_np.squeeze()
        sf.write(part_wav, audio_np, 24000)

        dur = get_duration(part_wav)
        spans.append(
            {
                "idx": idx,
                "speaker": "Sakal",
                "start": round(current_offset, 3),
                "end": round(current_offset + dur, 3),
                "text": line["caption_text"],
            }
        )
        all_words.extend(align_line_words(line["caption_text"], idx, current_offset, dur))
        current_offset += dur + gap

    filter_parts = []
    inputs = []
    for i, fpath in enumerate(tmp_files):
        inputs.extend(["-i", fpath])
        if i < len(tmp_files) - 1:
            filter_parts.append(f"[{i}:a]apad=pad_dur={gap}[a{i}]")
        else:
            filter_parts.append(f"[{i}:a]anull[a{i}]")

    concat_inputs = "".join(f"[a{i}]" for i in range(len(tmp_files)))
    filter_complex = (
        ";".join(filter_parts)
        + f";{concat_inputs}concat=n={len(tmp_files)}:v=0:a=1,"
        + "loudnorm=I=-16:TP=-1.5:LRA=11[outa]"
    )

    out_mp3 = os.path.join(AUDIO_DIR, f"{prefix}.mp3")
    cmd = (
        ["/opt/homebrew/bin/ffmpeg", "-y"]
        + inputs
        + [
            "-filter_complex",
            filter_complex,
            "-map",
            "[outa]",
            "-c:a",
            "libmp3lame",
            "-b:a",
            "192k",
            out_mp3,
        ]
    )
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for fpath in tmp_files:
        if os.path.exists(fpath):
            os.remove(fpath)

    # Group words into 3-word chunks
    group_size = 3
    grouped_words = []
    for idx in range(len(LINES)):
        line_words = [w for w in all_words if w["line_idx"] == idx]
        for g_start in range(0, len(line_words), group_size):
            gid = len(grouped_words)
            chunk = line_words[g_start : g_start + group_size]
            for w in chunk:
                w["group_id"] = gid
            grouped_words.append(chunk)

    flat_words = [w for chunk in grouped_words for w in chunk]
    with open(os.path.join(AUDIO_DIR, f"{prefix}.timestamps.json"), "w", encoding="utf-8") as f:
        json.dump(flat_words, f, ensure_ascii=False, indent=2)
    with open(os.path.join(AUDIO_DIR, f"{prefix}.spans.json"), "w", encoding="utf-8") as f:
        json.dump(spans, f, ensure_ascii=False, indent=2)

    final_dur = get_duration(out_mp3)
    print(f"Done {prefix}.mp3: {final_dur:.2f}s | {len(flat_words)} words | {len(grouped_words)} groups")


if __name__ == "__main__":
    main()
