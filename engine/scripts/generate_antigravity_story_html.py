import json
import os
import subprocess

ENGINE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(ENGINE_DIR, "assets/audio")

EPISODE_META = {
    1: {
        "num": "01",
        "title": "THE $5 UNLOCK",
        "theme": "CURIOSITY · ENVIRONMENT & WORKFLOW",
    },
    2: {
        "num": "02",
        "title": "FROM IDEAS TO PRODUCTS",
        "theme": "CREATIVITY · AAYOJON 3D & ARCHITECTURE",
    },
    3: {
        "num": "03",
        "title": "BUILDING BEYOND THE SCREEN",
        "theme": "OPPORTUNITY · AWS CLOUD & DIU COMMUNITY",
    },
    4: {
        "num": "04",
        "title": "BEYOND NORMAL DEVELOPMENT",
        "theme": "EXPLORATION · SOSDaR24 & RAILSIM RESEARCH",
    },
    5: {
        "num": "05",
        "title": "BUILDING MY OWN AI CREATOR WORKFLOW",
        "theme": "ACHIEVEMENT · OMNIVOICE & VIDMOTIONCRAFT",
    },
}


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
      <!-- SCENE 1: HOOK -->
      <div id="scene-1" class="scene">
        <div class="eyebrow">EPISODE 01 · OPENING HOOK</div>
        <div class="card hero-card">
          <div class="light-sweep"></div>
          <div class="kicker">WHAT IF JUST</div>
          <div class="price-hero">
            <span class="price-strike">$20</span>
            <span class="price-arrow">→</span>
            <span class="price-glow">$5</span>
          </div>
          <div class="headline-lg">THE $5 UNLOCK</div>
          <div class="subtext">A completely different way of building software.</div>
        </div>
      </div>

      <!-- SCENE 2: DISCOVERY -->
      <div id="scene-2" class="scene">
        <div class="eyebrow">DISCOVERY · STUDENT ACCESS</div>
        <div class="card">
          <div class="logo-row">
            <img src="assets/logos/antigravity-official.png" class="logo-box" alt="Antigravity" />
            <span class="conn-line"></span>
            <img src="assets/logos/gemini-official.svg" class="logo-box" alt="Gemini" />
          </div>
          <div class="headline-md">Antigravity Student Offer</div>
          <div class="subtext">Not just getting access—exploring what I could actually build with it.</div>
          <div class="pill-row">
            <span class="tech-pill blue">AI Workspace</span>
            <span class="tech-pill cyan">3D Laptop View ↑</span>
            <span class="tech-pill violet">Real Builds</span>
          </div>
        </div>
      </div>

      <!-- SCENE 3: DEVELOPMENT ENVIRONMENT -->
      <div id="scene-3" class="scene">
        <div class="eyebrow">ENVIRONMENT · UBUNTU &amp; OPENCODE</div>
        <div class="term-window">
          <div class="term-header">
            <span class="tdot r"></span><span class="tdot y"></span><span class="tdot g"></span>
            <span class="term-title">rafi@ubuntu-dev: ~/workspace</span>
          </div>
          <div class="term-body">
            <div class="tline"><span class="tprompt">$</span> sudo apt update &amp;&amp; opencode init</div>
            <div class="tline cyan">→ Configuring AI models &amp; agents...</div>
            <div class="tline"><span class="tprompt">$</span> agy workflow --connect-terminal</div>
            <div class="tline ok">✓ Ubuntu + OpenCode + AI pipeline active</div>
          </div>
        </div>
        <div class="icon-bar">
          <div class="ico-chip"><img src="assets/logos/ubuntu.svg" alt="Ubuntu" /><span>Ubuntu</span></div>
          <div class="ico-chip"><img src="assets/logos/python.svg" alt="Python" /><span>Python</span></div>
          <div class="ico-chip"><img src="assets/logos/nodedotjs.svg" alt="Node" /><span>OpenCode</span></div>
        </div>
      </div>

      <!-- SCENE 4: LEARNING BY EXPERIMENTING -->
      <div id="scene-4" class="scene">
        <div class="eyebrow">ITERATION · HANDS-ON LEARNING</div>
        <div class="card">
          <div class="headline-md">Every Command Taught Something New</div>
          <div class="diagram-grid">
            <div class="diag-node">
              <div class="diag-num">01</div>
              <div class="diag-lbl">Setup &amp; Config</div>
            </div>
            <div class="diag-node active">
              <div class="diag-num">02</div>
              <div class="diag-lbl">CLI Workflows</div>
            </div>
            <div class="diag-node">
              <div class="diag-num">03</div>
              <div class="diag-lbl">Model Tuning</div>
            </div>
          </div>
          <div class="subtext">And this was just the beginning of the 5-day journey.</div>
        </div>
      </div>

      <!-- SCENE 5: TRANSITION TO PRODUCTS -->
      <div id="scene-5" class="scene">
        <div class="eyebrow">THE NEXT CHALLENGE</div>
        <div class="card">
          <div class="kicker">BEYOND INSTALLING TOOLS</div>
          <div class="headline-lg">IDEAS INTO <span class="txt-cyan">PRODUCTS</span></div>
          <div class="flow-row">
            <span class="flow-box">Raw Concept</span>
            <span class="flow-arr">→</span>
            <span class="flow-box">Architecture</span>
            <span class="flow-arr">→</span>
            <span class="flow-box highlight">Real App</span>
          </div>
        </div>
      </div>

      <!-- SCENE 6: ENDING TEASER -->
      <div id="scene-6" class="scene">
        <div class="eyebrow">UP NEXT · EPISODE 02</div>
        <div class="card teaser-card">
          <div class="teaser-badge">NEXT EPISODE TEASER</div>
          <div class="headline-md">What happens when ideas become real products?</div>
          <div class="subtext">Exploring Aayojon 3D, system architecture, APIs &amp; SaaS design.</div>
          <div class="cta-pill">02 — FROM IDEAS TO PRODUCTS →</div>
        </div>
      </div>
"""
    if part_num == 2:
        return """
      <!-- SCENE 1: HOOK -->
      <div id="scene-1" class="scene">
        <div class="eyebrow">EPISODE 02 · OPENING HOOK</div>
        <div class="card hero-card">
          <div class="light-sweep"></div>
          <div class="kicker">THE REAL QUESTION</div>
          <div class="headline-lg">IDEAS ARE EASY.<br/><span class="txt-cyan">BUILDING IS DIFFERENT.</span></div>
          <div class="subtext">Can you turn an idea into something people can actually use?</div>
        </div>
      </div>

      <!-- SCENE 2: AAYOJON 3D REAL PROJECT FOOTAGE -->
      <div id="scene-2" class="scene">
        <div class="eyebrow">PROJECT · AAYOJON 3D SAAS</div>
        <div class="card">
          <div class="screenshot-grid">
            <div class="shot-card">
              <img src="assets/aayojon/home.png" alt="Aayojon Home" />
              <span>Dashboard</span>
            </div>
            <div class="shot-card">
              <img src="assets/aayojon/events.png" alt="Aayojon Events" />
              <span>Events</span>
            </div>
            <div class="shot-card">
              <img src="assets/aayojon/venues.png" alt="Aayojon Venues" />
              <span>3D Venues</span>
            </div>
          </div>
          <div class="headline-md">Aayojon 3D Event Platform</div>
          <div class="subtext">Exploring the concept of an event management SaaS platform.</div>
        </div>
      </div>

      <!-- SCENE 3: PRODUCT ARCHITECTURE -->
      <div id="scene-3" class="scene">
        <div class="eyebrow">THE BIGGER PICTURE · ARCHITECTURE</div>
        <div class="card">
          <div class="headline-md">Beyond Just the Interface</div>
          <svg class="arch-svg" viewBox="0 0 680 170">
            <rect x="10" y="25" width="140" height="120" rx="16" fill="#EFF6FF" stroke="#2563EB" stroke-width="2.5"/>
            <text x="80" y="78" text-anchor="middle" fill="#0F172A" font-size="20" font-weight="800">PRD &amp; UX</text>
            <text x="80" y="106" text-anchor="middle" fill="#475569" font-size="14">Requirements</text>
            <line x1="150" y1="85" x2="200" y2="85" stroke="#0284C7" stroke-width="3" stroke-dasharray="6 4"/>
            <rect x="200" y="25" width="140" height="120" rx="16" fill="#F0F9FF" stroke="#0284C7" stroke-width="2.5"/>
            <text x="270" y="78" text-anchor="middle" fill="#0F172A" font-size="20" font-weight="800">REST APIs</text>
            <text x="270" y="106" text-anchor="middle" fill="#475569" font-size="14">System Logic</text>
            <line x1="340" y1="85" x2="390" y2="85" stroke="#7C3AED" stroke-width="3" stroke-dasharray="6 4"/>
            <rect x="390" y="25" width="280" height="120" rx="16" fill="#F5F3FF" stroke="#7C3AED" stroke-width="2.5"/>
            <text x="530" y="78" text-anchor="middle" fill="#0F172A" font-size="20" font-weight="800">Database Schema</text>
            <text x="530" y="106" text-anchor="middle" fill="#7C3AED" font-size="14" font-weight="700">Scalable Data Layer</text>
          </svg>
          <div class="pill-row">
            <span class="tech-pill blue">PRD Docs</span>
            <span class="tech-pill cyan">System Design</span>
            <span class="tech-pill violet">DB Modeling</span>
          </div>
        </div>
      </div>

      <!-- SCENE 4: BREAKING DOWN COMPLEXITY -->
      <div id="scene-4" class="scene">
        <div class="eyebrow">ENGINEERING MINDSET</div>
        <div class="card">
          <div class="headline-md">Breaking Big Ideas Into Buildable Pieces</div>
          <div class="diagram-grid">
            <div class="diag-node"><div class="diag-num">UI</div><div class="diag-lbl">Frontend View</div></div>
            <div class="diag-node active"><div class="diag-num">API</div><div class="diag-lbl">Service Layer</div></div>
            <div class="diag-node"><div class="diag-num">DB</div><div class="diag-lbl">State &amp; Auth</div></div>
          </div>
          <div class="subtext">A professional product isn't just how it looks—it's how it works.</div>
        </div>
      </div>

      <!-- SCENE 5: FROM CONCEPT TO PRODUCT -->
      <div id="scene-5" class="scene">
        <div class="eyebrow">SYSTEM INTEGRATION</div>
        <div class="card">
          <div class="kicker">HOW EVERYTHING WORKS TOGETHER</div>
          <div class="headline-lg">FROM CONCEPT TO <span class="txt-cyan">PRODUCT</span></div>
          <div class="subtext">And then my attention shifted to something much bigger: the cloud.</div>
        </div>
      </div>

      <!-- SCENE 6: ENDING TEASER -->
      <div id="scene-6" class="scene">
        <div class="eyebrow">UP NEXT · EPISODE 03</div>
        <div class="card teaser-card">
          <div class="teaser-badge">NEXT EPISODE TEASER</div>
          <div class="headline-md">Taking development beyond the local machine.</div>
          <div class="subtext">Exploring AWS Cloud, DevOps &amp; Student Build &amp; Grow at DIU.</div>
          <div class="cta-pill">03 — BUILDING BEYOND THE SCREEN →</div>
        </div>
      </div>
"""
    if part_num == 3:
        return """
      <!-- SCENE 1: HOOK -->
      <div id="scene-1" class="scene">
        <div class="eyebrow">EPISODE 03 · OPENING HOOK</div>
        <div class="card hero-card">
          <div class="light-sweep"></div>
          <div class="kicker">ACCESSIBLE · SCALABLE · USEFUL</div>
          <div class="headline-lg">BEYOND THE <span class="txt-cyan">LOCAL MACHINE</span></div>
          <div class="subtext">Moving from local code to scalable cloud infrastructure.</div>
        </div>
      </div>

      <!-- SCENE 2: AWS & CLOUD -->
      <div id="scene-2" class="scene">
        <div class="eyebrow">CLOUD INFRASTRUCTURE · AWS</div>
        <div class="card">
          <div class="logo-row">
            <img src="assets/logos/aws-logo.svg" class="logo-box" alt="AWS" />
            <span class="conn-line"></span>
            <img src="assets/logos/cloud-nodes.svg" class="logo-box" alt="Cloud" />
            <span class="conn-line"></span>
            <img src="assets/logos/docker.svg" class="logo-box" alt="DevOps" />
          </div>
          <div class="headline-md">Exploring AWS &amp; Cloud Computing</div>
          <div class="pill-row">
            <span class="tech-pill blue">Cloud Nodes</span>
            <span class="tech-pill cyan">DevOps Pipelines</span>
            <span class="tech-pill violet">Global Scale</span>
          </div>
        </div>
      </div>

      <!-- SCENE 3: DIU AWS STUDENT BUILD & GROW REAL ASSETS -->
      <div id="scene-3" class="scene">
        <div class="eyebrow">COMMUNITY · AWS SBG AT DIU</div>
        <div class="card">
          <div class="sbg-showcase">
            <img src="assets/logos/sbg_post_graphic.jpg" class="sbg-poster" alt="AWS SBG DIU Poster" />
            <div class="sbg-meta">
              <img src="assets/logos/diu_full_logo.png" class="diu-logo" alt="DIU" />
              <div class="sbg-title">AWS Student Build &amp; Grow</div>
              <div class="sbg-sub">Cloud Computing · DevOps · Student Opportunities</div>
            </div>
          </div>
        </div>
      </div>

      <!-- SCENE 4: SHARED KNOWLEDGE -->
      <div id="scene-4" class="scene">
        <div class="eyebrow">COMMUNITY IMPACT</div>
        <div class="card">
          <div class="headline-md">Knowledge Shared = Stronger Communities</div>
          <div class="flow-row">
            <span class="flow-box">Students</span>
            <span class="flow-arr">→</span>
            <span class="flow-box highlight">Cloud Skills</span>
            <span class="flow-arr">→</span>
            <span class="flow-box">Real Builders</span>
          </div>
          <div class="subtext">Technology becomes more powerful when communities grow together.</div>
        </div>
      </div>

      <!-- SCENE 5: BIGGER PICTURE -->
      <div id="scene-5" class="scene">
        <div class="eyebrow">EXPANDING HORIZONS</div>
        <div class="card">
          <div class="kicker">LOCAL DEV → CLOUD INFRASTRUCTURE</div>
          <div class="headline-lg">NEXT: RESEARCH &amp; <span class="txt-cyan">SIMULATION</span></div>
          <div class="subtext">My next experiment took me somewhere completely unexpected.</div>
        </div>
      </div>

      <!-- SCENE 6: ENDING TEASER -->
      <div id="scene-6" class="scene">
        <div class="eyebrow">UP NEXT · EPISODE 04</div>
        <div class="card teaser-card">
          <div class="teaser-badge">NEXT EPISODE TEASER</div>
          <div class="headline-md">What if software development meets the real world?</div>
          <div class="subtext">Into SOSDaR24 datasets, CARLA &amp; railway simulation research.</div>
          <div class="cta-pill">04 — BEYOND NORMAL DEVELOPMENT →</div>
        </div>
      </div>
"""
    if part_num == 4:
        return """
      <!-- SCENE 1: HOOK -->
      <div id="scene-1" class="scene">
        <div class="eyebrow">EPISODE 04 · OPENING HOOK</div>
        <div class="card hero-card">
          <div class="light-sweep"></div>
          <div class="kicker">STARTS WITH A QUESTION</div>
          <div class="headline-lg">DEVELOPMENT MEETS <span class="txt-cyan">RESEARCH</span></div>
          <div class="subtext">Not every developer experiment starts with an app.</div>
        </div>
      </div>

      <!-- SCENE 2: SOSDaR24 DATASET -->
      <div id="scene-2" class="scene">
        <div class="eyebrow">DATASET EXPLORATION · SOSDaR24</div>
        <div class="card">
          <div class="headline-md">SOSDaR24 Railway Dataset</div>
          <svg class="arch-svg" viewBox="0 0 680 160">
            <rect x="15" y="20" width="200" height="120" rx="16" fill="#F0F9FF" stroke="#0284C7" stroke-width="2.5"/>
            <text x="115" y="72" text-anchor="middle" fill="#0284C7" font-size="20" font-weight="800">LiDAR Point Cloud</text>
            <text x="115" y="102" text-anchor="middle" fill="#475569" font-size="14">3D Track Geometry</text>
            <rect x="240" y="20" width="200" height="120" rx="16" fill="#EFF6FF" stroke="#2563EB" stroke-width="2.5"/>
            <text x="340" y="72" text-anchor="middle" fill="#0F172A" font-size="20" font-weight="800">Multi-Sensor Data</text>
            <text x="340" y="102" text-anchor="middle" fill="#475569" font-size="14">RGB + Radar + IMU</text>
            <rect x="465" y="20" width="200" height="120" rx="16" fill="#F5F3FF" stroke="#7C3AED" stroke-width="2.5"/>
            <text x="565" y="72" text-anchor="middle" fill="#0F172A" font-size="20" font-weight="800">Reconstruction</text>
            <text x="565" y="102" text-anchor="middle" fill="#7C3AED" font-size="14" font-weight="700">Synthetic Scenarios</text>
          </svg>
          <div class="subtext">Exploring possibilities of generating &amp; reconstructing railway simulation data.</div>
        </div>
      </div>

      <!-- SCENE 3: RAILSIM CONCEPT & CARLA -->
      <div id="scene-3" class="scene">
        <div class="eyebrow">CONCEPT · RAILSIM DATASET GENERATOR</div>
        <div class="term-window">
          <div class="term-header">
            <span class="tdot r"></span><span class="tdot y"></span><span class="tdot g"></span>
            <span class="term-title">railsim-research-spec.md</span>
          </div>
          <div class="term-body">
            <div class="tline cyan"># RailSim Environment Exploration</div>
            <div class="tline">• Simulator: CARLA Unreal Engine Pipeline</div>
            <div class="tline">• OS Target: Ubuntu 22.04 LTS</div>
            <div class="tline ok">• Compute: Dedicated GPU VRAM &amp; Raycasting</div>
          </div>
        </div>
        <div class="pill-row">
          <span class="tech-pill blue">CARLA Exploration</span>
          <span class="tech-pill cyan">Ubuntu 22.04</span>
          <span class="tech-pill violet">GPU Requirements</span>
        </div>
      </div>

      <!-- SCENE 4: RESEARCH PROCESS -->
      <div id="scene-4" class="scene">
        <div class="eyebrow">RESEARCH BEFORE IMPLEMENTATION</div>
        <div class="card">
          <div class="headline-md">Understanding Before Writing Code</div>
          <div class="subtext">There was a lot to map out before the first real implementation—and that's what makes research exciting.</div>
          <div class="pill-row">
            <span class="tech-pill cyan">Feasibility Study</span>
            <span class="tech-pill blue">Architecture Planning</span>
          </div>
        </div>
      </div>

      <!-- SCENE 5: HONEST RESEARCH PIPELINE -->
      <div id="scene-5" class="scene">
        <div class="eyebrow">PROPOSED RESEARCH PIPELINE</div>
        <div class="card">
          <div class="kicker">DISCOVERING WHAT'S POSSIBLE</div>
          <div class="pipe-grid">
            <div class="pipe-step"><span>01</span>DATA</div>
            <div class="pipe-step"><span>02</span>SIMULATION</div>
            <div class="pipe-step"><span>03</span>GENERATION</div>
            <div class="pipe-step active"><span>04</span>RECONSTRUCTION</div>
          </div>
          <div class="subtext">Mapping the path from raw dataset research to future simulation workflows.</div>
        </div>
      </div>

      <!-- SCENE 6: ENDING TEASER -->
      <div id="scene-6" class="scene">
        <div class="eyebrow">UP NEXT · EPISODE 05 (FINALE)</div>
        <div class="card teaser-card">
          <div class="teaser-badge">SERIES FINALE TEASER</div>
          <div class="headline-md">Next: Bringing everything together.</div>
          <div class="subtext">Building my own AI creator workflow with OmniVoice &amp; VidMotionCraft.</div>
          <div class="cta-pill">05 — AI CREATOR WORKFLOW →</div>
        </div>
      </div>
"""
    return """
      <!-- SCENE 1: 5-DAY RECAP MONTAGE -->
      <div id="scene-1" class="scene">
        <div class="eyebrow">EPISODE 05 · SERIES FINALE</div>
        <div class="card hero-card">
          <div class="light-sweep"></div>
          <div class="headline-lg">FIVE DAYS.<br/><span class="txt-cyan">COUNTLESS EXPERIMENTS.</span></div>
          <div class="ep-mini-grid">
            <div class="ep-mini"><span>01</span>$5 Unlock</div>
            <div class="ep-mini"><span>02</span>Aayojon 3D</div>
            <div class="ep-mini"><span>03</span>AWS @ DIU</div>
            <div class="ep-mini"><span>04</span>RailSim R&amp;D</div>
          </div>
        </div>
      </div>

      <!-- SCENE 2: HANDY + OMNIVOICE WORKFLOW -->
      <div id="scene-2" class="scene">
        <div class="eyebrow">VOICE PIPELINE · HANDY &amp; OMNIVOICE</div>
        <div class="card">
          <div class="wave-viz">
            <span class="wbar"></span><span class="wbar"></span><span class="wbar"></span>
            <span class="wbar"></span><span class="wbar"></span><span class="wbar"></span>
            <span class="wbar"></span><span class="wbar"></span><span class="wbar"></span>
            <span class="wbar"></span><span class="wbar"></span>
          </div>
          <div class="headline-md">Handy Dictation + OmniVoice Local Clone</div>
          <div class="subtext">Custom voice profiles synthesized locally on Apple Silicon MPS GPU.</div>
          <div class="pill-row">
            <span class="tech-pill blue">Handy STT</span>
            <span class="tech-pill cyan">OmniVoice TTS</span>
            <span class="tech-pill violet">native_rafi_ref.wav</span>
          </div>
        </div>
      </div>

      <!-- SCENE 3: VIDMOTIONCRAFT ENGINE -->
      <div id="scene-3" class="scene">
        <div class="eyebrow">VIDMOTIONCRAFT · CODE-DRIVEN VIDEO</div>
        <div class="term-window">
          <div class="term-header">
            <span class="tdot r"></span><span class="tdot y"></span><span class="tdot g"></span>
            <span class="term-title">VidMotionCraft — HyperFrames + Three.js + GSAP</span>
          </div>
          <div class="term-body">
            <div class="tline"><span class="tprompt">$</span> npx hyperframes render story-part5-en.html</div>
            <div class="tline cyan">→ HTML5 + GSAP Timeline + Three.js 3D Scene</div>
            <div class="tline ok">✓ Word-Synced Captions + Layered SFX → 1080p MP4</div>
          </div>
        </div>
        <div class="icon-bar">
          <div class="ico-chip"><img src="assets/logos/hyperframes-studio.png" alt="HyperFrames" /><span>HyperFrames</span></div>
          <div class="ico-chip"><img src="assets/logos/greensock.svg" alt="GSAP" /><span>GSAP</span></div>
          <div class="ico-chip"><img src="assets/logos/ffmpeg.svg" alt="FFmpeg" /><span>FFmpeg</span></div>
        </div>
      </div>

      <!-- SCENE 4: UNDERSTANDING THE WORKFLOW -->
      <div id="scene-4" class="scene">
        <div class="eyebrow">THE DEVELOPER MINDSET</div>
        <div class="card">
          <div class="headline-md">Understanding the Workflow Behind Creation</div>
          <div class="flow-row">
            <span class="flow-box">Script &amp; Voice</span>
            <span class="flow-arr">→</span>
            <span class="flow-box">2D/3D Code</span>
            <span class="flow-arr">→</span>
            <span class="flow-box highlight">Automated Reel</span>
          </div>
          <div class="subtext">Even this 5-part documentary series was built inside the experiment.</div>
        </div>
      </div>

      <!-- SCENE 5: CORE MESSAGE -->
      <div id="scene-5" class="scene">
        <div class="eyebrow">CORE MESSAGE</div>
        <div class="card hero-card">
          <div class="headline-md" style="font-size:36px; line-height:1.28;">
            "AI doesn't replace developers.<br/>
            <span class="txt-cyan">It gives developers new ways to think, create, and build."</span>
          </div>
          <div class="subtext">When students stop waiting for the future and start building it.</div>
        </div>
      </div>

      <!-- SCENE 6: FINAL REVEAL & CTA -->
      <div id="scene-6" class="scene">
        <div class="eyebrow">COMPLETE 5-PART SERIES</div>
        <div class="card teaser-card">
          <div class="ep-timeline-row">
            <span class="ep-dot">01</span><span class="ep-bar"></span>
            <span class="ep-dot">02</span><span class="ep-bar"></span>
            <span class="ep-dot">03</span><span class="ep-bar"></span>
            <span class="ep-dot">04</span><span class="ep-bar"></span>
            <span class="ep-dot active">05</span>
          </div>
          <div class="headline-lg" style="font-size:42px;">5 DAYS WITH ANTIGRAVITY</div>
          <div class="kicker" style="color:#0284C7;">THIS IS ONLY THE BEGINNING.</div>
          <div class="cta-pill">FOLLOW THE JOURNEY →</div>
        </div>
      </div>
"""


def build_part_html(part_num: int):
    prefix = f"story_part{part_num}_en"
    mp3_path = os.path.join(AUDIO_DIR, f"{prefix}.mp3")
    ts_path = os.path.join(AUDIO_DIR, f"{prefix}.timestamps.json")
    spans_path = os.path.join(AUDIO_DIR, f"{prefix}.spans.json")

    with open(ts_path, encoding="utf-8") as f:
        words = json.load(f)
    with open(spans_path, encoding="utf-8") as f:
        spans = json.load(f)

    dur = round(get_duration(mp3_path) + 0.5, 2)
    t1 = spans[0]["start"]
    t2 = spans[1]["start"]
    t3 = spans[2]["start"]
    t4 = spans[3]["start"]
    t5 = spans[4]["start"]
    t6 = spans[5]["start"]

    meta = EPISODE_META[part_num]
    scenes_html = scene_markup(part_num)
    words_json = json.dumps(words, ensure_ascii=False)
    comp_id = f"story-part{part_num}-en"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>{comp_id}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700;800;900&family=JetBrains+Mono:wght@600;700;800&family=Space+Grotesk:wght@700;800&display=swap" rel="stylesheet" />
<script src="assets/js/gsap.min.js"></script>
<script src="assets/js/three.min.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    width: 1080px;
    height: 1920px;
    overflow: hidden;
    background: #F8FAFC;
    font-family: 'Inter', -apple-system, sans-serif;
    color: #0F172A;
  }}
  .stage {{
    position: relative;
    width: 1080px;
    height: 1920px;
    background:
      radial-gradient(circle at 20% 15%, rgba(37, 99, 235, 0.14) 0%, transparent 45%),
      radial-gradient(circle at 80% 75%, rgba(124, 58, 237, 0.13) 0%, transparent 48%),
      linear-gradient(180deg, #F8FAFC 0%, #EEF2FF 52%, #F8FAFC 100%);
    overflow: hidden;
  }}
  .bg-grid {{
    position: absolute;
    inset: 0;
    background-image: radial-gradient(rgba(15, 23, 42, 0.10) 1.5px, transparent 1.5px);
    background-size: 38px 38px;
    pointer-events: none;
  }}
  #three-canvas {{
    position: absolute;
    inset: 0;
    width: 1080px;
    height: 1920px;
    pointer-events: none;
    z-index: 25;
  }}

  /* MANDATORY INSTAGRAM REELS SAFE ZONE: x=90..900 (width 810), y=220..1550 (height 1330) */
  .safe-zone {{
    position: absolute;
    left: 90px;
    top: 220px;
    width: 810px;
    height: 1330px;
    z-index: 20;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .safe-zone-guide {{
    position: absolute;
    left: 90px;
    top: 220px;
    width: 810px;
    height: 1330px;
    border: 3px dashed #2563EB;
    background: rgba(37, 99, 235, 0.03);
    z-index: 999;
    pointer-events: none;
    display: none;
  }}

  /* Top Series Header inside Safe Zone (Light Theme) */
  .series-header {{
    width: 100%;
    background: #FFFFFF;
    border: 2.5px solid #0F172A;
    border-radius: 24px;
    padding: 18px 24px;
    box-shadow: 0 8px 0 #0F172A, 0 18px 36px rgba(15, 23, 42, 0.08);
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}
  .sh-top {{
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .sh-brand {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}
  .sh-logo {{
    width: 42px;
    height: 42px;
    border-radius: 10px;
    border: 2px solid #0F172A;
  }}
  .sh-series {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 16px;
    font-weight: 800;
    letter-spacing: 0.12em;
    color: #2563EB;
  }}
  .sh-ep-pill {{
    padding: 6px 16px;
    border-radius: 999px;
    background: linear-gradient(90deg, #2563EB, #7C3AED);
    color: #FFFFFF;
    font-family: 'JetBrains Mono', monospace;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 0.08em;
  }}
  .sh-bottom {{
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .sh-title {{
    font-family: 'Space Grotesk', 'Inter', sans-serif;
    font-size: 24px;
    font-weight: 800;
    color: #0F172A;
    letter-spacing: -0.01em;
  }}
  .sh-narrator {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    font-weight: 800;
    color: #2563EB;
    padding: 5px 14px;
    border-radius: 999px;
    background: #EFF6FF;
    border: 1.5px solid #2563EB;
  }}

  /* 3D Viewport Indicator strip inside Safe Zone */
  .three-stage-banner {{
    width: 100%;
    height: 175px;
    border-radius: 22px;
    border: 2.5px solid #0F172A;
    background: linear-gradient(135deg, #EFF6FF 0%, #F5F3FF 50%, #ECFEFF 100%);
    box-shadow: 0 6px 0 #0F172A;
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    padding: 12px 18px;
  }}
  .three-tag {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 0.1em;
    color: #0F172A;
    background: rgba(255, 255, 255, 0.90);
    padding: 5px 12px;
    border-radius: 999px;
    border: 1.5px solid #0F172A;
  }}

  /* Scene Container inside Safe Zone */
  .scenes-wrap {{
    position: relative;
    width: 100%;
    height: 670px;
  }}
  .scene {{
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 18px;
    opacity: 0;
  }}
  .eyebrow {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 0.14em;
    color: #FFFFFF;
    background: #2563EB;
    border: 2px solid #0F172A;
    box-shadow: 0 4px 0 #0F172A;
    padding: 8px 20px;
    border-radius: 999px;
  }}
  .card {{
    width: 100%;
    background: #FFFFFF;
    border: 2.5px solid #0F172A;
    border-radius: 28px;
    padding: 34px 30px;
    box-shadow: 0 12px 0 #0F172A, 0 24px 48px rgba(15, 23, 42, 0.10);
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 18px;
    position: relative;
    overflow: hidden;
  }}
  .hero-card {{
    background: linear-gradient(155deg, #FFFFFF 0%, #EFF6FF 100%);
    border-color: #0F172A;
  }}
  .light-sweep {{
    position: absolute;
    top: 0;
    left: -120%;
    width: 80%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(37, 99, 235, 0.10), transparent);
    transform: skewX(-20deg);
    pointer-events: none;
  }}
  .kicker {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 16px;
    font-weight: 800;
    letter-spacing: 0.14em;
    color: #7C3AED;
  }}
  .headline-lg {{
    font-family: 'Space Grotesk', 'Inter', sans-serif;
    font-size: 46px;
    font-weight: 900;
    line-height: 1.12;
    letter-spacing: -0.02em;
    color: #0F172A;
  }}
  .headline-md {{
    font-family: 'Space Grotesk', 'Inter', sans-serif;
    font-size: 34px;
    font-weight: 800;
    line-height: 1.18;
    color: #0F172A;
  }}
  .subtext {{
    font-size: 22px;
    font-weight: 600;
    line-height: 1.38;
    color: #475569;
    max-width: 730px;
  }}
  .txt-cyan {{ color: #2563EB; }}

  .price-hero {{
    display: flex;
    align-items: center;
    gap: 22px;
  }}
  .price-strike {{
    font-size: 44px;
    font-weight: 800;
    color: #94A3B8;
    text-decoration: line-through;
  }}
  .price-arrow {{
    font-size: 38px;
    font-weight: 900;
    color: #2563EB;
  }}
  .price-glow {{
    font-size: 76px;
    font-weight: 900;
    color: #2563EB;
  }}

  .logo-row {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
  }}
  .logo-box {{
    width: 78px;
    height: 78px;
    padding: 12px;
    border-radius: 20px;
    background: #F8FAFC;
    border: 2.5px solid #0F172A;
    box-shadow: 0 5px 0 #0F172A;
    object-fit: contain;
  }}
  .conn-line {{
    width: 48px;
    height: 4px;
    background: linear-gradient(90deg, #2563EB, #7C3AED);
    border-radius: 99px;
  }}

  .pill-row {{
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 12px;
  }}
  .tech-pill {{
    padding: 10px 20px;
    border-radius: 999px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 16px;
    font-weight: 800;
  }}
  .tech-pill.blue {{ background: #EFF6FF; border: 2px solid #2563EB; color: #1D4ED8; }}
  .tech-pill.cyan {{ background: #F0F9FF; border: 2px solid #0284C7; color: #0369A1; }}
  .tech-pill.violet {{ background: #F5F3FF; border: 2px solid #7C3AED; color: #6D28D9; }}

  /* Terminal Window (Clean Dark-Contrast Terminal Card on Light Canvas) */
  .term-window {{
    width: 100%;
    border-radius: 24px;
    background: #0F172A;
    border: 2.5px solid #0F172A;
    overflow: hidden;
    box-shadow: 0 10px 0 #2563EB, 0 20px 44px rgba(15, 23, 42, 0.16);
  }}
  .term-header {{
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 14px 20px;
    background: #1E293B;
    border-bottom: 1.5px solid #334155;
  }}
  .tdot {{ width: 13px; height: 13px; border-radius: 99px; }}
  .tdot.r {{ background: #EF4444; }}
  .tdot.y {{ background: #F59E0B; }}
  .tdot.g {{ background: #22C55E; }}
  .term-title {{
    margin-left: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 15px;
    color: #CBD5E1;
  }}
  .term-body {{
    padding: 24px 26px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 20px;
    line-height: 1.65;
    text-align: left;
    color: #F8FAFC;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}
  .tprompt {{ color: #38BDF8; font-weight: 800; }}
  .tline.cyan {{ color: #38BDF8; }}
  .tline.ok {{ color: #4ADE80; font-weight: 800; }}

  .icon-bar {{
    display: flex;
    gap: 18px;
    justify-content: center;
  }}
  .ico-chip {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 20px;
    border-radius: 16px;
    background: #FFFFFF;
    border: 2px solid #0F172A;
    box-shadow: 0 5px 0 #0F172A;
    font-size: 18px;
    font-weight: 800;
    color: #0F172A;
  }}
  .ico-chip img {{ width: 28px; height: 28px; object-fit: contain; }}

  .diagram-grid {{
    display: flex;
    gap: 16px;
    width: 100%;
    justify-content: center;
  }}
  .diag-node {{
    flex: 1;
    padding: 18px 14px;
    border-radius: 20px;
    background: #F8FAFC;
    border: 2px solid #CBD5E1;
    text-align: center;
  }}
  .diag-node.active {{
    border-color: #2563EB;
    background: #EFF6FF;
    box-shadow: 0 5px 0 #2563EB;
  }}
  .diag-num {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 26px;
    font-weight: 900;
    color: #2563EB;
  }}
  .diag-lbl {{
    font-size: 17px;
    font-weight: 800;
    color: #0F172A;
    margin-top: 4px;
  }}

  .flow-row {{
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    justify-content: center;
  }}
  .flow-box {{
    padding: 14px 22px;
    border-radius: 16px;
    background: #F8FAFC;
    border: 2px solid #0F172A;
    font-size: 20px;
    font-weight: 800;
    color: #0F172A;
  }}
  .flow-box.highlight {{
    background: #2563EB;
    border-color: #0F172A;
    color: #FFFFFF;
    box-shadow: 0 5px 0 #0F172A;
  }}
  .flow-arr {{
    font-size: 26px;
    font-weight: 900;
    color: #2563EB;
  }}

  /* Aayojon Screenshots */
  .screenshot-grid {{
    display: flex;
    gap: 14px;
    width: 100%;
    justify-content: center;
  }}
  .shot-card {{
    flex: 1;
    background: #F8FAFC;
    border: 2px solid #0F172A;
    box-shadow: 0 5px 0 #0F172A;
    border-radius: 16px;
    padding: 8px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}
  .shot-card img {{
    width: 100%;
    height: 155px;
    object-fit: cover;
    border-radius: 10px;
  }}
  .shot-card span {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    font-weight: 800;
    color: #2563EB;
  }}

  .arch-svg {{
    width: 100%;
    max-width: 720px;
    height: auto;
  }}

  /* AWS SBG DIU Showcase */
  .sbg-showcase {{
    display: flex;
    align-items: center;
    gap: 22px;
    width: 100%;
    text-align: left;
  }}
  .sbg-poster {{
    width: 240px;
    height: 240px;
    object-fit: cover;
    border-radius: 18px;
    border: 2.5px solid #0F172A;
    box-shadow: 0 6px 0 #0F172A;
  }}
  .sbg-meta {{
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }}
  .diu-logo {{
    height: 54px;
    width: auto;
    object-fit: contain;
    align-self: flex-start;
    background: #F8FAFC;
    border: 1.5px solid #CBD5E1;
    padding: 6px 12px;
    border-radius: 10px;
  }}
  .sbg-title {{
    font-size: 30px;
    font-weight: 900;
    color: #0F172A;
  }}
  .sbg-sub {{
    font-size: 19px;
    font-weight: 700;
    color: #2563EB;
    line-height: 1.35;
  }}

  /* Pipeline Steps (Ep 4) */
  .pipe-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    width: 100%;
  }}
  .pipe-step {{
    padding: 16px;
    border-radius: 16px;
    background: #F8FAFC;
    border: 2px solid #0F172A;
    font-family: 'JetBrains Mono', monospace;
    font-size: 18px;
    font-weight: 800;
    color: #0F172A;
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .pipe-step span {{
    color: #2563EB;
    font-size: 15px;
  }}
  .pipe-step.active {{
    border-color: #2563EB;
    background: #EFF6FF;
    box-shadow: 0 4px 0 #2563EB;
  }}

  /* Ep 5 Mini Grid & Waveform */
  .ep-mini-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    width: 100%;
  }}
  .ep-mini {{
    padding: 14px 18px;
    border-radius: 16px;
    background: #F8FAFC;
    border: 2px solid #0F172A;
    font-size: 19px;
    font-weight: 800;
    color: #0F172A;
    display: flex;
    align-items: center;
    gap: 12px;
  }}
  .ep-mini span {{
    font-family: 'JetBrains Mono', monospace;
    color: #2563EB;
  }}
  .wave-viz {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    height: 84px;
  }}
  .wbar {{
    width: 14px;
    height: 36px;
    border-radius: 99px;
    background: linear-gradient(180deg, #0284C7, #2563EB, #7C3AED);
  }}
  .wbar:nth-child(2n) {{ height: 74px; }}
  .wbar:nth-child(3n) {{ height: 54px; }}

  .ep-timeline-row {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
  }}
  .ep-dot {{
    width: 44px;
    height: 44px;
    border-radius: 99px;
    background: #F8FAFC;
    border: 2px solid #0F172A;
    color: #0F172A;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 16px;
    font-weight: 800;
  }}
  .ep-dot.active {{
    background: #2563EB;
    border-color: #0F172A;
    color: #FFFFFF;
  }}
  .ep-bar {{
    width: 34px;
    height: 3px;
    background: #2563EB;
  }}

  /* Teaser / CTA Card */
  .teaser-card {{
    border-color: #0F172A;
    background: linear-gradient(155deg, #EFF6FF 0%, #F5F3FF 100%);
  }}
  .teaser-badge {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    font-weight: 800;
    letter-spacing: 0.14em;
    color: #7C3AED;
  }}
  .cta-pill {{
    margin-top: 4px;
    padding: 14px 30px;
    border-radius: 999px;
    background: linear-gradient(90deg, #2563EB, #7C3AED);
    border: 2px solid #0F172A;
    box-shadow: 0 5px 0 #0F172A;
    color: #FFFFFF;
    font-family: 'JetBrains Mono', monospace;
    font-size: 18px;
    font-weight: 800;
    letter-spacing: 0.06em;
  }}

  /* Subtitles & Progress strictly inside Safe Zone bottom (y <= 1550px) */
  .hud-bottom {{
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }}
  .caption-box {{
    width: 100%;
    min-height: 132px;
    padding: 18px 24px;
    border-radius: 22px;
    background: #FFFFFF;
    border: 2.5px solid #0F172A;
    box-shadow: 0 8px 0 #0F172A, 0 14px 34px rgba(15, 23, 42, 0.12);
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    gap: 10px 12px;
  }}
  .cap-word {{
    font-size: 34px;
    font-weight: 800;
    color: #0F172A;
    padding: 4px 10px;
    border-radius: 10px;
    line-height: 1.18;
  }}
  .cap-word.kw {{
    color: #2563EB;
  }}
  .cap-word.active {{
    background: #2563EB;
    color: #FFFFFF;
    box-shadow: 0 4px 0 #0F172A;
  }}
  .progress-track {{
    width: 100%;
    height: 10px;
    border-radius: 999px;
    background: #E2E8F0;
    border: 1.5px solid #0F172A;
    overflow: hidden;
  }}
  .progress-fill {{
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #2563EB, #0284C7, #7C3AED);
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
  <audio id="sfx-whoosh-2" src="assets/sfx/real/whoosh.wav" data-start="{t2}" volume="0.26"></audio>
  <audio id="sfx-pop-2" src="assets/sfx/real/pop.wav" data-start="{round(t2 + 0.25, 3)}" volume="0.24"></audio>
  <audio id="sfx-whoosh-3" src="assets/sfx/real/whoosh.wav" data-start="{t3}" volume="0.26"></audio>
  <audio id="sfx-click-3" src="assets/sfx/real/click.wav" data-start="{round(t3 + 0.22, 3)}" volume="0.22"></audio>
  <audio id="sfx-whoosh-4" src="assets/sfx/real/whoosh.wav" data-start="{t4}" volume="0.26"></audio>
  <audio id="sfx-whoosh-5" src="assets/sfx/real/whoosh.wav" data-start="{t5}" volume="0.26"></audio>
  <audio id="sfx-chime-6" src="assets/sfx/real/chime.wav" data-start="{t6}" volume="0.32"></audio>

  <div class="stage">
    <div class="bg-grid"></div>
    <canvas id="three-canvas" width="1080" height="1920"></canvas>

    <div id="safe-zone-guide" class="safe-zone-guide"></div>

    <div class="safe-zone">
      <!-- TOP SERIES HEADER -->
      <div class="series-header">
        <div class="sh-top">
          <div class="sh-brand">
            <img src="assets/logos/antigravity-official.png" class="sh-logo" alt="Antigravity" />
            <span class="sh-series">5 DAYS WITH ANTIGRAVITY</span>
          </div>
          <span class="sh-ep-pill">EPISODE {meta["num"]} / 05</span>
        </div>
        <div class="sh-bottom">
          <div class="sh-title">{meta["num"]} — {meta["title"]}</div>
          <div class="sh-narrator">● RAFI · NARRATOR</div>
        </div>
      </div>

      <!-- THREE.JS 3D STAGE WINDOW -->
      <div class="three-stage-banner">
        <span class="three-tag">{meta["theme"]}</span>
        <span class="three-tag">THREE.JS 3D + 2D MOTION</span>
      </div>

      <!-- MAIN 2D + 3D SCENES -->
      <div class="scenes-wrap">
        {scenes_html}
      </div>

      <!-- SUBTITLES & PROGRESS BAR (STRICTLY ABOVE y=1550px) -->
      <div class="hud-bottom">
        <div id="caption-box" class="caption-box"></div>
        <div class="progress-track">
          <div id="progress-fill" class="progress-fill"></div>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
if (window.location.search.includes('safezone=1')) {{
  document.getElementById('safe-zone-guide').style.display = 'block';
}}

const PART_NUM = {part_num};
const WORDS = {words_json};
const TOTAL_DUR = {dur};
const KEYWORDS = new Set([
  '$5', 'FIVE', 'DAYS', 'ANTIGRAVITY', 'UBUNTU', 'OPENCODE', 'PRODUCTS',
  'AAYOJON', '3D', 'SAAS', 'ARCHITECTURE', 'APIS', 'DATABASE', 'CLOUD',
  'AWS', 'DIU', 'DEVOPS', 'SOSDAR24', 'RAILSIM', 'CARLA', 'GPU',
  'HANDY', 'OMNIVOICE', 'VIDMOTIONCRAFT', 'HYPERFRAMES', 'GSAP', 'AI'
]);

const capBox = document.getElementById('caption-box');
const progFill = document.getElementById('progress-fill');

// Deterministic 3D Renderer (Three.js WebGL tuned for Light Theme)
const canvas = document.getElementById('three-canvas');
let useWebGL = false;
let renderer, scene3d, camera3d, mainGroup;

try {{
  if (window.THREE) {{
    renderer = new THREE.WebGLRenderer({{ canvas: canvas, alpha: true, antialias: true, preserveDrawingBuffer: true }});
    renderer.setSize(1080, 1920, false);
    scene3d = new THREE.Scene();
    camera3d = new THREE.PerspectiveCamera(45, 1080 / 1920, 0.1, 100);
    camera3d.position.set(0, 0, 12);

    const amb = new THREE.AmbientLight(0xffffff, 0.9);
    scene3d.add(amb);
    const dir = new THREE.DirectionalLight(0x2563eb, 1.5);
    dir.position.set(5, 8, 10);
    scene3d.add(dir);

    mainGroup = new THREE.Group();
    mainGroup.position.set(-0.22, 2.55, 0);
    scene3d.add(mainGroup);

    const wireMat = new THREE.MeshBasicMaterial({{ color: 0x1d4ed8, wireframe: true }});
    const blueMat = new THREE.MeshStandardMaterial({{ color: 0x2563eb, roughness: 0.25, metalness: 0.6 }});
    const violetMat = new THREE.MeshStandardMaterial({{ color: 0x7c3aed, roughness: 0.25, metalness: 0.6 }});

    if (PART_NUM === 1) {{
      const base = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.12, 1.5), blueMat);
      base.position.y = -0.35;
      const screen = new THREE.Mesh(new THREE.BoxGeometry(2.2, 1.35, 0.1), wireMat);
      screen.position.set(0, 0.35, -0.68);
      screen.rotation.x = -0.15;
      mainGroup.add(base, screen);
    }} else if (PART_NUM === 2) {{
      const core = new THREE.Mesh(new THREE.IcosahedronGeometry(0.95, 1), wireMat);
      mainGroup.add(core);
      for (let i = 0; i < 4; i++) {{
        const node = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.42, 0.42), i % 2 ? blueMat : violetMat);
        const a = (i / 4) * Math.PI * 2;
        node.position.set(Math.cos(a) * 1.85, Math.sin(a) * 0.55, Math.sin(a) * 1.2);
        mainGroup.add(node);
      }}
    }} else if (PART_NUM === 3) {{
      const torus = new THREE.Mesh(new THREE.TorusGeometry(1.35, 0.08, 12, 42), wireMat);
      torus.rotation.x = 1.1;
      mainGroup.add(torus);
      for (let i = 0; i < 6; i++) {{
        const s = new THREE.Mesh(new THREE.OctahedronGeometry(0.28, 0), i % 2 ? blueMat : violetMat);
        const a = (i / 6) * Math.PI * 2;
        s.position.set(Math.cos(a) * 1.35, Math.sin(a) * 0.4, Math.sin(a) * 1.35);
        mainGroup.add(s);
      }}
    }} else if (PART_NUM === 4) {{
      for (let i = -4; i <= 4; i++) {{
        const tie = new THREE.Mesh(new THREE.BoxGeometry(1.9, 0.08, 0.18), blueMat);
        tie.position.set(0, -0.45, i * 0.45);
        mainGroup.add(tie);
      }}
      const scan = new THREE.Mesh(new THREE.RingGeometry(0.8, 1.15, 24), wireMat);
      mainGroup.add(scan);
    }} else {{
      const center = new THREE.Mesh(new THREE.OctahedronGeometry(0.75, 1), wireMat);
      mainGroup.add(center);
      for (let i = 0; i < 5; i++) {{
        const card3d = new THREE.Mesh(new THREE.BoxGeometry(0.45, 0.72, 0.08), i % 2 ? blueMat : violetMat);
        const a = (i / 5) * Math.PI * 2;
        card3d.position.set(Math.cos(a) * 1.8, Math.sin(a) * 0.35, Math.sin(a) * 1.4);
        mainGroup.add(card3d);
      }}
    }}
    useWebGL = true;
  }}
}} catch (e) {{
  useWebGL = false;
}}

function render3D(t) {{
  if (useWebGL && renderer && mainGroup) {{
    mainGroup.rotation.y = t * 0.65;
    mainGroup.rotation.x = Math.sin(t * 0.8) * 0.18;
    renderer.render(scene3d, camera3d);
  }}
}}

let lastGroup = -1;
function updateHUD(t) {{
  progFill.style.width = Math.min(100, Math.max(0, (t / TOTAL_DUR) * 100)).toFixed(2) + '%';
  render3D(t);

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
      const clean = w.word.replace(/[^a-zA-Z0-9$]/g, '').toUpperCase();
      el.className = 'cap-word' + (KEYWORDS.has(clean) ? ' kw' : '');
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
    const clean = w.word.replace(/[^a-zA-Z0-9$]/g, '').toUpperCase();
    const isKw = KEYWORDS.has(clean);
    const isCurrent = (t >= w.start && t <= w.end + 0.08);
    el.className = 'cap-word' + (isKw ? ' kw' : '') + (isCurrent ? ' active' : '');
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
  tl.fromTo(
    sel,
    {{ opacity: 0, y: 34, scale: 0.96 }},
    {{ opacity: 1, y: 0, scale: 1, duration: 0.42, ease: 'power3.out' }},
    tStart
  );
  if (i < scenes.length - 1) {{
    tl.to(
      sel,
      {{ opacity: 0, y: -26, scale: 0.98, duration: 0.26, ease: 'power2.in' }},
      times[i + 1] - 0.14
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
"""
    out_path = os.path.join(ENGINE_DIR, f"story-part{part_num}-en.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated {out_path} (duration={dur}s)")


def main():
    for part_num in range(1, 6):
        build_part_html(part_num)


if __name__ == "__main__":
    main()
