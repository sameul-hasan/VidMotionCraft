# VidMotionCraft

An automated, 100% local **3D Motion-Graphics Vertical Video Engine** (`1080×1920`, `30 fps`) powered by **HyperFrames**, **GSAP**, **OmniVoice (`k2-fsa/OmniVoice`)**, and **FFmpeg** — built to script, voice-clone, animate, sync word-level captions, and render viral short-form reels in English and Bangla.

---

## Features

- **Code-Driven 3D Motion Graphics:** HTML5 + CSS 3D + GSAP timelines compiled into crisp `1080×1920` `30 fps` H.264/AAC MP4s via HyperFrames.
- **Local Zero-Shot Voice Cloning (Apple Silicon MPS GPU):** Uses `k2-fsa/OmniVoice` to synthesize natural English and Bangla voiceovers from 10-second reference clips.
- **Dual-Track Bangla TTS + Caption Sync:** Phonetic Bangla `tts_text` for natural pronunciation paired with clean `caption_text` (preserving English/numbers) and word-level highlighted captions.
- **Real Map & Infographic Support:** GeoJSON-to-SVG regional maps, animated charts, code/terminal cards, and layered real SFX (`whoosh`, `pop`, `click`, `chime`, `impact`).

## Finalized Voice Cast (`engine/assets/voices/`)

- **Rafi** (`native_rafi_ref.wav`) — Male voice
- **Sara** (`native_sara_ref.wav`) — Female voice
- **Riya** (`native_riya_ref.wav`) — Female voice
- **Siri** (`native_siri_ref.wav`) — Narrator voice
- **Sakal** (`native_sakal_ref.wav`) — Male English geo-explainer voice

---

## Prerequisites

- **macOS (Apple Silicon recommended)** for `mps` GPU acceleration with OmniVoice
- **Node.js `22.x`** (see `engine/.nvmrc`)
- **Python `3.11+`**
- **FFmpeg & FFprobe** (`brew install ffmpeg`)
- **Google Chrome** (used by HyperFrames headless renderer)

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/sameul-hasan/VidMotionCraft.git
cd VidMotionCraft/engine
```

### 2. Install Node.js dependencies (HyperFrames)
```bash
npm install
```

### 3. Create Python virtual environment & install dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Generate voiceover, build HTML composition, lint & render
Example (Sakal Bihar geo-explainer reel):
```bash
# 1. Synthesize voiceover & word timestamps on MPS GPU
.venv/bin/python scripts/build_sakal_bihar_en.py

# 2. Generate HTML composition
.venv/bin/python scripts/generate_sakal_bihar_html.py

# 3. Lint composition
npx hyperframes lint sakal-bihar-en.html

# 4. Render final 1080x1920 MP4
mkdir -p ../Export
HYPERFRAMES_BROWSER_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  npx hyperframes render --composition sakal-bihar-en.html --output "../Export/sakal-bihar-en.mp4"
```

For full pipeline details, see [WORKFLOW.md](WORKFLOW.md).
