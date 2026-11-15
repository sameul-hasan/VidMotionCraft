import json
import os
import re
import subprocess

ENGINE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(ENGINE_DIR, "assets/audio")
MAPS_DIR = os.path.join(ENGINE_DIR, "assets/maps")


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


def load_svg_inner(filename: str) -> str:
    with open(os.path.join(MAPS_DIR, filename), encoding="utf-8") as f:
        txt = f.read()
    m = re.search(r"<svg[^>]*>(.*)</svg>", txt, flags=re.S)
    return m.group(1).strip() if m else ""


def main():
    prefix = "sakal_bihar_en"
    mp3_path = os.path.join(AUDIO_DIR, f"{prefix}.mp3")
    with open(os.path.join(AUDIO_DIR, f"{prefix}.timestamps.json"), encoding="utf-8") as f:
        words = json.load(f)
    with open(os.path.join(AUDIO_DIR, f"{prefix}.spans.json"), encoding="utf-8") as f:
        spans = json.load(f)

    dur = round(get_duration(mp3_path) + 0.45, 2)
    t1, t2, t3, t4, t5, t6 = [sp["start"] for sp in spans]
    words_json = json.dumps(words, ensure_ascii=False)
    comp_id = "sakal-bihar-en"

    region_paths = load_svg_inner("bihar_region_real.svg")
    solo_paths = load_svg_inner("bihar_solo_real.svg")

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>{comp_id}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@600;700;800;900&family=JetBrains+Mono:wght@600;700;800&display=swap" rel="stylesheet" />
<script src="assets/js/gsap.min.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    width: 1080px; height: 1920px; overflow: hidden;
    background: #18191E;
    font-family: 'Inter', -apple-system, sans-serif;
    color: #FAFAFA;
  }}
  .stage {{
    position: relative; width: 1080px; height: 1920px;
    background: radial-gradient(circle at 50% 35%, #272932 0%, #18191E 68%, #101114 100%);
    overflow: hidden; perspective: 1400px; transform-style: preserve-3d;
  }}
  /* Subtle topographic grid */
  .topo-grid {{
    position: absolute; inset: 0;
    background-image:
      linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 64px 64px;
    pointer-events: none;
  }}
  .topo-ring {{
    position: absolute; border-radius: 999px;
    border: 1.5px dashed rgba(255,255,255,0.07);
    pointer-events: none;
  }}
  .ring-1 {{ width: 920px; height: 920px; top: 340px; left: 80px; }}
  .ring-2 {{ width: 1240px; height: 1240px; top: 180px; left: -80px; }}

  /* Top dailygeomap-style attribution bar */
  .top-bar {{
    position: absolute; top: 72px; left: 56px; right: 56px;
    display: flex; align-items: center; justify-content: space-between;
    z-index: 30;
  }}
  .osm-credit {{
    font-size: 20px; font-weight: 700; color: rgba(255,255,255,0.68);
    letter-spacing: 0.02em;
  }}
  .geo-badge {{
    display: flex; align-items: center; gap: 10px;
    padding: 8px 18px; border-radius: 999px;
    background: rgba(255,255,255,0.08);
    border: 1.5px solid rgba(255,255,255,0.18);
    font-size: 18px; font-weight: 800; color: #E4E4E7;
  }}
  .geo-dot {{
    width: 10px; height: 10px; border-radius: 999px; background: #EF4444;
  }}

  .speaker-wrap {{
    position: absolute; top: 142px; left: 56px; z-index: 30;
  }}
  .speaker-pill {{
    padding: 7px 18px; border-radius: 999px;
    background: rgba(217, 70, 239, 0.16);
    border: 1.5px solid #D946EF; color: #F0ABFC;
    font-size: 15px; font-weight: 800; letter-spacing: 0.08em;
  }}

  /* Scenes */
  .scene {{
    position: absolute; top: 210px; left: 48px; right: 48px; bottom: 420px;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    gap: 28px; opacity: 0; transform-style: preserve-3d;
  }}
  .eyebrow {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 21px; font-weight: 800; letter-spacing: 0.10em;
    color: #FAFAFA; background: rgba(37, 99, 235, 0.25);
    border: 2px solid #3B82F6; padding: 10px 26px; border-radius: 999px;
  }}
  .hero-title {{
    font-size: 58px; font-weight: 900; text-align: center; line-height: 1.12;
    text-shadow: 0 8px 28px rgba(0,0,0,0.45);
  }}
  .gold {{ color: #FACC15; }}
  .pink {{ color: #F472B6; }}
  .blue {{ color: #60A5FA; }}
  .green {{ color: #4ADE80; }}

  .map-frame {{
    position: relative; width: 920px; height: 700px;
    display: flex; align-items: center; justify-content: center;
    filter: drop-shadow(0 24px 48px rgba(0,0,0,0.55));
  }}
  .map-label {{
    position: absolute; padding: 8px 18px; border-radius: 12px;
    font-size: 22px; font-weight: 900; color: #FFFFFF;
    background: rgba(24,24,27,0.85); border: 2px solid rgba(255,255,255,0.35);
    box-shadow: 0 8px 20px rgba(0,0,0,0.4);
  }}

  /* Pie chart card */
  .pie-wrap {{
    position: relative; width: 520px; height: 520px;
    display: flex; align-items: center; justify-content: center;
    filter: drop-shadow(0 22px 44px rgba(0,0,0,0.5));
  }}
  .legend-row {{
    display: flex; flex-wrap: wrap; justify-content: center; gap: 18px;
  }}
  .leg-pill {{
    display: flex; align-items: center; gap: 10px;
    padding: 12px 22px; border-radius: 16px;
    background: rgba(255,255,255,0.07); border: 1.5px solid rgba(255,255,255,0.16);
    font-size: 24px; font-weight: 800;
  }}
  .swatch {{ width: 18px; height: 18px; border-radius: 5px; }}

  /* Chips & Stat cards */
  .chip-grid {{
    display: flex; flex-wrap: wrap; justify-content: center; gap: 16px; max-width: 880px;
  }}
  .gi-chip {{
    padding: 14px 26px; border-radius: 18px;
    background: rgba(255,255,255,0.08); border: 2px solid rgba(250, 204, 21, 0.55);
    font-size: 24px; font-weight: 800; color: #FEF08A;
  }}
  .stat-row {{
    display: flex; gap: 22px; justify-content: center; width: 100%;
  }}
  .stat-card {{
    flex: 1; max-width: 420px; padding: 28px 24px; border-radius: 26px;
    background: rgba(255,255,255,0.07); border: 2px solid rgba(255,255,255,0.16);
    text-align: center; display: flex; flex-direction: column; gap: 10px;
  }}
  .stat-num {{ font-size: 52px; font-weight: 900; color: #4ADE80; }}
  .stat-lbl {{ font-size: 22px; font-weight: 700; color: #D4D4D8; }}

  .cta-card {{
    width: 100%; max-width: 880px; padding: 48px 42px; border-radius: 34px;
    background: linear-gradient(145deg, rgba(37, 99, 235, 0.22), rgba(217, 70, 239, 0.20));
    border: 2.5px solid rgba(255,255,255,0.25);
    box-shadow: 0 28px 64px rgba(0,0,0,0.48);
    display: flex; flex-direction: column; align-items: center; text-align: center; gap: 22px;
  }}
  .cta-btn {{
    padding: 20px 48px; border-radius: 999px;
    background: #D946EF; color: #FFFFFF;
    font-size: 28px; font-weight: 900; letter-spacing: 0.04em;
    box-shadow: 0 12px 30px rgba(217, 70, 239, 0.45);
  }}

  /* Dailygeomap style lower-third captions with magenta active pill */
  .caption-wrap {{
    position: absolute; bottom: 130px; left: 48px; right: 48px;
    display: flex; justify-content: center; z-index: 40;
  }}
  .caption-box {{
    display: flex; flex-wrap: wrap; justify-content: center; gap: 10px 14px;
    padding: 18px 26px; border-radius: 24px;
    background: rgba(16, 17, 20, 0.72);
    max-width: 960px;
  }}
  .cap-word {{
    font-size: 46px; font-weight: 900; color: #FFFFFF;
    padding: 4px 12px; border-radius: 10px; line-height: 1.18;
    text-shadow: 0 4px 12px rgba(0,0,0,0.65);
  }}
  .cap-word.active {{ background: #D946EF; color: #FFFFFF; }}

  .progress-track {{
    position: absolute; bottom: 56px; left: 56px; right: 56px;
    height: 8px; border-radius: 999px;
    background: rgba(255,255,255,0.14); overflow: hidden; z-index: 40;
  }}
  .progress-fill {{
    height: 100%; width: 0%;
    background: linear-gradient(90deg, #3B82F6, #D946EF); border-radius: 999px;
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
  <audio id="sfx-whoosh-2" src="assets/sfx/real/whoosh.wav" data-start="{t2}" volume="0.26"></audio>
  <audio id="sfx-whoosh-3" src="assets/sfx/real/whoosh.wav" data-start="{t3}" volume="0.26"></audio>
  <audio id="sfx-pop-3" src="assets/sfx/real/pop.wav" data-start="{round(t3 + 0.3, 3)}" volume="0.26"></audio>
  <audio id="sfx-whoosh-4" src="assets/sfx/real/whoosh.wav" data-start="{t4}" volume="0.26"></audio>
  <audio id="sfx-click-5" src="assets/sfx/real/click.wav" data-start="{t5}" volume="0.24"></audio>
  <audio id="sfx-chime-6" src="assets/sfx/real/chime.wav" data-start="{t6}" volume="0.32"></audio>

  <div class="stage">
    <div class="topo-grid"></div>
    <div class="topo-ring ring-1"></div>
    <div class="topo-ring ring-2"></div>

    <div class="top-bar">
      <div class="osm-credit">Source Map : © OSM ©ESRI</div>
      <div class="geo-badge"><span class="geo-dot"></span> dailygeomap style</div>
    </div>

    <div class="speaker-wrap">
      <div class="speaker-pill">● SAKAL · VOICE CLONE</div>
    </div>

    <!-- SCENE 1: REAL BIHAR & NEIGHBORS MAP -->
    <div id="scene-1" class="scene">
      <div class="eyebrow anim-item">EASTERN INDIA · GEOGRAPHY</div>
      <div class="hero-title anim-item">BIHAR &amp; <span class="pink">BORDERS</span></div>
      <div class="map-frame anim-card">
        <svg viewBox="0 0 900 700" width="900" height="700">
          {region_paths}
        </svg>
        <div class="map-label anim-pop" style="top:190px; left:170px; border-color:#EC4899;">Uttar Pradesh</div>
        <div class="map-label anim-pop" style="top:290px; left:520px; border-color:#3B82F6; background:#1D4ED8;">BIHAR</div>
        <div class="map-label anim-pop" style="top:460px; left:520px;">Jharkhand</div>
        <div class="map-label anim-pop" style="top:370px; left:705px;">W. Bengal</div>
        <div class="map-label anim-pop" style="top:125px; left:535px; border-color:#FACC15; color:#FEF08A;">NEPAL ↑</div>
      </div>
    </div>

    <!-- SCENE 2: DEMOGRAPHICS PIE CHART -->
    <div id="scene-2" class="scene">
      <div class="eyebrow anim-item">POPULATION · *2011 CENSUS</div>
      <div class="hero-title anim-item"><span class="gold">130 MILLION+</span> PEOPLE</div>
      <div class="pie-wrap anim-card">
        <svg viewBox="0 0 400 400" width="460" height="460">
          <circle cx="200" cy="200" r="150" fill="none" stroke="#F97316" stroke-width="140"
                  stroke-dasharray="772 943" transform="rotate(-90 200 200)" />
          <circle cx="200" cy="200" r="150" fill="none" stroke="#22C55E" stroke-width="140"
                  stroke-dasharray="160 943" stroke-dashoffset="-772" transform="rotate(-90 200 200)" />
          <circle cx="200" cy="200" r="150" fill="none" stroke="#06B6D4" stroke-width="140"
                  stroke-dasharray="12 943" stroke-dashoffset="-932" transform="rotate(-90 200 200)" />
          <circle cx="200" cy="200" r="78" fill="#18191E" />
          <text x="200" y="196" text-anchor="middle" fill="#FAFAFA" font-size="30" font-weight="900">13 Cr+</text>
          <text x="200" y="226" text-anchor="middle" fill="#A1A1AA" font-size="16" font-weight="700">POPULATION</text>
        </svg>
      </div>
      <div class="legend-row anim-pop">
        <div class="leg-pill"><span class="swatch" style="background:#F97316;"></span> Hindus ~82%</div>
        <div class="leg-pill"><span class="swatch" style="background:#22C55E;"></span> Muslims ~17%</div>
        <div class="leg-pill"><span class="swatch" style="background:#06B6D4;"></span> Others ~1%</div>
      </div>
    </div>

    <!-- SCENE 3: GDP & GI PRODUCTS -->
    <div id="scene-3" class="scene">
      <div class="eyebrow anim-item">ECONOMY &amp; HERITAGE</div>
      <div class="hero-title anim-item">GDP : <span class="gold">$130 BILLION</span></div>
      <div class="map-frame anim-card" style="height:490px;">
        <svg viewBox="0 0 760 560" width="760" height="500">
          {solo_paths}
        </svg>
      </div>
      <div class="chip-grid anim-pop">
        <div class="gi-chip">Madhubani Art</div>
        <div class="gi-chip">Shahi Litchi</div>
        <div class="gi-chip">Bhagalpur Silk</div>
        <div class="gi-chip">Magahi Paan</div>
      </div>
    </div>

    <!-- SCENE 4: SHIWALIK & WILDLIFE -->
    <div id="scene-4" class="scene">
      <div class="eyebrow anim-item">NATURE &amp; WILDLIFE</div>
      <div class="hero-title anim-item"><span class="green">SHIWALIK</span> TO SANCTUARIES</div>
      <div class="map-frame anim-card" style="height:440px;">
        <svg viewBox="0 0 760 560" width="680" height="440">
          {solo_paths}
          <path d="M 110,95 Q 195,85 260,125" fill="none" stroke="#4ADE80" stroke-width="14" stroke-linecap="round" />
          <text x="190" y="72" text-anchor="middle" fill="#4ADE80" font-size="24" font-weight="900">Shiwalik Range</text>
        </svg>
      </div>
      <div class="stat-row anim-pop">
        <div class="stat-card">
          <div class="stat-num">12+</div>
          <div class="stat-lbl">Wildlife Sanctuaries</div>
        </div>
        <div class="stat-card">
          <div class="stat-num" style="color:#FACC15; font-size:38px; padding-top:10px;">House Sparrow</div>
          <div class="stat-lbl">Official State Bird</div>
        </div>
      </div>
    </div>

    <!-- SCENE 5: INFRASTRUCTURE & HIGHWAYS -->
    <div id="scene-5" class="scene">
      <div class="eyebrow anim-item">INFRASTRUCTURE</div>
      <div class="hero-title anim-item">EXPRESSWAY <span class="gold">NETWORK</span></div>
      <div class="map-frame anim-card" style="height:560px;">
        <svg viewBox="0 0 760 560" width="760" height="540">
          {solo_paths}
          <g stroke="#FACC15" stroke-width="5.5" stroke-linecap="round" fill="none" opacity="0.92">
            <path d="M 120,250 L 350,275 L 620,235" />
            <path d="M 180,150 L 350,275 L 480,430" />
            <path d="M 210,410 L 350,275 L 550,160" />
            <path d="M 270,180 L 450,210 L 580,350" />
          </g>
          <circle cx="350" cy="275" r="12" fill="#EF4444" stroke="#FFFFFF" stroke-width="3" />
          <text x="350" y="318" text-anchor="middle" fill="#FFFFFF" font-size="22" font-weight="900">PATNA</text>
        </svg>
      </div>
    </div>

    <!-- SCENE 6: ANCIENT LEGACY & CTA -->
    <div id="scene-6" class="scene">
      <div class="eyebrow anim-item">ANCIENT POWERHOUSE</div>
      <div class="cta-card anim-card">
        <div class="hero-title" style="font-size:50px;">Chanakya · <span class="gold">Ashoka</span> · Nalanda</div>
        <div style="font-size:28px; font-weight:700; color:#E4E4E7; line-height:1.4;">
          Centuries of scholarship, empire, and resilience — all in one state.
        </div>
        <div class="cta-btn anim-pop">FOLLOW FOR MORE GEO STORIES</div>
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
  if (!activeWord) {{
    capBox.innerHTML = '';
    lastGroup = -1;
    return;
  }}

  if (activeWord.group_id !== lastGroup) {{
    lastGroup = activeWord.group_id;
    const grp = WORDS.filter(w => w.group_id === lastGroup);
    capBox.innerHTML = grp.map((w, idx) =>
      `<span class="cap-word" data-idx="${{idx}}">${{w.word}}</span>`
    ).join('');
  }}

  const grp = WORDS.filter(w => w.group_id === lastGroup);
  const els = capBox.querySelectorAll('.cap-word');
  grp.forEach((w, idx) => {{
    if (els[idx]) {{
      els[idx].classList.toggle('active', w === activeWord);
    }}
  }});
}}

const master = gsap.timeline({{ paused: true }});
window.__timelines = window.__timelines || {{}};
window.__timelines["{comp_id}"] = master;
master.eventCallback("onUpdate", () => updateHUD(master.time()));

function addScene(sel, start, end, isLast) {{
  const el = document.querySelector(sel);
  const items = el.querySelectorAll('.anim-item');
  const card = el.querySelector('.anim-card');
  const pops = el.querySelectorAll('.anim-pop');
  const imm = start === 0;

  master.set(el, {{ opacity: 1 }}, start);
  master.fromTo(card,
    {{ opacity: 0, y: 40, scale: 0.94, rotateX: 8 }},
    {{ opacity: 1, y: 0, scale: 1, rotateX: 0, duration: 0.55, ease: 'power3.out', immediateRender: imm }},
    start
  );
  if (items.length) {{
    master.fromTo(items,
      {{ opacity: 0, y: 20 }},
      {{ opacity: 1, y: 0, duration: 0.4, stagger: 0.08, ease: 'power2.out', immediateRender: imm }},
      start + 0.05
    );
  }}
  if (pops.length) {{
    master.fromTo(pops,
      {{ opacity: 0, scale: 0.84 }},
      {{ opacity: 1, scale: 1, duration: 0.42, stagger: 0.09, ease: 'back.out(1.6)', immediateRender: imm }},
      start + 0.22
    );
  }}
  if (!isLast) {{
    master.to(el, {{ opacity: 0, y: -24, duration: 0.28, ease: 'power2.in' }}, end - 0.24);
  }}
}}

addScene('#scene-1', {t1}, {t2}, false);
addScene('#scene-2', {t2}, {t3}, false);
addScene('#scene-3', {t3}, {t4}, false);
addScene('#scene-4', {t4}, {t5}, false);
addScene('#scene-5', {t5}, {t6}, false);
addScene('#scene-6', {t6}, {dur}, true);
updateHUD(0);
</script>
</body>
</html>'''

    out_html = os.path.join(ENGINE_DIR, f"{comp_id}.html")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated {out_html} (duration={dur}s)")


if __name__ == "__main__":
    main()
