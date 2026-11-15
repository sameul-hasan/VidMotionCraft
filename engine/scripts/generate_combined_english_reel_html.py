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
    mp3_path = os.path.join(AUDIO_DIR, "combined_en.mp3")
    with open(os.path.join(AUDIO_DIR, "combined_en.timestamps.json")) as f:
        words = json.load(f)
    with open(os.path.join(AUDIO_DIR, "combined_en.spans.json")) as f:
        spans = json.load(f)

    dur = round(get_duration(mp3_path) + 0.35, 2)
    t1, t2, t3, t4, t5, t6 = [sp["start"] for sp in spans]

    words_json = json.dumps(words, ensure_ascii=False)
    spans_json = json.dumps(spans, ensure_ascii=False)
    comp_id = "handy-omnivoice-en"

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>{comp_id}</title>
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
    background: radial-gradient(circle at 15% 10%, #ECFDF5 0%, #F8FAFC 48%, #EEF2FF 100%);
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
    background: linear-gradient(135deg, #0D9488, #4F46E5);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-weight: 900;
    font-size: 24px;
    box-shadow: 0 10px 24px rgba(79, 70, 229, 0.24);
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
    border: 2px solid #059669;
    color: #047857;
    box-shadow: 0 8px 20px rgba(5, 150, 105, 0.14);
  }}
  .speaker-pill.sara {{
    border-color: #4F46E5;
    color: #4338CA;
    box-shadow: 0 8px 20px rgba(79, 70, 229, 0.16);
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
    background: #ECFDF5;
    color: #047857;
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
    font-size: 60px;
    font-weight: 900;
    line-height: 1.15;
    letter-spacing: -0.03em;
    color: #0F172A;
    margin-top: 28px;
  }}
  .scene-sub {{
    font-size: 28px;
    font-weight: 600;
    color: #475569;
    margin-top: 18px;
    line-height: 1.45;
  }}
  .compare-box {{
    display: flex;
    flex-direction: column;
    gap: 24px;
  }}
  .price-card {{
    border-radius: 28px;
    padding: 36px 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .price-old {{ background: #FEF2F2; border: 2px solid #FECACA; }}
  .price-new {{ background: #ECFDF5; border: 2px solid #A7F3D0; }}
  .price-val {{ font-size: 52px; font-weight: 900; }}
  .price-old .price-val {{ color: #DC2626; }}
  .price-new .price-val {{ color: #059669; }}
  .price-lbl {{ font-size: 26px; font-weight: 700; color: #334155; }}
  .keycap-stage {{
    background: #F8FAFC;
    border: 2px solid #E2E8F0;
    border-radius: 28px;
    padding: 52px 36px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 26px;
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
    font-size: 36px;
    font-weight: 800;
    color: #0F172A;
  }}
  .key-plus {{ font-size: 38px; font-weight: 900; color: #64748B; }}
  .clip-pill {{
    padding: 14px 32px;
    border-radius: 999px;
    background: #0F172A;
    color: #FFFFFF;
    font-size: 24px;
    font-weight: 800;
  }}
  .flow-box {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
  }}
  .flow-node {{
    width: 100%;
    padding: 34px 36px;
    border-radius: 26px;
    background: #F8FAFC;
    border: 2px solid #CBD5E1;
    text-align: center;
  }}
  .flow-node.teal {{ background: #F0FDFA; border-color: #99F6E4; }}
  .flow-node.indigo {{ background: #EEF2FF; border-color: #C7D2FE; }}
  .flow-title {{ font-size: 36px; font-weight: 900; color: #0F172A; }}
  .flow-sub {{ font-size: 24px; font-weight: 700; color: #475569; margin-top: 6px; }}
  .flow-arrow {{ font-size: 40px; font-weight: 900; color: #64748B; }}
  .terminal {{
    background: #0F172A;
    border-radius: 28px;
    padding: 36px;
    color: #E2E8F0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 24px;
    line-height: 1.65;
    box-shadow: 0 20px 44px rgba(15, 23, 42, 0.22);
  }}
  .term-dots {{ display: flex; gap: 12px; margin-bottom: 22px; }}
  .dot {{ width: 16px; height: 16px; border-radius: 50%; }}
  .d-red {{ background: #EF4444; }}
  .d-yel {{ background: #F59E0B; }}
  .d-grn {{ background: #10B981; }}
  .c-kw {{ color: #C084FC; }}
  .c-fn {{ color: #60A5FA; }}
  .c-str {{ color: #34D399; }}
  .c-cmt {{ color: #94A3B8; }}
  .perks-list {{ display: flex; flex-direction: column; gap: 22px; }}
  .perk-pill {{
    display: flex;
    align-items: center;
    gap: 24px;
    padding: 28px 32px;
    border-radius: 24px;
    background: #F8FAFC;
    border: 2px solid #E2E8F0;
  }}
  .perk-dot {{ width: 22px; height: 22px; border-radius: 50%; background: #059669; flex-shrink: 0; }}
  .perk-title {{ font-size: 32px; font-weight: 800; color: #0F172A; }}
  .perk-sub {{ font-size: 24px; font-weight: 600; color: #64748B; margin-top: 4px; }}
  .cta-box {{
    background: linear-gradient(135deg, #0D9488, #4F46E5);
    border-radius: 32px;
    padding: 52px 40px;
    text-align: center;
    color: #FFFFFF;
    box-shadow: 0 22px 44px rgba(79, 70, 229, 0.28);
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
    background: #059669;
    color: #FFFFFF;
    transform: scale(1.06);
  }}
  .cap-word.active-sara {{
    background: #4F46E5;
    color: #FFFFFF;
    transform: scale(1.06);
  }}
</style>
</head>
<body>
<div class="stage" data-composition-id="{comp_id}" data-width="1080" data-height="1920" data-fps="30" data-duration="{dur}">
  <div class="grid-bg"></div>
  <audio id="voiceover-audio" src="assets/audio/combined_en.mp3" data-start="0"></audio>
  <audio id="bg-drone" src="assets/sfx/tech_drone.wav" data-start="0" data-volume="0.06"></audio>

  <div class="header">
    <div class="brand-left">
      <div class="brand-icon">HO</div>
      <div>
        <div class="brand-name">Handy + OmniVoice</div>
        <div class="brand-sub">100% LOCAL AI STACK</div>
      </div>
    </div>
    <div class="tag-pill">OFFLINE WORKFLOW</div>
  </div>

  <div class="speaker-bar">
    <div class="speaker-pill" id="speaker-pill">RAFI · VOICE CLONE</div>
  </div>

  <div class="card-area">
    <div class="scene" id="scene-1">
      <div>
        <div class="scene-top">
          <div class="scene-badge">FREE LOCAL STACK</div>
          <div class="scene-num">01 / 06</div>
        </div>
        <div class="scene-title">Stop Typing &amp; Paying<br>For Cloud AI Voices!</div>
      </div>
      <div class="compare-box">
        <div class="price-card price-old">
          <div>
            <div class="price-lbl">Typing + Cloud TTS</div>
            <div class="scene-sub" style="margin-top:6px;font-size:24px;">Slow typing + monthly subscriptions</div>
          </div>
          <div class="price-val">$22 / mo</div>
        </div>
        <div class="price-card price-new">
          <div>
            <div class="price-lbl">Handy + OmniVoice</div>
            <div class="scene-sub" style="margin-top:6px;font-size:24px;">100% Offline · Runs Locally on Mac</div>
          </div>
          <div class="price-val">$0.00 / mo</div>
        </div>
      </div>
    </div>

    <div class="scene" id="scene-2">
      <div>
        <div class="scene-top">
          <div class="scene-badge">STEP 01 · HANDY</div>
          <div class="scene-num">02 / 06</div>
        </div>
        <div class="scene-title">Step 1: Write Scripts<br>3× Faster With Handy</div>
        <div class="scene-sub">Whisper &amp; Parakeet run locally and paste clean text</div>
      </div>
      <div class="keycap-stage">
        <div class="keycap-row">
          <div class="keycap">⌥ Option</div>
          <div class="key-plus">+</div>
          <div class="keycap">Space</div>
        </div>
        <div class="clip-pill">Speak → Instant Script Anywhere</div>
      </div>
    </div>

    <div class="scene" id="scene-3">
      <div>
        <div class="scene-top">
          <div class="scene-badge">THE PIPELINE</div>
          <div class="scene-num">03 / 06</div>
        </div>
        <div class="scene-title">Script Is Ready.<br>Now For The Voiceover?</div>
      </div>
      <div class="flow-box">
        <div class="flow-node teal">
          <div class="flow-title">1. Handy (Voice → Text)</div>
          <div class="flow-sub">Offline dictation for 3× faster writing</div>
        </div>
        <div class="flow-arrow">↓</div>
        <div class="flow-node indigo">
          <div class="flow-title">2. OmniVoice (Text → Voice)</div>
          <div class="flow-sub">Zero-shot voice cloning on your Mac</div>
        </div>
      </div>
    </div>

    <div class="scene" id="scene-4">
      <div>
        <div class="scene-top">
          <div class="scene-badge">STEP 02 · OMNIVOICE</div>
          <div class="scene-num">04 / 06</div>
        </div>
        <div class="scene-title">Step 2: Clone Your Voice<br>From A 10s Mic Clip</div>
      </div>
      <div class="terminal">
        <div class="term-dots"><div class="dot d-red"></div><div class="dot d-yel"></div><div class="dot d-grn"></div></div>
        <div><span class="c-kw">from</span> omnivoice <span class="c-kw">import</span> OmniVoice</div>
        <div>prompt = model.<span class="c-fn">create_voice_clone_prompt</span>(</div>
        <div>&nbsp;&nbsp;ref_audio=<span class="c-str">"my_voice_10s.wav"</span></div>
        <div>)</div>
        <div><span class="c-cmt"># Generate full reel voiceover locally</span></div>
        <div>wav = model.<span class="c-fn">generate</span>(text, language=<span class="c-str">"English"</span>)</div>
      </div>
    </div>

    <div class="scene" id="scene-5">
      <div>
        <div class="scene-top">
          <div class="scene-badge">WHY IT WORKS</div>
          <div class="scene-num">05 / 06</div>
        </div>
        <div class="scene-title">Fast Writing + Your Voice.<br>Zero Cloud Or Fees!</div>
      </div>
      <div class="perks-list">
        <div class="perk-pill">
          <div class="perk-dot"></div>
          <div>
            <div class="perk-title">Handy: 3× Faster Script Writing</div>
            <div class="perk-sub">Instant Option + Space voice dictation</div>
          </div>
        </div>
        <div class="perk-pill">
          <div class="perk-dot"></div>
          <div>
            <div class="perk-title">OmniVoice: Real Voice Cloning</div>
            <div class="perk-sub">Natural tone from a 10s reference clip</div>
          </div>
        </div>
        <div class="perk-pill">
          <div class="perk-dot"></div>
          <div>
            <div class="perk-title">$0.00 · 100% Private &amp; Offline</div>
            <div class="perk-sub">Everything runs locally on your Mac</div>
          </div>
        </div>
      </div>
    </div>

    <div class="scene" id="scene-6">
      <div>
        <div class="scene-top">
          <div class="scene-badge">GET BOTH TOOLS</div>
          <div class="scene-num">06 / 06</div>
        </div>
        <div class="scene-title">Want The Setup Guide<br>&amp; Python Script?</div>
      </div>
      <div class="cta-box">
        <div class="cta-main">COMMENT "LOCAL"</div>
        <div class="cta-sub">WE’LL SEND YOU THE FULL GUIDE &amp; PYTHON SCRIPT</div>
      </div>
    </div>
  </div>

  <div class="caption-box" id="caption-box"></div>
</div>

<script>
const WORDS = {words_json};
const SPANS = {spans_json};
const capBox = document.getElementById('caption-box');
const speakerPill = document.getElementById('speaker-pill');

let lastGroup = -1;
function updateHUD(t) {{
  let activeSpan = SPANS[0];
  for (let i = 0; i < SPANS.length; i++) {{
    if (t >= SPANS[i].start) activeSpan = SPANS[i];
  }}
  if (activeSpan.speaker === 'Sara') {{
    speakerPill.textContent = 'SARA · VOICE CLONE';
    speakerPill.className = 'speaker-pill sara';
  }} else {{
    speakerPill.textContent = 'RAFI · VOICE CLONE';
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
    grpWords.forEach((w) => {{
      const el = document.createElement('span');
      el.className = 'cap-word';
      el.textContent = w.word;
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
    el.className = 'cap-word' + (isCurrent ? (w.speaker === 'Sara' ? ' active-sara' : ' active-rafi') : '');
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
window.__timelines["{comp_id}"] = tl;
</script>
</body>
</html>
'''
    out_path = os.path.join(ENGINE_DIR, "handy-omnivoice-en.html")
    with open(out_path, "w") as f:
        f.write(html)
    print(f"Generated {out_path} (duration={dur}s)")


if __name__ == "__main__":
    main()
