"""
Pikku's Birthday Web App
=========================
A 5-tab Streamlit birthday experience with a 2D RPG dialogue character,
glassmorphism story cards, a surprise photo curtain, a video tab, and a
Lottie-powered finale.

Run with:
    streamlit run app.py

Dependencies (requirements.txt):
    streamlit
    streamlit-lottie
    requests
    Pillow
"""

import base64
import os

import requests
import streamlit as st
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
# ASSET PATHS (swap these with your own files — everything degrades safely
# if a file is missing, so the app never crashes)
# ---------------------------------------------------------------------------
ASSETS_DIR = "assets"
CHARACTER_IDLE_IMG = os.path.join(ASSETS_DIR, "boy_idle.png")
CHARACTER_TALK_IMG = os.path.join(ASSETS_DIR, "boy_talk.png")
BG_MUSIC_PATH = os.path.join(ASSETS_DIR, "bg_music.mp3")
VIDEO_PATHS = [
    os.path.join(ASSETS_DIR, "video1.mp4"),
    os.path.join(ASSETS_DIR, "video2.mp4"),
]
SECRET_PHOTOS = [
    {"path": os.path.join(ASSETS_DIR, "memory1.jpg"), "caption": "The day we first talked 💌"},
    {"path": os.path.join(ASSETS_DIR, "memory2.jpg"), "caption": "That silly joke you made 😂"},
    {"path": os.path.join(ASSETS_DIR, "memory3.jpg"), "caption": "The moment I knew 💗"},
    {"path": os.path.join(ASSETS_DIR, "memory4.jpg"), "caption": "Us, always 🌸"},
]

LOTTIE_BEAR_URL = "https://assets9.lottiefiles.com/packages/lf20_ttvtnye8.json"


# ---------------------------------------------------------------------------
# SAFE HELPERS — nothing below ever throws, the app just falls back quietly
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
    """Return base64 string of a local image, or None if it doesn't exist."""
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


def safe_image(path: str, emoji_fallback: str, width: int = 220):
    """Show a local image if present, else a big emoji placeholder."""
    b64 = img_to_base64(path)
    if b64:
        ext = path.split(".")[-1]
        st.markdown(
            f'<img src="data:image/{ext};base64,{b64}" width="{width}" '
            f'style="display:block;margin:0 auto;" />',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div style="font-size:{width * 0.55}px;text-align:center;">{emoji_fallback}</div>',
            unsafe_allow_html=True,
        )


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


def safe_photo(path: str, caption: str, fallback_emoji: str = "🌸"):
    if os.path.exists(path):
        st.image(path, caption=caption, use_container_width=True)
    else:
        st.markdown(
            f"""
            <div class="glass-card" style="text-align:center;">
                <div style="font-size:60px;">{fallback_emoji}</div>
                <p style="margin-top:8px;color:#a14a5c;font-weight:600;">{caption}</p>
                <p style="font-size:12px;color:#c98a97;">(add photo at {path})</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# GLOBAL CSS — pink gradient, glassmorphism, speech bubble, walk-in animation
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #ffdde1 0%, #ee9ca7 100%);
        background-attachment: fixed;
    }

    #MainMenu, header, footer {visibility: hidden;}

    h1, h2, h3, h4 {
        color: #a14a5c !important;
        text-shadow: 0 2px 6px rgba(255,255,255,0.4);
    }

    p, span, label, li {
        color: #7a3b47;
    }

    /* ---- Glassmorphism cards ---- */
    .glass-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 22px;
        border: 1.5px solid rgba(238, 156, 167, 0.55);
        box-shadow: 0 8px 32px rgba(238, 156, 167, 0.35);
        padding: 22px 26px;
        margin-bottom: 20px;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(238, 156, 167, 0.5);
    }

    /* ---- Speech bubble ---- */
    .speech-bubble {
        position: relative;
        background: #ffe3e8;
        border: 2px solid #ee9ca7;
        border-radius: 20px;
        padding: 18px 24px;
        max-width: 480px;
        margin: 0 auto 6px auto;
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

    /* ---- Walk-in animation ---- */
    @keyframes walkIn {
        0% {
            transform: translateX(-260px);
            opacity: 0;
        }
        70% {
            opacity: 1;
        }
        100% {
            transform: translateX(0);
            opacity: 1;
        }
    }
    .character-stage {
        animation: walkIn 1.4s ease-out forwards;
        text-align: center;
        margin-top: 10px;
    }

    /* ---- Buttons ---- */
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
    .stButton > button:hover {
        transform: scale(1.05);
        color: #6b2c3a;
    }

    .title-banner {
        text-align: center;
        padding: 10px 0 4px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------------------------
if "dialogue_stage" not in st.session_state:
    st.session_state.dialogue_stage = 0  # 0 = idle/prompt, 1+ = dialogue lines
if "curtain_value" not in st.session_state:
    st.session_state.curtain_value = 0

DIALOGUE_LINES = [
    "हाय। हे आई नो योर बर्थडे इस कमिंग एंड आप बहुत खुश हो उसके लिए।",
    "आई जस्ट वांटेड टू से... यू मीन अ लॉट टू मी। 💗",
    "हर दिन तुम्हारे साथ खास लगता है, और आज का दिन उससे भी खास है।",
    "हैप्पी बर्थडे पिक्कू! मे यू ऑलवेज़ स्माइल लाइक दिस। 🎂✨",
]

# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------
st.markdown(
    '<div class="title-banner"><h1>🎀 Happy Birthday, Pikku! 🎂</h1></div>',
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["💬 Meet Him", "📖 Our 4 Days", "🎁 Surprise", "🎬 Cute Videos", "🧸 Thank You"]
)

# ---------------------------------------------------------------------------
# TAB 1 — 2D RPG Character Dialogue System
# ---------------------------------------------------------------------------
with tab1:
    st.markdown("### He walked all this way just to say something to you...")

    safe_audio(BG_MUSIC_PATH)

    st.markdown('<div class="character-stage">', unsafe_allow_html=True)

    stage = st.session_state.dialogue_stage

    if stage == 0:
        st.markdown(
            '<div class="speech-bubble">Psst... click below to hear what he wants to say 👀</div>',
            unsafe_allow_html=True,
        )
        safe_image(CHARACTER_IDLE_IMG, "🚶‍♂️")
    else:
        line_index = min(stage - 1, len(DIALOGUE_LINES) - 1)
        st.markdown(
            f'<div class="speech-bubble">{DIALOGUE_LINES[line_index]}</div>',
            unsafe_allow_html=True,
        )
        safe_image(CHARACTER_TALK_IMG, "🗣️")

    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if stage == 0:
            if st.button("💬 Talk to him / बात सुनो", use_container_width=True):
                st.session_state.dialogue_stage = 1
                st.rerun()
        else:
            if stage < len(DIALOGUE_LINES):
                if st.button("➡️ Next / आगे बढ़ो", use_container_width=True):
                    st.session_state.dialogue_stage += 1
                    st.rerun()
            else:
                st.button("✅ End / खत्म", use_container_width=True, disabled=True)

    with col2:
        if stage > 0:
            if st.button("💗 Aww, that's sweet", use_container_width=True):
                st.toast("He's smiling right now, wherever he is. 😊")

    with col3:
        if stage > 0:
            if st.button("🔄 Restart / फिर से", use_container_width=True):
                st.session_state.dialogue_stage = 0
                st.rerun()

# ---------------------------------------------------------------------------
# TAB 2 — Our 4 Days Story
# ---------------------------------------------------------------------------
with tab2:
    st.markdown("### Our little story, four days at a time 📖")

    story_days = [
        ("Day 1", "First Impression", "✨", "The first time our paths crossed — something just felt different."),
        ("Day 2", "Getting Closer", "🌷", "Conversations got longer, laughs got easier, and distance got smaller."),
        ("Day 3", "Falling In Love", "💞", "Somewhere between the small talks, it turned into something real."),
        ("Day 4", "Always & Forever", "🌈", "And now? It's not just days anymore — it's forever, one day at a time."),
    ]

    row1 = st.columns(2)
    row2 = st.columns(2)
    positions = row1 + row2

    for col, (day, title, emoji, desc) in zip(positions, story_days):
        with col:
            st.markdown(
                f"""
                <div class="glass-card">
                    <div style="font-size:38px; text-align:center;">{emoji}</div>
                    <h4 style="text-align:center; margin:4px 0 2px 0;">{day}</h4>
                    <h3 style="text-align:center; margin:0 0 10px 0;">{title}</h3>
                    <p style="text-align:center; font-size:14px;">{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ---------------------------------------------------------------------------
# TAB 3 — Interactive Photo Curtain (Surprise Screen)
# ---------------------------------------------------------------------------
with tab3:
    st.markdown("### Pull the curtain to unlock a surprise 🎁")
    st.caption("Drag the slider past 50% to reveal secret memories...")

    curtain = st.slider(
        "Open the curtain",
        min_value=0,
        max_value=100,
        value=st.session_state.curtain_value,
        key="curtain_slider",
    )
    st.session_state.curtain_value = curtain

    progress_pct = curtain
    st.markdown(
        f"""
        <div style="background: rgba(255,255,255,0.5); border-radius: 20px; height: 22px;
                    overflow: hidden; border: 1.5px solid #ee9ca7; margin-bottom: 18px;">
            <div style="width:{progress_pct}%; height:100%;
                        background: linear-gradient(90deg, #ffb6c1, #ee9ca7);
                        transition: width 0.3s ease;"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if curtain > 50:
        st.balloons()
        st.markdown(
            '<div class="speech-bubble">🎉 Surprise unlocked! Here are our secret memories 🎉</div>',
            unsafe_allow_html=True,
        )
        st.write("")

        photo_cols = st.columns(2)
        for i, memory in enumerate(SECRET_PHOTOS):
            with photo_cols[i % 2]:
                safe_photo(memory["path"], memory["caption"])
    else:
        st.markdown(
            """
            <div class="glass-card" style="text-align:center;">
                <div style="font-size:50px;">🔒</div>
                <p>The curtain is still closed... drag past halfway to peek behind it 👀</p>
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
            st.markdown(f"<div class='glass-card'>", unsafe_allow_html=True)
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

    lottie_bear = load_lottie_url(LOTTIE_BEAR_URL)

    if lottie_bear:
        st_lottie(lottie_bear, height=280, key="finale_bear")
    else:
        st.markdown(
            '<div style="font-size:110px; text-align:center;">🧸</div>',
            unsafe_allow_html=True,
        )
        st.caption("(Lottie animation couldn't load — showing a fallback bear instead 🧸)")

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
