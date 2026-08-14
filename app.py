"""
╔══════════════════════════════════════════════════════════════╗
║           PIKKU'S BIRTHDAY WEB APP v2.0                      ║
║           Professional 2D RPG Animation Engine               ║
║           Streamlit + HTML5 Canvas + 30 FPS Game Loop        ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import json
import base64
from typing import Optional, List, Dict, Any

import streamlit as st
import streamlit.components.v1 as components

# ===========================================================================
# PAGE CONFIGURATION
# ===========================================================================
st.set_page_config(
    page_title="Happy Birthday, Pikku! 🎀",
    page_icon="🎂",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ===========================================================================
# CONSTANTS & CONFIGURATION
# ===========================================================================
ASSETS_DIR: str = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

BG_MUSIC_PATH: str = os.path.join(ASSETS_DIR, "bg_music.mp3")
VIDEO_PATHS: List[str] = [
    os.path.join(ASSETS_DIR, "video1.mp4"),
    os.path.join(ASSETS_DIR, "video2.mp4"),
]

POCKET_PHOTOS: List[Dict[str, str]] = [
    {"path": os.path.join(ASSETS_DIR, "memory1.jpg"), "caption": "My kuchupuchu 💌"},
    {"path": os.path.join(ASSETS_DIR, "memory2.jpg"), "caption": "My guguluu"},
    {"path": os.path.join(ASSETS_DIR, "memory3.jpg"), "caption": "Puchukukilu"},
    {"path": os.path.join(ASSETS_DIR, "memory4.jpg"), "caption": "Us, always 🌸"},
]

GREETING_LINE: str = "Hi. Hey, moi janu aji mur pukulu r special din."

CANVAS_WIDTH: int = 420
CANVAS_HEIGHT: int = 260
SCENE_HEIGHT: int = 280


# ===========================================================================
# UTILITY FUNCTIONS
# ===========================================================================
def safe_audio(path: str) -> None:
    if os.path.exists(path):
        try:
            with open(path, "rb") as f:
                audio_base64: str = base64.b64encode(f.read()).decode()
            st.markdown(f'<audio autoplay loop style="display:none;"><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
            st.caption("🎵 Background music is playing...")
        except Exception:
            st.caption("🎵 Add a valid MP3 file to assets/bg_music.mp3")
    else:
        st.caption("🎵 Place your music at assets/bg_music.mp3")


def safe_video(path: str, label: str) -> None:
    if os.path.exists(path):
        try:
            st.video(path)
        except Exception:
            st.info(f"📹 Add a valid video file at: {path}")
    else:
        st.info(f"📹 Place your video at: {path}")


def safe_image(path: str, caption: str = "", use_container_width: bool = True) -> None:
    if os.path.exists(path):
        try:
            st.image(path, caption=caption, use_container_width=use_container_width)
        except Exception:
            _render_image_placeholder(caption)
    else:
        _render_image_placeholder(caption)


def _render_image_placeholder(caption: str) -> None:
    st.markdown(f'<div style="text-align:center;padding:30px;background:rgba(255,255,255,0.9);border-radius:20px;border:2px dashed #ffb6c1;"><div style="font-size:64px;">🌸</div><p style="font-weight:600;font-size:16px;color:#c44569;">{caption}</p><p style="font-size:12px;color:#c98a97;">📸 Add your photo to the assets folder</p></div>', unsafe_allow_html=True)


# ===========================================================================
# GLOBAL STYLESHEET
# ===========================================================================
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #ffdde1 0%, #ee9ca7 100%); background-attachment: fixed; }
    #MainMenu, header, footer { visibility: hidden; }
    h1, h2, h3, h4 { color: #a14a5c !important; text-align: center; text-shadow: 0 2px 6px rgba(255,255,255,0.4); }
    p, span, label, div { color: #7a3b47; }
    .glass-card { background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-radius: 22px; border: 1.5px solid rgba(238, 156, 167, 0.55); box-shadow: 0 8px 32px rgba(238, 156, 167, 0.35); padding: 20px 24px; margin-bottom: 20px; }
    .stButton > button { background: linear-gradient(135deg, #ffb6c1 0%, #ee9ca7 100%); color: #6b2c3a; border: none; border-radius: 30px; padding: 12px 24px; font-weight: 700; font-size: 16px; width: 100%; cursor: pointer; box-shadow: 0 4px 14px rgba(238, 156, 167, 0.5); }
    .stButton > button:hover { transform: scale(1.05); box-shadow: 0 6px 20px rgba(238, 156, 167, 0.7); }
    .step-indicator { display: flex; justify-content: center; gap: 12px; margin: 20px 0 30px 0; }
    .step-dot { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 18px; background: rgba(255, 255, 255, 0.5); color: #c98a97; border: 2px solid #ee9ca7; }
    .step-dot.active { background: #ee9ca7; color: white; border-color: #c44569; box-shadow: 0 0 20px rgba(238, 156, 167, 0.6); animation: pulse 2s infinite; }
    .step-dot.done { background: #c44569; color: white; border-color: #c44569; }
    .dialogue-box { background: #fff8ec; border: 3px solid #2c2c54; border-radius: 10px; padding: 12px 16px; text-align: center; margin-top: 8px; font-family: 'Courier New', monospace; font-size: 15px; color: #2c2c54; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2); }
    @keyframes pulse { 0%, 100% { box-shadow: 0 0 20px rgba(238, 156, 167, 0.6); } 50% { box-shadow: 0 0 35px rgba(238, 156, 167, 0.9); } }
    @keyframes glowPulse { 0%, 100% { text-shadow: 0 0 10px rgba(255, 107, 157, 0.3); } 50% { text-shadow: 0 0 30px rgba(255, 107, 157, 0.8), 0 0 60px rgba(255, 107, 157, 0.4); } }
    .glow-text { animation: glowPulse 2s ease-in-out infinite; }
    @media (max-width: 768px) { .step-dot { width: 32px; height: 32px; font-size: 14px; } .glass-card { padding: 14px 16px; } }
</style>
""", unsafe_allow_html=True)


# ===========================================================================
# SESSION STATE MANAGEMENT
# ===========================================================================
def initialize_session_state() -> None:
    defaults: Dict[str, Any] = {
        "current_step": 1,
        "step1_stage": "walk",
        "step2_idx": 0,
        "step2_show": False,
        "step2_just": False,
        "step4_phase": "entry",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


initialize_session_state()


# ===========================================================================
# ANIMATION ENGINE - HTML5 Canvas Renderer
# ===========================================================================
def render_scene(pose: str = "idle", show_girl: bool = False, show_heart: bool = False, holding_photo: bool = False) -> None:
    html_content: str = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RPG Scene</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ background: transparent; display: flex; justify-content: center; align-items: center; min-height: 100vh; overflow: hidden; }}
        canvas {{ border: 3px solid #7a4a3a; border-radius: 16px; display: block; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); }}
    </style>
</head>
<body>
    <canvas id="gameCanvas" width="{CANVAS_WIDTH}" height="{CANVAS_HEIGHT}"></canvas>
    <script>
    (function() {{
        'use strict';
        
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        ctx.imageSmoothingEnabled = false;
        
        const W = {CANVAS_WIDTH};
        const H = {CANVAS_HEIGHT};
        const GROUND_Y = H - 22;
        
        const POSE = '{pose}';
        const SHOW_HEART = {str(show_heart).lower()};
        const SHOW_GIRL = {str(show_girl).lower()};
        const HOLDING_PHOTO = {str(holding_photo).lower()};
        
        // Color palette
        const C = {{
            hair: '#4a2c17', hairGirl: '#8B4513', skin: '#ffd9b3',
            shirt: '#4f8ecb', shirtDark: '#33618f', dress: '#FF69B4',
            dressDark: '#FF1493', pants: '#333355', shoe: '#22222a',
            eye: '#2c2c54', mouth: '#a14a5c', pocket: '#1a2538',
            heart: '#ff6f91', photoBg: '#fffef5', photoBorder: '#ffb6c1',
            shadow: 'rgba(0,0,0,0.2)', cloud: 'rgba(255,255,255,0.8)',
            cloudFar: 'rgba(255,255,255,0.5)', sky: '#c8e6ff', grass: '#7fc97f'
        }};
        
        // BOY character - walks in from LEFT
        const boy = {{
            x: -40, targetX: SHOW_GIRL ? 170 : 210, y: GROUND_Y,
            walking: true, legPhase: 0, armWaveTimer: 0, hopTimer: 0,
            mouthOpen: false, kissFrame: 0, isKissing: false
        }};
        
        // GIRL character - walks in from RIGHT (Step 4 finale)
        const girl = {{
            x: 460, targetX: 250, y: GROUND_Y,
            walking: SHOW_GIRL, legPhase: 1, armWaveTimer: 0, hopTimer: 0,
            kissFrame: 0, isKissing: false
        }};
        
        let tickCount = 0;
        
        function dr(x,y,w,h,c){{ctx.fillStyle=c;ctx.fillRect(Math.round(x),Math.round(y),w,h);}}
        function arm(sx,sy,a,c){{ctx.save();ctx.translate(sx,sy);ctx.rotate(a*Math.PI/180);ctx.fillStyle=c;ctx.fillRect(-2,0,5,15);ctx.restore();}}
        function shadow(cx,gy){{ctx.fillStyle=C.shadow;ctx.beginPath();ctx.ellipse(cx,gy+18,12,4,0,0,Math.PI*2);ctx.fill();}}
        
        // Draw BOY
        function dB(ax,gy,s){{
            var bob=0;
            if(POSE==='celebrate')bob=Math.sin(s.hopTimer)*5;
            else if(!s.walking&&POSE!=='walk')bob=Math.sin(tickCount/6)*1.8;
            var ay=gy+bob;
            shadow(ax,ay);
            var ll=0,lr=0;
            if(s.walking){{ll=s.legPhase?-5:0;lr=s.legPhase?0:-5;}}
            else if(POSE==='celebrate'){{ll=Math.sin(s.hopTimer)>0?-3:0;lr=Math.sin(s.hopTimer)>0?0:-3;}}
            // Legs
            dr(ax-7,ay-16+ll,6,16,C.pants);dr(ax-7,ay-1+ll,6,4,C.shoe);
            dr(ax+1,ay-16+lr,6,16,C.pants);dr(ax+1,ay-1+lr,6,4,C.shoe);
            // Body
            dr(ax-9,ay-34,18,20,C.shirt);dr(ax-9,ay-34,18,3,C.shirtDark);
            dr(ax+3,ay-20,5,5,C.pocket);
            // Arms
            var al=8,ar=-8;
            if(POSE==='talk')ar=-60+Math.sin(s.armWaveTimer)*40;
            else if(POSE==='reach')ar=75;
            else if(POSE==='celebrate'){{al=150+Math.sin(s.hopTimer)*15;ar=-150-Math.sin(s.hopTimer)*15;}}
            else if(POSE==='hug'){{al=-55;ar=55;}}
            else if(POSE==='kiss'){{al=-50;ar=50;}}
            else if(s.walking){{al=s.legPhase?30:-20;ar=s.legPhase?-20:30;}}
            arm(ax-9,ay-32,al,C.shirtDark);arm(ax+9,ay-32,ar,C.shirtDark);
            // Photo in hand
            if(HOLDING_PHOTO&&POSE==='reach'){{
                var px=ax+14,py=ay-38;
                dr(px-8,py-10,16,20,C.photoBg);
                ctx.strokeStyle=C.photoBorder;ctx.lineWidth=1;ctx.strokeRect(px-8,py-10,16,20);
                dr(px-4,py-4,3,3,C.heart);dr(px+3,py-4,3,3,C.heart);dr(px-4,py,10,3,C.heart);
            }}
            // Head
            dr(ax-8,ay-50,16,16,C.skin);
            dr(ax-9,ay-54,18,6,C.hair);dr(ax-9,ay-50,3,10,C.hair);dr(ax+6,ay-50,3,10,C.hair);
            // Face
            if(POSE==='kiss'&&s.isKissing){{dr(ax-4,ay-42,2,2,C.eye);dr(ax+2,ay-42,1,1,C.eye);dr(ax-2,ay-36,4,2,C.mouth);}}
            else{{dr(ax-5,ay-42,2,2,C.eye);dr(ax+3,ay-42,2,2,C.eye);var mh=(POSE==='talk'&&s.mouthOpen)?3:1;dr(ax-3,ay-37,6,mh,C.mouth);}}
            // Heart
            if(SHOW_HEART){{var hy=ay-66-Math.sin(tickCount/5)*6,hx=ax+12;dr(hx,hy,3,3,C.heart);dr(hx+4,hy,3,3,C.heart);dr(hx-1,hy+3,9,3,C.heart);dr(hx+1,hy+6,5,2,C.heart);}}
        }}
        
        // Draw GIRL
        function dG(ax,gy,s){{
            var bob=Math.sin(tickCount/6)*1.8,ay=gy+bob;
            shadow(ax,ay);
            var ll=0,lr=0;
            if(s.walking){{ll=s.legPhase?-5:0;lr=s.legPhase?0:-5;}}
            // Legs
            dr(ax-5,ay-8+ll,4,10,C.skin);dr(ax+1,ay-8+lr,4,10,C.skin);
            dr(ax-5,ay,4,3,C.dressDark);dr(ax+1,ay,4,3,C.dressDark);
            // Dress
            dr(ax-9,ay-26,18,20,C.dress);dr(ax-9,ay-26,18,3,C.dressDark);
            dr(ax-7,ay-38,14,14,C.dress);
            // Arms
            var al=8,ar=-8;
            if(POSE==='hug'){{al=-45;ar=45;}}
            else if(POSE==='kiss'){{al=-40;ar=40;}}
            else if(s.walking){{al=s.legPhase?30:-20;ar=s.legPhase?-20:30;}}
            arm(ax-7,ay-36,al,C.dressDark);arm(ax+7,ay-36,ar,C.dressDark);
            // Head
            dr(ax-8,ay-52,16,16,C.skin);
            dr(ax-9,ay-56,18,7,C.hairGirl);dr(ax-9,ay-52,3,10,C.hairGirl);dr(ax+6,ay-52,3,10,C.hairGirl);
            dr(ax-10,ay-53,4,5,C.hairGirl);dr(ax+6,ay-53,4,5,C.hairGirl);
            // Face
            if(POSE==='kiss'&&s.isKissing){{dr(ax-3,ay-44,2,2,C.eye);dr(ax+1,ay-44,1,1,C.eye);dr(ax-2,ay-38,4,2,C.mouth);}}
            else{{dr(ax-5,ay-44,3,3,C.eye);dr(ax+2,ay-44,3,3,C.eye);dr(ax-2,ay-39,5,2,C.mouth);ctx.fillStyle='rgba(255,150,150,0.4)';ctx.fillRect(ax-7,ay-41,3,2);ctx.fillRect(ax+4,ay-41,3,2);}}
            // Heart
            if(SHOW_HEART){{var hy=ay-68-Math.sin(tickCount/5+1)*5,hx=ax-8;dr(hx,hy,3,3,C.heart);dr(hx+4,hy,3,3,C.heart);dr(hx-1,hy+3,9,3,C.heart);dr(hx+1,hy+6,5,2,C.heart);}}
        }}
        
        // Background
        function drawBg(){{
            ctx.clearRect(0,0,W,H);
            var sky=ctx.createLinearGradient(0,0,0,H*0.55);sky.addColorStop(0,'#d4eeff');sky.addColorStop(1,C.sky);ctx.fillStyle=sky;ctx.fillRect(0,0,W,H*0.55);
            ctx.fillStyle=C.cloud;ctx.fillRect(15,8,35,9);ctx.fillRect(25,4,25,7);
            ctx.fillStyle=C.cloudFar;ctx.fillRect(W-55,12,30,7);
            var grass=ctx.createLinearGradient(0,H*0.55,0,H);grass.addColorStop(0,C.grass);grass.addColorStop(1,'#5a9e5a');ctx.fillStyle=grass;ctx.fillRect(0,H*0.55,W,H*0.45);
        }}
        
        // MAIN GAME LOOP - 30 FPS
        function gameLoop(){{
            tickCount++;
            boy.armWaveTimer+=0.4;boy.hopTimer+=0.3;
            girl.armWaveTimer+=0.35;girl.hopTimer+=0.28;
            
            // Kiss animation
            if(POSE==='kiss'){{boy.kissFrame++;girl.kissFrame++;if(boy.kissFrame>45){{boy.isKissing=true;girl.isKissing=true;}}}}
            
            // Boy walking
            if(boy.walking){{boy.x+=2.5;if(boy.x>=boy.targetX){{boy.x=boy.targetX;boy.walking=false;}}if(tickCount%3===0)boy.legPhase=1-boy.legPhase;}}
            
            // Girl walking
            if(girl.walking){{girl.x-=2.5;if(girl.x<=girl.targetX){{girl.x=girl.targetX;girl.walking=false;}}if(tickCount%3===0)girl.legPhase=1-girl.legPhase;}}
            
            // Mouth toggling for talk
            if(POSE==='talk'&&tickCount%4===0)boy.mouthOpen=!boy.mouthOpen;
            
            // Draw everything
            drawBg();
            dB(boy.x,boy.y,boy);
            if(SHOW_GIRL)dG(girl.x,girl.y,girl);
        }}
        
        // Start the game loop
        setInterval(gameLoop, 1000/30);
        gameLoop();
    }})();
    </script>
</body>
</html>"""
    
    components.html(html_content, height=SCENE_HEIGHT, scrolling=False)


# ===========================================================================
# STEP INDICATOR COMPONENT
# ===========================================================================
def render_step_indicator() -> None:
    dots = ""
    for i in range(1, 5):
        if i < st.session_state.current_step:
            cls, icon = "done", "✓"
        elif i == st.session_state.current_step:
            cls, icon = "active", str(i)
        else:
            cls, icon = "", str(i)
        dots += f'<div class="step-dot {cls}">{icon}</div>'
    st.markdown(f'<div class="step-indicator">{dots}</div>', unsafe_allow_html=True)


# ===========================================================================
# DIALOGUE BOX COMPONENT
# ===========================================================================
def render_dialogue(text: str) -> None:
    st.markdown(f'<div class="dialogue-box">💬 {text}</div>', unsafe_allow_html=True)


# ===========================================================================
# MAIN APP HEADER
# ===========================================================================
st.markdown('<h1>🎀 Happy Birthday, Pikku! 🎂</h1>', unsafe_allow_html=True)
render_step_indicator()

# ===========================================================================
# STEP 1: BOY WALKS IN AND TALKS
# ===========================================================================
if st.session_state.current_step == 1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 💬 Step 1: eitu jna kun eituuu tmr shona pakhi")
    safe_audio(BG_MUSIC_PATH)
    
    stage = st.session_state.step1_stage
    
    if stage == "walk":
        render_scene(pose="walk")
        render_dialogue("...")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("💬 Talk to him", use_container_width=True, key="btn_talk"):
                st.session_state.step1_stage = "talk"
                st.rerun()
    
    elif stage == "talk":
        render_scene(pose="talk")
        render_dialogue(GREETING_LINE)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Next ➡️", use_container_width=True, key="btn_step1_next"):
                st.session_state.current_step = 2
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===========================================================================
# STEP 2: POCKET PHOTO REVEAL GAME
# ===========================================================================
elif st.session_state.current_step == 2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🎁 Step 2: photo hihihi!")
    
    idx = st.session_state.step2_idx
    total = len(POCKET_PHOTOS)
    all_done = idx >= total
    
    if not all_done:
        photo = POCKET_PHOTOS[idx]
        render_scene(pose="reach", holding_photo=True)
        render_dialogue(f"Photo {idx+1} of {total}: {photo['caption']}")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if idx == 0 and not st.session_state.step2_show:
                if st.button("🎁 Pull photo from pocket", use_container_width=True, key="btn_pull"):
                    st.session_state.step2_show = True
                    st.session_state.step2_just = True
                    st.rerun()
            elif st.session_state.step2_show:
                label = "📸 Show Next Photo" if idx < total - 1 else "📸 View Final Photo"
                if st.button(label, use_container_width=True, key=f"btn_photo_{idx}"):
                    st.session_state.step2_idx += 1
                    st.session_state.step2_just = True
                    st.rerun()
        
        if st.session_state.step2_just:
            st.balloons()
            st.session_state.step2_just = False
        
        if st.session_state.step2_show:
            safe_image(photo["path"], photo["caption"])
    else:
        render_scene(pose="celebrate", show_heart=True)
        render_dialogue("usss pucki ussss! 💗")
        
        cols = st.columns(min(total, 4))
        for i, photo in enumerate(POCKET_PHOTOS):
            with cols[i % len(cols)]:
                safe_image(photo["path"], photo["caption"])
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Proceed to Next Step ➡️", use_container_width=True, key="btn_step2_next"):
                st.session_state.current_step = 3
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===========================================================================
# STEP 3: VIDEO SHOWCASE
# ===========================================================================
elif st.session_state.current_step == 3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🎬 Step 3: amiii hihi")
    
    video_cols = st.columns(2)
    labels = ["Cute Clip 1", "Cute Clip 2"]
    for col, path, label in zip(video_cols, VIDEO_PATHS, labels):
        with col:
            st.markdown(f"**{label}**")
            safe_video(path, label)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💖 Reveal Final Surprise ➡️", use_container_width=True, key="btn_step3_next"):
            st.session_state.current_step = 4
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===========================================================================
# STEP 4: GRAND FINALE - BOY & GIRL HUG & KISS
# ===========================================================================
elif st.session_state.current_step == 4:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 💕 Step 4: The Grand Finale")
    
    phase = st.session_state.step4_phase
    
    if phase == "entry":
        # Both characters walk in from opposite sides
        render_scene(pose="hug", show_girl=True, show_heart=True)
        render_dialogue("They walk toward each other... Hearts are racing! 💓")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🤗 Watch Them Hug!", use_container_width=True, key="btn_hug"):
                st.session_state.step4_phase = "hug"
                st.rerun()
    
    elif phase == "hug":
        # Hugging animation
        render_scene(pose="hug", show_girl=True, show_heart=True)
        render_dialogue("They embrace each other tightly... The warmest hug ever! 🤗")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("💋 Now Watch Them Kiss!", use_container_width=True, key="btn_kiss"):
                st.session_state.step4_phase = "kiss"
                st.rerun()
    
    elif phase == "kiss":
        # Kissing animation with hearts
        render_scene(pose="kiss", show_girl=True, show_heart=True)
        render_dialogue("Thank you for being my favorite person in the entire universe! 🎉💖")
        st.balloons()
        st.markdown(
            '<div class="glass-card" style="text-align:center;">'
            '<h2 class="glow-text">💝 Happy Birthday, Pikku! 💝</h2>'
            '<p style="font-size:18px;">'
            'Thank you for being my favorite person in the entire universe! '
            'May this year bring you endless joy and happiness. '
            'Here\'s to more beautiful memories together! 🌸✨'
            '</p>'
            '</div>',
            unsafe_allow_html=True,
        )
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎉 Celebrate Again! 🎉", use_container_width=True, key="btn_celebrate"):
                st.balloons()
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
