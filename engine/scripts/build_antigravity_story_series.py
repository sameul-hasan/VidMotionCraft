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
                "tts_text": "What if just five dollars could open the door to a completely different way of building software? I wanted to find out.",
                "caption_text": "What if just $5 could open a completely different way of building software? I wanted to find out.",
            },
            {
                "tts_text": "It started with the Antigravity Student Offer. But I didn't want to stop at getting access. I wanted to explore what I could actually build with it.",
                "caption_text": "It started with the Antigravity Student Offer—exploring what I could actually build with it.",
            },
            {
                "tts_text": "So, I started setting up my development environment, exploring Ubuntu, working with terminals, configuring AI models, and experimenting with OpenCode.",
                "caption_text": "Setting up my environment: exploring Ubuntu, terminals, AI models, and OpenCode.",
            },
            {
                "tts_text": "Every setup, every command, every experiment taught me something new. And this was just the beginning.",
                "caption_text": "Every setup, command, and experiment taught me something new. And this was just the beginning.",
            },
            {
                "tts_text": "Because the next challenge wasn't about installing tools. It was about turning ideas into actual products.",
                "caption_text": "Because the next challenge wasn't installing tools—it was turning ideas into actual products.",
            },
            {
                "tts_text": "Next: What happens when ideas become real products?",
                "caption_text": "Next: What happens when ideas become real products?",
            },
        ],
    },
    2: {
        "prefix": "story_part2_en",
        "lines": [
            {
                "tts_text": "Having powerful AI tools is exciting. But here's the real question: can you turn an idea into something people can actually use?",
                "caption_text": "Having powerful AI tools is exciting—but can you turn an idea into something people actually use?",
            },
            {
                "tts_text": "That's where things got interesting. I started exploring Aayojon three D and working through the concept of an event management SaaS platform.",
                "caption_text": "I started exploring Aayojon 3D and working through an event management SaaS platform.",
            },
            {
                "tts_text": "Not just the interface. The bigger picture. Product requirements, system architecture, A P Is, database design, and user experience.",
                "caption_text": "Not just the interface—product requirements, system architecture, APIs, database design, and UX.",
            },
            {
                "tts_text": "I began breaking big ideas into smaller, buildable pieces. Because a professional product isn't just about how it looks.",
                "caption_text": "Breaking big ideas into buildable pieces—because a product isn't just about how it looks.",
            },
            {
                "tts_text": "It's about how everything works together. And then, my attention shifted from building products to something much bigger: the cloud.",
                "caption_text": "It's about how everything works together. Then my attention shifted to something bigger: the cloud.",
            },
            {
                "tts_text": "Next: Taking development beyond the local machine.",
                "caption_text": "Next: Taking development beyond the local machine.",
            },
        ],
    },
    3: {
        "prefix": "story_part3_en",
        "lines": [
            {
                "tts_text": "Building software is one thing. But making technology accessible, scalable, and useful is another.",
                "caption_text": "Building software is one thing. Making technology accessible, scalable, and useful is another.",
            },
            {
                "tts_text": "During these days, I also explored the world of A W S and cloud technology.",
                "caption_text": "During these days, I also explored the world of AWS and cloud technology.",
            },
            {
                "tts_text": "I worked on promotional content for A W S Student Build and Grow at D I U, focusing on cloud computing, DevOps, and opportunities for students to get involved.",
                "caption_text": "Creating promos for AWS Student Build & Grow at DIU—cloud computing, DevOps, and student opportunities.",
            },
            {
                "tts_text": "It reminded me of something important. Technology becomes more powerful when knowledge is shared and communities grow together.",
                "caption_text": "Technology becomes more powerful when knowledge is shared and communities grow together.",
            },
            {
                "tts_text": "From local development environments to cloud infrastructure, I was beginning to see a much bigger picture. But my next experiment would take me somewhere unexpected.",
                "caption_text": "From local environments to cloud infrastructure—my next experiment took me somewhere unexpected.",
            },
            {
                "tts_text": "Into research, datasets, and railway simulation. Next: What if software development meets the real world?",
                "caption_text": "Into research, datasets, and railway simulation. What if development meets the real world?",
            },
        ],
    },
    4: {
        "prefix": "story_part4_en",
        "lines": [
            {
                "tts_text": "Not every developer experiment starts with an app. Sometimes, it starts with a research question.",
                "caption_text": "Not every developer experiment starts with an app. Sometimes, it starts with a research question.",
            },
            {
                "tts_text": "I began exploring S O S DaR twenty four, a railway-related dataset, and the possibilities of generating and reconstructing railway simulation data.",
                "caption_text": "I began exploring SOSDaR24, a railway dataset, and reconstructing railway simulation data.",
            },
            {
                "tts_text": "That led me toward a bigger idea: RailSim Dataset Generator. I started exploring CARLA, Ubuntu twenty two point oh four, G P U requirements, and how a simulation-based workflow could come together.",
                "caption_text": "That led to RailSim Dataset Generator—exploring CARLA, Ubuntu 22.04, and GPU requirements.",
            },
            {
                "tts_text": "There was a lot to understand before writing the first real implementation. But that's what makes research exciting.",
                "caption_text": "There was a lot to understand before writing code—but that's what makes research exciting.",
            },
            {
                "tts_text": "You don't always know the final answer when you begin. Sometimes, the most important step is discovering what's possible.",
                "caption_text": "You don't always know the final answer—the most important step is discovering what's possible.",
            },
            {
                "tts_text": "And now, it was time to bring all these experiments together into one creative workflow. Next: Bringing everything together.",
                "caption_text": "Now it was time to bring all these experiments together. Next: Bringing everything together.",
            },
        ],
    },
    5: {
        "prefix": "story_part5_en",
        "lines": [
            {
                "tts_text": "Five days. So many experiments. And one final question. What if I could build my own creative workflow?",
                "caption_text": "Five days. Countless experiments. What if I could build my own AI creative workflow?",
            },
            {
                "tts_text": "I explored Handy for voice dictation and OmniVoice for local voice synthesis. I experimented with custom voice profiles and started bringing everything together with VidMotionCraft.",
                "caption_text": "Exploring Handy dictation, OmniVoice local synthesis, and bringing it together with VidMotionCraft.",
            },
            {
                "tts_text": "H T M L based compositions, G S A P animations, HyperFrames, synchronized captions, sound effects, and automated video rendering. Even this five-part series became part of that experiment.",
                "caption_text": "HTML compositions, GSAP animations, HyperFrames, synced captions, SFX, and automated rendering.",
            },
            {
                "tts_text": "Instead of simply using AI to create content, I wanted to understand the workflow behind creating it. And that's what these five days were really about.",
                "caption_text": "Instead of just using AI, I wanted to build the workflow behind it.",
            },
            {
                "tts_text": "AI doesn't replace developers. It gives developers new ways to think, create, and build. This is what happens when students stop waiting for the future and start building it.",
                "caption_text": "AI doesn't replace developers—it gives developers new ways to think, create, and build.",
            },
            {
                "tts_text": "And this is only the beginning. Follow along. There's much more to build.",
                "caption_text": "This is only the beginning. Follow the journey—there's much more to build.",
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
        gap = 0.14

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
            audio_np = audios[0].detach().cpu().numpy() if hasattr(audios[0], "detach") else audios[0]
            sf.write(part_wav, audio_np.squeeze(), model.sampling_rate)
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
