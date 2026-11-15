import json
import os
import subprocess

ENGINE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(ENGINE_DIR, "assets/audio")


def get_duration(mp3_path: str) -> float:
    out = subprocess.check_output(
        [
            "/opt/homebrew/bin/ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            mp3_path,
        ],
        text=True,
    ).strip()
    return float(out)


def main():
    prefix = "siri_making_of_bn"
    mp3_path = os.path.join(AUDIO_DIR, f"{prefix}.mp3")
    with open(os.path.join(AUDIO_DIR, f"{prefix}.timestamps.json"), encoding="utf-8") as f:
        words = json.load(f)
    with open(os.path.join(AUDIO_DIR, f"{prefix}.spans.json"), encoding="utf-8") as f:
        spans = json.load(f)

    dur = round(get_duration(mp3_path) + 0.45, 2)
    t1, t2, t3, t4, t5, t6 = [sp["start"] for sp in spans]
    words_json = json.dumps(words, ensure_ascii=False)
    comp_id = "siri-making-of-bn"

    html = f'''<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8" />
<title>{comp_id}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@600;700;800;900&family=JetBrains+Mono:wght@600;700;800&family=Noto+Sans+Bengali:wght@600;700;800;900&display=swap" rel="stylesheet" />
<script src="assets/js/gsap.min.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    width: 1080px; height: 1920px; overflow: hidden;
    background: #F7F5F0;
    font-family: 'Inter', 'Noto Sans Bengali', -apple-system, sans-serif;
    color: #18181B;
  }}
  .stage {{
    position: relative; width: 1080px; height: 1920px;
    background: radial-gradient(circle at 18% 12%, #EEF2FF 0%, #F7F5F0 50%, #FFF7ED 100%);
    overflow: hidden; perspective: 1400px; transform-style: preserve-3d;
  }}
  .dot-grid {{
    position: absolute; inset: 0;
    background-image: radial-gradient(rgba(24, 24, 27, 0.11) 1.5px, transparent 1.5px);
    background-size: 36px 36px; pointer-events: none;
  }}
  .orb {{
    position: absolute; border-radius: 999px; filter: blur(85px); opacity: 0.42; pointer-events: none;
  }}
  .orb-1 {{ width: 500px; height: 500px; background: #A5B4FC; top: -110px; right: -110px; }}
  .orb-2 {{ width: 480px; height: 480px; background: #FDBA74; bottom: 200px; left: -120px; }}

  .header {{
    position: absolute; top: 64px; left: 56px; right: 56px;
    display: flex; align-items: center; justify-content: space-between; z-index: 30;
  }}
  .brand-left {{ display: flex; align-items: center; gap: 16px; }}
  .brand-logo {{
    width: 60px; height: 60px; border-radius: 16px;
    border: 2.5px solid #18181B; box-shadow: 0 6px 0 #18181B;
  }}
  .brand-name {{ font-size: 26px; font-weight: 900; }}
  .brand-sub {{ font-size: 15px; font-weight: 800; color: #4F46E5; letter-spacing: 0.08em; }}
  .tag-pill {{
    padding: 12px 22px; border-radius: 999px; background: #FFFFFF;
    border: 2.5px solid #18181B; box-shadow: 0 5px 0 #18181B;
    font-size: 17px; font-weight: 900; letter-spacing: 0.05em;
  }}

  .speaker-wrap {{ position: absolute; top: 154px; left: 56px; z-index: 30; }}
  .speaker-pill {{
    padding: 9px 22px; border-radius: 999px;
    background: #EEF2FF; border: 2px solid #4F46E5; color: #4338CA;
    font-size: 17px; font-weight: 800; letter-spacing: 0.06em;
  }}

  .scene {{
    position: absolute; top: 230px; left: 56px; right: 56px; bottom: 420px;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    gap: 26px; opacity: 0; transform-style: preserve-3d;
  }}
  .eyebrow {{
    font-family: 'JetBrains Mono', 'Noto Sans Bengali', monospace;
    font-size: 22px; font-weight: 800; letter-spacing: 0.08em;
    color: #FFFFFF; background: #4F46E5; border: 2.5px solid #18181B;
    padding: 10px 26px; border-radius: 999px; box-shadow: 0 6px 0 #18181B;
  }}
  .card {{
    width: 100%; background: #FFFFFF;
    border: 3px solid #18181B; border-radius: 34px; padding: 46px 40px;
    box-shadow: 0 14px 0 #18181B, 0 28px 60px rgba(24, 24, 27, 0.12);
    display: flex; flex-direction: column; align-items: center; text-align: center; gap: 22px;
  }}
  .card-title {{ font-size: 46px; font-weight: 900; line-height: 1.18; }}
  .card-sub {{ font-size: 27px; font-weight: 600; color: #52525B; line-height: 1.38; }}

  .icon-row {{ display: flex; align-items: center; justify-content: center; gap: 26px; }}
  .tool-ico {{
    width: 92px; height: 92px; padding: 14px;
    background: #F4F4F5; border: 2.5px solid #18181B; border-radius: 22px;
    box-shadow: 0 6px 0 #18181B; object-fit: contain;
  }}
  .arrow {{ font-size: 36px; font-weight: 900; color: #EA580C; }}

  .chip-grid {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 14px; }}
  .chip {{
    padding: 15px 26px; border-radius: 18px;
    background: #EEF2FF; border: 2px solid #4F46E5; color: #4338CA;
    font-size: 24px; font-weight: 800;
  }}
  .chip.strike {{
    background: #FEE2E2; border-color: #EF4444; color: #B91C1C;
    text-decoration: line-through;
  }}

  .term-box {{
    width: 100%; background: #18181B; border-radius: 22px; padding: 28px 30px;
    text-align: left; font-family: 'JetBrains Mono', monospace; font-size: 23px; line-height: 1.65;
  }}
  .t-cmd {{ color: #FB923C; font-weight: 700; }}
  .t-ok {{ color: #4ADE80; font-weight: 700; }}

  .wave-bars {{ display: flex; align-items: center; gap: 14px; height: 96px; }}
  .wave-bars .bar {{
    width: 18px; border-radius: 999px; background: linear-gradient(180deg, #4F46E5, #EA580C);
    height: 42px;
  }}
  .wave-bars .bar:nth-child(2n) {{ height: 84px; }}
  .wave-bars .bar:nth-child(3n) {{ height: 60px; }}

  .cta-card {{
    width: 100%; background: #18181B; color: #FFFFFF;
    border: 3px solid #18181B; border-radius: 36px; padding: 48px 38px;
    box-shadow: 0 16px 0 #4F46E5;
    display: flex; flex-direction: column; align-items: center; text-align: center; gap: 22px;
  }}
  .cta-btn {{
    padding: 20px 44px; border-radius: 999px;
    background: #EA580C; color: #FFFFFF; font-size: 28px; font-weight: 900;
  }}

  .caption-wrap {{
    position: absolute; bottom: 120px; left: 40px; right: 40px;
    display: flex; justify-content: center; z-index: 40;
  }}
  .caption-box {{
    display: flex; flex-wrap: wrap; justify-content: center; gap: 12px 14px;
    padding: 24px 32px; border-radius: 28px;
    background: rgba(24, 24, 27, 0.95);
    box-shadow: 0 18px 42px rgba(24, 24, 27, 0.28);
    max-width: 980px;
  }}
  .cap-word {{
    font-size: 46px; font-weight: 900; color: #F4F4F5;
    padding: 5px 12px; border-radius: 12px; line-height: 1.18;
  }}
  .cap-word.active {{ background: #4F46E5; color: #FFFFFF; }}

  .progress-track {{
    position: absolute; bottom: 58px; left: 56px; right: 56px;
    height: 10px; border-radius: 999px;
    background: rgba(24, 24, 27, 0.14); overflow: hidden; z-index: 40;
  }}
  .progress-fill {{
    height: 100%; width: 0%;
    background: linear-gradient(90deg, #4F46E5, #EA580C); border-radius: 999px;
  }}
</style>
</head>
<body>
<div id="root"
     data-composition-id="{comp_id}"
     data-width="1080"
     data-height="1920"
     data-fps="30"
     data-duration="{dur}">

  <audio id="vo-main" src="assets/audio/{prefix}.mp3" data-start="0.0" volume="1.0"></audio>
  <audio id="sfx-bed" src="assets/sfx/tech_drone.wav" data-start="0.0" volume="0.05"></audio>
  <audio id="sfx-impact-1" src="assets/sfx/impact.wav" data-start="{t1}" volume="0.22"></audio>
  <audio id="sfx-whoosh-2" src="assets/sfx/real/whoosh.wav" data-start="{t2}" volume="0.28"></audio>
  <audio id="sfx-pop-2" src="assets/sfx/real/pop.wav" data-start="{round(t2 + 0.25, 3)}" volume="0.26"></audio>
  <audio id="sfx-whoosh-3" src="assets/sfx/real/whoosh.wav" data-start="{t3}" volume="0.28"></audio>
  <audio id="sfx-click-4" src="assets/sfx/real/click.wav" data-start="{t4}" volume="0.24"></audio>
  <audio id="sfx-whoosh-5" src="assets/sfx/real/whoosh.wav" data-start="{t5}" volume="0.28"></audio>
  <audio id="sfx-chime-6" src="assets/sfx/real/chime.wav" data-start="{t6}" volume="0.34"></audio>

  <div class="stage">
    <div class="dot-grid"></div>
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>

    <div class="header">
      <div class="brand-left">
        <img src="assets/logos/antigravity-official.png" class="brand-logo" alt="Video Engine" />
        <div>
          <div class="brand-name">VIDEO ENGINE</div>
          <div class="brand-sub">CODE → 3D REELS</div>
        </div>
      </div>
      <div class="tag-pill">100% LOCAL PIPELINE</div>
    </div>

    <div class="speaker-wrap">
      <div class="speaker-pill">● SIRI · VOICE CLONE</div>
    </div>

    <!-- SCENE 1 -->
    <div id="scene-1" class="scene">
      <div class="eyebrow anim-item">BEHIND THE SCENES</div>
      <div class="card anim-card">
        <div class="chip-grid">
          <div class="chip strike anim-pop">After Effects</div>
          <div class="chip strike anim-pop">Premiere Pro</div>
        </div>
        <div class="card-title">পুরো 3D রিলস তৈরি হয় কোড দিয়ে!</div>
        <div class="card-sub">Python + HTML5 + GSAP + Local AI</div>
      </div>
    </div>

    <!-- SCENE 2 -->
    <div id="scene-2" class="scene">
      <div class="eyebrow anim-item">STEP 1 · ANALYSIS &amp; SCRIPT</div>
      <div class="card anim-card">
        <div class="icon-row">
          <img src="assets/logos/yt-dlp.png" class="tool-ico anim-pop" alt="yt-dlp" />
          <span class="arrow">→</span>
          <img src="assets/logos/ffmpeg.svg" class="tool-ico anim-pop" alt="ffprobe" />
        </div>
        <div class="card-title">ভাইরাল পেসিং অ্যানালাইসিস</div>
        <div class="card-sub">yt-dlp ও ffprobe দিয়ে সিন কাট ও স্ক্রিপ্ট প্ল্যান</div>
      </div>
    </div>

    <!-- SCENE 3 -->
    <div id="scene-3" class="scene">
      <div class="eyebrow anim-item">STEP 2 · OFFLINE VOICE CLONE</div>
      <div class="card anim-card">
        <div class="wave-bars">
          <span class="bar"></span><span class="bar"></span><span class="bar"></span>
          <span class="bar"></span><span class="bar"></span><span class="bar"></span>
          <span class="bar"></span>
        </div>
        <div class="card-title">OmniVoice (10s Clip → Bangla)</div>
        <div class="card-sub">Mac-এ অফলাইনে ন্যাচারাল বাংলা ভয়েসওভার</div>
      </div>
    </div>

    <!-- SCENE 4 -->
    <div id="scene-4" class="scene">
      <div class="eyebrow anim-item">STEP 3 · 3D HTML + GSAP</div>
      <div class="card anim-card">
        <div class="icon-row">
          <img src="assets/logos/greensock.svg" class="tool-ico anim-pop" alt="GSAP" />
          <span class="arrow">+</span>
          <img src="assets/logos/python.svg" class="tool-ico anim-pop" alt="Python" />
        </div>
        <div class="card-title">3D কার্ড ও সিংকড ক্যাপশন</div>
        <div class="term-box">
          <div class="t-cmd">tl.fromTo('#card', {{ rotateY: -10 }}, {{ rotateY: 0 }})</div>
          <div class="t-ok">✓ Word-level timestamps synced</div>
        </div>
      </div>
    </div>

    <!-- SCENE 5 -->
    <div id="scene-5" class="scene">
      <div class="eyebrow anim-item">STEP 4 · RENDER &amp; SFX</div>
      <div class="card anim-card">
        <div class="icon-row">
          <img src="assets/logos/hyperframes-studio.png" class="tool-ico anim-pop" alt="HyperFrames" />
          <span class="arrow">→</span>
          <img src="assets/logos/googlechrome.svg" class="tool-ico anim-pop" alt="Chrome" />
        </div>
        <div class="card-title">1080p · 30fps · Real SFX</div>
        <div class="card-sub">HyperFrames + FFmpeg দিয়ে ক্রিস্প ফাইনাল MP4</div>
      </div>
    </div>

    <!-- SCENE 6 -->
    <div id="scene-6" class="scene">
      <div class="eyebrow anim-item">100% AUTOMATED</div>
      <div class="cta-card anim-card">
        <div class="card-title" style="color:#FFFFFF;">পুরো Video Engine গাইড চাও?</div>
        <div class="card-sub" style="color:#D4D4D8;">নিচে "CODE" কমেন্ট করো—সম্পূর্ণ ওয়ার্কফ্লো পেয়ে যাবে!</div>
        <div class="cta-btn anim-pop">COMMENT "CODE" ↓</div>
      </div>
    </div>

    <div class="caption-wrap">
      <div id="caption-box" class="caption-box"></div>
    </div>

    <div class="progress-track">
      <div id="progress-fill" class="progress-fill"></div>
    </div>
  </div>
</div>

<script>
const WORDS = {words_json};
const TOTAL_DUR = {dur};
const capBox = document.getElementById('caption-box');
const progFill = document.getElementById('progress-fill');

let lastGroup = -1;
function updateHUD(t) {{
  progFill.style.width = Math.min(100, Math.max(0, (t / TOTAL_DUR) * 100)).toFixed(2) + '%';

  let activeWord = null;
  for (let i = 0; i < WORDS.length; i++) {{
    if (t >= WORDS[i].start && t <= WORDS[i].end + 0.12) {{
      activeWord = WORDS[i];
      break;
    }}
  }}
  if (!activeWord) {{
    for (let i = WORDS.length - 1; i >= 0; i--) {{
      if (t >= WORDS[i].start) {{
        activeWord = WORDS[i];
        break;
      }}
    }}
  }}
  if (!activeWord) activeWord = WORDS[0];

  const grp = activeWord.group;
  if (grp !== lastGroup) {{
    lastGroup = grp;
    const grpWords = WORDS.filter(w => w.group === grp);
    capBox.innerHTML = '';
    grpWords.forEach((w) => {{
      const el = document.createElement('span');
      el.className = 'cap-word';
      el.textContent = w.word;
      capBox.appendChild(el);
    }});
  }}
  const grpWords = WORDS.filter(w => w.group === grp);
  const children = capBox.children;
  for (let i = 0; i < grpWords.length; i++) {{
    const w = grpWords[i];
    const el = children[i];
    if (!el) continue;
    const isCurrent = (t >= w.start && t <= w.end + 0.08);
    el.className = 'cap-word' + (isCurrent ? ' active' : '');
  }}
}}

const tl = gsap.timeline({{
  paused: true,
  onUpdate: function() {{ updateHUD(this.time()); }}
}});

tl.to('.orb-1', {{ x: -40, y: 30, duration: TOTAL_DUR, ease: 'sine.inOut' }}, 0);
tl.to('.orb-2', {{ x: 40, y: -30, duration: TOTAL_DUR, ease: 'sine.inOut' }}, 0);

const scenes = ['#scene-1', '#scene-2', '#scene-3', '#scene-4', '#scene-5', '#scene-6'];
const times = [{t1}, {t2}, {t3}, {t4}, {t5}, {t6}];

scenes.forEach((sel, i) => {{
  const tStart = times[i];
  const rotY = (i % 2 === 0) ? -10 : 10;
  tl.fromTo(
    sel,
    {{ opacity: 0, y: 48, z: -120, rotateX: 8, rotateY: rotY, scale: 0.94 }},
    {{ opacity: 1, y: 0, z: 0, rotateX: 0, rotateY: 0, scale: 1, duration: 0.45, ease: 'power3.out' }},
    tStart
  );
  tl.fromTo(
    sel + ' .anim-pop',
    {{ scale: 0.80, opacity: 0 }},
    {{ scale: 1, opacity: 1, duration: 0.36, stagger: 0.08, ease: 'back.out(1.7)' }},
    tStart + 0.14
  );
  if (i < scenes.length - 1) {{
    tl.to(
      sel,
      {{ opacity: 0, y: -36, z: 60, rotateX: -6, duration: 0.28, ease: 'power2.in' }},
      times[i + 1] - 0.16
    );
  }}
}});

tl.to({{}}, {{ duration: 0.1 }}, TOTAL_DUR);
updateHUD(0);

window.__timelines = window.__timelines || {{}};
window.__timelines["{comp_id}"] = tl;
</script>
</body>
</html>
'''
    out_path = os.path.join(ENGINE_DIR, "siri-making-of-bn.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated {out_path} (duration={dur}s)")


if __name__ == "__main__":
    main()
