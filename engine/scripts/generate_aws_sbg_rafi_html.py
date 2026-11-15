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


CONFIGS = {
    "en": {
        "comp_id": "aws-sbg-diu-rafi-en",
        "out_html": "aws-sbg-diu-rafi-en.html",
        "prefix": "aws_sbg_rafi_en",
        "lang_attr": "en",
        "tag": "OFFICIAL · DIU CAMPUS",
        "s1_eye": "THE CLOUD GAP",
        "s1_title": "10-Hour Tutorials ≠ Real Skills",
        "s1_sub": "Why solo video watching leaves students stuck",
        "s2_eye": "NOW LIVE AT DIU",
        "s2_badge": "OFFICIAL LAUNCH · AWS × DIU",
        "s3_eye": "ZERO BORING SLIDES",
        "s3_title": "Deploy Real Cloud Architecture",
        "s3_chips": ["EC2 & Lambda", "RDS & DynamoDB", "Serverless APIs"],
        "s4_eye": "MENTORED FROM ZERO",
        "s4_title": "Senior Builders Guide Every Step",
        "s4_sub": "Hands-On Labs · Live Hackathons · Code Reviews",
        "s5_eye": "CAREER LAUNCHPAD",
        "s5_title": "Production Portfolio + AWS Certs",
        "s5_sub": "Stand out to top tech employers before you graduate",
        "s6_eye": "JOIN THE SQUAD",
        "s6_title": "AWS SBG DIU",
        "s6_sub": "Follow the page & grab your seat at the next meetup!",
        "s6_btn": "GRAB YOUR SEAT →",
    },
    "bn": {
        "comp_id": "aws-sbg-diu-rafi-bn",
        "out_html": "aws-sbg-diu-rafi-bn.html",
        "prefix": "aws_sbg_rafi_bn",
        "lang_attr": "bn",
        "tag": "অফিশিয়াল · DIU ক্যাম্পাস",
        "s1_eye": "ক্লাউড শেখার আসল সত্য",
        "s1_title": "YouTube দেখে কি Cloud Engineer হওয়া যায়?",
        "s1_sub": "একা টিউটোরিয়াল দেখে রিয়েল প্রোডাকশন স্কিল আসে না",
        "s2_eye": "এখন DIU ক্যাম্পাসে",
        "s2_badge": "অফিশিয়াল লঞ্চ · AWS × DIU",
        "s3_eye": "কোনো বোরিং স্লাইড না",
        "s3_title": "লাইভ Cloud সার্ভার ও রিয়েল প্রজেক্ট",
        "s3_chips": ["EC2 & Lambda", "Database & S3", "Serverless API"],
        "s4_eye": "আগে AWS না ছুঁয়ে থাকলেও",
        "s4_title": "সিনিয়র বিল্ডাররা হাতে-কলমে শেখাবে",
        "s4_sub": "ল্যাব সেশন · লাইভ হ্যাকাথন · প্রজেক্ট রিভিউ",
        "s5_eye": "PRO-লেভেল CV",
        "s5_title": "হ্যাকাথন + AWS Certification",
        "s5_sub": "গ্র্যাজুয়েশনের আগেই হবে প্রো-লেভেল পোর্টফোলিও",
        "s6_eye": "আর দেরি কেন?",
        "s6_title": "AWS SBG DIU",
        "s6_sub": "পেজ ফলো করো এবং Next Meetup-এ সিট বুক করে ফেলো!",
        "s6_btn": "মিটআপে সিট বুক করো →",
    },
}


def build_html(lang: str, c: dict) -> None:
    prefix = c["prefix"]
    mp3_path = os.path.join(AUDIO_DIR, f"{prefix}.mp3")
    with open(os.path.join(AUDIO_DIR, f"{prefix}.timestamps.json"), encoding="utf-8") as f:
        words = json.load(f)
    with open(os.path.join(AUDIO_DIR, f"{prefix}.spans.json"), encoding="utf-8") as f:
        spans = json.load(f)

    dur = round(get_duration(mp3_path) + 0.45, 2)
    t1, t2, t3, t4, t5, t6 = [sp["start"] for sp in spans]
    words_json = json.dumps(words, ensure_ascii=False)
    comp_id = c["comp_id"]

    chips_html = "".join(f'<div class="chip anim-pop">{ch}</div>' for ch in c["s3_chips"])

    html = f'''<!DOCTYPE html>
<html lang="{c['lang_attr']}">
<head>
<meta charset="UTF-8" />
<title>{comp_id}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@600;700;800;900&family=JetBrains+Mono:wght@600;700;800&family=Noto+Sans+Bengali:wght@600;700;800;900&display=swap" rel="stylesheet" />
<script src="assets/js/gsap.min.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    width: 1080px;
    height: 1920px;
    overflow: hidden;
    background: #F7F5F0;
    font-family: 'Inter', 'Noto Sans Bengali', -apple-system, sans-serif;
    color: #18181B;
  }}
  .stage {{
    position: relative;
    width: 1080px;
    height: 1920px;
    background: radial-gradient(circle at 18% 10%, #ECFDF5 0%, #F7F5F0 50%, #FFF7ED 100%);
    overflow: hidden;
    perspective: 1400px;
    transform-style: preserve-3d;
  }}
  .tech-grid {{
    position: absolute;
    inset: 0;
    background-image:
      linear-gradient(rgba(24, 24, 27, 0.05) 1px, transparent 1px),
      linear-gradient(90deg, rgba(24, 24, 27, 0.05) 1px, transparent 1px);
    background-size: 64px 64px;
    pointer-events: none;
  }}
  .glow-1 {{
    position: absolute; width: 540px; height: 540px; border-radius: 999px;
    background: #34D399; opacity: 0.24; filter: blur(95px);
    top: -110px; right: -110px; pointer-events: none;
  }}
  .glow-2 {{
    position: absolute; width: 500px; height: 500px; border-radius: 999px;
    background: #FDBA74; opacity: 0.30; filter: blur(95px);
    bottom: 200px; left: -120px; pointer-events: none;
  }}
  .px-block {{
    position: absolute;
    background: rgba(22, 163, 74, 0.16);
    border: 2px solid #16A34A;
    pointer-events: none;
  }}
  .px-1 {{ width: 54px; height: 54px; top: 210px; right: 86px; }}
  .px-2 {{ width: 32px; height: 32px; top: 278px; right: 150px; background: rgba(234, 88, 12, 0.18); border-color: #EA580C; }}
  .px-3 {{ width: 44px; height: 44px; bottom: 420px; left: 72px; }}

  .header {{
    position: absolute;
    top: 62px; left: 56px; right: 56px;
    display: flex; align-items: center; justify-content: space-between;
    z-index: 30;
  }}
  .brand-left {{ display: flex; align-items: center; gap: 16px; }}
  .sbg-logo-hdr {{
    width: 68px; height: 68px; border-radius: 16px;
    border: 2.5px solid #18181B;
    box-shadow: 0 6px 0 #18181B;
    object-fit: cover;
  }}
  .brand-name {{ font-size: 26px; font-weight: 900; letter-spacing: 0.02em; color: #18181B; }}
  .brand-sub {{ font-size: 16px; font-weight: 800; color: #16A34A; letter-spacing: 0.08em; }}
  .tag-pill {{
    padding: 12px 22px; border-radius: 999px;
    background: #FFFFFF;
    border: 2.5px solid #18181B;
    box-shadow: 0 5px 0 #18181B;
    color: #18181B; font-size: 17px; font-weight: 900; letter-spacing: 0.05em;
  }}

  .speaker-wrap {{
    position: absolute; top: 152px; left: 56px; z-index: 30;
    display: flex; align-items: center; gap: 12px;
  }}
  .speaker-pill {{
    padding: 9px 20px; border-radius: 999px;
    background: #ECFDF5;
    border: 2px solid #16A34A;
    color: #15803D; font-size: 17px; font-weight: 800; letter-spacing: 0.06em;
  }}

  .scene {{
    position: absolute;
    top: 225px; left: 56px; right: 56px; bottom: 430px;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    gap: 26px; opacity: 0; transform-style: preserve-3d;
  }}
  .eyebrow {{
    font-family: 'JetBrains Mono', 'Noto Sans Bengali', monospace;
    font-size: 22px; font-weight: 800; letter-spacing: 0.1em;
    color: #FFFFFF; background: #16A34A;
    border: 2.5px solid #18181B;
    padding: 10px 26px; border-radius: 999px;
    box-shadow: 0 6px 0 #18181B;
  }}
  .hud-card {{
    width: 100%;
    background: #FFFFFF;
    border: 3px solid #18181B;
    border-radius: 34px;
    padding: 44px 38px;
    box-shadow: 0 14px 0 #18181B, 0 28px 60px rgba(24, 24, 27, 0.12);
    display: flex; flex-direction: column; align-items: center; text-align: center; gap: 22px;
  }}
  .card-title {{ font-size: 46px; font-weight: 900; line-height: 1.18; color: #18181B; }}
  .card-sub {{ font-size: 27px; font-weight: 600; line-height: 1.38; color: #52525B; }}

  .dual-logos {{ display: flex; align-items: center; justify-content: center; gap: 26px; }}
  .aws-pill {{
    background: #F4F4F5; padding: 14px 24px; border-radius: 20px;
    border: 2px solid #18181B;
    display: flex; align-items: center; justify-content: center;
  }}
  .aws-img {{ height: 52px; object-fit: contain; }}
  .diu-img {{ height: 74px; object-fit: contain; background: #F4F4F5; border: 2px solid #18181B; padding: 8px 14px; border-radius: 16px; }}
  .x-sign {{ font-size: 38px; font-weight: 900; color: #EA580C; }}

  .showcase-frame {{
    width: 100%; max-width: 720px;
    border-radius: 28px; overflow: hidden;
    border: 3.5px solid #18181B;
    box-shadow: 0 14px 0 #16A34A, 0 24px 55px rgba(24, 24, 27, 0.18);
    background: #0B111E;
  }}
  .showcase-img {{ width: 100%; display: block; object-fit: cover; }}

  .cover-frame {{
    width: 100%; border-radius: 22px; overflow: hidden;
    border: 2.5px solid #18181B;
    box-shadow: 0 10px 26px rgba(24, 24, 27, 0.15);
  }}
  .cover-img {{ width: 100%; display: block; }}

  .chip-grid {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 16px; }}
  .chip {{
    padding: 16px 28px; border-radius: 18px;
    background: #ECFDF5; border: 2.5px solid #16A34A;
    color: #15803D; font-size: 25px; font-weight: 800;
  }}

  .term-box {{
    width: 100%; background: #18181B; border: 2.5px solid #18181B;
    border-radius: 22px; padding: 26px 28px; text-align: left;
    font-family: 'JetBrains Mono', monospace; font-size: 23px; line-height: 1.6;
  }}
  .t-cmd {{ color: #FB923C; font-weight: 700; }}
  .t-ok {{ color: #4ADE80; font-weight: 700; }}

  .svg-row {{ display: flex; align-items: center; justify-content: center; gap: 28px; }}
  .svg-badge {{
    width: 118px; height: 118px; padding: 14px;
    background: #0F172A; border: 2.5px solid #18181B; border-radius: 26px;
    box-shadow: 0 8px 0 #16A34A;
    object-fit: contain;
  }}

  .cta-card {{
    width: 100%;
    background: #FFFFFF;
    border: 3.5px solid #18181B;
    border-radius: 36px; padding: 48px 38px;
    box-shadow: 0 16px 0 #16A34A, 0 32px 64px rgba(24, 24, 27, 0.16);
    display: flex; flex-direction: column; align-items: center; text-align: center; gap: 22px;
  }}
  .cta-logo-hero {{
    width: 136px; height: 136px; border-radius: 28px;
    border: 3px solid #18181B;
    box-shadow: 0 10px 0 #16A34A;
  }}
  .cta-btn {{
    padding: 20px 44px; border-radius: 999px;
    background: #EA580C; color: #FFFFFF;
    border: 2.5px solid #18181B;
    font-size: 28px; font-weight: 900; letter-spacing: 0.04em;
    box-shadow: 0 8px 0 #18181B;
  }}

  /* BIGGER HIGH-IMPACT CAPTIONS */
  .caption-wrap {{
    position: absolute;
    bottom: 120px; left: 40px; right: 40px;
    display: flex; justify-content: center; z-index: 40;
  }}
  .caption-box {{
    display: flex; flex-wrap: wrap; justify-content: center; gap: 12px 16px;
    padding: 26px 34px; border-radius: 30px;
    background: rgba(24, 24, 27, 0.95);
    border: 2.5px solid #18181B;
    box-shadow: 0 16px 38px rgba(24, 24, 27, 0.25);
    max-width: 980px;
  }}
  .cap-word {{
    font-size: 50px;
    font-weight: 900;
    color: #F4F4F5;
    padding: 6px 14px;
    border-radius: 14px;
    line-height: 1.15;
  }}
  .cap-word.active {{
    background: #16A34A;
    color: #FFFFFF;
  }}

  .progress-track {{
    position: absolute; bottom: 58px; left: 56px; right: 56px;
    height: 10px; border-radius: 999px;
    background: rgba(24, 24, 27, 0.14); overflow: hidden; z-index: 40;
  }}
  .progress-fill {{
    height: 100%; width: 0%;
    background: linear-gradient(90deg, #16A34A, #EA580C);
    border-radius: 999px;
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
  <audio id="sfx-bed" src="assets/sfx/tech_drone.wav" data-start="0.0" volume="0.06"></audio>
  <audio id="sfx-impact-1" src="assets/sfx/impact.wav" data-start="{t1}" volume="0.24"></audio>
  <audio id="sfx-whoosh-2" src="assets/sfx/real/whoosh.wav" data-start="{t2}" volume="0.30"></audio>
  <audio id="sfx-pop-2" src="assets/sfx/real/pop.wav" data-start="{round(t2 + 0.25, 3)}" volume="0.28"></audio>
  <audio id="sfx-whoosh-3" src="assets/sfx/real/whoosh.wav" data-start="{t3}" volume="0.30"></audio>
  <audio id="sfx-click-3" src="assets/sfx/real/click.wav" data-start="{round(t3 + 0.22, 3)}" volume="0.26"></audio>
  <audio id="sfx-whoosh-4" src="assets/sfx/real/whoosh.wav" data-start="{t4}" volume="0.30"></audio>
  <audio id="sfx-pop-4" src="assets/sfx/real/pop.wav" data-start="{round(t4 + 0.25, 3)}" volume="0.28"></audio>
  <audio id="sfx-whoosh-5" src="assets/sfx/real/whoosh.wav" data-start="{t5}" volume="0.30"></audio>
  <audio id="sfx-chime-6" src="assets/sfx/real/chime.wav" data-start="{t6}" volume="0.36"></audio>

  <div class="stage">
    <div class="tech-grid"></div>
    <div class="glow-1"></div>
    <div class="glow-2"></div>
    <div class="px-block px-1"></div>
    <div class="px-block px-2"></div>
    <div class="px-block px-3"></div>

    <div class="header">
      <div class="brand-left">
        <img src="assets/logos/sbg_fb_logo.jpg" class="sbg-logo-hdr" alt="AWS SBG DIU" />
        <div>
          <div class="brand-name">AWS SBG DIU</div>
          <div class="brand-sub">STUDENT BUILDER GROUP</div>
        </div>
      </div>
      <div class="tag-pill">{c['tag']}</div>
    </div>

    <div class="speaker-wrap">
      <div class="speaker-pill">● RAFI · VOICE CLONE</div>
    </div>

    <!-- SCENE 1: Problem + AWS x DIU Logos -->
    <div id="scene-1" class="scene">
      <div class="eyebrow anim-item">{c['s1_eye']}</div>
      <div class="hud-card anim-card">
        <div class="dual-logos">
          <div class="aws-pill"><img src="assets/logos/aws_logo.png" class="aws-img" alt="AWS" /></div>
          <span class="x-sign">×</span>
          <img src="assets/logos/diu_full_logo.png" class="diu-img" alt="DIU" />
        </div>
        <div class="card-title">{c['s1_title']}</div>
        <div class="card-sub">{c['s1_sub']}</div>
      </div>
    </div>

    <!-- SCENE 2: Official Launch Post Graphic -->
    <div id="scene-2" class="scene">
      <div class="eyebrow anim-item">{c['s2_eye']}</div>
      <div class="showcase-frame anim-card">
        <img src="assets/logos/sbg_post_graphic.jpg" class="showcase-img" alt="AWS SBG DIU Launch" />
      </div>
      <div class="tag-pill anim-pop">{c['s2_badge']}</div>
    </div>

    <!-- SCENE 3: Cloud Nodes + Terminal Deploy -->
    <div id="scene-3" class="scene">
      <div class="eyebrow anim-item">{c['s3_eye']}</div>
      <div class="hud-card anim-card">
        <div class="svg-row">
          <img src="assets/logos/cloud-nodes.svg" class="svg-badge anim-pop" alt="Cloud Nodes" />
          <img src="assets/logos/sbg-diu-badge.svg" class="svg-badge anim-pop" alt="SBG DIU Badge" />
        </div>
        <div class="card-title">{c['s3_title']}</div>
        <div class="chip-grid">{chips_html}</div>
        <div class="term-box">
          <div class="t-cmd">$ aws deploy --stack diu-builder-lab</div>
          <div class="t-ok">✓ Cloud architecture live in ap-south-1</div>
        </div>
      </div>
    </div>

    <!-- SCENE 4: Official Cover + Mentorship -->
    <div id="scene-4" class="scene">
      <div class="eyebrow anim-item">{c['s4_eye']}</div>
      <div class="hud-card anim-card">
        <div class="cover-frame">
          <img src="assets/logos/sbg_official_cover.jpg" class="cover-img" alt="AWS SBG DIU Cover" />
        </div>
        <div class="card-title">{c['s4_title']}</div>
        <div class="card-sub">{c['s4_sub']}</div>
      </div>
    </div>

    <!-- SCENE 5: Cert Badge + DIU Crest -->
    <div id="scene-5" class="scene">
      <div class="eyebrow anim-item">{c['s5_eye']}</div>
      <div class="hud-card anim-card">
        <div class="svg-row">
          <img src="assets/logos/cert-badge.svg" class="svg-badge anim-pop" alt="AWS Certification" />
          <img src="assets/logos/diu_crest.jpg" class="svg-badge anim-pop" alt="DIU Crest" />
        </div>
        <div class="card-title">{c['s5_title']}</div>
        <div class="card-sub">{c['s5_sub']}</div>
      </div>
    </div>

    <!-- SCENE 6: AWS SBG DIU Logo Hero CTA -->
    <div id="scene-6" class="scene">
      <div class="eyebrow anim-item">{c['s6_eye']}</div>
      <div class="cta-card anim-card">
        <img src="assets/logos/sbg_fb_logo.jpg" class="cta-logo-hero anim-pop" alt="AWS SBG DIU Logo" />
        <div class="card-title">{c['s6_title']}</div>
        <div class="card-sub">{c['s6_sub']}</div>
        <div class="cta-btn anim-pop">{c['s6_btn']}</div>
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

tl.to('.px-1', {{ y: 30, rotation: 90, duration: TOTAL_DUR, ease: 'sine.inOut' }}, 0);
tl.to('.px-2', {{ x: -24, y: -20, duration: TOTAL_DUR, ease: 'sine.inOut' }}, 0);
tl.to('.px-3', {{ y: -36, rotation: -90, duration: TOTAL_DUR, ease: 'sine.inOut' }}, 0);

const scenes = ['#scene-1', '#scene-2', '#scene-3', '#scene-4', '#scene-5', '#scene-6'];
const times = [{t1}, {t2}, {t3}, {t4}, {t5}, {t6}];

scenes.forEach((sel, i) => {{
  const tStart = times[i];
  const rotY = (i % 2 === 0) ? -12 : 12;
  tl.fromTo(
    sel,
    {{ opacity: 0, y: 50, z: -130, rotateX: 9, rotateY: rotY, scale: 0.93 }},
    {{ opacity: 1, y: 0, z: 0, rotateX: 0, rotateY: 0, scale: 1, duration: 0.45, ease: 'power3.out' }},
    tStart
  );
  tl.fromTo(
    sel + ' .anim-pop',
    {{ scale: 0.78, opacity: 0 }},
    {{ scale: 1, opacity: 1, duration: 0.36, stagger: 0.08, ease: 'back.out(1.7)' }},
    tStart + 0.14
  );
  if (i < scenes.length - 1) {{
    tl.to(
      sel,
      {{ opacity: 0, y: -38, z: 70, rotateX: -7, duration: 0.28, ease: 'power2.in' }},
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
    out_path = os.path.join(ENGINE_DIR, c["out_html"])
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated {out_path} (duration={dur}s)")


def main():
    for lang, cfg in CONFIGS.items():
        build_html(lang, cfg)


if __name__ == "__main__":
    main()
