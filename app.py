Pikku's Birthday Web App — Complete RPG Sprite Edition
=======================================================
A guided 5-step Streamlit birthday experience featuring
authentic 2D RPG characters rendered on HTML5 Canvas at 30 FPS.
No external image assets required — everything is drawn in code.

Run with:
    streamlit run app.py

requirements.txt:
    streamlit
    requests
    Pillow
"""

import os
import json
import base64

import streamlit as st
import streamlit.components.v1 as components

# ---------------------------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Happy Birthday, Pikku! 🎀",
    page_icon="🎂",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# ASSET PATHS — degrade safely to placeholders when files are missing
# ---------------------------------------------------------------------------
ASSETS_DIR = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

BG_MUSIC_PATH = os.path.join(ASSETS_DIR, "bg_music.mp3")
VIDEO_PATHS = [
    os.path.join(ASSETS_DIR, "video1.mp4"),
    os.path.join(ASSETS_DIR, "video2.mp4"),
]
POCKET_PHOTOS = [
    {"path": os.path.join(ASSETS_DIR, "memory1.jpg"), "caption": "The day we first talked 💌"},
    {"path": os.path.join(ASSETS_DIR, "memory2.jpg"), "caption": "That silly joke you made 😂"},
    {"path": os.path.join(ASSETS_DIR, "memory3.jpg"), "caption": "The moment I knew 💗"},
    {"path": os.path.join(ASSETS_DIR, "memory4.jpg"), "caption": "Us, always 🌸"},
]

GREETING_LINE = "Hi. Hey, I know your birthday is coming and you are very happy for that."

# ---------------------------------------------------------------------------
# SAFE HELPERS — never crash because of missing files
# ---------------------------------------------------------------------------
def safe_audio(path: str) -> None:
    """Play background music if the file exists, otherwise show a hint."""
    if os.path.exists(path):
        try:
            with open(path, "rb") as f:
                audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
            st.markdown(
                f"""
                <audio autoplay loop style="display:none;">
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                </audio>
                """,
                unsafe_allow_html=True,
            )
            st.caption("🎵 Background music is playing...")
        except Exception:
            st.caption("🎵 Add a valid MP3 file at `assets/bg_music.mp3` to enable background music.")
    else:
        st.caption("🎵 Add your song at `assets/bg_music.mp3` to enable background music.")


def safe_video(path: str, label: str) -> None:
    """Display a video if the file exists, otherwise show a placeholder."""
    if os.path.exists(path):
        try:
            st.video(path)
        except Exception:
            st.info(f"📹 Add a valid video at `{path}` to show '{label}' here.")
    else:
        st.info(f"📹 Add a clip at `{path}` to show '{label}' here.")


def safe_image(path: str, caption: str = "", use_container_width: bool = True) -> None:
    """Display an image if the file exists, otherwise show a placeholder card."""
    if os.path.exists(path):
        try:
            st.image(path, caption=caption, use_container_width=use_container_width)
        except Exception:
            _image_placeholder(caption, path)
    else:
        _image_placeholder(caption, path)


def _image_placeholder(caption: str, path: str) -> None:
    """Render a pretty placeholder card for missing images."""
    st.markdown(
        f"""
        <div class="glass-card" style="text-align:center; padding:30px;">
            <div style="font-size:64px;">🌸</div>
            <p style="font-weight:600;font-size:18px;color:#c44569;">{caption}</p>
            <p style="font-size:12px;color:#c98a97;">(add photo at {path})</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# GLOBAL STREAMLIT CSS — pink gradient + glassmorphism
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Global background */
    .stApp {
        background: linear-gradient(135deg, #ffdde1 0%, #ee9ca7 100%);
        background-attachment: fixed;
    }
    #MainMenu, header, footer {visibility: hidden;}

    /* Typography */
    h1, h2, h3, h4 {
        color: #a14a5c !important;
        text-shadow: 0 2px 6px rgba(255,255,255,0.4);
    }
    p, span, label, li, div {
        color: #7a3b47;
    }

    /* Glassmorphism card */
    .glass-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 22px;
        border: 1.5px solid rgba(238, 156, 167, 0.55);
        box-shadow: 0 8px 32px rgba(238, 156, 167, 0.35);
        padding: 20px 24px;
        margin-bottom: 20px;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(238, 156, 167, 0.5);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #ffb6c1 0%, #ee9ca7 100%);
        color: #6b2c3a;
        border: none;
        border-radius: 30px;
        padding: 10px 22px;
        font-weight: 700;
        box-shadow: 0 4px 14px rgba(238, 156, 167, 0.5);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(238, 156, 167, 0.7);
        color: #6b2c3a;
    }
    .stButton > button:disabled {
        background: #e0c0c8;
        color: #a08088;
        box-shadow: none;
    }

    /* Title banner */
    .title-banner {
        text-align: center;
        padding: 10px 0 4px 0;
    }

    /* Step indicator */
    .step-indicator {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin: 15px 0 25px 0;
    }
    .step-dot {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 18px;
        background: rgba(255,255,255,0.5);
        color: #c98a97;
        border: 2px solid #ee9ca7;
        transition: all 0.3s ease;
    }
    .step-dot.active {
        background: #ee9ca7;
        color: white;
        border-color: #c44569;
        box-shadow: 0 0 15px rgba(238, 156, 167, 0.6);
    }
    .step-dot.done {
        background: #c44569;
        color: white;
        border-color: #c44569;
    }

    /* Pop-in animation for revealed photos */
    @keyframes popIn {
        0%   { transform: scale(0.05); opacity: 0; }
        60%  { transform: scale(1.08); opacity: 1; }
        100% { transform: scale(1); opacity: 1; }
    }
    .pocket-photo-new {
        animation: popIn 0.6s cubic-bezier(.2,.9,.3,1.3) forwards;
    }

    /* Glowing text */
    @keyframes glowPulse {
        0%, 100% { text-shadow: 0 0 10px rgba(255,107,157,0.3); }
        50%      { text-shadow: 0 0 25px rgba(255,107,157,0.7), 0 0 50px rgba(255,107,157,0.3); }
    }
    .glow-text {
        animation: glowPulse 2s ease-in-out infinite;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .step-dot { width: 30px; height: 30px; font-size: 14px; }
        .glass-card { padding: 14px 16px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# SESSION STATE — guided step-by-step progression
# ---------------------------------------------------------------------------
if "current_step" not in st.session_state:
    st.session_state.current_step = 1  # 1 through 5

if "step1_stage" not in st.session_state:
    st.session_state.step1_stage = "idle"  # idle | talking | done

if "step3_pocket_revealed" not in st.session_state:
    st.session_state.step3_pocket_revealed = []

if "step3_just_revealed" not in st.session_state:
    st.session_state.step3_just_revealed = False

if "step5_phase" not in st.session_state:
    st.session_state.step5_phase = "entry"  # entry | approach | hug | done


# ---------------------------------------------------------------------------
# RPG SCENE HTML TEMPLATE
# ---------------------------------------------------------------------------
RPG_SCENE_TEMPLATE = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  html, body {
      margin: 0; padding: 0; background: transparent; overflow: hidden;
      font-family: 'Courier New', 'Comic Sans MS', monospace, cursive;
  }

  .scene-wrap {
      position: relative;
      width: __SCENE_W__px;
      height: __SCENE_H__px;
      margin: 0 auto;
      border-radius: 14px;
      overflow: hidden;
      border: 3px solid #7a4a3a;
      box-shadow: 0 6px 18px rgba(0,0,0,0.25);
      background: linear-gradient(#bdeaff 0%, #bdeaff 55%, #7fc97f 55%, #7fc97f 100%);
  }

  .ground-strip {
      position: absolute;
      left: 0; right: 0; bottom: 0;
      height: 26px;
      background-image: repeating-linear-gradient(
          90deg,
          #6ab86a 0px, #6ab86a 8px,
          #5aa65a 8px, #5aa65a 16px
      );
      background-size: 32px 26px;
      animation: groundScroll 0.8s steps(4) infinite;
      opacity: 0.9;
      z-index: 1;
  }
  @keyframes groundScroll {
      from { background-position-x: 0px; }
      to   { background-position-x: -32px; }
  }

  canvas#rpgCanvas {
      position: absolute;
      left: 50%; top: 8px;
      transform: translateX(-50%);
      image-rendering: pixelated;
      image-rendering: -moz-crisp-edges;
      image-rendering: crisp-edges;
      width: __CANVAS_DISPLAY_W__px;
      height: __CANVAS_DISPLAY_H__px;
      z-index: 2;
  }

  .dbox-wrap {
      position: absolute;
      left: 6px; right: 6px; bottom: 6px;
      display: __DBOX_DISPLAY__;
      z-index: 10;
  }
  .dbox {
      background: #fff8ec;
      border: 3px solid #2c2c54;
      border-radius: 6px;
      box-shadow: inset 0 0 0 2px #ffe9c7, 0 4px 10px rgba(0,0,0,0.3);
      padding: 8px 30px 8px 10px;
      min-height: 44px;
      font-size: 13px;
      line-height: 1.35;
      color: #2c2c54;
      position: relative;
      cursor: pointer;
  }
  .dbox-arrow {
      position: absolute;
      right: 10px; bottom: 6px;
      width: 0; height: 0;
      border-left: 6px solid transparent;
      border-right: 6px solid transparent;
      border-top: 8px solid #2c2c54;
      animation: arrowBlink 0.6s steps(1) infinite;
  }
  @keyframes arrowBlink {
      0%, 49%   { opacity: 1; }
      50%, 100% { opacity: 0; }
  }

  .floating-hearts {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      pointer-events: none;
      z-index: 3;
  }
  .heart-particle {
      position: absolute;
      font-size: 18px;
      animation: floatUp 2.5s ease-out forwards;
      pointer-events: none;
  }
  @keyframes floatUp {
      0%   { transform: translateY(0) scale(0.5); opacity: 1; }
      100% { transform: translateY(-200px) scale(1.5); opacity: 0; }
  }
</style>
</head>
<body>
  <div class="scene-wrap">
    <canvas id="rpgCanvas" width="__CANVAS_W__" height="__CANVAS_H__"></canvas>
    <div class="ground-strip"></div>
    <div class="floating-hearts" id="floatingHearts"></div>
    <div class="dbox-wrap">
      <div class="dbox" id="dboxClickArea">
        <span id="dboxText"></span>
        <div class="dbox-arrow" id="dboxArrow" style="display:none;"></div>
      </div>
    </div>
  </div>

<script>
(function () {
  var canvas = document.getElementById('rpgCanvas');
  var ctx = canvas.getContext('2d');
  ctx.imageSmoothingEnabled = false;

  var W = canvas.width, H = canvas.height;
  var GROUND_Y = H - 22;

  var POSE = "__POSE__";
  var SHOW_HEART = __SHOW_HEART__;
  var SHOW_GIRL = __SHOW_GIRL__;
  var DIALOGUE = __DIALOGUE_JSON__;

  var C_HAIR   = "#4a2c17";
  var C_HAIR_G = "#8B4513";
  var C_SKIN   = "#ffd9b3";
  var C_SHIRT  = "#4f8ecb";
  var C_SHIRT_DK = "#33618f";
  var C_DRESS  = "#FF69B4";
  var C_DRESS_DK = "#FF1493";
  var C_PANTS  = "#333355";
  var C_SHOE   = "#22222a";
  var C_EYE    = "#2c2c54";
  var C_MOUTH  = "#a14a5c";
  var C_POCKET = "#22314a";
  var C_HEART  = "#ff6f91";

  var boy = {
      x: -20,
      targetX: SHOW_GIRL ? Math.round(W / 2) - 20 : Math.round(W / 2),
      walking: true,
      legPhase: 0,
      armWaveT: 0,
      hopT: 0,
      mouthOpen: false,
      pocketItemY: 0,
      pocketItemScale: 0,
      pocketRevealing: false
  };

  var girl = {
      x: W + 40,
      targetX: Math.round(W / 2) + 20,
      walking: SHOW_GIRL,
      legPhase: 1,
      armWaveT: 0,
      hopT: 0
  };

  var tickCounter = 0;
  var dialogueLines = DIALOGUE || [];
  var currentLineIdx = 0;
  var typingTimer = null;
  var typingComplete = false;

  function drawRect(x, y, w, h, color) {
      ctx.fillStyle = color;
      ctx.fillRect(Math.round(x), Math.round(y), w, h);
  }

  function drawArm(shoulderX, shoulderY, angleDeg, color) {
      ctx.save();
      ctx.translate(shoulderX, shoulderY);
      ctx.rotate(angleDeg * Math.PI / 180);
      ctx.fillStyle = color;
      ctx.fillRect(-2, 0, 5, 15);
      ctx.restore();
  }

  function drawBoy(ax, groundY, s) {
      var bob = 0;
      if (POSE === "celebrate") {
          bob = Math.sin(s.hopT) * 3;
      } else if (!s.walking && POSE !== "walk") {
          bob = Math.sin(tickCounter / 12) * 1.2;
      }
      var ay = groundY + bob;

      var liftL = 0, liftR = 0;
      if (s.walking) {
          liftL = s.legPhase === 0 ? -3 : 0;
          liftR = s.legPhase === 0 ? 0 : -3;
      } else if (POSE === "celebrate") {
          liftL = Math.sin(s.hopT) > 0 ? -2 : 0;
          liftR = Math.sin(s.hopT) > 0 ? 0 : -2;
      }
      drawRect(ax - 7, ay - 16 + liftL, 6, 16, C_PANTS);
      drawRect(ax - 7, ay - 3 + liftL, 6, 3, C_SHOE);
      drawRect(ax + 1, ay - 16 + liftR, 6, 16, C_PANTS);
      drawRect(ax + 1, ay - 3 + liftR, 6, 3, C_SHOE);

      drawRect(ax - 9, ay - 34, 18, 20, C_SHIRT);
      drawRect(ax - 9, ay - 34, 18, 3, C_SHIRT_DK);

      drawRect(ax + 3, ay - 20, 5, 5, C_POCKET);

      var armAngleL = 8, armAngleR = -8;
      if (POSE === "talk") {
          armAngleR = -60 + Math.sin(s.armWaveT) * 35;
      } else if (POSE === "reach") {
          armAngleR = 70;
      } else if (POSE === "celebrate") {
          armAngleL = 150 + Math.sin(s.hopT) * 10;
          armAngleR = -150 - Math.sin(s.hopT) * 10;
      } else if (POSE === "hug") {
          armAngleL = -60;
          armAngleR = 60;
      } else if (s.walking) {
          armAngleL = s.legPhase === 0 ? 30 : -20;
          armAngleR = s.legPhase === 0 ? -20 : 30;
      }
      drawArm(ax - 9, ay - 32, armAngleL, C_SHIRT_DK);
      drawArm(ax + 9, ay - 32, armAngleR, C_SHIRT_DK);

      drawRect(ax - 8, ay - 50, 16, 16, C_SKIN);
      drawRect(ax - 9, ay - 54, 18, 6, C_HAIR);
      drawRect(ax - 9, ay - 50, 3, 10, C_HAIR);
      drawRect(ax + 6, ay - 50, 3, 10, C_HAIR);

      drawRect(ax - 5, ay - 42, 2, 2, C_EYE);
      drawRect(ax + 3, ay - 42, 2, 2, C_EYE);

      var mouthH = (POSE === "talk" && s.mouthOpen) ? 3 : 1;
      drawRect(ax - 3, ay - 37, 6, mouthH, C_MOUTH);

      if (s.pocketRevealing) {
          var itemX = ax + 8;
          var itemY = ay - 22 - s.pocketItemY;
          var scale = s.pocketItemScale;
          ctx.save();
          ctx.translate(itemX, itemY);
          ctx.scale(scale, scale);
          ctx.fillStyle = "#fffef5";
          ctx.fillRect(-6, -8, 12, 16);
          ctx.strokeStyle = "#ffb6c1";
          ctx.lineWidth = 1;
          ctx.strokeRect(-6, -8, 12, 16);
          ctx.fillStyle = C_HEART;
          ctx.fillRect(-2, -2, 2, 2);
          ctx.fillRect(2, -2, 2, 2);
          ctx.fillRect(-3, 0, 8, 2);
          ctx.fillRect(-1, 2, 4, 1);
          ctx.restore();
      }

      if (SHOW_HEART) {
          var hy = ay - 66 - Math.sin(tickCounter / 10) * 4;
          var hx = ax + 12;
          ctx.fillStyle = C_HEART;
          ctx.fillRect(hx, hy, 3, 3);
          ctx.fillRect(hx + 4, hy, 3, 3);
          ctx.fillRect(hx - 1, hy + 3, 9, 3);
          ctx.fillRect(hx + 1, hy + 6, 5, 2);
      }
  }

  function drawGirl(ax, groundY, s) {
      var bob = Math.sin(tickCounter / 12) * 1.5;
      var ay = groundY + bob;

      var liftL = 0, liftR = 0;
      if (s.walking) {
          liftL = s.legPhase === 0 ? -3 : 0;
          liftR = s.legPhase === 0 ? 0 : -3;
      }
      drawRect(ax - 5, ay - 8 + liftL, 4, 10, C_SKIN);
      drawRect(ax + 1, ay - 8 + liftR, 4, 10, C_SKIN);
      drawRect(ax - 5, ay - 2 + liftL, 4, 3, C_DRESS_DK);
      drawRect(ax + 1, ay - 2 + liftR, 4, 3, C_DRESS_DK);

      drawRect(ax - 9, ay - 26, 18, 20, C_DRESS);
      drawRect(ax - 9, ay - 26, 18, 3, C_DRESS_DK);

      drawRect(ax - 7, ay - 38, 14, 14, C_DRESS);
      drawRect(ax - 7, ay - 38, 14, 2, C_DRESS_DK);

      var armAngleL = 8, armAngleR = -8;
      if (POSE === "hug") {
          armAngleL = -50;
          armAngleR = 50;
      } else if (s.walking) {
          armAngleL = s.legPhase === 0 ? 30 : -20;
          armAngleR = s.legPhase === 0 ? -20 : 30;
      }
      drawArm(ax - 7, ay - 36, armAngleL, C_DRESS_DK);
      drawArm(ax + 7, ay - 36, armAngleR, C_DRESS_DK);

      drawRect(ax - 8, ay - 52, 16, 16, C_SKIN);
      drawRect(ax - 9, ay - 56, 18, 7, C_HAIR_G);
      drawRect(ax - 9, ay - 52, 3, 10, C_HAIR_G);
      drawRect(ax + 6, ay - 52, 3, 10, C_HAIR_G);
      drawRect(ax - 12, ay - 53, 4, 6, C_HAIR_G);
      drawRect(ax + 8, ay - 53, 4, 6, C_HAIR_G);

      drawRect(ax - 5, ay - 44, 3, 3, C_EYE);
      drawRect(ax + 2, ay - 44, 3, 3, C_EYE);
      drawRect(ax - 6, ay - 46, 1, 2, C_EYE);
      drawRect(ax + 5, ay - 46, 1, 2, C_EYE);

      drawRect(ax - 2, ay - 39, 5, 2, C_MOUTH);

      ctx.fillStyle = "rgba(255,150,150,0.4)";
      ctx.fillRect(ax - 7, ay - 41, 3, 2);
      ctx.fillRect(ax + 4, ay - 41, 3, 2);

      if (SHOW_HEART) {
          var hy = ay - 68 - Math.sin(tickCounter / 10 + 1) * 3;
          var hx = ax - 8;
          ctx.fillStyle = C_HEART;
          ctx.fillRect(hx, hy, 3, 3);
          ctx.fillRect(hx + 4, hy, 3, 3);
          ctx.fillRect(hx - 1, hy + 3, 9, 3);
          ctx.fillRect(hx + 1, hy + 6, 5, 2);
      }
  }

  function drawBackground() {
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = "rgba(255,255,255,0.5)";
      ctx.fillRect(15, 10, 30, 8);
      ctx.fillRect(20, 5, 20, 6);
      ctx.fillRect(W - 50, 18, 28, 7);
      ctx.fillRect(W - 45, 13, 18, 6);
  }

  function spawnHeartParticle(x, y) {
      var container = document.getElementById('floatingHearts');
      if (!container) return;
      var heart = document.createElement('div');
      heart.className = 'heart-particle';
      heart.textContent = ['💕','💖','💗','💝','✨'][Math.floor(Math.random()*5)];
      heart.style.left = x + 'px';
      heart.style.top = y + 'px';
      container.appendChild(heart);
      setTimeout(function() {
          if (heart.parentNode) heart.parentNode.removeChild(heart);
      }, 2600);
  }

  var FPS = 30;
  function tick() {
      tickCounter++;
      boy.armWaveT += 0.35;
      boy.hopT += 0.28;
      girl.armWaveT += 0.32;
      girl.hopT += 0.26;

      if (boy.walking) {
          boy.x += 2.2;
          if (boy.x >= boy.targetX) {
              boy.x = boy.targetX;
              boy.walking = false;
          }
          if (tickCounter % 4 === 0) boy.legPhase = 1 - boy.legPhase;
      }

      if (girl.walking) {
          girl.x -= 1.8;
          if (girl.x <= girl.targetX) {
              girl.x = girl.targetX;
              girl.walking = false;
          }
          if (tickCounter % 4 === 0) girl.legPhase = 1 - girl.legPhase;
      }

      if (POSE === "talk" && tickCounter % 5 === 0) {
          boy.mouthOpen = !boy.mouthOpen;
      }

      if (boy.pocketRevealing) {
          boy.pocketItemY += 1.2;
          boy.pocketItemScale += 0.04;
          if (boy.pocketItemY > 40) {
              boy.pocketRevealing = false;
          }
      }

      if ((POSE === "hug" || POSE === "celebrate") && tickCounter % 15 === 0) {
          var sceneWrap = document.querySelector('.scene-wrap');
          if (sceneWrap) {
              var rect = sceneWrap.getBoundingClientRect();
              var hx = (boy.x / W) * rect.width;
              var hy = (GROUND_Y / H) * rect.height;
              spawnHeartParticle(hx, hy - 40);
          }
      }

      drawBackground();
      drawBoy(boy.x, GROUND_Y, boy);
      if (SHOW_GIRL) {
          drawGirl(girl.x, GROUND_Y, girl);
      }
  }
  setInterval(tick, 1000 / FPS);
  tick();

  var textEl = document.getElementById('dboxText');
  var arrowEl = document.getElementById('dboxArrow');
  var dboxArea = document.getElementById('dboxClickArea');

  function typeLine(line) {
      textEl.textContent = "";
      arrowEl.style.display = "none";
      typingComplete = false;
      var i = 0;
      var speed = 28;
      if (typingTimer) clearInterval(typingTimer);
      typingTimer = setInterval(function () {
          textEl.textContent += line.charAt(i);
          i++;
          if (i >= line.length) {
              clearInterval(typingTimer);
              typingTimer = null;
              typingComplete = true;
              arrowEl.style.display = "block";
          }
      }, speed);
  }

  function advanceDialogue() {
      if (!typingComplete) {
          if (typingTimer) clearInterval(typingTimer);
          typingTimer = null;
          textEl.textContent = dialogueLines[currentLineIdx];
          typingComplete = true;
          arrowEl.style.display = "block";
          return;
      }
      if (currentLineIdx < dialogueLines.length - 1) {
          currentLineIdx++;
          typeLine(dialogueLines[currentLineIdx]);
      }
  }

  if (dialogueLines && dialogueLines.length > 0) {
      typeLine(dialogueLines[0]);
  }

  if (dboxArea) {
      dboxArea.addEventListener('click', advanceDialogue);
  }

  window.triggerPocketReveal = function() {
      boy.pocketRevealing = true;
      boy.pocketItemY = 0;
      boy.pocketItemScale = 0.3;
  };

})();
</script>
</body>
</html>
"""


def render_rpg_scene(
    pose: str = "idle",
    dialogue=None,
    show_heart: bool = False,
    show_girl: bool = False,
    scene_w: int = 420,
    scene_h: int = 260,
    canvas_w: int = 140,
    canvas_h: int = 110,
    scale: int = 3,
) -> None:
    """Render the RPG scene inside an HTML5 Canvas at 30 FPS."""
    if isinstance(dialogue, str):
        dialogue = [dialogue]

    html = (
        RPG_SCENE_TEMPLATE
        .replace("__SCENE_W__", str(scene_w))
        .replace("__SCENE_H__", str(scene_h))
        .replace("__CANVAS_W__", str(canvas_w))
        .replace("__CANVAS_H__", str(canvas_h))
        .replace("__CANVAS_DISPLAY_W__", str(canvas_w * scale))
        .replace("__CANVAS_DISPLAY_H__", str(canvas_h * scale))
        .replace("__POSE__", pose)
        .replace("__SHOW_HEART__", "true" if show_heart else "false")
        .replace("__SHOW_GIRL__", "true" if show_girl else "false")
        .replace("__DIALOGUE_JSON__", json.dumps(dialogue) if dialogue else "null")
        .replace("__DBOX_DISPLAY__", "block" if dialogue else "none")
    )
    components.html(html, height=scene_h + 10, scrolling=False)


# ---------------------------------------------------------------------------
# STEP INDICATOR
# ---------------------------------------------------------------------------
def render_step_indicator():
    """Display the step progress dots."""
    dots = ""
    for i in range(1, 6):
        if i < st.session_state.current_step:
            cls = "done"
            icon = "✓"
        elif i == st.session_state.current_step:
            cls = "active"
            icon = str(i)
        else:
            cls = ""
            icon = str(i)
        dots += f'<div class="step-dot {cls}">{icon}</div>'
    st.markdown(f'<div class="step-indicator">{dots}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------
st.markdown(
    '<div class="title-banner"><h1>🎀 Happy Birthday, Pikku! 🎂</h1></div>',
    unsafe_allow_html=True,
)
render_step_indicator()

# ===========================================================================
# STEP 1 — 2D Animated Boy Entrance & Greeting
# ===========================================================================
if st.session_state.current_step == 1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 💬 Step 1: A Special Visitor Arrives")
    safe_audio(BG_MUSIC_PATH)

    stage = st.session_state.step1_stage

    if stage == "idle":
        render_rpg_scene(
            pose="walk",
            dialogue=["...", "Click the button below to talk to him!"],
        )
    elif stage == "talking":
        render_rpg_scene(
            pose="talk",
            dialogue=[GREETING_LINE],
        )

    st.write("")
    col1, col2, col3 = st.columns([1, 2, 1])

    if stage == "idle":
        with col2:
            if st.button("💬 Talk to him / बात सुनो", use_container_width=True, key="btn_talk"):
                st.session_state.step1_stage = "talking"
                st.rerun()

    elif stage == "talking":
        with col2:
            if st.button("Next Step ➡️", use_container_width=True, key="btn_step1_next"):
                st.session_state.current_step = 2
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ===========================================================================
# STEP 2 — Interactive Story Milestones
# ===========================================================================
elif st.session_state.current_step == 2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True
