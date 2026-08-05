Here's the **COMPLETE, SUPER PROFESSIONAL** `app.py` with all animations, both characters, and full comments:

```python
"""
╔══════════════════════════════════════════════════════════════╗
║           PIKKU'S BIRTHDAY WEB APP v2.0                      ║
║           Professional 2D RPG Animation Engine               ║
║           Streamlit + HTML5 Canvas + 30 FPS Game Loop        ║
╚══════════════════════════════════════════════════════════════╝

Author: Birthday App Team
Version: 2.0.0
Description: A guided 4-step interactive birthday experience
             featuring hand-coded 2D RPG character animations
             rendered on HTML5 Canvas at 30 FPS.

Features:
  • Step 1: Boy character walks in and talks
  • Step 2: Interactive pocket photo reveal game
  • Step 3: Video showcase gallery
  • Step 4: Boy & Girl couple finale (hug + kiss)
  
Architecture:
  • Frontend: Streamlit (Python)
  • Animation: HTML5 Canvas (JavaScript)
  • Game Loop: 30 FPS requestAnimationFrame-style interval
  • Assets: All characters are code-drawn (no external images)
"""

# ===========================================================================
# STANDARD LIBRARY IMPORTS
# ===========================================================================
import os
import json
import base64
from typing import Optional, List, Dict, Any

# ===========================================================================
# THIRD-PARTY IMPORTS
# ===========================================================================
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
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "A special birthday surprise for Pikku! 💝",
    },
)

# ===========================================================================
# CONSTANTS & CONFIGURATION
# ===========================================================================

# Asset directory - create if doesn't exist
ASSETS_DIR: str = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

# File paths for optional media
BG_MUSIC_PATH: str = os.path.join(ASSETS_DIR, "bg_music.mp3")
VIDEO_PATHS: List[str] = [
    os.path.join(ASSETS_DIR, "video1.mp4"),
    os.path.join(ASSETS_DIR, "video2.mp4"),
]

# Memory photos configuration
POCKET_PHOTOS: List[Dict[str, str]] = [
    {"path": os.path.join(ASSETS_DIR, "memory1.jpg"), "caption": "The day we first talked 💌"},
    {"path": os.path.join(ASSETS_DIR, "memory2.jpg"), "caption": "That silly joke you made 😂"},
    {"path": os.path.join(ASSETS_DIR, "memory3.jpg"), "caption": "The moment I knew 💗"},
    {"path": os.path.join(ASSETS_DIR, "memory4.jpg"), "caption": "Us, always 🌸"},
]

# Dialogue constants
GREETING_LINE: str = (
    "Hi. Hey, I know your birthday is coming "
    "and you are very happy for that."
)

FINAL_MESSAGE: str = (
    "Thank you for being my favorite person "
    "in the entire universe! Happy Birthday! 🎉💖"
)

# Canvas dimensions
CANVAS_WIDTH: int = 420
CANVAS_HEIGHT: int = 260
SCENE_HEIGHT: int = 280  # Component height in Streamlit


# ===========================================================================
# UTILITY FUNCTIONS
# ===========================================================================

def safe_audio(path: str) -> None:
    """
    Safely load and play background music.
    Falls back gracefully if file doesn't exist or is invalid.
    """
    if os.path.exists(path):
        try:
            with open(path, "rb") as f:
                audio_base64: str = base64.b64encode(f.read()).decode()
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
            st.caption("🎵 Add a valid MP3 file to assets/bg_music.mp3")
    else:
        st.caption("🎵 Place your music at assets/bg_music.mp3")


def safe_video(path: str, label: str) -> None:
    """
    Safely load and display a video file.
    Shows an info message if the file is missing or invalid.
    """
    if os.path.exists(path):
        try:
            st.video(path)
        except Exception:
            st.info(f"📹 Add a valid video file at: {path}")
    else:
        st.info(f"📹 Place your video at: {path}")


def safe_image(
    path: str,
    caption: str = "",
    use_container_width: bool = True
) -> None:
    """
    Safely load and display an image file.
    Renders a beautiful placeholder card if the image is missing.
    """
    if os.path.exists(path):
        try:
            st.image(
                path,
                caption=caption,
                use_container_width=use_container_width,
            )
        except Exception:
            _render_image_placeholder(caption)
    else:
        _render_image_placeholder(caption)


def _render_image_placeholder(caption: str) -> None:
    """Render a decorative placeholder when an image is missing."""
    st.markdown(
        f"""
        <div style="
            text-align:center;
            padding:30px;
            background:rgba(255,255,255,0.9);
            border-radius:20px;
            border:2px dashed #ffb6c1;
        ">
            <div style="font-size:64px;">🌸</div>
            <p style="font-weight:600;font-size:16px;color:#c44569;">
                {caption}
            </p>
            <p style="font-size:12px;color:#c98a97;">
                📸 Add your photo to the assets folder
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ===========================================================================
# GLOBAL STYLESHEET
# ===========================================================================
st.markdown("""
<style>
    /* ===== GLOBAL BACKGROUND ===== */
    .stApp {
        background: linear-gradient(135deg, #ffdde1 0%, #ee9ca7 100%);
        background-attachment: fixed;
    }
    
    /* ===== HIDE STREAMLIT BRANDING ===== */
    #MainMenu, header, footer {
        visibility: hidden;
    }
    
    /* ===== TYPOGRAPHY ===== */
    h1, h2, h3, h4 {
        color: #a14a5c !important;
        text-align: center;
        text-shadow: 0 2px 6px rgba(255,255,255,0.4);
    }
    
    p, span, label, div {
        color: #7a3b47;
    }
    
    /* ===== GLASSMORPHISM CARDS ===== */
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
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, #ffb6c1 0%, #ee9ca7 100%);
        color: #6b2c3a;
        border: none;
        border-radius: 30px;
        padding: 12px 24px;
        font-weight: 700;
        font-size: 16px;
        width: 100%;
        cursor: pointer;
        box-shadow: 0 4px 14px rgba(238, 156, 167, 0.5);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(238, 156, 167, 0.7);
    }
    
    .stButton > button:active {
        transform: scale(0.98);
    }
    
    /* ===== STEP INDICATOR DOTS ===== */
    .step-indicator {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin: 20px 0 30px 0;
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
        background: rgba(255, 255, 255, 0.5);
        color: #c98a97;
        border: 2px solid #ee9ca7;
        transition: all 0.3s ease;
    }
    
    .step-dot.active {
        background: #ee9ca7;
        color: white;
        border-color: #c44569;
        box-shadow: 0 0 20px rgba(238, 156, 167, 0.6);
        animation: pulse 2s infinite;
    }
    
    .step-dot.done {
        background: #c44569;
        color: white;
        border-color: #c44569;
    }
    
    /* ===== RPG DIALOGUE BOX ===== */
    .dialogue-box {
        background: #fff8ec;
        border: 3px solid #2c2c54;
        border-radius: 10px;
        padding: 12px 16px;
        text-align: center;
        margin-top: 8px;
        font-family: 'Courier New', monospace;
        font-size: 15px;
        color: #2c2c54;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        position: relative;
    }
    
    .dialogue-box::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 0;
        height: 0;
        border-left: 10px solid transparent;
        border-right: 10px solid transparent;
        border-top: 10px solid #2c2c54;
    }
    
    /* ===== ANIMATIONS ===== */
    @keyframes pulse {
        0%, 100% {
            box-shadow: 0 0 20px rgba(238, 156, 167, 0.6);
        }
        50% {
            box-shadow: 0 0 35px rgba(238, 156, 167, 0.9);
        }
    }
    
    @keyframes glowPulse {
        0%, 100% {
            text-shadow: 0 0 10px rgba(255, 107, 157, 0.3);
        }
        50% {
            text-shadow: 0 0 30px rgba(255, 107, 157, 0.8),
                         0 0 60px rgba(255, 107, 157, 0.4);
        }
    }
    
    @keyframes popIn {
        0% {
            transform: scale(0.05);
            opacity: 0;
        }
        60% {
            transform: scale(1.05);
            opacity: 1;
        }
        100% {
            transform: scale(1);
            opacity: 1;
        }
    }
    
    .glow-text {
        animation: glowPulse 2s ease-in-out infinite;
    }
    
    .photo-reveal {
        animation: popIn 0.6s cubic-bezier(0.2, 0.9, 0.3, 1.3) forwards;
    }
    
    /* ===== RESPONSIVE DESIGN ===== */
    @media (max-width: 768px) {
        .step-dot {
            width: 32px;
            height: 32px;
            font-size: 14px;
        }
        .glass-card {
            padding: 14px 16px;
        }
        .stButton > button {
            font-size: 14px;
            padding: 10px 18px;
        }
    }
</style>
""", unsafe_allow_html=True)


# ===========================================================================
# SESSION STATE MANAGEMENT
# ===========================================================================

def initialize_session_state() -> None:
    """
    Initialize all session state variables for guided step-by-step flow.
    Uses st.session_state to track progression through 4 steps.
    """
    defaults: Dict[str, Any] = {
        "current_step": 1,          # Tracks which step (1-4) user is on
        "step1_stage": "walk",      # Step 1: walk -> talk
        "step2_idx": 0,             # Step 2: which photo index
        "step2_show": False,        # Step 2: are photos revealed?
        "step2_just": False,        # Step 2: just revealed (triggers balloons)
        "step4_phase": "entry",     # Step 4: entry -> hug -> kiss
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


initialize_session_state()


# ===========================================================================
# ANIMATION ENGINE - HTML5 Canvas Renderer
# ===========================================================================

def render_scene(
    pose: str = "idle",
    show_girl: bool = False,
    show_heart: bool = False,
    holding_photo: bool = False,
) -> None:
    """
    Render the 2D RPG animation scene inside an HTML5 Canvas.
    
    This is the core animation engine. It generates a complete HTML document
    with embedded JavaScript that draws characters pixel-by-pixel on a canvas
    at 30 frames per second.
    
    Args:
        pose: Character pose - "walk", "talk", "reach", "celebrate", "hug", "kiss"
        show_girl: Whether to display the girl character alongside the boy
        show_heart: Whether to show floating heart animations
        holding_photo: Whether the boy is holding a photo in his hand
    """
    
    # Build the complete HTML document
    html_content: str = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RPG Scene</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            background: transparent;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow: hidden;
        }}
        
        canvas {{
            border: 3px solid #7a4a3a;
            border-radius: 16px;
            display: block;
            box-shadow:
                0 8px 32px rgba(0, 0, 0, 0.3),
                0 0 0 1px rgba(255, 255, 255, 0.1) inset;
        }}
    </style>
</head>
<body>
    <canvas id="gameCanvas" width="{CANVAS_WIDTH}" height="{CANVAS_HEIGHT}"></canvas>
    
    <script>
    (function() {{
        'use strict';
        
        // ================================================================
        // CANVAS SETUP
        // ================================================================
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        
        // Disable image smoothing for crisp pixel art
        ctx.imageSmoothingEnabled = false;
        
        // Canvas dimensions
        const W = {CANVAS_WIDTH};
        const H = {CANVAS_HEIGHT};
        const GROUND_Y = H - 22;  // Ground level (22px from bottom)
        
        // ================================================================
        // SCENE CONFIGURATION (passed from Python)
        // ================================================================
        const POSE = '{pose}';
        const SHOW_HEART = {str(show_heart).lower()};
        const SHOW_GIRL = {str(show_girl).lower()};
        const HOLDING_PHOTO = {str(holding_photo).lower()};
        
        // ================================================================
        // COLOR PALETTE
        // ================================================================
        const COLORS = {{
            hair:       '#4a2c17',
            hairGirl:   '#8B4513',
            skin:       '#ffd9b3',
            skinLight:  '#ffe8cc',
            shirt:      '#4f8ecb',
            shirtDark:  '#33618f',
            dress:      '#FF69B4',
            dressDark:  '#FF1493',
            pants:      '#333355',
            shoe:       '#22222a',
            eye:        '#2c2c54',
            mouth:      '#a14a5c',
            pocket:     '#1a2538',
            heart:      '#ff6f91',
            photoBg:    '#fffef5',
            photoBorder:'#ffb6c1',
            shadow:     'rgba(0, 0, 0, 0.2)',
            cloud:      'rgba(255, 255, 255, 0.8)',
            cloudFar:   'rgba(255, 255, 255, 0.5)',
            sky:        '#c8e6ff',
            grass:      '#7fc97f',
        }};
        
        // ================================================================
        // CHARACTER STATE
        // ================================================================
        
        // Boy character - walks in from LEFT side
        const boy = {{
            x: -40,                    // Start off-screen left
            targetX: SHOW_GIRL ? 180 : 210,  // Center position
            y: GROUND_Y,
            walking: true,             // Start walking immediately
            legPhase: 0,               // 0 = left forward, 1 = right forward
            armWaveTimer: 0,           // For talking arm wave
            hopTimer: 0,               // For celebrate bounce
            mouthOpen: false,          // Toggles for talking animation
            kissFrame: 0,              // Counts frames for kiss animation
            isKissing: false,          // True when kiss animation active
        }};
        
        // Girl character - walks in from RIGHT side (only in Step 4 finale)
        const girl = {{
            x: 460,                    // Start off-screen right
            targetX: 240,              // Center-right position
            y: GROUND_Y,
            walking: SHOW_GIRL,        // Only walk if girl is visible
            legPhase: 1,               // Opposite phase to boy
            armWaveTimer: 0,
            hopTimer: 0,
            kissFrame: 0,
            isKissing: false,
        }};
        
        // Global animation counter
        let tickCount = 0;
        
        // ================================================================
        // DRAWING PRIMITIVES
        // ================================================================
        
        /**
         * Draw a filled rectangle at integer coordinates.
         * All positions are rounded for crisp pixel art.
         */
        function drawRect(x, y, w, h, color) {{
            ctx.fillStyle = color;
            ctx.fillRect(Math.round(x), Math.round(y), w, h);
        }}
        
        /**
         * Draw an arm segment at a given angle.
         * The arm rotates around its shoulder joint.
         */
        function drawArm(shoulderX, shoulderY, angleDeg, color) {{
            ctx.save();
            ctx.translate(shoulderX, shoulderY);
            ctx.rotate(angleDeg * Math.PI / 180);
            ctx.fillStyle = color;
            ctx.fillRect(-2, 0, 5, 15);
            ctx.restore();
        }}
        
        /**
         * Draw an elliptical shadow on the ground beneath a character.
         */
        function drawShadow(centerX, groundY) {{
            ctx.fillStyle = COLORS.shadow;
            ctx.beginPath();
            ctx.ellipse(centerX, groundY + 18, 12, 4, 0, 0, Math.PI * 2);
            ctx.fill();
        }}
        
        // ================================================================
        // BOY CHARACTER DRAWING
        // ================================================================
        
        /**
         * Draw the complete boy character at the given position.
         * This is the main character - a cute chibi-style RPG sprite.
         */
        function drawBoy(anchorX, groundY, state) {{
            // ---- Calculate bobbing animation ----
            let bobOffset = 0;
            if (POSE === 'celebrate') {{
                bobOffset = Math.sin(state.hopTimer) * 5;
            }} else if (!state.walking && POSE !== 'walk') {{
                bobOffset = Math.sin(tickCount / 6) * 1.8;
            }}
            const footY = groundY + bobOffset;
            
            // ---- Draw shadow ----
            drawShadow(anchorX, footY);
            
            // ---- Legs with walking animation ----
            let leftLift = 0, rightLift = 0;
            if (state.walking) {{
                // Alternating leg lift creates walking motion
                leftLift = state.legPhase ? -5 : 0;
                rightLift = state.legPhase ? 0 : -5;
            }} else if (POSE === 'celebrate') {{
                leftLift = Math.sin(state.hopTimer) > 0 ? -3 : 0;
                rightLift = Math.sin(state.hopTimer) > 0 ? 0 : -3;
            }}
            
            // Left leg
            drawRect(anchorX - 7, footY - 16 + leftLift, 6, 16, COLORS.pants);
            drawRect(anchorX - 7, footY - 1 + leftLift, 6, 4, COLORS.shoe);
            
            // Right leg
            drawRect(anchorX + 1, footY - 16 + rightLift, 6, 16, COLORS.pants);
            drawRect(anchorX + 1, footY - 1 + rightLift, 6, 4, COLORS.shoe);
            
            // ---- Body (blue shirt) ----
            drawRect(anchorX - 9, footY - 34, 18, 20, COLORS.shirt);
            drawRect(anchorX - 9, footY - 34, 18, 3, COLORS.shirtDark);  // Collar
            
            // ---- Pocket on shirt ----
            drawRect(anchorX + 3, footY - 20, 5, 5, COLORS.pocket);
            
            // ---- Arms with pose-based animation ----
            let leftArmAngle = 8, rightArmAngle = -8;  // Default: arms at sides
            
            switch (POSE) {{
                case 'talk':
                    // Right arm waves while talking
                    rightArmAngle = -60 + Math.sin(state.armWaveTimer) * 40;
                    break;
                case 'reach':
                    // Right arm reaches toward pocket
                    rightArmAngle = 75;
                    break;
                case 'celebrate':
                    // Both arms up in celebration
                    leftArmAngle = 150 + Math.sin(state.hopTimer) * 15;
                    rightArmAngle = -150 - Math.sin(state.hopTimer) * 15;
                    break;
                case 'hug':
                    // Arms wide open for hug
                    leftArmAngle = -55;
                    rightArmAngle = 55;
                    break;
                case 'kiss':
                    // Arms ready for kiss
                    leftArmAngle = -50;
                    rightArmAngle = 50;
                    break;
                default:
                    if (state.walking) {{
                        // Arms swing while walking
                        leftArmAngle = state.legPhase ? 30 : -20;
                        rightArmAngle = state.legPhase ? -20 : 30;
                    }}
            }}
            
            drawArm(anchorX - 9, footY - 32, leftArmAngle, COLORS.shirtDark);
            drawArm(anchorX + 9, footY - 32, rightArmAngle, COLORS.shirtDark);
            
            // ---- Photo in hand (Step 2 pocket reveal) ----
            if (HOLDING_PHOTO && POSE === 'reach') {{
                const photoX = anchorX + 14;
                const photoY = footY - 38;
                
                // Photo paper
                drawRect(photoX - 8, photoY - 10, 16, 20, COLORS.photoBg);
                
                // Photo border
                ctx.strokeStyle = COLORS.photoBorder;
                ctx.lineWidth = 1;
                ctx.strokeRect(photoX - 8, photoY - 10, 16, 20);
                
                // Heart decoration on photo
                drawRect(photoX - 4, photoY - 4, 3, 3, COLORS.heart);
                drawRect(photoX + 3, photoY - 4, 3, 3, COLORS.heart);
                drawRect(photoX - 4, photoY, 10, 3, COLORS.heart);
            }}
            
            // ---- Head ----
            drawRect(anchorX - 8, footY - 50, 16, 16, COLORS.skin);
            
            // ---- Hair ----
            drawRect(anchorX - 9, footY - 54, 18, 6, COLORS.hair);
            drawRect(anchorX - 9, footY - 50, 3, 10, COLORS.hair);
            drawRect(anchorX + 6, footY - 50, 3, 10, COLORS.hair);
            
            // ---- Face (eyes and mouth) ----
            if (POSE === 'kiss' && state.isKissing) {{
                // Kissing face: eyes closed, puckered lips
                drawRect(anchorX - 4, footY - 42, 2, 2, COLORS.eye);
                drawRect(anchorX + 2, footY - 42, 1, 1, COLORS.eye);
                drawRect(anchorX - 2, footY - 36, 4, 2, COLORS.mouth);
            }} else {{
                // Normal face: open eyes
                drawRect(anchorX - 5, footY - 42, 2, 2, COLORS.eye);
                drawRect(anchorX + 3, footY - 42, 2, 2, COLORS.eye);
                
                // Mouth (opens when talking)
                const mouthHeight = (POSE === 'talk' && state.mouthOpen) ? 3 : 1;
                drawRect(anchorX - 3, footY - 37, 6, mouthHeight, COLORS.mouth);
            }}
            
            // ---- Floating heart above head ----
            if (SHOW_HEART) {{
                const heartX = anchorX + 12;
                const heartY = footY - 66 - Math.sin(tickCount / 5) * 6;
                
                drawRect(heartX, heartY, 3, 3, COLORS.heart);
                drawRect(heartX + 4, heartY, 3, 3, COLORS.heart);
                drawRect(heartX - 1, heartY + 3, 9, 3, COLORS.heart);
                drawRect(heartX + 1, heartY + 6, 5, 2, COLORS.heart);
            }}
        }}
        
        // ================================================================
        // GIRL CHARACTER DRAWING
        // ================================================================
        
        /**
         * Draw the complete girl character at the given position.
         * She appears in Step 4 for the hug and kiss finale.
         */
        function drawGirl(anchorX, groundY, state) {{
            // Bobbing animation (slightly different timing than boy)
            const bobOffset = Math.sin(tickCount / 6) * 1.8;
            const footY = groundY + bobOffset;
            
            // Shadow
            drawShadow(anchorX, footY);
            
            // ---- Legs ----
            let leftLift = 0, rightLift = 0;
            if (state.walking) {{
                leftLift = state.legPhase ? -5 : 0;
                rightLift = state.legPhase ? 0 : -5;
            }}
            
            drawRect(anchorX - 5, footY - 8 + leftLift, 4, 10, COLORS.skin);
            drawRect(anchorX + 1, footY - 8 + rightLift, 4, 10, COLORS.skin);
            drawRect(anchorX - 5, footY + 0, 4, 3, COLORS.dressDark);
            drawRect(anchorX + 1, footY + 0, 4, 3, COLORS.dressDark);
            
            // ---- Dress ----
            drawRect(anchorX - 9, footY - 26, 18, 20, COLORS.dress);
            drawRect(anchorX - 9, footY - 26, 18, 3, COLORS.dressDark);
            
            // ---- Torso ----
            drawRect(anchorX - 7, footY - 38, 14, 14, COLORS.dress);
            
            // ---- Arms ----
            let leftArmAngle = 8, rightArmAngle = -8;
            
            if (POSE === 'hug') {{
                leftArmAngle = -45;
                rightArmAngle = 45;
            }} else if (POSE === 'kiss') {{
                leftArmAngle = -40;
                rightArmAngle = 40;
            }} else if (state.walking) {{
                leftArmAngle = state.legPhase ? 30 : -20;
                rightArmAngle = state.legPhase ? -20 : 30;
            }}
            
            drawArm(anchorX - 7, footY - 36, leftArmAngle, COLORS.dressDark);
            drawArm(anchorX + 7, footY - 36, rightArmAngle, COLORS.dressDark);
            
            // ---- Head ----
            drawRect(anchorX - 8, footY - 52, 16, 16, COLORS.skin);
            
            // ---- Hair (longer with ponytails) ----
            drawRect(anchorX - 9, footY - 56, 18, 7, COLORS.hairGirl);
            drawRect(anchorX - 9, footY - 52, 3, 10, COLORS.hairGirl);
            drawRect(anchorX + 6, footY - 52, 3, 10, COLORS.hairGirl);
            
            // Ponytails on sides
            drawRect(anchorX - 10, footY - 53, 4, 5, COLORS.hairGirl);
            drawRect(anchorX + 6, footY - 53, 4, 5, COLORS.hairGirl);
            
            // ---- Face ----
            if (POSE === 'kiss' && state.isKissing) {{
                // Kissing face
                drawRect(anchorX - 3, footY - 44, 2, 2, COLORS.eye);
                drawRect(anchorX + 1, footY - 44, 1, 1, COLORS.eye);
                drawRect(anchorX - 2, footY - 38, 4, 2, COLORS.mouth);
            }} else {{
                // Normal face with blush
                drawRect(anchorX - 5, footY - 44, 3, 3, COLORS.eye);
                drawRect(anchorX + 2, footY - 44, 3, 3, COLORS.eye);
                drawRect(anchorX - 2, footY - 39, 5, 2, COLORS.mouth);
                
                // Blush cheeks
                ctx.fillStyle = 'rgba(255, 150, 150, 0.4)';
                ctx.fillRect(anchorX - 7, footY - 41, 3, 2);
                ctx.fillRect(anchorX + 4, footY - 41, 3, 2);
            }}
            
            // ---- Floating heart ----
            if (SHOW_HEART) {{
                const heartX = anchorX - 8;
                const heartY = footY - 68 - Math.sin(tickCount / 5 + 1) * 5;
                
                drawRect(heartX, heartY, 3, 3, COLORS.heart);
                drawRect(heartX + 4, heartY, 3, 3, COLORS.heart);
                drawRect(heartX - 1, heartY + 3, 9, 3, COLORS.heart);
                drawRect(heartX + 1, heartY + 6, 5, 2, COLORS.heart);
            }}
        }}
        
        // ================================================================
        // BACKGROUND DRAWING
        // ================================================================
        
        /**
         * Draw the complete background: sky, clouds, and grass.
         */
        function drawBackground() {{
            // Clear canvas
            ctx.clearRect(0, 0, W, H);
            
            // Sky gradient
            const skyGradient = ctx.createLinearGradient(0, 0, 0, H * 0.55);
            skyGradient.addColorStop(0, '#d4eeff');
            skyGradient.addColorStop(1, COLORS.sky);
            ctx.fillStyle = skyGradient;
            ctx.fillRect(0, 0, W, H * 0.55);
            
            // Clouds (near)
            ctx.fillStyle = COLORS.cloud;
            ctx.fillRect(15, 8, 35, 9);
            ctx.fillRect(25, 4, 25, 7);
            
            // Clouds (far)
            ctx.fillStyle = COLORS.cloudFar;
            ctx.fillRect(W - 55, 12, 30, 7);
            
            // Grass
            const grassGradient = ctx.createLinearGradient(0, H * 0.55, 0, H);
            grassGradient.addColorStop(0, COLORS.grass);
            grassGradient.addColorStop(1, '#5a9e5a');
            ctx.fillStyle = grassGradient;
            ctx.fillRect(0, H * 0.55, W, H * 0.45);
        }}
        
        // ================================================================
        // MAIN GAME LOOP - 30 FPS
        // ================================================================
        
        /**
         * Main animation loop. Called 30 times per second.
         * Updates character positions and redraws the scene.
         */
        function gameLoop() {{
            tickCount++;
            
            // Update animation timers
            boy.armWaveTimer += 0.4;
            boy.hopTimer += 0.3;
            girl.armWaveTimer += 0.35;
            girl.hopTimer += 0.28;
            
            // ---- Kiss animation ----
            if (POSE === 'kiss') {{
                boy.kissFrame++;
                girl.kissFrame++;
                // After 50 frames (~1.7 seconds), characters start kissing
                if
                
