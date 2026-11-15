import os
import subprocess

ENGINE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORT_DIR = os.path.join(os.path.dirname(ENGINE_DIR), "Export")
os.makedirs(EXPORT_DIR, exist_ok=True)

COVERS = [
    {
        "part": 1,
        "num": "01",
        "tag": "DAY 01 · CURIOSITY",
        "title": "THE $5 UNLOCK",
        "sub": "Opening a New AI Development Workflow with Ubuntu, Terminals & OpenCode",
        "accent": "#2563EB",
        "badge": "$20/mo → $5/mo STUDENT OFFER",
        "visual": """
          <div class="hero-visual">
            <div class="price-pill"><span class="strike">$20</span> → <span class="big">$5</span></div>
            <div class="logo-strip">
              <img src="assets/logos/antigravity-official.png" class="cov-logo" />
              <img src="assets/logos/ubuntu.svg" class="cov-logo" />
              <img src="assets/logos/python.svg" class="cov-logo" />
              <img src="assets/logos/gemini-official.svg" class="cov-logo" />
            </div>
          </div>
        """,
    },
    {
        "part": 2,
        "num": "02",
        "tag": "DAY 02 · CREATIVITY",
        "title": "FROM IDEAS TO PRODUCTS",
        "sub": "Aayojon 3D SaaS · Product Requirements · System Architecture · Database Design",
        "accent": "#7C3AED",
        "badge": "CONCEPT → ARCHITECTURE → SAAS",
        "visual": """
          <div class="hero-visual">
            <div class="shot-row">
              <img src="assets/aayojon/home.png" class="cov-shot" />
              <img src="assets/aayojon/events.png" class="cov-shot" />
              <img src="assets/aayojon/venues.png" class="cov-shot" />
            </div>
          </div>
        """,
    },
    {
        "part": 3,
        "num": "03",
        "tag": "DAY 03 · OPPORTUNITY",
        "title": "BUILDING BEYOND THE SCREEN",
        "sub": "AWS Cloud Infrastructure · DevOps · AWS Student Build & Grow at DIU",
        "accent": "#0284C7",
        "badge": "LOCAL MACHINE → AWS CLOUD @ DIU",
        "visual": """
          <div class="hero-visual">
            <div class="sbg-row">
              <img src="assets/logos/sbg_post_graphic.jpg" class="cov-poster" />
              <div class="sbg-col">
                <img src="assets/logos/aws-logo.svg" class="cov-logo" />
                <img src="assets/logos/docker.svg" class="cov-logo" />
              </div>
            </div>
          </div>
        """,
    },
    {
        "part": 4,
        "num": "04",
        "tag": "DAY 04 · EXPLORATION",
        "title": "BEYOND NORMAL DEVELOPMENT",
        "sub": "SOSDaR24 Railway Dataset · RailSim Generator · CARLA & Ubuntu 22.04 Research",
        "accent": "#2563EB",
        "badge": "DATA → SIMULATION → RECONSTRUCTION",
        "visual": """
          <div class="hero-visual">
            <div class="pipe-cards">
              <div class="pcard"><span>01</span>SOSDaR24 LiDAR</div>
              <div class="pcard"><span>02</span>CARLA Sim</div>
              <div class="pcard"><span>03</span>Ubuntu 22.04</div>
              <div class="pcard active"><span>04</span>RailSim R&amp;D</div>
            </div>
          </div>
        """,
    },
    {
        "part": 5,
        "num": "05",
        "tag": "DAY 05 · SERIES FINALE",
        "title": "BUILDING MY OWN AI CREATOR WORKFLOW",
        "sub": "Handy Dictation · OmniVoice Local Clone · VidMotionCraft · HyperFrames + Three.js",
        "accent": "#7C3AED",
        "badge": "THIS IS ONLY THE BEGINNING",
        "visual": """
          <div class="hero-visual">
            <div class="logo-strip">
              <img src="assets/logos/hyperframes-studio.png" class="cov-logo" />
              <img src="assets/logos/greensock.svg" class="cov-logo" />
              <img src="assets/logos/ffmpeg.svg" class="cov-logo" />
              <img src="assets/logos/antigravity-official.png" class="cov-logo" />
            </div>
            <div class="quote-pill">"AI gives developers new ways to think, create &amp; build."</div>
          </div>
        """,
    },
]


def main():
    chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    for c in COVERS:
        part = c["part"]
        html_path = os.path.join(ENGINE_DIR, f"_tmp_cover_part{part}.html")
        out_png = os.path.join(EXPORT_DIR, f"antigravity-story-part{part}-cover.png")

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@600;700;800;900&family=JetBrains+Mono:wght@700;800&family=Space+Grotesk:wght@700;800&display=swap" rel="stylesheet" />
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
  .canvas {{
    position: relative;
    width: 1080px;
    height: 1920px;
    background:
      radial-gradient(circle at 20% 18%, rgba(37, 99, 235, 0.16) 0%, transparent 45%),
      radial-gradient(circle at 82% 78%, rgba(124, 58, 237, 0.16) 0%, transparent 48%),
      linear-gradient(180deg, #F8FAFC 0%, #EEF2FF 52%, #F8FAFC 100%);
  }}
  .dot-grid {{
    position: absolute;
    inset: 0;
    background-image: radial-gradient(rgba(15, 23, 42, 0.11) 1.5px, transparent 1.5px);
    background-size: 38px 38px;
  }}
  /* Centered inside Instagram Reels Safe Zone & 1:1 Profile Grid Safe Zone */
  .safe-cover {{
    position: absolute;
    left: 90px;
    top: 260px;
    width: 810px;
    height: 1260px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    text-align: center;
  }}
  .series-pill {{
    display: inline-flex;
    align-items: center;
    gap: 14px;
    padding: 14px 28px;
    border-radius: 999px;
    background: #FFFFFF;
    border: 3px solid #0F172A;
    box-shadow: 0 8px 0 #0F172A;
  }}
  .series-pill img {{
    width: 44px;
    height: 44px;
    border-radius: 10px;
    border: 2px solid #0F172A;
  }}
  .series-pill span {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 20px;
    font-weight: 800;
    letter-spacing: 0.12em;
    color: #2563EB;
  }}
  .main-card {{
    width: 100%;
    background: #FFFFFF;
    border: 3.5px solid #0F172A;
    border-radius: 36px;
    padding: 46px 38px;
    box-shadow: 0 16px 0 #0F172A, 0 32px 64px rgba(15, 23, 42, 0.14);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 24px;
  }}
  .ep-row {{
    display: flex;
    align-items: center;
    gap: 14px;
  }}
  .ep-num {{
    padding: 10px 22px;
    border-radius: 999px;
    background: {c["accent"]};
    color: #FFFFFF;
    font-family: 'JetBrains Mono', monospace;
    font-size: 20px;
    font-weight: 800;
    border: 2.5px solid #0F172A;
  }}
  .ep-tag {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 18px;
    font-weight: 800;
    color: #475569;
    letter-spacing: 0.08em;
  }}
  .cov-title {{
    font-family: 'Space Grotesk', 'Inter', sans-serif;
    font-size: 62px;
    font-weight: 900;
    line-height: 1.06;
    letter-spacing: -0.02em;
    color: #0F172A;
  }}
  .cov-sub {{
    font-size: 25px;
    font-weight: 600;
    line-height: 1.38;
    color: #475569;
    max-width: 700px;
  }}
  .hero-visual {{
    width: 100%;
    padding: 26px;
    border-radius: 26px;
    background: linear-gradient(135deg, #EFF6FF 0%, #F5F3FF 100%);
    border: 2.5px solid #0F172A;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 18px;
  }}
  .price-pill {{
    font-size: 68px;
    font-weight: 900;
    color: #0F172A;
  }}
  .price-pill .strike {{
    color: #94A3B8;
    text-decoration: line-through;
    font-size: 46px;
  }}
  .price-pill .big {{
    color: #2563EB;
    font-size: 82px;
  }}
  .logo-strip {{
    display: flex;
    gap: 22px;
    justify-content: center;
  }}
  .cov-logo {{
    width: 88px;
    height: 88px;
    padding: 14px;
    background: #FFFFFF;
    border: 2.5px solid #0F172A;
    border-radius: 22px;
    box-shadow: 0 6px 0 #0F172A;
    object-fit: contain;
  }}
  .shot-row {{
    display: flex;
    gap: 14px;
    width: 100%;
  }}
  .cov-shot {{
    flex: 1;
    width: 0;
    min-width: 0;
    height: 155px;
    object-fit: cover;
    border-radius: 16px;
    border: 2.5px solid #0F172A;
    box-shadow: 0 6px 0 #0F172A;
  }}
  .sbg-row {{
    display: flex;
    align-items: center;
    gap: 24px;
  }}
  .cov-poster {{
    width: 240px;
    height: 240px;
    object-fit: cover;
    border-radius: 20px;
    border: 2.5px solid #0F172A;
    box-shadow: 0 6px 0 #0F172A;
  }}
  .sbg-col {{
    display: flex;
    flex-direction: column;
    gap: 16px;
  }}
  .pipe-cards {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    width: 100%;
  }}
  .pcard {{
    padding: 20px;
    border-radius: 18px;
    background: #FFFFFF;
    border: 2.5px solid #0F172A;
    box-shadow: 0 5px 0 #0F172A;
    font-family: 'JetBrains Mono', monospace;
    font-size: 20px;
    font-weight: 800;
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .pcard span {{ color: #2563EB; }}
  .pcard.active {{ background: #2563EB; color: #FFFFFF; }}
  .pcard.active span {{ color: #FFFFFF; }}
  .quote-pill {{
    font-size: 22px;
    font-weight: 800;
    color: #1D4ED8;
  }}
  .badge-bottom {{
    padding: 14px 30px;
    border-radius: 999px;
    background: #0F172A;
    color: #FFFFFF;
    font-family: 'JetBrains Mono', monospace;
    font-size: 18px;
    font-weight: 800;
    letter-spacing: 0.08em;
  }}
  .footer-pill {{
    padding: 14px 32px;
    border-radius: 999px;
    background: #FFFFFF;
    border: 3px solid #0F172A;
    box-shadow: 0 6px 0 #0F172A;
    font-family: 'JetBrains Mono', monospace;
    font-size: 19px;
    font-weight: 800;
    color: #0F172A;
  }}
</style>
</head>
<body>
  <div class="canvas">
    <div class="dot-grid"></div>
    <div class="safe-cover">
      <div class="series-pill">
        <img src="assets/logos/antigravity-official.png" alt="Antigravity" />
        <span>5 DAYS WITH ANTIGRAVITY</span>
      </div>

      <div class="main-card">
        <div class="ep-row">
          <span class="ep-num">EPISODE {c["num"]} / 05</span>
          <span class="ep-tag">{c["tag"]}</span>
        </div>
        <div class="cov-title">{c["num"]} — {c["title"]}</div>
        <div class="cov-sub">{c["sub"]}</div>
        {c["visual"]}
        <div class="badge-bottom">{c["badge"]}</div>
      </div>

      <div class="footer-pill">● NARRATED BY RAFI · 2D + THREE.JS 3D DOCUMENTARY</div>
    </div>
  </div>
</body>
</html>
"""
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        file_url = f"file://{os.path.abspath(html_path)}"
        subprocess.run(
            [
                chrome_bin,
                "--headless=new",
                "--disable-gpu",
                "--hide-scrollbars",
                "--window-size=1080,1920",
                f"--screenshot={out_png}",
                file_url,
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if os.path.exists(html_path):
            os.remove(html_path)
        print(f"Generated cover: {out_png}")


if __name__ == "__main__":
    main()
