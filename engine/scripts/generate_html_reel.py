#!/usr/bin/env python3
"""Generate the frame-accurate HyperFrames HTML composition for AWS SBG DIU reel."""

import json
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parent.parent
AUDIO_DIR = ENGINE_DIR / "assets" / "audio"

def build():
    timestamps_file = AUDIO_DIR / "aws_sbg_dialogue.timestamps.json"
    spans_file = AUDIO_DIR / "aws_sbg_dialogue.spans.json"

    words = json.loads(timestamps_file.read_text(encoding="utf-8"))
    spans = json.loads(spans_file.read_text(encoding="utf-8"))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AWS SBG DIU — Join The Squad</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      width: 1080px;
      height: 1920px;
      background: #080C16;
      color: #F8FAFC;
      font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, sans-serif;
      overflow: hidden;
      perspective: 1400px;
    }}
    #root {{
      width: 1080px;
      height: 1920px;
      position: relative;
      background: radial-gradient(circle at 50% 25%, #1A253C 0%, #080C16 80%);
      overflow: hidden;
    }}

    /* Grid Background */
    .grid-bg {{
      position: absolute;
      inset: 0;
      background-image: 
        linear-gradient(to right, rgba(56, 189, 248, 0.05) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(56, 189, 248, 0.05) 1px, transparent 1px);
      background-size: 60px 60px;
      z-index: 1;
    }}

    /* Ambient Glow Orbs */
    .glow-orb {{
      position: absolute;
      border-radius: 50%;
      filter: blur(120px);
      pointer-events: none;
      z-index: 2;
    }}
    .glow-orange {{
      width: 600px;
      height: 600px;
      background: rgba(255, 153, 0, 0.18);
      top: 15%;
      left: 20%;
    }}
    .glow-cyan {{
      width: 500px;
      height: 500px;
      background: rgba(56, 189, 248, 0.15);
      bottom: 25%;
      right: 15%;
    }}

    /* Top Header Bar */
    .header-bar {{
      position: absolute;
      top: 90px;
      left: 80px;
      right: 80px;
      height: 90px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 50;
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 28px;
      padding: 0 32px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }}
    .brand-group {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}
    .brand-aws {{
      font-size: 32px;
      font-weight: 900;
      color: #FF9900;
      letter-spacing: -1px;
    }}
    .brand-divider {{
      width: 2px;
      height: 24px;
      background: rgba(255, 255, 255, 0.2);
    }}
    .brand-sbg {{
      font-size: 20px;
      font-weight: 800;
      letter-spacing: 2px;
      color: #F8FAFC;
    }}
    .brand-diu {{
      color: #38BDF8;
      font-weight: 900;
    }}
    .live-pill {{
      display: flex;
      align-items: center;
      gap: 8px;
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.4);
      padding: 8px 16px;
      border-radius: 20px;
      font-size: 14px;
      font-weight: 800;
      color: #10B981;
      letter-spacing: 1px;
    }}
    .live-dot {{
      width: 10px;
      height: 10px;
      background: #10B981;
      border-radius: 50%;
    }}

    /* Speaker Pill Indicator */
    .speaker-dock {{
      position: absolute;
      top: 210px;
      left: 0;
      right: 0;
      display: flex;
      justify-content: center;
      z-index: 50;
    }}
    .speaker-tag {{
      display: flex;
      align-items: center;
      gap: 12px;
      background: rgba(15, 23, 42, 0.9);
      border: 2px solid rgba(56, 189, 248, 0.4);
      border-radius: 40px;
      padding: 12px 28px;
      font-size: 18px;
      font-weight: 800;
      letter-spacing: 1px;
      box-shadow: 0 8px 25px rgba(0,0,0,0.5);
    }}
    .speaker-tag.student {{
      border-color: #38BDF8;
      color: #38BDF8;
      box-shadow: 0 0 25px rgba(56, 189, 248, 0.3);
    }}
    .speaker-tag.ai {{
      border-color: #FF9900;
      color: #FF9900;
      box-shadow: 0 0 25px rgba(255, 153, 0, 0.35);
    }}

    /* Main 3D Card Stage */
    .stage-container {{
      position: absolute;
      top: 295px;
      left: 80px;
      right: 80px;
      height: 1030px;
      z-index: 20;
      display: flex;
      align-items: center;
      justify-content: center;
      transform-style: preserve-3d;
    }}

    .scene-card {{
      position: absolute;
      width: 100%;
      height: 100%;
      border-radius: 40px;
      background: linear-gradient(145deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.98) 100%);
      border: 2px solid rgba(255, 255, 255, 0.12);
      box-shadow: 0 30px 80px rgba(0, 0, 0, 0.7);
      padding: 50px 45px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      opacity: 0;
      transform: translateY(60px) rotateX(10deg);
    }}

    /* Card Elements */
    .card-top {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
    }}
    .topic-pill {{
      display: inline-block;
      padding: 10px 22px;
      border-radius: 20px;
      font-size: 15px;
      font-weight: 800;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      background: rgba(255, 153, 0, 0.15);
      border: 1px solid rgba(255, 153, 0, 0.4);
      color: #FF9900;
    }}
    .topic-pill.cyan {{
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid rgba(56, 189, 248, 0.4);
      color: #38BDF8;
    }}
    .card-number {{
      font-family: monospace;
      font-size: 24px;
      font-weight: 700;
      color: rgba(255, 255, 255, 0.3);
    }}

    .card-main {{
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      gap: 30px;
    }}
    .card-title {{
      font-size: 52px;
      font-weight: 900;
      line-height: 1.15;
      letter-spacing: -1.5px;
    }}
    .highlight-orange {{
      color: #FF9900;
      text-shadow: 0 0 35px rgba(255, 153, 0, 0.4);
    }}
    .highlight-cyan {{
      color: #38BDF8;
      text-shadow: 0 0 35px rgba(56, 189, 248, 0.4);
    }}

    .card-graphic {{
      width: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      filter: drop-shadow(0 20px 40px rgba(0,0,0,0.5));
    }}
    .card-graphic img {{
      max-width: 100%;
      height: auto;
      object-fit: contain;
    }}

    .stat-row {{
      width: 100%;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
    }}
    .stat-box {{
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 24px;
      padding: 24px;
      text-align: center;
    }}
    .stat-val {{
      font-size: 38px;
      font-weight: 900;
      color: #FF9900;
      font-family: monospace;
    }}
    .stat-label {{
      font-size: 15px;
      font-weight: 700;
      color: #94A3B8;
      margin-top: 6px;
      letter-spacing: 0.5px;
    }}

    /* Bottom Subtitle / Caption Dock */
    .caption-dock {{
      position: absolute;
      bottom: 110px;
      left: 80px;
      right: 80px;
      height: 380px;
      z-index: 50;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
    }}
    .caption-box {{
      width: 100%;
      background: rgba(10, 15, 26, 0.94);
      border: 2px solid rgba(255, 255, 255, 0.12);
      border-radius: 32px;
      padding: 36px 40px;
      text-align: center;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8);
    }}
    .caption-speaker-badge {{
      display: inline-block;
      font-size: 14px;
      font-weight: 900;
      letter-spacing: 1.5px;
      margin-bottom: 18px;
      text-transform: uppercase;
      padding: 6px 18px;
      border-radius: 14px;
    }}
    .caption-speaker-badge.student {{
      background: rgba(56, 189, 248, 0.2);
      color: #38BDF8;
      border: 1px solid #38BDF8;
    }}
    .caption-speaker-badge.ai {{
      background: rgba(255, 153, 0, 0.2);
      color: #FF9900;
      border: 1px solid #FF9900;
    }}
    .caption-text {{
      font-size: 40px;
      font-weight: 800;
      line-height: 1.35;
      letter-spacing: -0.5px;
      color: #E2E8F0;
      min-height: 120px;
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      align-items: center;
      gap: 12px;
    }}
    .word {{
      display: inline-block;
      padding: 2px 6px;
      border-radius: 8px;
    }}
    .word.active-student {{
      color: #030712;
      background: #38BDF8;
      font-weight: 900;
      transform: scale(1.15) translateY(-3px);
      box-shadow: 0 0 25px rgba(56, 189, 248, 0.8);
    }}
    .word.active-ai {{
      color: #030712;
      background: #FF9900;
      font-weight: 900;
      transform: scale(1.15) translateY(-3px);
      box-shadow: 0 0 25px rgba(255, 153, 0, 0.8);
    }}

    /* Progress Bar */
    .progress-track {{
      position: absolute;
      bottom: 50px;
      left: 120px;
      right: 120px;
      height: 6px;
      background: rgba(255, 255, 255, 0.15);
      border-radius: 3px;
      overflow: hidden;
      z-index: 50;
    }}
    .progress-fill {{
      width: 0%;
      height: 100%;
      background: linear-gradient(90deg, #38BDF8, #FF9900);
      border-radius: 3px;
    }}
  </style>
</head>
<body>
  <div id="root" data-composition-id="aws-sbg-diu-reel" data-width="1080" data-height="1920" data-fps="30" data-duration="61.4">
    <!-- Atmospheric Layers -->
    <div class="grid-bg"></div>
    <div class="glow-orb glow-orange" id="orb-orange"></div>
    <div class="glow-orb glow-cyan" id="orb-cyan"></div>

    <!-- Master Voiceover & Audio Cues -->
    <audio id="vo-main" src="assets/audio/aws_sbg_dialogue.mp3" data-start="0.00" volume="1.0"></audio>
    <audio id="bg-drone" src="assets/sfx/tech_drone.wav" data-start="0.00" volume="0.08"></audio>
    <audio id="sfx-whoosh1" src="assets/sfx/real/whoosh.wav" data-start="0.10" volume="0.35"></audio>
    <audio id="sfx-pop1" src="assets/sfx/real/pop.wav" data-start="7.50" volume="0.35"></audio>
    <audio id="sfx-whoosh2" src="assets/sfx/real/whoosh.wav" data-start="16.10" volume="0.35"></audio>
    <audio id="sfx-click1" src="assets/sfx/real/click.wav" data-start="28.60" volume="0.35"></audio>
    <audio id="sfx-whoosh3" src="assets/sfx/real/whoosh.wav" data-start="41.50" volume="0.35"></audio>
    <audio id="sfx-chime1" src="assets/sfx/real/chime.wav" data-start="54.40" volume="0.45"></audio>

    <!-- Top Sticky Header -->
    <div class="header-bar">
      <div class="brand-group">
        <div class="brand-aws">aws</div>
        <div class="brand-divider"></div>
        <div class="brand-sbg">SBG <span class="brand-diu">DIU</span></div>
      </div>
      <div class="live-pill">
        <div class="live-dot" id="live-dot"></div>
        STUDENT BUILDER SQUAD
      </div>
    </div>

    <!-- Active Speaker Pill Indicator -->
    <div class="speaker-dock">
      <div id="speaker-tag" class="speaker-tag student">
        <span id="speaker-icon">🎓</span>
        <span id="speaker-name">STUDENT BUILDER</span>
      </div>
    </div>

    <!-- 3D Card Stage (6 Scenes) -->
    <div class="stage-container">
      <!-- Scene 1: Lost in the Cloud (0.00 - 7.50s) -->
      <div class="scene-card" id="card-1">
        <div class="card-top">
          <span class="topic-pill cyan">THE DILEMMA</span>
          <span class="card-number">01 / 06</span>
        </div>
        <div class="card-main">
          <h1 class="card-title">Lost in the<br/><span class="highlight-cyan">Cloud Maze?</span></h1>
          <div class="card-graphic">
            <img src="assets/logos/aws-logo.svg" style="width: 320px;" alt="AWS"/>
          </div>
          <div class="stat-box" style="width: 100%;">
            <div class="stat-val" style="color: #38BDF8;">200+ SERVICES</div>
            <div class="stat-label">Where does a student even start?</div>
          </div>
        </div>
        <div style="height: 10px;"></div>
      </div>

      <!-- Scene 2: Enter AWS SBG DIU (7.50 - 16.10s) -->
      <div class="scene-card" id="card-2">
        <div class="card-top">
          <span class="topic-pill">THE SOLUTION</span>
          <span class="card-number">02 / 06</span>
        </div>
        <div class="card-main">
          <h1 class="card-title">Enter<br/><span class="highlight-orange">AWS SBG DIU</span></h1>
          <div class="card-graphic">
            <img src="assets/logos/sbg-diu-badge.svg" style="width: 440px;" alt="AWS SBG DIU"/>
          </div>
          <div class="stat-box" style="width: 100%;">
            <div class="stat-val">OFFICIAL CHAPTER</div>
            <div class="stat-label">Daffodil International University</div>
          </div>
        </div>
        <div style="height: 10px;"></div>
      </div>

      <!-- Scene 3: Hands-On Architecture (16.10 - 28.60s) -->
      <div class="scene-card" id="card-3">
        <div class="card-top">
          <span class="topic-pill">NO BORING SLIDES</span>
          <span class="card-number">03 / 06</span>
        </div>
        <div class="card-main">
          <h1 class="card-title">Real Deployments.<br/><span class="highlight-orange">Live Cloud Labs.</span></h1>
          <div class="card-graphic">
            <img src="assets/logos/cloud-nodes.svg" style="width: 480px;" alt="Cloud Architecture"/>
          </div>
          <div class="stat-row">
            <div class="stat-box">
              <div class="stat-val">SERVERLESS</div>
              <div class="stat-label">Lambda & S3</div>
            </div>
            <div class="stat-box">
              <div class="stat-val">HACKATHONS</div>
              <div class="stat-label">Hands-On Sprints</div>
            </div>
          </div>
        </div>
        <div style="height: 10px;"></div>
      </div>

      <!-- Scene 4: Beginner Mentorship (28.60 - 41.50s) -->
      <div class="scene-card" id="card-4">
        <div class="card-top">
          <span class="topic-pill cyan">ZERO TO HERO</span>
          <span class="card-number">04 / 06</span>
        </div>
        <div class="card-main">
          <h1 class="card-title">Zero Experience?<br/><span class="highlight-cyan">Senior Mentors Got You.</span></h1>
          <div class="card-graphic">
            <img src="assets/logos/cert-badge.svg" style="width: 260px;" alt="AWS Certified"/>
          </div>
          <div class="stat-box" style="width: 100%;">
            <div class="stat-val" style="color: #38BDF8;">AWS CERTIFIED</div>
            <div class="stat-label">Guided preparation & free student roadmap</div>
          </div>
        </div>
        <div style="height: 10px;"></div>
      </div>

      <!-- Scene 5: Career Ready (41.50 - 54.40s) -->
      <div class="scene-card" id="card-5">
        <div class="card-top">
          <span class="topic-pill">CAREER ADVANTAGE</span>
          <span class="card-number">05 / 06</span>
        </div>
        <div class="card-main">
          <h1 class="card-title">Production Skills<br/><span class="highlight-orange">Employers Fight For</span></h1>
          <div class="stat-row" style="margin-top: 20px;">
            <div class="stat-box">
              <div class="stat-val">RESUME</div>
              <div class="stat-label">Real Portfolio Work</div>
            </div>
            <div class="stat-box">
              <div class="stat-val">NETWORK</div>
              <div class="stat-label">Top Industry Alumni</div>
            </div>
          </div>
          <div class="stat-box" style="width: 100%; border-color: rgba(255,153,0,0.4);">
            <div class="stat-val">COMMUNITY</div>
            <div class="stat-label">Dozens of passionate Daffodil engineers</div>
          </div>
        </div>
        <div style="height: 10px;"></div>
      </div>

      <!-- Scene 6: The Call to Action (54.40 - 61.40s) -->
      <div class="scene-card" id="card-6">
        <div class="card-top">
          <span class="topic-pill">GRAB YOUR SEAT</span>
          <span class="card-number">06 / 06</span>
        </div>
        <div class="card-main">
          <h1 class="card-title">Next Meetup<br/><span class="highlight-orange">On Campus</span></h1>
          <div class="card-graphic">
            <img src="assets/logos/meetup-banner.svg" style="width: 480px;" alt="Meetup Banner"/>
          </div>
          <div class="stat-box" style="width: 100%; background: rgba(255, 153, 0, 0.15); border-color: #FF9900;">
            <div class="stat-val" style="color: #FFFFFF;">👇 COMMENT BELOW</div>
            <div class="stat-label" style="color: #FFB84D; font-size: 18px; font-weight: 800;">"MEETUP" FOR THE DIRECT LINK</div>
          </div>
        </div>
        <div style="height: 10px;"></div>
      </div>
    </div>

    <!-- Subtitle Caption Box -->
    <div class="caption-dock">
      <div class="caption-box">
        <div id="caption-badge" class="caption-speaker-badge student">STUDENT BUILDER</div>
        <div id="caption-text" class="caption-text">
          Loading conversation...
        </div>
      </div>
    </div>

    <!-- Progress Track -->
    <div class="progress-track">
      <div id="progress-fill" class="progress-fill"></div>
    </div>
  </div>

  <!-- GSAP Animation Core -->
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
  <script>
    const WORDS = {json.dumps(words)};
    const SPANS = {json.dumps(spans)};

    const speakerTag = document.getElementById("speaker-tag");
    const speakerIcon = document.getElementById("speaker-icon");
    const speakerName = document.getElementById("speaker-name");
    const captionBadge = document.getElementById("caption-badge");
    const captionText = document.getElementById("caption-text");
    const progressFill = document.getElementById("progress-fill");

    let currentSpanIndex = -1;

    function renderSpan(spanIndex) {{
      const span = SPANS[spanIndex];
      const speaker = span.speaker;
      
      // Update Speaker indicators
      if (speaker === "student") {{
        speakerTag.className = "speaker-tag student";
        speakerIcon.textContent = "🎓";
        speakerName.textContent = "STUDENT BUILDER";
        captionBadge.className = "caption-speaker-badge student";
        captionBadge.textContent = "STUDENT BUILDER";
      }} else {{
        speakerTag.className = "speaker-tag ai";
        speakerIcon.textContent = "⚡";
        speakerName.textContent = "AWS CLOUD AI";
        captionBadge.className = "caption-speaker-badge ai";
        captionBadge.textContent = "AWS CLOUD AI";
      }}

      // Build word elements for this span
      const spanWords = WORDS.filter(w => w.start >= span.start - 0.05 && w.end <= span.end + 0.15);
      captionText.innerHTML = spanWords.map((w, idx) => 
        `<span class="word" id="w-${{spanIndex}}-${{idx}}" data-start="${{w.start}}" data-end="${{w.end}}" data-speaker="${{speaker}}">${{w.word}}</span>`
      ).join(" ");
    }}

    function updateHUD(t) {{
      const totalDur = 61.4;
      progressFill.style.width = Math.min(100, (t / totalDur) * 100) + "%";

      // Check Dialogue Span
      for (let i = 0; i < SPANS.length; i++) {{
        if (t >= SPANS[i].start && t < SPANS[i].end + 0.25) {{
          if (currentSpanIndex !== i) {{
            currentSpanIndex = i;
            renderSpan(i);
          }}
          break;
        }}
      }}

      // Highlight active words
      const wordEls = captionText.getElementsByClassName("word");
      for (let i = 0; i < wordEls.length; i++) {{
        const el = wordEls[i];
        const wStart = parseFloat(el.getAttribute("data-start"));
        const wEnd = parseFloat(el.getAttribute("data-end"));
        const speaker = el.getAttribute("data-speaker");
        const activeClass = speaker === "student" ? "active-student" : "active-ai";

        if (t >= wStart && t <= wEnd + 0.08) {{
          if (!el.classList.contains(activeClass)) {{
            el.classList.add(activeClass);
          }}
        }} else {{
          el.classList.remove("active-student", "active-ai");
        }}
      }}
    }}

    const tl = gsap.timeline({{ paused: true, onUpdate: function() {{ updateHUD(this.time()); }} }});

    // Ambient floating lights
    tl.to("#orb-orange", {{ x: 40, y: -30, duration: 6, yoyo: true, repeat: 10, ease: "sine.inOut" }}, 0);
    tl.to("#orb-cyan", {{ x: -50, y: 40, duration: 7, yoyo: true, repeat: 9, ease: "sine.inOut" }}, 0);

    // Scene 1: Lost in the Cloud (0.00 -> 7.50)
    tl.set("#card-1", {{ opacity: 1 }}, 0)
      .fromTo("#card-1", {{ y: 80, scale: 0.85, rotateX: 15 }}, {{ y: 0, scale: 1, rotateX: 0, duration: 0.6, ease: "back.out(1.5)" }}, 0.05)
      .to("#card-1", {{ opacity: 0, y: -60, scale: 0.9, duration: 0.35, ease: "power2.in" }}, 7.15);

    // Scene 2: Enter AWS SBG DIU (7.50 -> 16.10)
    tl.set("#card-2", {{ opacity: 1 }}, 7.50)
      .fromTo("#card-2", {{ y: 80, scale: 0.85, rotateX: 15 }}, {{ y: 0, scale: 1, rotateX: 0, duration: 0.6, ease: "back.out(1.5)" }}, 7.50)
      .to("#card-2", {{ opacity: 0, y: -60, scale: 0.9, duration: 0.35, ease: "power2.in" }}, 15.75);

    // Scene 3: Hands-On Architecture (16.10 -> 28.60)
    tl.set("#card-3", {{ opacity: 1 }}, 16.10)
      .fromTo("#card-3", {{ y: 80, scale: 0.85, rotateX: 15 }}, {{ y: 0, scale: 1, rotateX: 0, duration: 0.6, ease: "back.out(1.5)" }}, 16.10)
      .to("#card-3", {{ opacity: 0, y: -60, scale: 0.9, duration: 0.35, ease: "power2.in" }}, 28.25);

    // Scene 4: Beginner Mentorship (28.60 -> 41.50)
    tl.set("#card-4", {{ opacity: 1 }}, 28.60)
      .fromTo("#card-4", {{ y: 80, scale: 0.85, rotateX: 15 }}, {{ y: 0, scale: 1, rotateX: 0, duration: 0.6, ease: "back.out(1.5)" }}, 28.60)
      .to("#card-4", {{ opacity: 0, y: -60, scale: 0.9, duration: 0.35, ease: "power2.in" }}, 41.15);

    // Scene 5: Career Ready (41.50 -> 54.40)
    tl.set("#card-5", {{ opacity: 1 }}, 41.50)
      .fromTo("#card-5", {{ y: 80, scale: 0.85, rotateX: 15 }}, {{ y: 0, scale: 1, rotateX: 0, duration: 0.6, ease: "back.out(1.5)" }}, 41.50)
      .to("#card-5", {{ opacity: 0, y: -60, scale: 0.9, duration: 0.35, ease: "power2.in" }}, 54.05);

    // Scene 6: The Call to Action (54.40 -> 61.40)
    tl.set("#card-6", {{ opacity: 1 }}, 54.40)
      .fromTo("#card-6", {{ y: 80, scale: 0.85, rotateX: 15 }}, {{ y: 0, scale: 1, rotateX: 0, duration: 0.6, ease: "back.out(1.5)" }}, 54.40)
      .to("#card-6 .stat-box", {{ scale: 1.05, duration: 0.7, yoyo: true, repeat: 7, ease: "sine.inOut" }}, 55.0);

    tl.set({{}}, {{}}, 61.40);
    updateHUD(0);

    window.__timelines = window.__timelines || {{}};
    window.__timelines["aws-sbg-diu-reel"] = tl;
  </script>
</body>
</html>
"""
    out_path = ENGINE_DIR / "aws-sbg-diu.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"Generated HyperFrames composition: {out_path}")

if __name__ == "__main__":
    build()
