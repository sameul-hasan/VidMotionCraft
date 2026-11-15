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
        "out_html": "handy-en.html",
        "comp_id": "handy-reel-en",
        "mp3": "handy_en.mp3",
        "ts": "handy_en.timestamps.json",
        "spans": "handy_en.spans.json",
        "tag": "OFFLINE DICTATION",
        "s1_badge": "SPEED BOOST",
        "s1_title": "Stop Typing Long<br>Prompts By Hand",
        "s1_old": "45 WPM",
        "s1_old_sub": "Manual Typing · Slow Flow",
        "s1_new": "150+ WPM",
        "s1_new_sub": "3× Faster Voice Dictation",
        "s2_badge": "OPEN SOURCE",
        "s2_title": "Meet Handy<br>Offline Speech-to-Text",
        "s2_sub": "Free Local Alternative to Wispr Flow · Mac, Win & Linux",
        "s3_badge": "GLOBAL HOTKEY",
        "s3_title": "Works Inside<br>Any App On Mac",
        "s3_sub": "Press once to speak, release to paste clean text",
        "s4_badge": "LOCAL MODELS",
        "s4_title": "Whisper & Parakeet<br>Run 100% Offline",
        "s4_pills": [
            ("Whisper Local Model", "Multilingual accuracy on CPU/GPU"),
            ("Parakeet V3 Model", "Ultra-low latency English"),
            ("Zero Cloud Uploads", "Audio never leaves your Mac"),
        ],
        "s5_badge": "HONEST CHECK",
        "s5_title": "Fast Dictation Only.<br>Zero Subscriptions.",
        "s5_pills": [
            ("Pure Speech-to-Text", "Pastes directly into editor, notes, chat"),
            ("Not a Click-Bot", "Focused on ultra-fast typing replacement"),
            ("$0.00 Forever", "Open-source MIT · cjpais/Handy"),
        ],
        "s6_badge": "GET HANDY",
        "s6_title": "Dictate 3× Faster<br>For Free Today",
        "s6_cta": 'COMMENT "HANDY"',
        "s6_cta_sub": "WE’LL SEND THE DOWNLOAD LINK & SETUP GUIDE",
        "rafi_label": "RAFI · CREATOR",
        "riya_label": "RIYA · AI MENTOR",
    },
    "bn": {
        "out_html": "handy-bn.html",
        "comp_id": "handy-reel-bn",
        "mp3": "handy_bn.mp3",
        "ts": "handy_bn.timestamps.json",
        "spans": "handy_bn.spans.json",
        "tag": "OFFLINE DICTATION",
        "s1_badge": "SPEED BOOST",
        "s1_title": "হাতে লম্বা প্রম্পট<br>টাইপ করা বন্ধ করো",
        "s1_old": "45 WPM",
        "s1_old_sub": "ম্যানুয়াল টাইপিং · স্লো",
        "s1_new": "150+ WPM",
        "s1_new_sub": "৩ গুণ ফাস্ট ভয়েস ডিকটেশন",
        "s2_badge": "OPEN SOURCE",
        "s2_title": "পরিচিত হও Handy<br>অফলাইন স্পিচ-টু-টেক্সট",
        "s2_sub": "Wispr Flow এর ফ্রি লোকাল অল্টারনেটিভ · Mac, Win, Linux",
        "s3_badge": "GLOBAL HOTKEY",
        "s3_title": "যেকোনো অ্যাপের ভেতর<br>সরাসরি কাজ করে",
        "s3_sub": "একবার চাপো, কথা বলো, সাথে সাথে টেক্সট পেস্ট",
        "s4_badge": "LOCAL MODELS",
        "s4_title": "Whisper ও Parakeet<br>১০০% অফলাইন রান হয়",
        "s4_pills": [
            ("Whisper Local Model", "বাংলা ও English হাই একুরেসি"),
            ("Parakeet V3 Model", "সুপার ফাস্ট রিয়েল-টাইম ডিকটেশন"),
            ("Zero Cloud Uploads", "তোমার অডিও কখনোই ক্লাউডে যায় না"),
        ],
        "s5_badge": "PRIVACY FIRST",
        "s5_title": "কোনো ক্লাউড আপলোড নেই।<br>মান্থলি ফি-ও নেই।",
        "s5_pills": [
            ("১০০% লোকাল প্রসেসিং", "তোমার Mac এই সব ট্রান্সক্রিপশন"),
            ("যেকোনো এডিটর বা চ্যাটে", "VS Code, Notes, Browser সব জায়গায়"),
            ("$0.00 / আজীবন ফ্রি", "Open-Source · cjpais/Handy v0.10.1"),
        ],
        "s6_badge": "GET HANDY",
        "s6_title": "আজ থেকেই ৩ গুণ ফাস্ট<br>ভয়েস টাইপিং শুরু করো",
        "s6_cta": 'COMMENT "HANDY"',
        "s6_cta_sub": "ডাউনলোড লিংক ও সেটআপ গাইড পেতে কমেন্ট করো",
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
    t1, t2, t3, t4, t5, t6 = s_times

    words_json = json.dumps(words, ensure_ascii=False)
    spans_json = json.dumps(spans, ensure_ascii=False)

    s4_pills_html = "\n".join(
        f'''          <div class="perk-pill">
            <div class="perk-dot teal"></div>
            <div>
              <div class="perk-title">{title}</div>
              <div class="perk-sub">{sub}</div>
            </div>
          </div>'''
        for title, sub in c["s4_pills"]
    )

    s5_pills_html = "\n".join(
        f'''          <div class="perk-pill">
            <div class="perk-dot amber"></div>
            <div>
              <div class="perk-title">{title}</div>
              <div class="perk-sub">{sub}</div>
            </div>
          </div>'''
        for title, sub in c["s5_pills"]
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
    background: radial-gradient(circle at 85% 12%, #ECFEFF 0%, #F8FAFC 48%, #FFFBEB 100%);
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
    background: linear-gradient(135deg, #0D9488, #0284C7);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-weight: 900;
    font-size: 26px;
    box-shadow: 0 10px 24px rgba(13, 148, 136, 0.25);
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
    color: #0D9488;
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
    border: 2px solid #0D9488;
    color: #0F766E;
    box-shadow: 0 8px 20px rgba(13, 148, 136, 0.14);
  }}
  .speaker-pill.riya {{
    border-color: #D97706;
    color: #B45309;
    box-shadow: 0 8px 20px rgba(217, 119, 6, 0.16);
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
    background: #F0FDFA;
    color: #0F766E;
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
    background: #F0FDFA;
    border: 2px solid #99F6E4;
  }}
  .price-val {{
    font-size: 54px;
    font-weight: 900;
  }}
  .price-old .price-val {{ color: #DC2626; }}
  .price-new .price-val {{ color: #0D9488; }}
  .price-lbl {{
    font-size: 26px;
    font-weight: 700;
    color: #334155;
  }}
  .hero-badge-box {{
    background: linear-gradient(135deg, #F0FDFA 0%, #F8FAFC 100%);
    border: 2px solid #99F6E4;
    border-radius: 32px;
    padding: 56px 40px;
    text-align: center;
  }}
  .hero-logo-txt {{
    font-size: 76px;
    font-weight: 900;
    background: linear-gradient(135deg, #0D9488, #0284C7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.03em;
  }}
  .hero-org {{
    margin-top: 14px;
    font-size: 26px;
    font-weight: 800;
    color: #0F766E;
    letter-spacing: 0.08em;
  }}
  .keycap-stage {{
    background: #F8FAFC;
    border: 2px solid #E2E8F0;
    border-radius: 28px;
    padding: 56px 36px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 28px;
  }}
  .keycap-row {{
    display: flex;
    align-items: center;
    gap: 20px;
  }}
  .keycap {{
    padding: 24px 40px;
    border-radius: 22px;
    background: #FFFFFF;
    border: 3px solid #CBD5E1;
    box-shadow: 0 10px 0 #CBD5E1;
    font-family: 'JetBrains Mono', monospace;
    font-size: 38px;
    font-weight: 800;
    color: #0F172A;
  }}
  .key-plus {{
    font-size: 40px;
    font-weight: 900;
    color: #64748B;
  }}
  .clip-pill {{
    padding: 14px 32px;
    border-radius: 999px;
    background: #0F172A;
    color: #FFFFFF;
    font-size: 26px;
    font-weight: 800;
  }}
  .perks-list {{
    display: flex;
    flex-direction: column;
    gap: 22px;
  }}
  .perk-pill {{
    display: flex;
    align-items: center;
    gap: 24px;
    padding: 28px 32px;
    border-radius: 24px;
    background: #F8FAFC;
    border: 2px solid #E2E8F0;
  }}
  .perk-dot {{
    width: 22px;
    height: 22px;
    border-radius: 50%;
    flex-shrink: 0;
  }}
  .perk-dot.teal {{ background: #0D9488; }}
  .perk-dot.amber {{ background: #D97706; }}
  .perk-title {{ font-size: 32px; font-weight: 800; color: #0F172A; }}
  .perk-sub {{ font-size: 24px; font-weight: 600; color: #64748B; margin-top: 4px; }}
  .cta-box {{
    background: linear-gradient(135deg, #0D9488, #0284C7);
    border-radius: 32px;
    padding: 52px 40px;
    text-align: center;
    color: #FFFFFF;
    box-shadow: 0 22px 44px rgba(13, 148, 136, 0.28);
  }}
  .cta-main {{ font-size: 54px; font-weight: 900; letter-spacing: 0.02em; }}
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
    background: #0D9488;
    color: #FFFFFF;
    transform: scale(1.06);
  }}
  .cap-word.active-riya {{
    background: #D97706;
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
      <div class="brand-icon">HY</div>
      <div>
        <div class="brand-name">Handy</div>
        <div class="brand-sub">cjpais / Handy · v0.10.1</div>
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
            <div class="price-lbl">Keyboard Typing</div>
            <div class="scene-sub" style="margin-top:6px;font-size:24px;">{c['s1_old_sub']}</div>
          </div>
          <div class="price-val">{c['s1_old']}</div>
        </div>
        <div class="price-card price-new">
          <div>
            <div class="price-lbl">Handy Dictation</div>
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
        <div class="hero-logo-txt">cjpais / Handy</div>
        <div class="hero-org">OFFLINE · PRIVACY FIRST · $0/MONTH</div>
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
      <div class="keycap-stage">
        <div class="keycap-row">
          <div class="keycap">⌥ Option</div>
          <div class="key-plus">+</div>
          <div class="keycap">Space</div>
        </div>
        <div class="clip-pill">Speak → Instant Paste Anywhere</div>
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
      <div class="perks-list">
{s4_pills_html}
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
{s5_pills_html}
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
