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
        "out_html": "omnivoice-en.html",
        "comp_id": "omnivoice-reel-en",
        "mp3": "omnivoice_en.mp3",
        "ts": "omnivoice_en.timestamps.json",
        "spans": "omnivoice_en.spans.json",
        "tag": "LOCAL AI VOICE",
        "s1_badge": "COST TRAP",
        "s1_title": "Still Paying Monthly<br>For AI Voice Cloning?",
        "s1_old": "$22 / mo",
        "s1_old_sub": "Cloud API · Usage Caps",
        "s1_new": "$0.00 / mo",
        "s1_new_sub": "100% Local on Apple Silicon",
        "s2_badge": "OPEN SOURCE",
        "s2_title": "Meet OmniVoice<br>by k2-fsa",
        "s2_sub": "Zero-Shot Voice Cloning · 600+ Languages",
        "s3_badge": "REFERENCE CLIP",
        "s3_title": "Just 5–15 Seconds<br>Of Your Voice",
        "s3_sub": "Record one clean mic sample — no studio needed",
        "s4_badge": "APPLE SILICON MPS",
        "s4_title": "Run Locally In<br>3 Lines Of Python",
        "s5_badge": "CAPABILITIES",
        "s5_title": "600+ Languages.<br>Zero API Limits.",
        "s5_pills": [
            ("Zero-Shot Cloning", "5–15s reference audio"),
            ("600+ Languages", "English, Bangla & more"),
            ("Apple Silicon MPS", "Fast local inference"),
            ("Whisper Word Sync", "Frame-accurate captions"),
        ],
        "s6_badge": "GET THE SCRIPT",
        "s6_title": "Run OmniVoice<br>On Your Mac Today",
        "s6_cta": 'COMMENT "OMNI"',
        "s6_cta_sub": "WE’LL SEND YOU THE PYTHON SETUP SCRIPT",
        "rafi_label": "RAFI · CREATOR",
        "riya_label": "RIYA · AI MENTOR",
    },
    "bn": {
        "out_html": "omnivoice-bn.html",
        "comp_id": "omnivoice-reel-bn",
        "mp3": "omnivoice_bn.mp3",
        "ts": "omnivoice_bn.timestamps.json",
        "spans": "omnivoice_bn.spans.json",
        "tag": "LOCAL AI VOICE",
        "s1_badge": "COST TRAP",
        "s1_title": "ভয়েস ক্লোনিংয়ের জন্য<br>এখনো মান্থলি সাবস্ক্রিপশন?",
        "s1_old": "$22 / মাস",
        "s1_old_sub": "Cloud API · লিমিটসহ",
        "s1_new": "$0.00 / মাস",
        "s1_new_sub": "১০০% লোকাল · Apple Silicon",
        "s2_badge": "OPEN SOURCE",
        "s2_title": "পরিচিত হও OmniVoice<br>k2-fsa থেকে",
        "s2_sub": "Zero-Shot Voice Cloning · ৬০০+ ভাষা",
        "s3_badge": "REFERENCE CLIP",
        "s3_title": "মাত্র ৫–১৫ সেকেন্ডের<br>তোমার ভয়েস ক্লিপ",
        "s3_sub": "একটা সাধারণ মাইক স্যাম্পলই যথেষ্ট",
        "s4_badge": "APPLE SILICON MPS",
        "s4_title": "মাত্র ৩ লাইন Python এ<br>লোকাল রান করো",
        "s5_badge": "CAPABILITIES",
        "s5_title": "৬০০+ ভাষা সাপোর্ট।<br>কোনো API লিমিট নেই।",
        "s5_pills": [
            ("Zero-Shot Cloning", "৫–১৫ সেকেন্ডের অডিও"),
            ("৬০০+ ভাষা সাপোর্ট", "বাংলা, English ও আরও"),
            ("Apple Silicon MPS", "সুপার ফাস্ট লোকাল রান"),
            ("Whisper Word Sync", "ফ্রেম-পারফেক্ট ক্যাপশন"),
        ],
        "s6_badge": "GET THE SCRIPT",
        "s6_title": "আজই তোমার Mac এ<br>OmniVoice সেটআপ করো",
        "s6_cta": 'COMMENT "OMNI"',
        "s6_cta_sub": "কমেন্ট করলে PYTHON স্ক্রিপ্ট পেয়ে যাবে",
        "rafi_label": "RAFI · CREATOR",
        "riya_label": "RIYA · AI MENTOR",
    },
}


def build_html(lang: str):
    c = CONFIGS[lang]
    mp3_path = os.path.join(AUDIO_DIR, c["mp3"])
    with open(os.path.join(AUDIO_DIR, c["ts"])) as f:
        words = json.load(f)
    with open(os.path.join(AUDIO_DIR, c["spans"])) as f:
        spans = json.load(f)

    dur = round(get_duration(mp3_path) + 0.35, 2)
    s_times = [sp["start"] for sp in spans]
    # 6 lines -> 6 scenes
    t1 = s_times[0]
    t2 = s_times[1]
    t3 = s_times[2]
    t4 = s_times[3]
    t5 = s_times[4]
    t6 = s_times[5]

    words_json = json.dumps(words, ensure_ascii=False)
    spans_json = json.dumps(spans, ensure_ascii=False)

    pills_html = "\n".join(
        f'''          <div class="perk-pill" id="perk-{i}">
            <div class="perk-dot"></div>
            <div>
              <div class="perk-title">{title}</div>
              <div class="perk-sub">{sub}</div>
            </div>
          </div>'''
        for i, (title, sub) in enumerate(c["s5_pills"])
    )

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>{c["comp_id"]}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet" />
<script src="assets/js/gsap.min.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    width: 1080px;
    height: 1920px;
    overflow: hidden;
    background: #F4F7FB;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #0F172A;
  }}
  .stage {{
    position: relative;
    width: 1080px;
    height: 1920px;
    background: radial-gradient(circle at 15% 10%, #EEF2FF 0%, #F8FAFC 45%, #ECFDF5 100%);
    overflow: hidden;
  }}
  .grid-bg {{
    position: absolute;
    inset: 0;
    background-image: linear-gradient(rgba(15, 23, 42, 0.035) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(15, 23, 42, 0.035) 1px, transparent 1px);
    background-size: 56px 56px;
    pointer-events: none;
  }}
  .header {{
    position: absolute;
    top: 72px;
    left: 64px;
    right: 64px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    z-index: 30;
  }}
  .brand-left {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}
  .brand-icon {{
    width: 58px;
    height: 58px;
    border-radius: 16px;
    background: linear-gradient(135deg, #2563EB, #7C3AED);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-weight: 900;
    font-size: 26px;
    box-shadow: 0 10px 24px rgba(37, 99, 235, 0.25);
  }}
  .brand-name {{
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #0F172A;
  }}
  .brand-sub {{
    font-size: 16px;
    font-weight: 700;
    color: #64748B;
    letter-spacing: 0.06em;
  }}
  .tag-pill {{
    padding: 10px 20px;
    border-radius: 999px;
    background: #FFFFFF;
    border: 2px solid #E2E8F0;
    font-size: 18px;
    font-weight: 800;
    color: #2563EB;
    letter-spacing: 0.06em;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
  }}
  .speaker-bar {{
    position: absolute;
    top: 164px;
    left: 64px;
    right: 64px;
    display: flex;
    justify-content: center;
    z-index: 30;
  }}
  .speaker-pill {{
    padding: 10px 26px;
    border-radius: 999px;
    font-size: 20px;
    font-weight: 800;
    letter-spacing: 0.06em;
    background: #FFFFFF;
    border: 2px solid #10B981;
    color: #047857;
    box-shadow: 0 8px 20px rgba(16, 185, 129, 0.14);
  }}
  .speaker-pill.riya {{
    border-color: #6366F1;
    color: #4338CA;
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.16);
  }}
  .card-area {{
    position: absolute;
    top: 245px;
    left: 64px;
    right: 64px;
    height: 1120px;
    z-index: 20;
  }}
  .scene {{
    position: absolute;
    inset: 0;
    background: #FFFFFF;
    border: 2px solid #E2E8F0;
    border-radius: 40px;
    padding: 64px 56px;
    box-shadow: 0 28px 60px rgba(15, 23, 42, 0.08);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    opacity: 0;
  }}
  .scene-top {{
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .scene-badge {{
    padding: 10px 20px;
    border-radius: 12px;
    background: #EFF6FF;
    color: #1D4ED8;
    font-size: 20px;
    font-weight: 800;
    letter-spacing: 0.08em;
  }}
  .scene-num {{
    font-size: 22px;
    font-weight: 800;
    color: #94A3B8;
  }}
  .scene-title {{
    font-size: 62px;
    font-weight: 900;
    line-height: 1.14;
    letter-spacing: -0.03em;
    color: #0F172A;
    margin-top: 28px;
  }}
  .scene-sub {{
    font-size: 30px;
    font-weight: 600;
    color: #475569;
    margin-top: 18px;
    line-height: 1.4;
  }}
  .compare-box {{
    display: flex;
    flex-direction: column;
    gap: 24px;
    margin-top: 24px;
  }}
  .price-card {{
    border-radius: 28px;
    padding: 36px 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .price-old {{
    background: #FEF2F2;
    border: 2px solid #FECACA;
  }}
  .price-new {{
    background: #ECFDF5;
    border: 2px solid #A7F3D0;
  }}
  .price-val {{
    font-size: 56px;
    font-weight: 900;
  }}
  .price-old .price-val {{ color: #DC2626; }}
  .price-new .price-val {{ color: #059669; }}
  .price-lbl {{
    font-size: 26px;
    font-weight: 700;
    color: #334155;
  }}
  .hero-badge-box {{
    background: linear-gradient(135deg, #EEF2FF 0%, #F8FAFC 100%);
    border: 2px solid #C7D2FE;
    border-radius: 32px;
    padding: 56px 40px;
    text-align: center;
  }}
  .hero-logo-txt {{
    font-size: 76px;
    font-weight: 900;
    background: linear-gradient(135deg, #2563EB, #7C3AED);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.03em;
  }}
  .hero-org {{
    margin-top: 14px;
    font-size: 28px;
    font-weight: 800;
    color: #4338CA;
    letter-spacing: 0.08em;
  }}
  .wave-card {{
    background: #F8FAFC;
    border: 2px solid #E2E8F0;
    border-radius: 28px;
    padding: 48px 36px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 28px;
  }}
  .wave-bars {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    height: 180px;
  }}
  .wbar {{
    width: 18px;
    border-radius: 999px;
    background: linear-gradient(180deg, #2563EB, #10B981);
  }}
  .clip-pill {{
    padding: 14px 32px;
    border-radius: 999px;
    background: #0F172A;
    color: #FFFFFF;
    font-size: 28px;
    font-weight: 800;
  }}
  .terminal {{
    background: #0F172A;
    border-radius: 28px;
    padding: 36px;
    color: #E2E8F0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 25px;
    line-height: 1.65;
    box-shadow: 0 20px 44px rgba(15, 23, 42, 0.22);
  }}
  .term-dots {{
    display: flex;
    gap: 12px;
    margin-bottom: 24px;
  }}
  .dot {{ width: 16px; height: 16px; border-radius: 50%; }}
  .d-red {{ background: #EF4444; }}
  .d-yel {{ background: #F59E0B; }}
  .d-grn {{ background: #10B981; }}
  .c-kw {{ color: #C084FC; }}
  .c-fn {{ color: #60A5FA; }}
  .c-str {{ color: #34D399; }}
  .c-cmt {{ color: #94A3B8; }}
  .perks-list {{
    display: flex;
    flex-direction: column;
    gap: 22px;
  }}
  .perk-pill {{
    display: flex;
    align-items: center;
    gap: 24px;
    padding: 26px 32px;
    border-radius: 24px;
    background: #F8FAFC;
    border: 2px solid #E2E8F0;
  }}
  .perk-dot {{
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: #2563EB;
    flex-shrink: 0;
  }}
  .perk-title {{ font-size: 32px; font-weight: 800; color: #0F172A; }}
  .perk-sub {{ font-size: 24px; font-weight: 600; color: #64748B; margin-top: 4px; }}
  .cta-box {{
    background: linear-gradient(135deg, #2563EB, #4F46E5);
    border-radius: 32px;
    padding: 52px 40px;
    text-align: center;
    color: #FFFFFF;
    box-shadow: 0 22px 44px rgba(37, 99, 235, 0.28);
  }}
  .cta-main {{ font-size: 56px; font-weight: 900; letter-spacing: 0.02em; }}
  .cta-sub {{ font-size: 24px; font-weight: 700; opacity: 0.92; margin-top: 14px; }}
  .caption-box {{
    position: absolute;
    bottom: 130px;
    left: 64px;
    right: 64px;
    min-height: 220px;
    background: #FFFFFF;
    border: 2px solid #E2E8F0;
    border-radius: 32px;
    padding: 36px 42px;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    gap: 14px 18px;
    box-shadow: 0 20px 44px rgba(15, 23, 42, 0.08);
    z-index: 30;
  }}
  .cap-word {{
    font-size: 46px;
    font-weight: 800;
    color: #475569;
    padding: 6px 14px;
    border-radius: 14px;
  }}
  .cap-word.active-rafi {{
    background: #10B981;
    color: #FFFFFF;
    transform: scale(1.06);
  }}
  .cap-word.active-riya {{
    background: #4F46E5;
    color: #FFFFFF;
    transform: scale(1.06);
  }}
</style>
</head>
<body>
<div class="stage" data-composition-id="{c['comp_id']}" data-width="1080" data-height="1920" data-fps="30" data-duration="{dur}">
  <div class="grid-bg"></div>
  <audio id="voiceover-audio" src="assets/audio/{c['mp3']}" data-start="0"></audio>
  <audio id="bg-drone" src="assets/sfx/tech_drone.wav" data-start="0" data-volume="0.06"></audio>

  <div class="header">
    <div class="brand-left">
      <div class="brand-icon">OV</div>
      <div>
        <div class="brand-name">OmniVoice</div>
        <div class="brand-sub">k2-fsa · APPLE SILICON</div>
      </div>
    </div>
    <div class="tag-pill">{c['tag']}</div>
  </div>

  <div class="speaker-bar">
    <div class="speaker-pill" id="speaker-pill">{c['rafi_label']}</div>
  </div>

  <div class="card-area">
    <div class="scene" id="scene-1">
      <div>
        <div class="scene-top">
          <div class="scene-badge">{c['s1_badge']}</div>
          <div class="scene-num">01 / 06</div>
        </div>
        <div class="scene-title">{c['s1_title']}</div>
      </div>
      <div class="compare-box">
        <div class="price-card price-old">
          <div>
            <div class="price-lbl">Cloud Voice APIs</div>
            <div class="scene-sub" style="margin-top:6px;font-size:24px;">{c['s1_old_sub']}</div>
          </div>
          <div class="price-val">{c['s1_old']}</div>
        </div>
        <div class="price-card price-new">
          <div>
            <div class="price-lbl">OmniVoice Local</div>
            <div class="scene-sub" style="margin-top:6px;font-size:24px;">{c['s1_new_sub']}</div>
          </div>
          <div class="price-val">{c['s1_new']}</div>
        </div>
      </div>
    </div>

    <div class="scene" id="scene-2">
      <div>
        <div class="scene-top">
          <div class="scene-badge">{c['s2_badge']}</div>
          <div class="scene-num">02 / 06</div>
        </div>
        <div class="scene-title">{c['s2_title']}</div>
        <div class="scene-sub">{c['s2_sub']}</div>
      </div>
      <div class="hero-badge-box">
        <div class="hero-logo-txt">k2-fsa / OmniVoice</div>
        <div class="hero-org">600+ LANGUAGES · ZERO-SHOT CLONING</div>
      </div>
    </div>

    <div class="scene" id="scene-3">
      <div>
        <div class="scene-top">
          <div class="scene-badge">{c['s3_badge']}</div>
          <div class="scene-num">03 / 06</div>
        </div>
        <div class="scene-title">{c['s3_title']}</div>
        <div class="scene-sub">{c['s3_sub']}</div>
      </div>
      <div class="wave-card">
        <div class="wave-bars">
          <div class="wbar" style="height:60px"></div>
          <div class="wbar" style="height:120px"></div>
          <div class="wbar" style="height:165px"></div>
          <div class="wbar" style="height:95px"></div>
          <div class="wbar" style="height:150px"></div>
          <div class="wbar" style="height:175px"></div>
          <div class="wbar" style="height:110px"></div>
          <div class="wbar" style="height:140px"></div>
          <div class="wbar" style="height:80px"></div>
        </div>
        <div class="clip-pill">5–15s Reference Audio (.wav / .mp3)</div>
      </div>
    </div>

    <div class="scene" id="scene-4">
      <div>
        <div class="scene-top">
          <div class="scene-badge">{c['s4_badge']}</div>
          <div class="scene-num">04 / 06</div>
        </div>
        <div class="scene-title">{c['s4_title']}</div>
      </div>
      <div class="terminal">
        <div class="term-dots"><div class="dot d-red"></div><div class="dot d-yel"></div><div class="dot d-grn"></div></div>
        <div><span class="c-kw">from</span> omnivoice <span class="c-kw">import</span> OmniVoice</div>
        <div>model = OmniVoice.<span class="c-fn">from_pretrained</span>(</div>
        <div>&nbsp;&nbsp;<span class="c-str">"k2-fsa/OmniVoice"</span>,</div>
        <div>&nbsp;&nbsp;device_map=<span class="c-str">"mps"</span></div>
        <div>)</div>
        <div><span class="c-cmt"># Clones locally on your Mac</span></div>
        <div>wav = model.<span class="c-fn">generate</span>(text, ref_audio)</div>
      </div>
    </div>

    <div class="scene" id="scene-5">
      <div>
        <div class="scene-top">
          <div class="scene-badge">{c['s5_badge']}</div>
          <div class="scene-num">05 / 06</div>
        </div>
        <div class="scene-title">{c['s5_title']}</div>
      </div>
      <div class="perks-list">
{pills_html}
      </div>
    </div>

    <div class="scene" id="scene-6">
      <div>
        <div class="scene-top">
          <div class="scene-badge">{c['s6_badge']}</div>
          <div class="scene-num">06 / 06</div>
        </div>
        <div class="scene-title">{c['s6_title']}</div>
      </div>
      <div class="cta-box">
        <div class="cta-main">{c['s6_cta']}</div>
        <div class="cta-sub">{c['s6_cta_sub']}</div>
      </div>
    </div>
  </div>

  <div class="caption-box" id="caption-box"></div>
</div>

<script>
const WORDS = {words_json};
const SPANS = {spans_json};
const RAFI_LABEL = {json.dumps(c["rafi_label"])};
const RIYA_LABEL = {json.dumps(c["riya_label"])};

const capBox = document.getElementById('caption-box');
const speakerPill = document.getElementById('speaker-pill');

let lastGroup = -1;
function updateHUD(t) {{
  let activeSpan = SPANS[0];
  for (let i = 0; i < SPANS.length; i++) {{
    if (t >= SPANS[i].start) activeSpan = SPANS[i];
  }}
  if (activeSpan.speaker === 'Riya') {{
    speakerPill.textContent = RIYA_LABEL;
    speakerPill.className = 'speaker-pill riya';
  }} else {{
    speakerPill.textContent = RAFI_LABEL;
    speakerPill.className = 'speaker-pill';
  }}

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

  const grp = activeWord.g;
  if (grp !== lastGroup) {{
    lastGroup = grp;
    const grpWords = WORDS.filter(w => w.g === grp);
    capBox.innerHTML = '';
    grpWords.forEach((w, idx) => {{
      const el = document.createElement('span');
      el.className = 'cap-word';
      el.textContent = w.word;
      el.dataset.idx = idx;
      capBox.appendChild(el);
    }});
  }}
  const grpWords = WORDS.filter(w => w.g === grp);
  const children = capBox.children;
  for (let i = 0; i < grpWords.length; i++) {{
    const w = grpWords[i];
    const el = children[i];
    if (!el) continue;
    const isCurrent = (t >= w.start && t <= w.end + 0.08);
    el.className = 'cap-word' + (isCurrent ? (w.speaker === 'Riya' ? ' active-riya' : ' active-rafi') : '');
  }}
}}

const tl = gsap.timeline({{
  paused: true,
  onUpdate: function() {{ updateHUD(this.time()); }}
}});

const scenes = ['#scene-1', '#scene-2', '#scene-3', '#scene-4', '#scene-5', '#scene-6'];
const times = [{t1}, {t2}, {t3}, {t4}, {t5}, {t6}];

scenes.forEach((sel, i) => {{
  const tStart = times[i];
  tl.fromTo(sel, {{ opacity: 0, y: 28, scale: 0.97 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.35, ease: 'power3.out' }}, tStart);
  if (i < scenes.length - 1) {{
    tl.to(sel, {{ opacity: 0, y: -20, duration: 0.25, ease: 'power2.in' }}, times[i + 1] - 0.15);
  }}
}});

tl.to({{}}, {{ duration: 0.1 }}, {dur});
updateHUD(0);

window.__timelines = window.__timelines || {{}};
window.__timelines["{c['comp_id']}"] = tl;
</script>
</body>
</html>
'''
    out_path = os.path.join(ENGINE_DIR, c["out_html"])
    with open(out_path, "w") as f:
        f.write(html)
    print(f"Generated {out_path} (duration={dur}s)")


if __name__ == "__main__":
    for lang in ("en", "bn"):
        build_html(lang)
