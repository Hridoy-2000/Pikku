"""
Pikku's Birthday Web App — Pokémon 2D RPG Sprite Edition
===========================================================
A 5-tab Streamlit birthday experience featuring an authentic Game Boy /
Pokémon-style 2D sprite: drawn frame-by-frame on an HTML5 Canvas (no
external image assets, so nothing can ever 404), scaled with
`image-rendering: pixelated` for a crisp retro look, running a real
30 FPS game loop. A classic RPG dialogue box types text out letter by
letter with a blinking indicator arrow. CSS `steps()` keyframes drive
the scrolling tiled ground and the arrow blink.

Run with:
    streamlit run app.py

requirements.txt:
    streamlit
    requests
"""

import os
import json

import requests
import streamlit as st
import streamlit.components.v1 as components

# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Happy Birthday, Pikku! 🎀",
    page_icon="🎂",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# ASSET PATHS — everything degrades safely to a placeholder if missing
# ---------------------------------------------------------------------------
ASSETS_DIR = "assets"
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
# SAFE HELPERS
# ---------------------------------------------------------------------------
def safe_audio(path: str) -> None:
    if os.path.exists(path):
        st.audio(path, format="audio/mp3")
    else:
        st.caption("🎵 Add your song at `assets/bg_music.mp3` to enable background music.")


def safe_video(path: str, label: str) -> None:
    if os.path.exists(path):
        st.video(path)
    else:
        st.info(f"📹 Add a clip at `{path}` to show '{label}' here.")


# ---------------------------------------------------------------------------
# GLOBAL STREAMLIT CSS — pink gradient + glassmorphism (surrounds the game)
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #ffdde1 0%, #ee9ca7 100%);
        background-attachment: fixed;
    }
    #MainMenu, header, footer {visibility: hidden;}
    h1, h2, h3, h4 { color: #a14a5c !important; text-shadow: 0 2px 6px rgba(255,255,255,0.4); }
    p, span, label, li { color: #7a3b47; }

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
    .glass-card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(238, 156, 167, 0.5); }

    .stButton > button {
        background: linear-gradient(135deg, #ffb6c1 0%, #ee9ca7 100%);
        color: #6b2c3a;
        border: none;
        border-radius: 30px;
        padding: 10px 22px;
        font-weight: 700;
        box-shadow: 0 4px 14px rgba(238, 156, 167, 0.5);
        transition: transform 0.15s ease;
    }
    .stButton > button:hover { transform: scale(1.05); color: #6b2c3a; }

    .title-banner { text-align: center; padding: 10px 0 4px 0; }

    @keyframes popIn {
        0%   { transform: scale(0.05); opacity: 0; }
        60%  { transform: scale(1.08); opacity: 1; }
        100% { transform: scale(1); opacity: 1; }
    }
    .pocket-photo-new { animation: popIn 0.6s cubic-bezier(.2,.9,.3,1.3) forwards; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# THE RPG SCENE COMPONENT
# ---------------------------------------------------------------------------
# Plain (non f-string) template — the JS below is full of { } so an f-string
# would require escaping every brace. We substitute placeholders with
# .replace() instead, which keeps the JS readable.
RPG_SCENE_TEMPLATE = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  html, body {
      margin: 0; padding: 0; background: transparent; overflow: hidden;
      font-family: 'Courier New', monospace;
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

  /* Retro scrolling tile strip — classic CSS sprite-sheet steps() trick */
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
  }

  /* ---- Classic GBA-style dialogue box ---- */
  .dbox-wrap {
      position: absolute;
      left: 6px; right: 6px; bottom: 6px;
      display: __DBOX_DISPLAY__;
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
</style>
</head>
<body>
  <div class="scene-wrap">
    <canvas id="rpgCanvas" width="__CANVAS_W__" height="__CANVAS_H__"></canvas>
    <div class="ground-strip"></div>
    <div class="dbox-wrap">
      <div class="dbox">
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
  var DIALOGUE = __DIALOGUE_JSON__;   // array of strings, or null

  // ---- palette ----
  var C_HAIR = "#4a2c17";
  var C_SKIN = "#ffd9b3";
  var C_SHIRT = "#4f8ecb";
  var C_SHIRT_DK = "#33618f";
  var C_PANTS = "#333355";
  var C_SHOE = "#22222a";
  var C_EYE = "#2c2c54";
  var C_MOUTH = "#a14a5c";
  var C_POCKET = "#22314a";
  var C_HEART = "#ff6f91";

  var state = {
      x: POSE === "walk" ? -20 : Math.round(W / 2),
      targetX: Math.round(W / 2),
      walking: POSE === "walk",
      legPhase: 0,
      tick: 0,
      armWaveT: 0,
      hopT: 0,
      mouthOpen: false
  };

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
      // ax, groundY = feet anchor (bottom-center)
      var bob = 0;
      if (POSE === "celebrate") {
          bob = Math.sin(s.hopT) * 3;
      } else if (!s.walking) {
          bob = Math.sin(s.tick / 12) * 1.2;
      }
      var ay = groundY + bob;

      // legs
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

      // body
      drawRect(ax - 9, ay - 34, 18, 20, C_SHIRT);
      drawRect(ax - 9, ay - 34, 18, 3, C_SHIRT_DK);

      // pocket
      drawRect(ax + 3, ay - 20, 5, 5, C_POCKET);

      // arms
      var armAngleL = 8, armAngleR = -8;
      if (POSE === "talk") {
          armAngleR = -60 + Math.sin(s.armWaveT) * 35;
      } else if (POSE === "reach") {
          armAngleR = 70;
      } else if (POSE === "celebrate") {
          armAngleL = 150 + Math.sin(s.hopT) * 10;
          armAngleR = -150 - Math.sin(s.hopT) * 10;
      } else if (s.walking) {
          armAngleL = s.legPhase === 0 ? 30 : -20;
          armAngleR = s.legPhase === 0 ? -20 : 30;
      }
      drawArm(ax - 9, ay - 32, armAngleL, C_SHIRT_DK);
      drawArm(ax + 9, ay - 32, armAngleR, C_SHIRT_DK);

      // head
      drawRect(ax - 8, ay - 50, 16, 16, C_SKIN);
      drawRect(ax - 9, ay - 54, 18, 6, C_HAIR);
      drawRect(ax - 9, ay - 50, 3, 10, C_HAIR);
      drawRect(ax + 6, ay - 50, 3, 10, C_HAIR);

      // eyes
      drawRect(ax - 5, ay - 42, 2, 2, C_EYE);
      drawRect(ax + 3, ay - 42, 2, 2, C_EYE);

      // mouth (toggles for talk)
      var mouthH = (POSE === "talk" && s.mouthOpen) ? 3 : 1;
      drawRect(ax - 3, ay - 37, 6, mouthH, C_MOUTH);

      // floating heart
      if (SHOW_HEART) {
          var hy = ay - 66 - Math.sin(s.tick / 10) * 4;
          var hx = ax + 12;
          ctx.fillStyle = C_HEART;
          ctx.fillRect(hx, hy, 3, 3);
          ctx.fillRect(hx + 4, hy, 3, 3);
          ctx.fillRect(hx - 1, hy + 3, 9, 3);
          ctx.fillRect(hx + 1, hy + 6, 5, 2);
      }
  }

  function drawBackground() {
      ctx.clearRect(0, 0, W, H);
  }

  // ---- 30 FPS game loop ----
  var FPS = 30;
  function tick() {
      state.tick++;
      state.armWaveT += 0.35;
      state.hopT += 0.28;

      if (state.walking) {
          state.x += 2.2;
          if (state.tick % 4 === 0) state.legPhase = 1 - state.legPhase;
          if (state.x >= state.targetX) {
              state.x = state.targetX;
              state.walking = false;
          }
      }
      if (POSE === "talk" && state.tick % 5 === 0) {
          state.mouthOpen = !state.mouthOpen;
      }

      drawBackground();
      drawBoy(state.x, GROUND_Y, state);
  }
  setInterval(tick, 1000 / FPS);
  tick();

  // ---- Dialogue typing effect ----
  if (DIALOGUE && DIALOGUE.length > 0) {
      var lines = DIALOGUE;
      var lineIdx = 0;
      var textEl = document.getElementById('dboxText');
      var arrowEl = document.getElementById('dboxArrow');

      function typeLine(line) {
          textEl.textContent = "";
          arrowEl.style.display = "none";
          var i = 0;
          var speed = 28;
          var timer = setInterval(function () {
              textEl.textContent += line.charAt(i);
              i++;
              if (i >= line.length) {
                  clearInterval(timer);
                  arrowEl.style.display = "block";
              }
          }, speed);
      }
      typeLine(lines[0]);
  }
})();
</script>
</body>
</html>
"""


def render_rpg_scene(
    pose: str = "idle",
    dialogue=None,
    show_heart: bool = False,
    scene_w: int = 420,
    scene_h: int = 260,
    canvas_w: int = 140,
    canvas_h: int = 110,
    scale: int = 3,
) -> None:
    """Render one frame of the Pokémon-style RPG scene inside an isolated
    HTML5 Canvas component running a real 30 FPS game loop.

    pose: "idle" | "walk" | "talk" | "reach" | "celebrate"
    dialogue: list[str] or None — first line is typed out in the RPG text box
    """
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
        .replace("__DIALOGUE_JSON__", json.dumps(dialogue) if dialogue else "null")
        .replace("__DBOX_DISPLAY__", "block" if dialogue else "none")
    )
    components.html(html, height=scene_h + 10, scrolling=False)


# ---------------------------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------------------------
if "dialogue_stage" not in st.session_state:
    st.session_state.dialogue_stage = "idle"   # idle -> greet -> yes/more -> end
if "pocket_revealed" not in st.session_state:
    st.session_state.pocket_revealed = []
if "just_revealed" not in st.session_state:
    st.session_state.just_revealed = False

# ---------------------------------------------------------------------------
# HEADER + TABS
# ---------------------------------------------------------------------------
st.markdown(
    '<div class="title-banner"><h1>🎀 Happy Birthday, Pikku! 🎂</h1></div>',
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["💬 Meet Him", "📖 His Story", "🎁 Pocket Surprise", "🎬 Cute Videos", "🧸 Thank You"]
)

# ---------------------------------------------------------------------------
# TAB 1 — 2D Pokémon RPG Intro
# ---------------------------------------------------------------------------
with tab1:
    st.markdown("### He walks into the scene, just for you...")
    safe_audio(BG_MUSIC_PATH)

    stage = st.session_state.dialogue_stage

    if stage == "idle":
        render_rpg_scene(pose="walk", dialogue=["...", "Click below to talk to him!"])
    elif stage == "greet":
        render_rpg_scene(pose="talk", dialogue=[GREETING_LINE])
    elif stage == "yes":
        render_rpg_scene(
            pose="celebrate",
            show_heart=True,
            dialogue=["Yay! I'm so glad. 🎉 This is going to be the best birthday yet."],
        )
    elif stage == "more":
        render_rpg_scene(
            pose="talk",
            dialogue=["Well... I've been planning a few little surprises for you. Check the other tabs. 👀"],
        )

    st.write("")
    col1, col2, col3 = st.columns([1, 1, 1])

    if stage == "idle":
        with col1:
            if st.button("💬 Talk to him", use_container_width=True):
                st.session_state.dialogue_stage = "greet"
                st.rerun()

    elif stage == "greet":
        with col1:
            if st.button("Yes! 💗", use_container_width=True):
                st.session_state.dialogue_stage = "yes"
                st.rerun()
        with col2:
            if st.button("Tell me more!", use_container_width=True):
                st.session_state.dialogue_stage = "more"
                st.rerun()

    else:
        with col1:
            if st.button("🔄 Restart", use_container_width=True):
                st.session_state.dialogue_stage = "idle"
                st.rerun()

# ---------------------------------------------------------------------------
# TAB 2 — Interactive Story Scenes
# ---------------------------------------------------------------------------
with tab2:
    st.markdown("### Our little story, told through him 📖")

    story_days = [
        ("Day 1", "The Arrival", "walk", False,
         "He walks in, a little nervous, and introduces himself for the first time."),
        ("Day 2", "The Gesture", "talk", True,
         "He shows up with a small gesture — nothing big, just something from the heart."),
        ("Day 3", "Getting Closer", "talk", False,
         "He shares a memory that means a lot to him, hoping it means something to you too."),
        ("Day 4", "Forever", "celebrate", True,
         "He's celebrating right beside you — because forever starts with days like this."),
    ]

    row1 = st.columns(2)
    row2 = st.columns(2)
    positions = row1 + row2

    for col, (day, title, pose, heart, desc) in zip(positions, story_days):
        with col:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(
                f'<h4 style="text-align:center;margin:0;">{day}</h4>'
                f'<h3 style="text-align:center;margin:0 0 6px 0;">{title}</h3>',
                unsafe_allow_html=True,
            )
            render_rpg_scene(
                pose=pose, show_heart=heart,
                scene_w=320, scene_h=200, canvas_w=110, canvas_h=90, scale=2,
            )
            st.markdown(
                f'<p style="text-align:center;font-size:14px;">{desc}</p>',
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# TAB 3 — Interactive Pocket-Photo Reveal (Game Mechanic)
# ---------------------------------------------------------------------------
with tab3:
    st.markdown("### He's got something hidden in his pocket 🎁")
    st.caption("Click the button and watch him pull out a memory...")

    revealed = st.session_state.pocket_revealed
    next_index = len(revealed)
    all_revealed = next_index >= len(POCKET_PHOTOS)

    pose = "reach" if not all_revealed else "celebrate"
    dlg = (
        ["He reaches into his pocket..."] if not all_revealed
        else ["That's everything he had in there. 💗"]
    )
    render_rpg_scene(pose=pose, show_heart=all_revealed, dialogue=dlg)

    st.write("")
    btn_col, _ = st.columns([1, 2])
    with btn_col:
        if not all_revealed:
            if st.button("🎁 Pull photo from pocket", use_container_width=True):
                st.session_state.pocket_revealed.append(next_index)
                st.session_state.just_revealed = True
                st.rerun()
        else:
            st.button("✨ All memories found!", use_container_width=True, disabled=True)

    if st.session_state.just_revealed:
        st.balloons()
        st.session_state.just_revealed = False

    if revealed:
        st.write("")
        st.markdown("#### Revealed memories")

        # Newest photo gets a big, prominent "expanding" reveal card.
        newest_idx = revealed[-1]
        newest = POCKET_PHOTOS[newest_idx]
        st.markdown('<div class="pocket-photo-new">', unsafe_allow_html=True)
        if os.path.exists(newest["path"]):
            st.image(newest["path"], caption=newest["caption"], use_container_width=True)
        else:
            st.markdown(
                f"""
                <div class="glass-card" style="text-align:center;">
                    <div style="font-size:64px;">🌸</div>
                    <p style="font-weight:600;font-size:18px;">{newest['caption']}</p>
                    <p style="font-size:12px;color:#c98a97;">(add photo at {newest['path']})</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

        if len(revealed) > 1:
            st.caption("Earlier finds:")
            older_cols = st.columns(3)
            for pos, idx in enumerate(revealed[:-1]):
                memory = POCKET_PHOTOS[idx]
                with older_cols[pos % 3]:
                    if os.path.exists(memory["path"]):
                        st.image(memory["path"], caption=memory["caption"], use_container_width=True)
                    else:
                        st.markdown(
                            f"""
                            <div class="glass-card" style="text-align:center;padding:12px;">
                                <div style="font-size:34px;">🌸</div>
                                <p style="font-size:12px;font-weight:600;">{memory['caption']}</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
    else:
        st.markdown(
            """
            <div class="glass-card" style="text-align:center;">
                <div style="font-size:46px;">🤫</div>
                <p>His pocket is still full of secrets... go on, ask him.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------------------------
# TAB 4 — Cute Videos
# ---------------------------------------------------------------------------
with tab4:
    st.markdown("### A few cute clips, just for you 🎬")

    vid_cols = st.columns(2)
    labels = ["Cute Clip 1", "Cute Clip 2"]
    for col, path, label in zip(vid_cols, VIDEO_PATHS, labels):
        with col:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(f"**{label}**")
            safe_video(path, label)
            st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# TAB 5 — Thank You & Finale
# ---------------------------------------------------------------------------
with tab5:
    st.markdown(
        '<h2 style="text-align:center;">Thank you for being you, Pikku 🧸</h2>',
        unsafe_allow_html=True,
    )

    render_rpg_scene(
        pose="celebrate",
        show_heart=True,
        dialogue=["Happy Birthday, Pikku! 🎂"],
    )

    if st.button("🎉 Celebrate!", use_container_width=True):
        st.balloons()

    st.markdown(
        """
        <div class="glass-card" style="text-align:center; margin-top:10px;">
            <p style="font-size:18px; font-weight:600;">
                Happy Birthday, Pikku! 🎂<br>
                May this year bring you as much joy as you bring into everyone else's life.
                Here's to more days, more stories, and more reasons to smile together. 💗
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
