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


def scene_markup(part_num: int) -> str:
    if part_num == 1:
        return """
    <!-- SCENE 1 -->
    <div id="scene-1" class="scene">
      <div class="eyebrow anim-item">DAY 1 · THE UNLOCK</div>
      <div class="hero-card anim-card">
        <div class="logo-row">
          <img src="assets/logos/antigravity-official.png" class="logo-lg" alt="Antigravity" />
          <span class="plus-sign">+</span>
          <img src="assets/logos/gemini-official.svg" class="logo-lg" alt="Gemini" />
        </div>
        <div class="price-compare">
          <span class="old-price">$20/mo</span>
          <span class="arrow-right">→</span>
          <span class="new-price">$5/mo</span>
        </div>
        <div class="badge-green anim-pop">STUDENT OFFER · 75% OFF</div>
      </div>
      <div class="sub-card anim-item">One verified student email unlocks the full AI workspace.</div>
    </div>

    <!-- SCENE 2 -->
    <div id="scene-2" class="scene">
      <div class="eyebrow anim-item">75% STUDENT DISCOUNT</div>
      <div class="glass-card anim-card">
        <div class="stat-big">$20 → $5</div>
        <div class="card-title">Verified .edu / Student Pass</div>
        <div class="chip-grid">
          <div class="chip anim-pop">Gemini Pro Models</div>
          <div class="chip anim-pop">Autonomous Agent</div>
          <div class="chip anim-pop">Full Terminal + Browser</div>
        </div>
      </div>
    </div>

    <!-- SCENE 3 -->
    <div id="scene-3" class="scene">
      <div class="eyebrow anim-item">THE 5-DAY EXPERIMENT</div>
      <div class="vs-stack">
        <div class="vs-card muted anim-card">
          <div class="vs-label">OLD STACK</div>
          <div class="vs-val">$200+/mo</div>
          <div class="vs-sub">After Effects · Cloud TTS · Stock</div>
        </div>
        <div class="vs-badge anim-pop">VS</div>
        <div class="vs-card highlight anim-card">
          <div class="vs-label">ONE WORKSPACE</div>
          <div class="vs-val">$5/mo</div>
          <div class="vs-sub">Antigravity + Local Tools</div>
        </div>
      </div>
    </div>

    <!-- SCENE 4 -->
    <div id="scene-4" class="scene">
      <div class="eyebrow anim-item">DAY 1 · ONE PROMPT</div>
      <div class="terminal-card anim-card">
        <div class="term-bar">
          <span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>
          <span class="term-title">antigravity-prompt</span>
        </div>
        <div class="term-body">
          <div class="term-line"><span class="prompt">&gt;</span> Build a 3D motion-graphics</div>
          <div class="term-line">&nbsp;&nbsp;reel engine from scratch</div>
          <div class="term-line ok">✓ HyperFrames + GSAP initialized</div>
          <div class="term-line ok">✓ 1080×1920 @ 30fps pipeline ready</div>
        </div>
      </div>
      <div class="icon-strip anim-pop">
        <img src="assets/logos/hyperframes-studio.png" class="tool-ico" alt="HyperFrames" />
        <img src="assets/logos/greensock.svg" class="tool-ico" alt="GSAP" />
        <img src="assets/logos/googlechrome.svg" class="tool-ico" alt="Chrome" />
      </div>
    </div>

    <!-- SCENE 5 -->
    <div id="scene-5" class="scene">
      <div class="eyebrow anim-item">ZERO TEMPLATES</div>
      <div class="glass-card anim-card">
        <div class="card-title">Pure Code → 3D Reels</div>
        <div class="pipe-row anim-pop">
          <span class="pipe-pill">HTML5</span>
          <span class="pipe-arrow">→</span>
          <span class="pipe-pill">GSAP 3D</span>
          <span class="pipe-arrow">→</span>
          <span class="pipe-pill dark">1080p MP4</span>
        </div>
        <div class="stat-mini">No After Effects · Deterministic 30fps Render</div>
      </div>
    </div>

    <!-- SCENE 6 -->
    <div id="scene-6" class="scene">
      <div class="eyebrow anim-item">END OF DAY 1</div>
      <div class="cta-card anim-card">
        <div class="cta-tag">NEXT UP · PART 2 / 5</div>
        <div class="cta-title">The Viral Reel Factory</div>
        <div class="cta-sub">Analyzing real reels + shipping Aayojon 3D</div>
        <div class="cta-btn anim-pop">FOLLOW FOR PART 2 →</div>
      </div>
    </div>
"""
    if part_num == 2:
        return """
    <!-- SCENE 1 -->
    <div id="scene-1" class="scene">
      <div class="eyebrow anim-item">DAY 2 · VIRAL ENGINE</div>
      <div class="hero-card anim-card">
        <div class="stat-big orange">DAY 2</div>
        <div class="card-title">Building the Viral Reel Factory</div>
        <div class="badge-dark anim-pop">$5 ANTIGRAVITY WORKSPACE</div>
      </div>
    </div>

    <!-- SCENE 2 -->
    <div id="scene-2" class="scene">
      <div class="eyebrow anim-item">DATA-DRIVEN PACING</div>
      <div class="glass-card anim-card">
        <div class="card-title">Real Style Reference Analysis</div>
        <div class="chip-grid">
          <div class="chip anim-pop">Cut Cadence</div>
          <div class="chip anim-pop">Color &amp; Luma</div>
          <div class="chip anim-pop">Hook Timing</div>
        </div>
        <div class="stat-mini">No guessing—every beat measured from real reels</div>
      </div>
    </div>

    <!-- SCENE 3 -->
    <div id="scene-3" class="scene">
      <div class="eyebrow anim-item">AUTOMATED PIPELINE</div>
      <div class="glass-card anim-card">
        <div class="logo-row">
          <img src="assets/logos/yt-dlp.png" class="logo-md" alt="yt-dlp" />
          <span class="plus-sign">→</span>
          <img src="assets/logos/ffmpeg.svg" class="logo-md" alt="FFmpeg" />
        </div>
        <div class="card-title">yt-dlp + ffprobe</div>
        <div class="stat-mini">Auto-extracts frame rates, durations &amp; scene rhythm</div>
      </div>
    </div>

    <!-- SCENE 4 -->
    <div id="scene-4" class="scene">
      <div class="eyebrow anim-item">REAL PRODUCT REELS</div>
      <div class="phone-frame anim-card">
        <img src="assets/aayojon/home.png" class="phone-img" alt="Aayojon App" />
      </div>
      <div class="badge-green anim-pop">AAYOJON PART 1 &amp; 2 · 3D REELS</div>
    </div>

    <!-- SCENE 5 -->
    <div id="scene-5" class="scene">
      <div class="eyebrow anim-item">BEHIND THE SCENES</div>
      <div class="terminal-card anim-card">
        <div class="term-bar">
          <span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>
          <span class="term-title">making-of-v2-en.html</span>
        </div>
        <div class="term-body">
          <div class="term-line ok">✓ Official Brand SVGs Staged</div>
          <div class="term-line ok">✓ Real Openverse SFX Layered</div>
          <div class="term-line ok">✓ Code + Timeline Breakdown</div>
        </div>
      </div>
    </div>

    <!-- SCENE 6 -->
    <div id="scene-6" class="scene">
      <div class="eyebrow anim-item">END OF DAY 2</div>
      <div class="cta-card anim-card">
        <div class="cta-tag">NEXT UP · PART 3 / 5</div>
        <div class="cta-title">Live University Tech Event</div>
        <div class="cta-sub">AWS Student Build &amp; Grow @ DIU</div>
        <div class="cta-btn anim-pop">WATCH PART 3 →</div>
      </div>
    </div>
"""
    if part_num == 3:
        return """
    <!-- SCENE 1 -->
    <div id="scene-1" class="scene">
      <div class="eyebrow anim-item">DAYS 3 &amp; 4 · REAL PROMOS</div>
      <div class="hero-card anim-card">
        <div class="stat-big indigo">DAYS 3–4</div>
        <div class="card-title">Can a $5 AI Handle Live Events?</div>
        <div class="badge-dark anim-pop">CLIENT &amp; COMMUNITY TEST</div>
      </div>
    </div>

    <!-- SCENE 2 -->
    <div id="scene-2" class="scene">
      <div class="eyebrow anim-item">LIVE EVENT BRIEF</div>
      <div class="glass-card anim-card">
        <div class="logo-row">
          <img src="assets/logos/aws-logo.svg" class="logo-md" alt="AWS" />
          <span class="plus-sign">×</span>
          <img src="assets/logos/sbg-diu-badge.svg" class="logo-md" alt="SBG DIU" />
        </div>
        <div class="card-title">AWS Student Build &amp; Grow</div>
        <div class="stat-mini">Daffodil International University (DIU)</div>
      </div>
    </div>

    <!-- SCENE 3 -->
    <div id="scene-3" class="scene">
      <div class="eyebrow anim-item">3D MOTION CARDS</div>
      <div class="glass-card anim-card">
        <div class="card-title">Official Badges &amp; Beat Sync</div>
        <div class="chip-grid">
          <div class="chip anim-pop">3D Perspective</div>
          <div class="chip anim-pop">Speaker Cards</div>
          <div class="chip anim-pop">Event Schedule</div>
        </div>
      </div>
    </div>

    <!-- SCENE 4 -->
    <div id="scene-4" class="scene">
      <div class="eyebrow anim-item">COMPILED IN MINUTES</div>
      <div class="terminal-card anim-card">
        <div class="term-bar">
          <span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>
          <span class="term-title">hyperframes render</span>
        </div>
        <div class="term-body">
          <div class="term-line ok">✓ 3D Transitions Compiled</div>
          <div class="term-line ok">✓ Multi-Track SFX Synced</div>
          <div class="term-line ok">✓ Word-Level Captions Locked</div>
        </div>
      </div>
    </div>

    <!-- SCENE 5 -->
    <div id="scene-5" class="scene">
      <div class="eyebrow anim-item">SPEED MULTIPLIER</div>
      <div class="vs-stack">
        <div class="vs-card muted anim-card">
          <div class="vs-label">MANUAL KEYFRAMING</div>
          <div class="vs-val">Days</div>
        </div>
        <div class="vs-badge anim-pop">→</div>
        <div class="vs-card highlight anim-card">
          <div class="vs-label">AUTOMATED ENGINE</div>
          <div class="vs-val">Minutes</div>
        </div>
      </div>
    </div>

    <!-- SCENE 6 -->
    <div id="scene-6" class="scene">
      <div class="eyebrow anim-item">ONE BOTTLENECK LEFT</div>
      <div class="cta-card anim-card">
        <div class="cta-tag">NEXT UP · PART 4 / 5</div>
        <div class="cta-title">Eliminating Paid Voiceovers</div>
        <div class="cta-sub">100% Offline Voice Cloning on Mac</div>
        <div class="cta-btn anim-pop">WATCH PART 4 →</div>
      </div>
    </div>
"""
    if part_num == 4:
        return """
    <!-- SCENE 1 -->
    <div id="scene-1" class="scene">
      <div class="eyebrow anim-item">DAY 5 · THE BREAKTHROUGH</div>
      <div class="hero-card anim-card">
        <div class="stat-big green">$0 / MO</div>
        <div class="card-title">Zero Cloud Fees for Voiceovers</div>
        <div class="badge-green anim-pop">100% LOCAL &amp; OFFLINE</div>
      </div>
    </div>

    <!-- SCENE 2 -->
    <div id="scene-2" class="scene">
      <div class="eyebrow anim-item">STEP 1 · HANDY DICTATION</div>
      <div class="glass-card anim-card">
        <div class="kbd-row anim-pop">
          <span class="kbd">Option</span><span>+</span><span class="kbd">Space</span>
        </div>
        <div class="card-title">Handy (Whisper / Parakeet)</div>
        <div class="stat-mini">Dictate scripts 3× faster—zero cloud uploads</div>
      </div>
    </div>

    <!-- SCENE 3 -->
    <div id="scene-3" class="scene">
      <div class="eyebrow anim-item">STEP 2 · OMNIVOICE CLONING</div>
      <div class="glass-card anim-card">
        <div class="stat-big">10 SEC</div>
        <div class="card-title">k2-fsa / OmniVoice on Mac</div>
        <div class="stat-mini">Clone any voice locally from a 10-second audio clip</div>
      </div>
    </div>

    <!-- SCENE 4 -->
    <div id="scene-4" class="scene">
      <div class="eyebrow anim-item">LIVE PROOF</div>
      <div class="wave-card anim-card">
        <div class="badge-green">RAFI · 10s VOICE CLONE</div>
        <div class="wave-bars">
          <span class="bar"></span><span class="bar"></span><span class="bar"></span>
          <span class="bar"></span><span class="bar"></span><span class="bar"></span>
          <span class="bar"></span><span class="bar"></span><span class="bar"></span>
        </div>
        <div class="card-title">Speaking English Right Now</div>
      </div>
    </div>

    <!-- SCENE 5 -->
    <div id="scene-5" class="scene">
      <div class="eyebrow anim-item">BILINGUAL LOCAL ENGINE</div>
      <div class="glass-card anim-card">
        <div class="pipe-row anim-pop">
          <span class="pipe-pill">English</span>
          <span class="pipe-arrow">+</span>
          <span class="pipe-pill">Bangla</span>
        </div>
        <div class="card-title">100% Offline · $0 API Bills</div>
        <div class="stat-mini">Rafi · Sara · Riya finalized in one local pipeline</div>
      </div>
    </div>

    <!-- SCENE 6 -->
    <div id="scene-6" class="scene">
      <div class="eyebrow anim-item">FINAL PART NEXT</div>
      <div class="cta-card anim-card">
        <div class="cta-tag">FINALE · PART 5 / 5</div>
        <div class="cta-title">The Complete 5-Day Blueprint</div>
        <div class="cta-sub">Everything we built + how to start today</div>
        <div class="cta-btn anim-pop">WATCH PART 5 →</div>
      </div>
    </div>
"""
    # Part 5
    return """
    <!-- SCENE 1 -->
    <div id="scene-1" class="scene">
      <div class="eyebrow anim-item">PART 5 · THE COMPLETE STORY</div>
      <div class="hero-card anim-card">
        <div class="logo-row">
          <img src="assets/logos/antigravity-official.png" class="logo-lg" alt="Antigravity" />
        </div>
        <div class="stat-big">5 DAYS · $5</div>
        <div class="card-title">Everything We Built This Week</div>
      </div>
    </div>

    <!-- SCENE 2 -->
    <div id="scene-2" class="scene">
      <div class="eyebrow anim-item">THE PRODUCTION STACK</div>
      <div class="glass-card anim-card">
        <div class="icon-strip">
          <img src="assets/logos/hyperframes-studio.png" class="tool-ico" alt="HyperFrames" />
          <img src="assets/logos/greensock.svg" class="tool-ico" alt="GSAP" />
          <img src="assets/logos/yt-dlp.png" class="tool-ico" alt="yt-dlp" />
          <img src="assets/logos/ffmpeg.svg" class="tool-ico" alt="FFmpeg" />
        </div>
        <div class="card-title">3D Engine + Analysis + SFX</div>
        <div class="stat-mini">Automated from script to final 1080p render</div>
      </div>
    </div>

    <!-- SCENE 3 -->
    <div id="scene-3" class="scene">
      <div class="eyebrow anim-item">REAL DELIVERABLES</div>
      <div class="glass-card anim-card">
        <div class="chip-grid">
          <div class="chip anim-pop">Aayojon 3D Reels</div>
          <div class="chip anim-pop">AWS DIU Event Promo</div>
          <div class="chip anim-pop">Offline Voice Clones</div>
          <div class="chip anim-pop">EN + BN Pipelines</div>
        </div>
      </div>
    </div>

    <!-- SCENE 4 -->
    <div id="scene-4" class="scene">
      <div class="eyebrow anim-item">UNREAL ROI</div>
      <div class="vs-stack">
        <div class="vs-card muted anim-card">
          <div class="vs-label">COST</div>
          <div class="vs-val">$5/mo</div>
          <div class="vs-sub">Less than 1 coffee</div>
        </div>
        <div class="vs-badge anim-pop">=</div>
        <div class="vs-card highlight anim-card">
          <div class="vs-label">OUTPUT</div>
          <div class="vs-val">Full Studio</div>
          <div class="vs-sub">Code · 3D · Voice · Video</div>
        </div>
      </div>
    </div>

    <!-- SCENE 5 -->
    <div id="scene-5" class="scene">
      <div class="eyebrow anim-item">DON'T SLEEP ON THIS</div>
      <div class="glass-card anim-card">
        <img src="assets/logos/antigravity-official.png" class="logo-md" alt="Antigravity" />
        <div class="card-title">Antigravity Student Offer</div>
        <div class="badge-green anim-pop">$5/MO WITH STUDENT EMAIL</div>
      </div>
    </div>

    <!-- SCENE 6 -->
    <div id="scene-6" class="scene">
      <div class="eyebrow anim-item">GET THE FULL WORKFLOW</div>
      <div class="cta-card anim-card">
        <div class="cta-tag">5-DAY BLUEPRINT + SETUP</div>
        <div class="cta-title">Comment "STUDENT"</div>
        <div class="cta-sub">I'll send our complete workflow &amp; setup guide</div>
        <div class="cta-btn anim-pop">COMMENT "STUDENT" ↓</div>
      </div>
    </div>
"""


def build_part_html(part_num: int) -> None:
    prefix = f"story_part{part_num}_en"
    mp3_path = os.path.join(AUDIO_DIR, f"{prefix}.mp3")
    with open(os.path.join(AUDIO_DIR, f"{prefix}.timestamps.json"), encoding="utf-8") as f:
        words = json.load(f)
    with open(os.path.join(AUDIO_DIR, f"{prefix}.spans.json"), encoding="utf-8") as f:
        spans = json.load(f)

    dur = round(get_duration(mp3_path) + 0.40, 2)
    t1, t2, t3, t4, t5, t6 = [sp["start"] for sp in spans]
    words_json = json.dumps(words, ensure_ascii=False)
    comp_id = f"antigravity-story-part{part_num}-en"
    scenes_html = scene_markup(part_num)

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
    background: #F7F5F0;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #18181B;
  }}
  .stage {{
    position: relative;
    width: 1080px;
    height: 1920px;
    background: radial-gradient(circle at 18% 12%, #FFF7ED 0%, #F7F5F0 46%, #EEF2FF 100%);
    overflow: hidden;
    perspective: 1400px;
    transform-style: preserve-3d;
  }}
  .dot-grid {{
    position: absolute;
    inset: 0;
    background-image: radial-gradient(rgba(24, 24, 27, 0.11) 1.5px, transparent 1.5px);
    background-size: 36px 36px;
    pointer-events: none;
  }}
  .orb {{
    position: absolute;
    border-radius: 999px;
    filter: blur(80px);
    opacity: 0.45;
    pointer-events: none;
  }}
  .orb-1 {{ width: 520px; height: 520px; background: #FDBA74; top: -120px; right: -120px; }}
  .orb-2 {{ width: 480px; height: 480px; background: #A5B4FC; bottom: 180px; left: -140px; }}

  .header {{
    position: absolute;
    top: 68px;
    left: 64px;
    right: 64px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    z-index: 30;
  }}
  .brand-left {{ display: flex; align-items: center; gap: 16px; }}
  .brand-logo {{
    width: 60px; height: 60px; border-radius: 16px;
    border: 2.5px solid #18181B;
    box-shadow: 0 6px 0 #18181B;
  }}
  .brand-name {{ font-size: 26px; font-weight: 900; letter-spacing: -0.02em; }}
  .brand-sub {{ font-size: 15px; font-weight: 800; color: #EA580C; letter-spacing: 0.08em; }}
  .part-pill {{
    padding: 12px 24px;
    border-radius: 999px;
    background: #18181B;
    color: #FFFFFF;
    font-size: 20px;
    font-weight: 900;
    letter-spacing: 0.08em;
    box-shadow: 0 8px 20px rgba(24, 24, 27, 0.18);
  }}

  .speaker-wrap {{
    position: absolute;
    top: 166px;
    left: 64px;
    z-index: 30;
  }}
  .speaker-pill {{
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 10px 22px;
    border-radius: 999px;
    background: #ECFDF5;
    border: 2px solid #16A34A;
    color: #15803D;
    font-size: 18px;
    font-weight: 800;
    letter-spacing: 0.06em;
  }}

  .scene {{
    position: absolute;
    top: 250px;
    left: 64px;
    right: 64px;
    bottom: 400px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 28px;
    opacity: 0;
    transform-style: preserve-3d;
  }}
  .eyebrow {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 0.14em;
    color: #EA580C;
    background: #FFF7ED;
    border: 2px solid #FDBA74;
    padding: 10px 22px;
    border-radius: 999px;
  }}
  .hero-card, .glass-card, .terminal-card, .cta-card, .wave-card {{
    width: 100%;
    background: #FFFFFF;
    border: 3px solid #18181B;
    border-radius: 36px;
    padding: 52px 44px;
    box-shadow: 0 14px 0 #18181B, 0 32px 64px rgba(24, 24, 27, 0.12);
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 24px;
  }}
  .sub-card {{
    font-size: 28px;
    font-weight: 700;
    color: #3F3F46;
    text-align: center;
    line-height: 1.35;
    max-width: 820px;
  }}
  .logo-row {{ display: flex; align-items: center; gap: 26px; }}
  .logo-lg {{ width: 96px; height: 96px; border-radius: 22px; object-fit: contain; }}
  .logo-md {{ width: 84px; height: 84px; object-fit: contain; }}
  .plus-sign {{ font-size: 42px; font-weight: 900; color: #71717A; }}
  .price-compare {{ display: flex; align-items: center; gap: 24px; }}
  .old-price {{ font-size: 56px; font-weight: 900; color: #A1A1AA; text-decoration: line-through; }}
  .arrow-right {{ font-size: 46px; font-weight: 900; color: #EA580C; }}
  .new-price {{ font-size: 86px; font-weight: 900; color: #16A34A; letter-spacing: -0.03em; }}
  .stat-big {{ font-size: 88px; font-weight: 900; letter-spacing: -0.03em; color: #18181B; line-height: 1; }}
  .stat-big.orange {{ color: #EA580C; }}
  .stat-big.indigo {{ color: #4F46E5; }}
  .stat-big.green {{ color: #16A34A; }}
  .card-title {{ font-size: 42px; font-weight: 900; letter-spacing: -0.02em; line-height: 1.15; }}
  .stat-mini {{ font-size: 25px; font-weight: 600; color: #52525B; line-height: 1.35; }}

  .badge-green {{
    background: #16A34A; color: #FFFFFF;
    padding: 14px 30px; border-radius: 999px;
    font-size: 22px; font-weight: 900; letter-spacing: 0.06em;
  }}
  .badge-dark {{
    background: #18181B; color: #FFFFFF;
    padding: 14px 30px; border-radius: 999px;
    font-size: 22px; font-weight: 900; letter-spacing: 0.06em;
  }}

  .chip-grid {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 16px; }}
  .chip {{
    padding: 16px 26px;
    border-radius: 20px;
    background: #F4F4F5;
    border: 2px solid #18181B;
    font-size: 24px;
    font-weight: 800;
  }}

  .vs-stack {{ width: 100%; display: flex; flex-direction: column; align-items: center; gap: 18px; }}
  .vs-card {{
    width: 100%; padding: 36px; border-radius: 30px;
    border: 3px solid #18181B; text-align: center;
    background: #FFFFFF; box-shadow: 0 10px 0 #18181B;
  }}
  .vs-card.muted {{ background: #F4F4F5; color: #71717A; }}
  .vs-card.highlight {{ background: #ECFDF5; border-color: #16A34A; box-shadow: 0 10px 0 #16A34A; }}
  .vs-label {{ font-size: 18px; font-weight: 800; letter-spacing: 0.1em; }}
  .vs-val {{ font-size: 64px; font-weight: 900; margin: 6px 0; }}
  .vs-sub {{ font-size: 24px; font-weight: 600; }}
  .vs-badge {{
    width: 68px; height: 68px; border-radius: 999px;
    background: #EA580C; color: #FFFFFF; border: 3px solid #18181B;
    display: flex; align-items: center; justify-content: center;
    font-size: 24px; font-weight: 900;
  }}

  .terminal-card {{ padding: 0; overflow: hidden; align-items: stretch; text-align: left; background: #18181B; color: #F4F4F5; }}
  .term-bar {{
    display: flex; align-items: center; gap: 10px;
    padding: 20px 28px; background: #27272A; border-bottom: 2px solid #3F3F46;
  }}
  .dot {{ width: 16px; height: 16px; border-radius: 999px; }}
  .dot.r {{ background: #EF4444; }} .dot.y {{ background: #F59E0B; }} .dot.g {{ background: #22C55E; }}
  .term-title {{ font-family: 'JetBrains Mono', monospace; font-size: 18px; color: #A1A1AA; margin-left: 10px; }}
  .term-body {{ padding: 36px 34px; font-family: 'JetBrains Mono', monospace; font-size: 26px; line-height: 1.65; }}
  .prompt {{ color: #FB923C; font-weight: 700; }}
  .term-line.ok {{ color: #4ADE80; font-weight: 700; margin-top: 8px; }}

  .icon-strip {{ display: flex; align-items: center; justify-content: center; gap: 28px; margin-top: 8px; }}
  .tool-ico {{
    width: 84px; height: 84px; padding: 14px;
    background: #FFFFFF; border: 2.5px solid #18181B; border-radius: 22px;
    box-shadow: 0 6px 0 #18181B; object-fit: contain;
  }}

  .pipe-row {{ display: flex; align-items: center; gap: 16px; flex-wrap: wrap; justify-content: center; }}
  .pipe-pill {{
    padding: 16px 28px; border-radius: 18px;
    background: #FFF7ED; border: 2.5px solid #EA580C; color: #EA580C;
    font-size: 28px; font-weight: 900;
  }}
  .pipe-pill.dark {{ background: #18181B; border-color: #18181B; color: #FFFFFF; }}
  .pipe-arrow {{ font-size: 32px; font-weight: 900; color: #71717A; }}

  .phone-frame {{
    width: 500px; padding: 16px; background: #18181B; border-radius: 42px;
    box-shadow: 0 24px 60px rgba(24, 24, 27, 0.25);
  }}
  .phone-img {{ width: 100%; border-radius: 28px; display: block; }}

  .kbd-row {{ display: flex; align-items: center; gap: 16px; font-size: 32px; font-weight: 900; }}
  .kbd {{
    padding: 16px 30px; border-radius: 18px;
    background: #F4F4F5; border: 3px solid #18181B;
    box-shadow: 0 8px 0 #18181B; font-family: 'JetBrains Mono', monospace; font-size: 30px;
  }}

  .wave-bars {{ display: flex; align-items: center; gap: 14px; height: 110px; }}
  .wave-bars .bar {{
    width: 18px; border-radius: 999px; background: linear-gradient(180deg, #16A34A, #4F46E5);
    height: 44px;
  }}
  .wave-bars .bar:nth-child(2n) {{ height: 86px; }}
  .wave-bars .bar:nth-child(3n) {{ height: 64px; }}

  .cta-card {{ background: #18181B; color: #FFFFFF; border-color: #18181B; box-shadow: 0 16px 0 #EA580C; }}
  .cta-tag {{ font-family: 'JetBrains Mono', monospace; font-size: 20px; color: #FB923C; font-weight: 700; letter-spacing: 0.1em; }}
  .cta-title {{ font-size: 56px; font-weight: 900; letter-spacing: -0.02em; line-height: 1.1; }}
  .cta-sub {{ font-size: 26px; font-weight: 600; color: #D4D4D8; }}
  .cta-btn {{
    margin-top: 8px; padding: 20px 40px; border-radius: 999px;
    background: #EA580C; color: #FFFFFF; font-size: 26px; font-weight: 900; letter-spacing: 0.04em;
  }}

  .caption-wrap {{
    position: absolute;
    bottom: 130px;
    left: 64px;
    right: 64px;
    display: flex;
    justify-content: center;
    z-index: 40;
  }}
  .caption-box {{
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 12px 14px;
    padding: 22px 32px;
    border-radius: 28px;
    background: rgba(24, 24, 27, 0.94);
    box-shadow: 0 18px 40px rgba(24, 24, 27, 0.28);
    max-width: 940px;
  }}
  .cap-word {{
    font-size: 38px;
    font-weight: 800;
    color: #E4E4E7;
    padding: 4px 10px;
    border-radius: 12px;
  }}
  .cap-word.active {{
    background: #EA580C;
    color: #FFFFFF;
    transform: scale(1.07);
  }}

  .progress-track {{
    position: absolute;
    bottom: 64px;
    left: 64px;
    right: 64px;
    height: 10px;
    border-radius: 999px;
    background: rgba(24, 24, 27, 0.12);
    overflow: hidden;
    z-index: 40;
  }}
  .progress-fill {{
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #EA580C, #16A34A);
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
  <audio id="sfx-bed" src="assets/sfx/tech_drone.wav" data-start="0.0" volume="0.05"></audio>
  <audio id="sfx-impact-1" src="assets/sfx/impact.wav" data-start="{t1}" volume="0.22"></audio>
  <audio id="sfx-whoosh-2" src="assets/sfx/real/whoosh.wav" data-start="{t2}" volume="0.28"></audio>
  <audio id="sfx-pop-2" src="assets/sfx/real/pop.wav" data-start="{round(t2 + 0.25, 3)}" volume="0.26"></audio>
  <audio id="sfx-whoosh-3" src="assets/sfx/real/whoosh.wav" data-start="{t3}" volume="0.28"></audio>
  <audio id="sfx-click-3" src="assets/sfx/real/click.wav" data-start="{round(t3 + 0.22, 3)}" volume="0.24"></audio>
  <audio id="sfx-whoosh-4" src="assets/sfx/real/whoosh.wav" data-start="{t4}" volume="0.28"></audio>
  <audio id="sfx-pop-4" src="assets/sfx/real/pop.wav" data-start="{round(t4 + 0.25, 3)}" volume="0.26"></audio>
  <audio id="sfx-whoosh-5" src="assets/sfx/real/whoosh.wav" data-start="{t5}" volume="0.28"></audio>
  <audio id="sfx-chime-6" src="assets/sfx/real/chime.wav" data-start="{t6}" volume="0.34"></audio>

  <div class="stage">
    <div class="dot-grid"></div>
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>

    <div class="header">
      <div class="brand-left">
        <img src="assets/logos/antigravity-official.png" class="brand-logo" alt="Antigravity" />
        <div>
          <div class="brand-name">ANTIGRAVITY</div>
          <div class="brand-sub">5-DAY BUILD STORY</div>
        </div>
      </div>
      <div class="part-pill">PART {part_num} / 5</div>
    </div>

    <div class="speaker-wrap">
      <div class="speaker-pill">● RAFI · VOICE CLONE</div>
    </div>

    {scenes_html}

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

// Subtle ambient orb drift
tl.to('.orb-1', {{ x: -45, y: 35, duration: TOTAL_DUR, ease: 'sine.inOut' }}, 0);
tl.to('.orb-2', {{ x: 45, y: -35, duration: TOTAL_DUR, ease: 'sine.inOut' }}, 0);

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
    {{ scale: 0.82, opacity: 0 }},
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
    out_path = os.path.join(ENGINE_DIR, f"story-part{part_num}-en.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated {out_path} (duration={dur}s)")


def main():
    for part_num in range(1, 6):
        build_part_html(part_num)


if __name__ == "__main__":
    main()
