"""
Pikku's Birthday Web App — Animated Edition
=============================================
A 5-tab Streamlit birthday experience featuring a fully-animated 2D CSS
character (walk cycle, talking pose, pocket-photo reveal game), pink
glassmorphism styling, a Lottie finale, and safe fallbacks everywhere.

Run with:
    streamlit run app.py

requirements.txt:
    streamlit
    streamlit-lottie
    requests
    Pillow
"""

import os
import base64

import requests
import streamlit as st
import streamlit.components.v1 as components
from streamlit_lottie import st_lottie

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

LOTTIE_URLS = {
    "bear": "https://assets9.lottiefiles.com/packages/lf20_ttvtnye8.json",
    "confetti": "https://assets2.lottiefiles.com/packages/lf20_u4yrau.json",
}

DIALOGUE_LINES = [
    "Hi. Hey, I know your birthday is coming and you are very happy for that.",
    "I just wanted to say... you mean a lot to me. 💗",
    "Every day with you feels special, and today is even more special.",
    "Happy Birthday, Pikku! May you always smile like this. 🎂✨",
]

# ---------------------------------------------------------------------------
# SAFE HELPERS — nothing below ever throws; the app falls back quietly
# ---------------------------------------------------------------------------
def load_lottie_url(url: str, timeout: int = 6):
    """Fetch a Lottie JSON animation. Returns None on any failure."""
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


def img_to_base64(path: str):
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


def safe_audio(path: str):
    if os.path.exists(path):
        st.audio(path, format="audio/mp3")
    else:
        st.caption("🎵 Add your song at `assets/bg_music.mp3` to enable background music.")


def safe_video(path: str, label: str):
    if os.path.exists(path):
        st.video(path)
    else:
        st.info(f"📹 Add a clip at `{path}` to show '{label}' here.")


# ---------------------------------------------------------------------------
# GLOBAL CSS — pink gradient, glassmorphism, speech bubble, character rig
# ---------------------------------------------------------------------------
BASE_CSS = """
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

.speech-bubble {
    position: relative;
    background: #ffe3e8;
    border: 2px solid #ee9ca7;
    border-radius: 20px;
    padding: 16px 22px;
    max-width: 480px;
    margin: 0 auto 30px auto;
    text-align: center;
    font-size: 17px;
    font-weight: 600;
    color: #a14a5c;
    box-shadow: 0 6px 18px rgba(238, 156, 167, 0.4);
}
.speech-bubble::after {
    content: "";
    position: absolute;
    bottom: -14px;
    left: 50%;
    transform: translateX(-50%);
    border-width: 14px 14px 0 14px;
    border-style: solid;
    border-color: #ee9ca7 transparent transparent transparent;
}

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
</style>
"""
st.markdown(BASE_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# ANIMATED 2D CHARACTER — built from CSS shapes, no image assets required.
# Rendered through components.html so keyframes run isolated & reliably.
# Walk cycle uses short (0.28s) stepped leg/arm swings x 4 to approximate a
# smooth 30 FPS-style sprite walk while gliding across the stage.
# ---------------------------------------------------------------------------
CHARACTER_CSS = """
<style>
  * { box-sizing: border-box; }
  body { margin: 0; background: transparent; overflow: visible; }

  .stage {
      width: 100%;
      height: 100%;
      display: flex;
      align-items: flex-end;
      justify-content: center;
  }

  .pc-wrap {
      position: relative;
      width: 140px;
      height: 200px;
      animation: idleBob 2.2s ease-in-out infinite;
  }
  .pc-wrap.walk-in {
      animation: walkIn 1.3s cubic-bezier(.2,.8,.3,1) forwards,
                 idleBob 2.2s ease-in-out infinite 1.3s;
  }

  @keyframes walkIn {
      0%   { transform: translateX(-340px); opacity: 0; }
      55%  { opacity: 1; }
      100% { transform: translateX(0); opacity: 1; }
  }
  @keyframes idleBob {
      0%, 100% { transform: translateY(0); }
      50%      { transform: translateY(-5px); }
  }

  .pc-head {
      position: absolute; top: 0; left: 38px;
      width: 64px; height: 64px;
      background: #ffd9b3;
      border-radius: 50%;
      border: 3px solid #6b3f2a;
      z-index: 5;
  }
  .pc-hair {
      position: absolute; top: -8px; left: -3px;
      width: 70px; height: 34px;
      background: #4a2c17;
      border-radius: 50% 50% 0 0 / 100% 100% 0 0;
  }
  .pc-face-dot { position: absolute; top: 26px; width: 5px; height: 5px; background: #4a2c17; border-radius: 50%; }
  .pc-eye-l { left: 16px; } .pc-eye-r { left: 40px; }
  .pc-mouth {
      position: absolute; top: 40px; left: 22px;
      width: 18px; height: 6px;
      border-bottom: 3px solid #a14a5c;
      border-radius: 0 0 10px 10px;
      transition: all 0.15s ease;
  }
  .pc-wrap.talking .pc-mouth { animation: talkMouth 0.35s steps(2) infinite; }
  @keyframes talkMouth {
      0%   { height: 6px; }
      50%  { height: 12px; border-radius: 50%; }
      100% { height: 6px; }
  }

  .pc-torso {
      position: absolute; top: 58px; left: 30px;
      width: 80px; height: 78px;
      background: linear-gradient(160deg, #6fb1e0, #4f8ecb);
      border-radius: 26px 26px 20px 20px;
      border: 3px solid #33618f;
      z-index: 4;
  }

  .pc-arm {
      position: absolute; top: 64px;
      width: 16px; height: 58px;
      background: #6fb1e0;
      border: 3px solid #33618f;
      border-radius: 10px;
      transform-origin: top center;
      z-index: 3;
  }
  .pc-arm-l { left: 20px; transform: rotate(14deg); }
  .pc-arm-r { left: 104px; transform: rotate(-14deg); }

  .pc-wrap.walk-in .pc-arm-l { animation: armSwingL 0.56s ease-in-out 4, idleArm 2.2s ease-in-out infinite 2.5s; }
  .pc-wrap.walk-in .pc-arm-r { animation: armSwingR 0.56s ease-in-out 4, idleArm 2.2s ease-in-out infinite 2.5s; }
  @keyframes armSwingL { 0%,100% { transform: rotate(30deg); } 50% { transform: rotate(-25deg); } }
  @keyframes armSwingR { 0%,100% { transform: rotate(-30deg); } 50% { transform: rotate(25deg); } }
  @keyframes idleArm    { 0%,100% { transform: rotate(14deg); } 50% { transform: rotate(8deg); } }

  .pc-wrap.talking .pc-arm-r {
      animation: talkWave 0.7s ease-in-out infinite;
      transform-origin: top center;
  }
  @keyframes talkWave {
      0%, 100% { transform: rotate(-70deg); }
      50%      { transform: rotate(-110deg); }
  }

  .pc-wrap.reaching .pc-arm-r {
      animation: reachPocket 0.9s ease forwards;
  }
  @keyframes reachPocket {
      0%   { transform: rotate(-14deg); }
      100% { transform: rotate(55deg); }
  }

  .pc-wrap.celebrating .pc-arm-l { animation: celebrateL 0.6s ease-in-out infinite; }
  .pc-wrap.celebrating .pc-arm-r { animation: celebrateR 0.6s ease-in-out infinite; }
  @keyframes celebrateL { 0%,100% { transform: rotate(-150deg); } 50% { transform: rotate(-170deg); } }
  @keyframes celebrateR { 0%,100% { transform: rotate(150deg); }  50% { transform: rotate(170deg); } }

  .pc-pocket {
      position: absolute; top: 108px; left: 92px;
      width: 20px; height: 16px;
      background: #33618f;
      border-radius: 4px;
      z-index: 6;
  }

  .pc-legs { position: absolute; top: 132px; left: 42px; width: 56px; height: 60px; }
  .pc-leg {
      position: absolute; top: 0;
      width: 16px; height: 56px;
      background: #3a3a52;
      border-radius: 8px;
      transform-origin: top center;
  }
  .pc-leg-l { left: 4px; }
  .pc-leg-r { left: 36px; }

  .pc-wrap.walk-in .pc-leg-l { animation: legSwingL 0.56s ease-in-out 4; }
  .pc-wrap.walk-in .pc-leg-r { animation: legSwingR 0.56s ease-in-out 4; }
  @keyframes legSwingL { 0%,100% { transform: rotate(-26deg); } 50% { transform: rotate(26deg); } }
  @keyframes legSwingR { 0%,100% { transform: rotate(26deg); }  50% { transform: rotate(-26deg); } }

  .pc-wrap.celebrating .pc-leg-l { animation: hopL 0.5s ease-in-out infinite; }
  .pc-wrap.celebrating .pc-leg-r { animation: hopR 0.5s ease-in-out infinite; }
  @keyframes hopL { 0%,100% { transform: rotate(-8deg); } 50% { transform: rotate(8deg); } }
  @keyframes hopR { 0%,100% { transform: rotate(8deg); }  50% { transform: rotate(-8deg); } }

  .pc-heart {
      position: absolute; top: -10px; left: 96px;
      font-size: 22px;
      opacity: 0;
      animation: heartFloat 2s ease-in infinite;
  }
  @keyframes heartFloat {
      0%   { transform: translateY(0) scale(0.6); opacity: 0; }
      20%  { opacity: 1; }
      100% { transform: translateY(-70px) scale(1.3); opacity: 0; }
  }
</style>
"""


def render_character(pose: str = "idle", show_heart: bool = False, height: int = 230) -> None:
    """Render the animated 2D character inside an isolated HTML component.

    pose: one of "idle", "walk", "talk", "reach", "celebrate"
    """
    pose_class = {
        "idle": "",
        "walk": "walk-in",
        "talk": "talking",
        "reach": "reaching",
        "celebrate": "celebrating",
    }.get(pose, "")

    heart_html = '<div class="pc-heart">💗</div>' if show_heart else ""

    html = f"""
    {CHARACTER_CSS}
    <div class="stage">
      <div class="pc-wrap {pose_class}">
        {heart_html}
        <div class="pc-head">
          <div class="pc-hair"></div>
          <div class="pc-face-dot pc-eye-l"></div>
          <div class="pc-face-dot pc-eye-r"></div>
          <div class="pc-mouth"></div>
        </div>
        <div class="pc-torso"></div>
        <div class="pc-arm pc-arm-l"></div>
        <div class="pc-arm pc-arm-r"></div>
        <div class="pc-pocket"></div>
        <div class="pc-legs">
          <div class="pc-leg pc-leg-l"></div>
          <div class="pc-leg pc-leg-r"></div>
        </div>
      </div>
    </div>
    """
    components.html(html, height=height, scrolling=False)


# ---------------------------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------------------------
if "dialogue_stage" not in st.session_state:
    st.session_state.dialogue_stage = 0
if "pocket_revealed" not in st.session_state:
    st.session_state.pocket_revealed = []  # list of revealed photo indices, in order
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
# TAB 1 — 2D Animated RPG Intro
# ---------------------------------------------------------------------------
with tab1:
    st.markdown("### He walked all this way just to say something to you...")
    safe_audio(BG_MUSIC_PATH)

    stage = st.session_state.dialogue_stage

    if stage == 0:
        st.markdown(
            '<div class="speech-bubble">Psst... click below to hear what he wants to say 👀</div>',
            unsafe_allow_html=True,
        )
        render_character(pose="walk")
    else:
        line_index = min(stage - 1, len(DIALOGUE_LINES) - 1)
        st.markdown(
            f'<div class="speech-bubble">{DIALOGUE_LINES[line_index]}</div>',
            unsafe_allow_html=True,
        )
        render_character(pose="talk")

    st.write("")
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if stage == 0:
            if st.button("💬 Talk to him", use_container_width=True):
                st.session_state.dialogue_stage = 1
                st.rerun()
        else:
            if stage < len(DIALOGUE_LINES):
                if st.button("➡️ Next", use_container_width=True):
                    st.session_state.dialogue_stage += 1
                    st.rerun()
            else:
                st.button("✅ End", use_container_width=True, disabled=True)

    with col2:
        if stage > 0:
            if st.button("💗 Aww, that's sweet", use_container_width=True):
                st.toast("He's smiling right now, wherever he is. 😊")

    with col3:
        if stage > 0:
            if st.button("🔄 Restart", use_container_width=True):
                st.session_state.dialogue_stage = 0
                st.rerun()

# ---------------------------------------------------------------------------
# TAB 2 — The Boy's Interactive Story
# ---------------------------------------------------------------------------
with tab2:
    st.markdown("### Our little story, told through him 📖")

    story_days = [
        ("Day 1", "The Arrival", "walk", False,
         "He walks in, a little nervous, and introduces himself for the first time."),
        ("Day 2", "The Gesture", "idle", True,
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
            render_character(pose=pose, show_heart=heart, height=190)
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
    render_character(pose=pose)

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
        pop_style = """
        <style>
        @keyframes pocketPop {
            0%   { transform: scale(0.05); opacity: 0; }
            60%  { transform: scale(1.08); opacity: 1; }
            100% { transform: scale(1); opacity: 1; }
        }
        .pocket-photo-new { animation: pocketPop 0.6s cubic-bezier(.2,.9,.3,1.3) forwards; }
        </style>
        """
        st.markdown(pop_style, unsafe_allow_html=True)

        photo_cols = st.columns(2)
        for pos, idx in enumerate(revealed):
            memory = POCKET_PHOTOS[idx]
            is_newest = pos == len(revealed) - 1
            anim_class = "pocket-photo-new" if is_newest else ""
            with photo_cols[pos % 2]:
                if os.path.exists(memory["path"]):
                    st.markdown(f'<div class="{anim_class}">', unsafe_allow_html=True)
                    st.image(memory["path"], caption=memory["caption"], use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.markdown(
                        f"""
                        <div class="glass-card {anim_class}" style="text-align:center;">
                            <div style="font-size:56px;">🌸</div>
                            <p style="font-weight:600;">{memory['caption']}</p>
                            <p style="font-size:12px;color:#c98a97;">(add photo at {memory['path']})</p>
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
# TAB 4 — Video Showcase
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

    render_character(pose="celebrate", show_heart=True)

    lottie_bear = load_lottie_url(LOTTIE_URLS["bear"])
    if lottie_bear:
        st_lottie(lottie_bear, height=220, key="finale_bear")
    else:
        st.markdown('<div style="font-size:90px;text-align:center;">🧸</div>', unsafe_allow_html=True)
        st.caption("(Bear animation couldn't load — showing a fallback bear instead 🧸)")

    if st.button("🎉 Celebrate!", use_container_width=True):
        lottie_confetti = load_lottie_url(LOTTIE_URLS["confetti"])
        if lottie_confetti:
            st_lottie(lottie_confetti, height=200, key="confetti_burst")
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
