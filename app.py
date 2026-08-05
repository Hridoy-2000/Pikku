"""
Pikku's Birthday Web App - Complete RPG Sprite Edition
=======================================================
A guided 4-step Streamlit birthday experience featuring
authentic 2D RPG characters rendered on HTML5 Canvas at 30 FPS.
No external image assets required - everything is drawn in code.

Run with:
    streamlit run app.py

requirements.txt:
    streamlit
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
    page_title="Happy Birthday, Pikku!",
    page_icon="🎂",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# ASSET PATHS
# ---------------------------------------------------------------------------
ASSETS_DIR = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)
BG_MUSIC_PATH = os.path.join(ASSETS_DIR, "bg_music.mp3")
VIDEO_PATHS = [
    os.path.join(ASSETS_DIR, "video1.mp4"),
    os.path.join(ASSETS_DIR, "video2.mp4"),
]
POCKET_PHOTOS = [
    {"path": os.path.join(ASSETS_DIR, "memory1.jpg"), "caption": "The day we first talked"},
    {"path": os.path.join(ASSETS_DIR, "memory2.jpg"), "caption": "That silly joke you made"},
    {"path": os.path.join(ASSETS_DIR, "memory3.jpg"), "caption": "The moment I knew"},
    {"path": os.path.join(ASSETS_DIR, "memory4.jpg"), "caption": "Us, always"},
]
GREETING_LINE = "Hi. Hey, I know your birthday is coming and you are very happy for that."

# ---------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------
def safe_audio(path):
    if os.path.exists(path):
        try:
            with open(path, "rb") as f:
                audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
            st.markdown(f'<audio autoplay loop style="display:none;"><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
            st.caption("Background music is playing...")
        except:
            st.caption("Add a valid MP3 file at assets/bg_music.mp3")
    else:
        st.caption("Add your song at assets/bg_music.mp3")

def safe_video(path, label):
    if os.path.exists(path):
        try:
            st.video(path)
        except:
            st.info(f"Add a valid video at {path}")
    else:
        st.info(f"Add a clip at {path}")

def safe_image(path, caption="", use_container_width=True):
    if os.path.exists(path):
        try:
            st.image(path, caption=caption, use_container_width=use_container_width)
        except:
            st.markdown(f'<div class="glass-card" style="text-align:center;padding:30px;"><div style="font-size:64px;">🌸</div><p style="font-weight:600;font-size:18px;color:#c44569;">{caption}</p><p style="font-size:12px;color:#c98a97;">(add photo at {path})</p></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="glass-card" style="text-align:center;padding:30px;"><div style="font-size:64px;">🌸</div><p style="font-weight:600;font-size:18px;color:#c44569;">{caption}</p><p style="font-size:12px;color:#c98a97;">(add photo at {path})</p></div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# GLOBAL CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #ffdde1 0%, #ee9ca7 100%); background-attachment: fixed; }
#MainMenu, header, footer {visibility: hidden;}
h1, h2, h3, h4 { color: #a14a5c !important; text-shadow: 0 2px 6px rgba(255,255,255,0.4); }
p, span, label, li, div { color: #7a3b47; }
.glass-card { background: rgba(255,255,255,0.85); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-radius: 22px; border: 1.5px solid rgba(238,156,167,0.55); box-shadow: 0 8px 32px rgba(238,156,167,0.35); padding: 20px 24px; margin-bottom: 20px; transition: transform 0.25s ease, box-shadow 0.25s ease; }
.glass-card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(238,156,167,0.5); }
.stButton > button { background: linear-gradient(135deg, #ffb6c1 0%, #ee9ca7 100%); color: #6b2c3a; border: none; border-radius: 30px; padding: 10px 22px; font-weight: 700; box-shadow: 0 4px 14px rgba(238,156,167,0.5); transition: transform 0.15s ease; }
.stButton > button:hover { transform: scale(1.05); box-shadow: 0 6px 20px rgba(238,156,167,0.7); color: #6b2c3a; }
.stButton > button:disabled { background: #e0c0c8; color: #a08088; box-shadow: none; }
.title-banner { text-align: center; padding: 10px 0 4px 0; }
.step-indicator { display: flex; justify-content: center; gap: 10px; margin: 15px 0 25px 0; }
.step-dot { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 18px; background: rgba(255,255,255,0.5); color: #c98a97; border: 2px solid #ee9ca7; transition: all 0.3s ease; }
.step-dot.active { background: #ee9ca7; color: white; border-color: #c44569; box-shadow: 0 0 15px rgba(238,156,167,0.6); }
.step-dot.done { background: #c44569; color: white; border-color: #c44569; }
@keyframes popIn { 0% { transform: scale(0.05); opacity: 0; } 60% { transform: scale(1.08); opacity: 1; } 100% { transform: scale(1); opacity: 1; } }
.pocket-photo-new { animation: popIn 0.6s cubic-bezier(.2,.9,.3,1.3) forwards; }
@keyframes glowPulse { 0%, 100% { text-shadow: 0 0 10px rgba(255,107,157,0.3); } 50% { text-shadow: 0 0 25px rgba(255,107,157,0.7), 0 0 50px rgba(255,107,157,0.3); } }
.glow-text { animation: glowPulse 2s ease-in-out infinite; }
@media (max-width: 768px) { .step-dot { width: 30px; height: 30px; font-size: 14px; } .glass-card { padding: 14px 16px; } }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------------------------
if "current_step" not in st.session_state:
    st.session_state.current_step = 1
if "step1_stage" not in st.session_state:
    st.session_state.step1_stage = "idle"
if "step2_photo_index" not in st.session_state:
    st.session_state.step2_photo_index = 0
if "step2_showing_photo" not in st.session_state:
    st.session_state.step2_showing_photo = False
if "step2_just_switched" not in st.session_state:
    st.session_state.step2_just_switched = False
if "step4_phase" not in st.session_state:
    st.session_state.step4_phase = "entry"

# ---------------------------------------------------------------------------
# RPG SCENE HTML TEMPLATE
# ---------------------------------------------------------------------------
RPG_SCENE_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  html, body { margin: 0; padding: 0; background: transparent; overflow: hidden; font-family: 'Courier New', monospace; }
  .scene-wrap { position: relative; width: SCENE_Wpx; height: SCENE_Hpx; margin: 0 auto; border-radius: 14px; overflow: hidden; border: 3px solid #7a4a3a; box-shadow: 0 6px 18px rgba(0,0,0,0.25); background: linear-gradient(#bdeaff 0%, #bdeaff 55%, #7fc97f 55%, #7fc97f 100%); }
  .ground-strip { position: absolute; left: 0; right: 0; bottom: 0; height: 26px; background-image: repeating-linear-gradient(90deg, #6ab86a 0px, #6ab86a 8px, #5aa65a 8px, #5aa65a 16px); background-size: 32px 26px; animation: groundScroll 0.8s steps(4) infinite; opacity: 0.9; z-index: 1; }
  @keyframes groundScroll { from { background-position-x: 0px; } to { background-position-x: -32px; } }
  canvas#rpgCanvas { position: absolute; left: 50%; top: 8px; transform: translateX(-50%); image-rendering: pixelated; image-rendering: -moz-crisp-edges; image-rendering: crisp-edges; width: CANVAS_DWpx; height: CANVAS_DHpx; z-index: 2; }
  .dbox-wrap { position: absolute; left: 6px; right: 6px; bottom: 6px; display: DBOX_DISPLAY; z-index: 10; }
  .dbox { background: #fff8ec; border: 3px solid #2c2c54; border-radius: 6px; box-shadow: inset 0 0 0 2px #ffe9c7, 0 4px 10px rgba(0,0,0,0.3); padding: 8px 30px 8px 10px; min-height: 44px; font-size: 13px; line-height: 1.35; color: #2c2c54; position: relative; cursor: pointer; }
  .dbox-arrow { position: absolute; right: 10px; bottom: 6px; width: 0; height: 0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-top: 8px solid #2c2c54; animation: arrowBlink 0.6s steps(1) infinite; }
  @keyframes arrowBlink { 0%, 49% { opacity: 1; } 50%, 100% { opacity: 0; } }
  .floating-hearts { position: absolute; top: 0; left: 0; right: 0; bottom: 0; pointer-events: none; z-index: 3; }
  .heart-particle { position: absolute; font-size: 18px; animation: floatUp 2.5s ease-out forwards; pointer-events: none; }
  @keyframes floatUp { 0% { transform: translateY(0) scale(0.5); opacity: 1; } 100% { transform: translateY(-200px) scale(1.5); opacity: 0; } }
</style>
</head>
<body>
<div class="scene-wrap">
  <canvas id="rpgCanvas" width="CANVAS_W" height="CANVAS_H"></canvas>
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
var canvas = document.getElementById('rpgCanvas');
var ctx = canvas.getContext('2d');
ctx.imageSmoothingEnabled = false;
var W = canvas.width, H = canvas.height;
var GROUND_Y = H - 22;
var POSE = "POSE_VAL";
var SHOW_HEART = SHOW_HEART_VAL;
var SHOW_GIRL = SHOW_GIRL_VAL;
var HOLDING_PHOTO = HOLDING_PHOTO_VAL;
var DIALOGUE = DIALOGUE_VAL;

var C_HAIR = "#4a2c17", C_HAIR_G = "#8B4513", C_SKIN = "#ffd9b3", C_SHIRT = "#4f8ecb", C_SHIRT_DK = "#33618f";
var C_DRESS = "#FF69B4", C_DRESS_DK = "#FF1493", C_PANTS = "#333355", C_SHOE = "#22222a";
var C_EYE = "#2c2c54", C_MOUTH = "#a14a5c", C_POCKET = "#22314a", C_HEART = "#ff6f91";

var boy = { x: -20, targetX: SHOW_GIRL ? Math.round(W/2)-20 : Math.round(W/2), walking: true, legPhase: 0, armWaveT: 0, hopT: 0, mouthOpen: false, kissFrame: 0, kissing: false };
var girl = { x: W+40, targetX: Math.round(W/2)+20, walking: SHOW_GIRL, legPhase: 1, armWaveT: 0, hopT: 0, kissFrame: 0, kissing: false };
var tickCounter = 0;
var dialogueLines = DIALOGUE || [];
var currentLineIdx = 0;
var typingTimer = null;
var typingComplete = false;

function drawRect(x,y,w,h,c) { ctx.fillStyle=c; ctx.fillRect(Math.round(x),Math.round(y),w,h); }
function drawArm(sx,sy,angle,c) { ctx.save(); ctx.translate(sx,sy); ctx.rotate(angle*Math.PI/180); ctx.fillStyle=c; ctx.fillRect(-2,0,5,15); ctx.restore(); }

function drawBoy(ax,groundY,s) {
  var bob=0;
  if(POSE==="celebrate") bob=Math.sin(s.hopT)*3;
  else if(!s.walking&&POSE!=="walk") bob=Math.sin(tickCounter/12)*1.2;
  var ay=groundY+bob;
  var liftL=0,liftR=0;
  if(s.walking){ liftL=s.legPhase===0?-3:0; liftR=s.legPhase===0?0:-3; }
  else if(POSE==="celebrate"){ liftL=Math.sin(s.hopT)>0?-2:0; liftR=Math.sin(s.hopT)>0?0:-2; }
  drawRect(ax-7,ay-16+liftL,6,16,C_PANTS); drawRect(ax-7,ay-3+liftL,6,3,C_SHOE);
  drawRect(ax+1,ay-16+liftR,6,16,C_PANTS); drawRect(ax+1,ay-3+liftR,6,3,C_SHOE);
  drawRect(ax-9,ay-34,18,20,C_SHIRT); drawRect(ax-9,ay-34,18,3,C_SHIRT_DK);
  drawRect(ax+3,ay-20,5,5,C_POCKET);
  var armL=8,armR=-8;
  if(POSE==="talk") armR=-60+Math.sin(s.armWaveT)*35;
  else if(POSE==="reach") armR=70;
  else if(POSE==="celebrate"){ armL=150+Math.sin(s.hopT)*10; armR=-150-Math.sin(s.hopT)*10; }
  else if(POSE==="hug"){ armL=-55; armR=55; }
  else if(POSE==="kiss"){ armL=-50; armR=50; }
  else if(s.walking){ armL=s.legPhase===0?30:-20; armR=s.legPhase===0?-20:30; }
  drawArm(ax-9,ay-32,armL,C_SHIRT_DK); drawArm(ax+9,ay-32,armR,C_SHIRT_DK);
  if(HOLDING_PHOTO && POSE==="reach"){
    var px=ax+12, py=ay-40;
    ctx.fillStyle="#fffef5"; ctx.fillRect(px-8,py-10,16,20);
    ctx.strokeStyle="#ffb6c1"; ctx.lineWidth=1; ctx.strokeRect(px-8,py-10,16,20);
    ctx.fillStyle=C_HEART; ctx.fillRect(px-3,py-3,3,3); ctx.fillRect(px+3,py-3,3,3); ctx.fillRect(px-4,py,10,3); ctx.fillRect(px-1,py+3,5,2);
  }
  drawRect(ax-8,ay-50,16,16,C_SKIN); drawRect(ax-9,ay-54,18,6,C_HAIR);
  drawRect(ax-9,ay-50,3,10,C_HAIR); drawRect(ax+6,ay-50,3,10,C_HAIR);
  if(POSE==="kiss" && s.kissing){
    drawRect(ax-4,ay-46,2,2,C_EYE); drawRect(ax+2,ay-46,1,1,C_EYE);
    drawRect(ax-2,ay-40,4,2,C_MOUTH);
  } else {
    drawRect(ax-5,ay-42,2,2,C_EYE); drawRect(ax+3,ay-42,2,2,C_EYE);
    var mouthH=(POSE==="talk"&&s.mouthOpen)?3:1;
    drawRect(ax-3,ay-37,6,mouthH,C_MOUTH);
  }
  if(SHOW_HEART){
    var hy=ay-66-Math.sin(tickCounter/10)*4,hx=ax+12;
    ctx.fillStyle=C_HEART; ctx.fillRect(hx,hy,3,3); ctx.fillRect(hx+4,hy,3,3); ctx.fillRect(hx-1,hy+3,9,3); ctx.fillRect(hx+1,hy+6,5,2);
  }
}

function drawGirl(ax,groundY,s) {
  var bob=Math.sin(tickCounter/12)*1.5,ay=groundY+bob;
  var liftL=0,liftR=0;
  if(s.walking){ liftL=s.legPhase===0?-3:0; liftR=s.legPhase===0?0:-3; }
  drawRect(ax-5,ay-8+liftL,4,10,C_SKIN); drawRect(ax+1,ay-8+liftR,4,10,C_SKIN);
  drawRect(ax-5,ay-2+liftL,4,3,C_DRESS_DK); drawRect(ax+1,ay-2+liftR,4,3,C_DRESS_DK);
  drawRect(ax-9,ay-26,18,20,C_DRESS); drawRect(ax-9,ay-26,18,3,C_DRESS_DK);
  drawRect(ax-7,ay-38,14,14,C_DRESS); drawRect(ax-7,ay-38,14,2,C_DRESS_DK);
  var armL=8,armR=-8;
  if(POSE==="hug"){ armL=-45; armR=45; }
  else if(POSE==="kiss"){ armL=-40; armR=40; }
  else if(s.walking){ armL=s.legPhase===0?30:-20; armR=s.legPhase===0?-20:30; }
  drawArm(ax-7,ay-36,armL,C_DRESS_DK); drawArm(ax+7,ay-36,armR,C_DRESS_DK);
  drawRect(ax-8,ay-52,16,16,C_SKIN); drawRect(ax-9,ay-56,18,7,C_HAIR_G);
  drawRect(ax-9,ay-52,3,10,C_HAIR_G); drawRect(ax+6,ay-52,3,10,C_HAIR_G);
  drawRect(ax-12,ay-53,4,6,C_HAIR_G); drawRect(ax+8,ay-53,4,6,C_HAIR_G);
  if(POSE==="kiss" && s.kissing){
    drawRect(ax-3,ay-46,2,2,C_EYE); drawRect(ax+1,ay-46,1,1,C_EYE);
    drawRect(ax-2,ay-40,4,2,C_MOUTH);
  } else {
    drawRect(ax-5,ay-44,3,3,C_EYE); drawRect(ax+2,ay-44,3,3,C_EYE);
    drawRect(ax-6,ay-46,1,2,C_EYE); drawRect(ax+5,ay-46,1,2,C_EYE);
    drawRect(ax-2,ay-39,5,2,C_MOUTH);
  }
  ctx.fillStyle="rgba(255,150,150,0.4)"; ctx.fillRect(ax-7,ay-41,3,2); ctx.fillRect(ax+4,ay-41,3,2);
  if(SHOW_HEART){
    var hy=ay-68-Math.sin(tickCounter/10+1)*3,hx=ax-8;
    ctx.fillStyle=C_HEART; ctx.fillRect(hx,hy,3,3); ctx.fillRect(hx+4,hy,3,3); ctx.fillRect(hx-1,hy+3,9,3); ctx.fillRect(hx+1,hy+6,5,2);
  }
}

function spawnHeart(x,y){
  var c=document.getElementById('floatingHearts'); if(!c) return;
  var h=document.createElement('div'); h.className='heart-particle';
  h.textContent=['❤️','💕','💖','💗','💝','✨'][Math.floor(Math.random()*6)];
  h.style.left=x+'px'; h.style.top=y+'px'; c.appendChild(h);
  setTimeout(function(){ if(h.parentNode) h.parentNode.removeChild(h); },2600);
}

function tick(){
  tickCounter++; boy.armWaveT+=0.35; boy.hopT+=0.28; girl.armWaveT+=0.32; girl.hopT+=0.26;
  if(POSE==="kiss"){ boy.kissFrame++; girl.kissFrame++; if(boy.kissFrame>40){ boy.kissing=true; girl.kissing=true; } }
  if(boy.walking){ boy.x+=2.2; if(boy.x>=boy.targetX){ boy.x=boy.targetX; boy.walking=false; } if(tickCounter%4===0) boy.legPhase=1-boy.legPhase; }
  if(girl.walking){ girl.x-=1.8; if(girl.x<=girl.targetX){ girl.x=girl.targetX; girl.walking=false; } if(tickCounter%4===0) girl.legPhase=1-girl.legPhase; }
  if(POSE==="talk"&&tickCounter%5===0) boy.mouthOpen=!boy.mouthOpen;
  if((POSE==="hug"||POSE==="kiss"||POSE==="celebrate")&&tickCounter%10===0){
    var sw=document.querySelector('.scene-wrap'); if(sw){ var r=sw.getBoundingClientRect(); spawnHeart((boy.x/W)*r.width,(GROUND_Y/H)*r.height-40); spawnHeart((girl.x/W)*r.width,(GROUND_Y/H)*r.height-40); }
  }
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle="rgba(255,255,255,0.5)"; ctx.fillRect(15,10,30,8); ctx.fillRect(20,5,20,6); ctx.fillRect(W-50,18,28,7); ctx.fillRect(W-45,13,18,6);
  drawBoy(boy.x,GROUND_Y,boy); if(SHOW_GIRL) drawGirl(girl.x,GROUND_Y,girl);
}
setInterval(tick,1000/30); tick();

var textEl=document.getElementById('dboxText'),arrowEl=document.getElementById('dboxArrow'),dboxArea=document.getElementById('dboxClickArea');
function typeLine(line){
  textEl.textContent=""; arrowEl.style.display="none"; typingComplete=false; var i=0;
  if(typingTimer) clearInterval(typingTimer);
  typingTimer=setInterval(function(){ textEl.textContent+=line.charAt(i); i++; if(i>=line.length){ clearInterval(typingTimer); typingTimer=null; typingComplete=true; arrowEl.style.display="block"; } },28);
}
function advanceDialogue(){
  if(!typingComplete){ if(typingTimer) clearInterval(typingTimer); typingTimer=null; textEl.textContent=dialogueLines[currentLineIdx]; typingComplete=true; arrowEl.style.display="block"; return; }
  if(currentLineIdx<dialogueLines.length-1){ currentLineIdx++; typeLine(dialogueLines[currentLineIdx]); }
}
if(dialogueLines&&dialogueLines.length>0) typeLine(dialogueLines[0]);
if(dboxArea) dboxArea.addEventListener('click',advanceDialogue);
</script>
</body>
</html>
"""

def render_rpg_scene(pose="idle", dialogue=None, show_heart=False, show_girl=False, holding_photo=False, scene_w=420, scene_h=260, canvas_w=140, canvas_h=110, scale=3):
    if isinstance(dialogue, str):
        dialogue = [dialogue]
    html = RPG_SCENE_HTML
    html = html.replace("SCENE_W", str(scene_w))
    html = html.replace("SCENE_H", str(scene_h))
    html = html.replace("CANVAS_W", str(canvas_w))
    html = html.replace("CANVAS_H", str(canvas_h))
    html = html.replace("CANVAS_DW", str(canvas_w * scale))
    html = html.replace("CANVAS_DH", str(canvas_h * scale))
    html = html.replace("POSE_VAL", pose)
    html = html.replace("SHOW_HEART_VAL", "true" if show_heart else "false")
    html = html.replace("SHOW_GIRL_VAL", "true" if show_girl else "false")
    html = html.replace("HOLDING_PHOTO_VAL", "true" if holding_photo else "false")
    html = html.replace("DIALOGUE_VAL", json.dumps(dialogue) if dialogue else "null")
    html = html.replace("DBOX_DISPLAY", "block" if dialogue else "none")
    components.html(html, height=scene_h + 10, scrolling=False)

def render_step_indicator():
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

# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------
st.markdown('<div class="title-banner"><h1>Happy Birthday, Pikku!</h1></div>', unsafe_allow_html=True)
render_step_indicator()

# ===========================================================================
# STEP 1 - 2D Animated Boy Entrance & Greeting
# ===========================================================================
if st.session_state.current_step == 1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Step 1: A Special Visitor Arrives")
    safe_audio(BG_MUSIC_PATH)
    stage = st.session_state.step1_stage
    if stage == "idle":
        render_rpg_scene(pose="walk", dialogue=["...", "Click the button below to talk to him!"])
    elif stage == "talking":
        render_rpg_scene(pose="talk", dialogue=[GREETING_LINE])
    st.write("")
    col1, col2, col3 = st.columns([1, 2, 1])
    if stage == "idle":
        with col2:
            if st.button("Talk to him", use_container_width=True, key="btn_talk"):
                st.session_state.step1_stage = "talking"
                st.rerun()
    elif stage == "talking":
        with col2:
            if st.button("Next Step", use_container_width=True, key="btn_step1_next"):
                st.session_state.current_step = 2
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ===========================================================================
# STEP 2 - Interactive Pocket Photo Reveal
# ===========================================================================
elif st.session_state.current_step == 2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Step 2: Pocket Photo Surprise!")
    photo_index = st.session_state.step2_photo_index
    total_photos = len(POCKET_PHOTOS)
    all_shown = photo_index >= total_photos
    if not all_shown:
        current_photo = POCKET_PHOTOS[photo_index]
        render_rpg_scene(pose="reach", holding_photo=True, dialogue=[f"Photo {photo_index+1} of {total_photos}: {current_photo['caption']}"])
        st.write("")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if photo_index == 0 and not st.session_state.step2_showing_photo:
                if st.button("Pull photo from pocket", use_container_width=True, key="btn_pull_first"):
                    st.session_state.step2_showing_photo = True
                    st.session_state.step2_just_switched = True
                    st.rerun()
            elif st.session_state.step2_showing_photo:
                if st.button("Show Next Photo" if photo_index < total_photos - 1 else "View Final Photo", use_container_width=True, key=f"btn_next_photo_{photo_index}"):
                    st.session_state.step2_photo_index += 1
                    st.session_state.step2_just_switched = True
                    st.rerun()
        if st.session_state.step2_just_switched:
            st.balloons()
            st.session_state.step2_just_switched = False
        if st.session_state.step2_showing_photo:
            st.write("")
            st.markdown(f"#### Photo {photo_index+1}: {current_photo['caption']}")
            safe_image(current_photo["path"], current_photo["caption"])
    else:
        render_rpg_scene(pose="celebrate", show_heart=True, dialogue=["That is all the memories in his pocket!", "What a beautiful collection!"])
        st.write("")
        st.markdown("#### All Photos Shown!")
        cols = st.columns(min(total_photos, 4))
        for i, photo in enumerate(POCKET_PHOTOS):
            with cols[i % len(cols)]:
                safe_image(photo["path"], photo["caption"])
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Proceed to Next Step", use_container_width=True, key="btn_step2_next"):
                st.session_state.current_step = 3
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ===========================================================================
# STEP 3 - Cute Video Showcase
# ===========================================================================
elif st.session_state.current_step == 3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Step 3: Cute Videos")
    vid_cols = st.columns(2)
    labels = ["Cute Clip 1", "Cute Clip 2"]
    for col, path, label in zip(vid_cols, VIDEO_PATHS, labels):
        with col:
            st.markdown(f"**{label}**")
            safe_video(path, label)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Reveal Final Surprise", use_container_width=True, key="btn_step3_next"):
            st.session_state.current_step = 4
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ===========================================================================
# STEP 4 - FINAL FINALE (Boy & Girl Hug & Kiss)
# ===========================================================================
elif st.session_state.current_step == 4:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Step 4: The Grand Finale")
    phase = st.session_state.step4_phase
    if phase == "entry":
        render_rpg_scene(pose="hug", show_heart=True, show_girl=True, dialogue=["They walk toward each other from across the screen...", "Their hearts are racing!"], scene_w=500, canvas_w=180)
        st.write("")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Watch Them Hug!", use_container_width=True, key="btn_hug"):
                st.session_state.step4_phase = "hug"
                st.rerun()
    elif phase == "hug":
        render_rpg_scene(pose="hug", show_heart=True, show_girl=True, dialogue=["They embrace each other tightly...", "This is the warmest hug ever!"], scene_w=500, canvas_w=180)
        st.write("")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Now Watch Them Kiss!", use_container_width=True, key="btn_kiss"):
                st.session_state.step4_phase = "kiss"
                st.rerun()
    elif phase == "kiss":
        render_rpg_scene(pose="kiss", show_heart=True, show_girl=True, dialogue=["Thank you for being my favorite person in the entire universe!", "Happy Birthday
