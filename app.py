"""
Pikku's Birthday Web App - Complete RPG Sprite Edition
A guided 5-step Streamlit birthday experience with 2D RPG characters
"""

import os
import json
import base64
import streamlit as st
import streamlit.components.v1 as components

# Page config
st.set_page_config(
    page_title="Happy Birthday, Pikku!",
    page_icon="🎂",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Asset paths
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

# Helper functions
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
            st.markdown(f'<div class="glass-card" style="text-align:center;padding:30px;"><div style="font-size:64px;">🌸</div><p style="font-weight:600;font-size:18px;color:#c44569;">{caption}</p></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="glass-card" style="text-align:center;padding:30px;"><div style="font-size:64px;">🌸</div><p style="font-weight:600;font-size:18px;color:#c44569;">{caption}</p></div>', unsafe_allow_html=True)

# Global CSS
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #ffdde1 0%, #ee9ca7 100%); background-attachment: fixed; }
#MainMenu, header, footer {visibility: hidden;}
h1, h2, h3, h4 { color: #a14a5c !important; text-shadow: 0 2px 6px rgba(255,255,255,0.4); }
p, span, label, li, div { color: #7a3b47; }
.glass-card { background: rgba(255,255,255,0.85); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-radius: 22px; border: 1.5px solid rgba(238,156,167,0.55); box-shadow: 0 8px 32px rgba(238,156,167,0.35); padding: 20px 24px; margin-bottom: 20px; }
.stButton > button { background: linear-gradient(135deg, #ffb6c1 0%, #ee9ca7 100%); color: #6b2c3a; border: none; border-radius: 30px; padding: 10px 22px; font-weight: 700; box-shadow: 0 4px 14px rgba(238,156,167,0.5); }
.stButton > button:hover { transform: scale(1.05); }
.title-banner { text-align: center; padding: 10px 0; }
.step-indicator { display: flex; justify-content: center; gap: 10px; margin: 15px 0 25px 0; }
.step-dot { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 18px; background: rgba(255,255,255,0.5); color: #c98a97; border: 2px solid #ee9ca7; }
.step-dot.active { background: #ee9ca7; color: white; border-color: #c44569; box-shadow: 0 0 15px rgba(238,156,167,0.6); }
.step-dot.done { background: #c44569; color: white; border-color: #c44569; }
@keyframes popIn { 0% { transform: scale(0.05); opacity: 0; } 60% { transform: scale(1.08); opacity: 1; } 100% { transform: scale(1); opacity: 1; } }
.pocket-photo-new { animation: popIn 0.6s cubic-bezier(.2,.9,.3,1.3) forwards; }
@keyframes glowPulse { 0%, 100% { text-shadow: 0 0 10px rgba(255,107,157,0.3); } 50% { text-shadow: 0 0 25px rgba(255,107,157,0.7); } }
.glow-text { animation: glowPulse 2s ease-in-out infinite; }
</style>
""", unsafe_allow_html=True)

# Session state
if "current_step" not in st.session_state:
    st.session_state.current_step = 1
if "step1_stage" not in st.session_state:
    st.session_state.step1_stage = "idle"
if "step3_pocket_revealed" not in st.session_state:
    st.session_state.step3_pocket_revealed = []
if "step3_just_revealed" not in st.session_state:
    st.session_state.step3_just_revealed = False
if "step5_phase" not in st.session_state:
    st.session_state.step5_phase = "entry"

# RPG Scene HTML Template
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
  canvas#rpgCanvas { position: absolute; left: 50%; top: 8px; transform: translateX(-50%); image-rendering: pixelated; width: CANVAS_DWpx; height: CANVAS_DHpx; z-index: 2; }
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
var DIALOGUE = DIALOGUE_VAL;

var boy = { x: -20, targetX: SHOW_GIRL ? Math.round(W/2)-20 : Math.round(W/2), walking: true, legPhase: 0, armWaveT: 0, hopT: 0, mouthOpen: false, pocketItemY: 0, pocketItemScale: 0, pocketRevealing: false };
var girl = { x: W+40, targetX: Math.round(W/2)+20, walking: SHOW_GIRL, legPhase: 1, armWaveT: 0, hopT: 0 };
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
  drawRect(ax-7,ay-16+liftL,6,16,"#333355"); drawRect(ax-7,ay-3+liftL,6,3,"#22222a");
  drawRect(ax+1,ay-16+liftR,6,16,"#333355"); drawRect(ax+1,ay-3+liftR,6,3,"#22222a");
  drawRect(ax-9,ay-34,18,20,"#4f8ecb"); drawRect(ax-9,ay-34,18,3,"#33618f");
  drawRect(ax+3,ay-20,5,5,"#22314a");
  var armL=8,armR=-8;
  if(POSE==="talk") armR=-60+Math.sin(s.armWaveT)*35;
  else if(POSE==="reach") armR=70;
  else if(POSE==="celebrate"){ armL=150+Math.sin(s.hopT)*10; armR=-150-Math.sin(s.hopT)*10; }
  else if(POSE==="hug"){ armL=-60; armR=60; }
  else if(s.walking){ armL=s.legPhase===0?30:-20; armR=s.legPhase===0?-20:30; }
  drawArm(ax-9,ay-32,armL,"#33618f"); drawArm(ax+9,ay-32,armR,"#33618f");
  drawRect(ax-8,ay-50,16,16,"#ffd9b3"); drawRect(ax-9,ay-54,18,6,"#4a2c17");
  drawRect(ax-9,ay-50,3,10,"#4a2c17"); drawRect(ax+6,ay-50,3,10,"#4a2c17");
  drawRect(ax-5,ay-42,2,2,"#2c2c54"); drawRect(ax+3,ay-42,2,2,"#2c2c54");
  var mouthH=(POSE==="talk"&&s.mouthOpen)?3:1;
  drawRect(ax-3,ay-37,6,mouthH,"#a14a5c");
  if(s.pocketRevealing){
    var ix=ax+8,iy=ay-22-s.pocketItemY,sc=s.pocketItemScale;
    ctx.save(); ctx.translate(ix,iy); ctx.scale(sc,sc);
    ctx.fillStyle="#fffef5"; ctx.fillRect(-6,-8,12,16);
    ctx.strokeStyle="#ffb6c1"; ctx.lineWidth=1; ctx.strokeRect(-6,-8,12,16);
    ctx.fillStyle="#ff6f91"; ctx.fillRect(-2,-2,2,2); ctx.fillRect(2,-2,2,2); ctx.fillRect(-3,0,8,2); ctx.fillRect(-1,2,4,1);
    ctx.restore();
  }
  if(SHOW_HEART){
    var hy=ay-66-Math.sin(tickCounter/10)*4,hx=ax+12;
    ctx.fillStyle="#ff6f91"; ctx.fillRect(hx,hy,3,3); ctx.fillRect(hx+4,hy,3,3); ctx.fillRect(hx-1,hy+3,9,3); ctx.fillRect(hx+1,hy+6,5,2);
  }
}

function drawGirl(ax,groundY,s) {
  var bob=Math.sin(tickCounter/12)*1.5,ay=groundY+bob;
  var liftL=0,liftR=0;
  if(s.walking){ liftL=s.legPhase===0?-3:0; liftR=s.legPhase===0?0:-3; }
  drawRect(ax-5,ay-8+liftL,4,10,"#ffd9b3"); drawRect(ax+1,ay-8+liftR,4,10,"#ffd9b3");
  drawRect(ax-5,ay-2+liftL,4,3,"#FF1493"); drawRect(ax+1,ay-2+liftR,4,3,"#FF1493");
  drawRect(ax-9,ay-26,18,20,"#FF69B4"); drawRect(ax-9,ay-26,18,3,"#FF1493");
  drawRect(ax-7,ay-38,14,14,"#FF69B4"); drawRect(ax-7,ay-38,14,2,"#FF1493");
  var armL=8,armR=-8;
  if(POSE==="hug"){ armL=-50; armR=50; }
  else if(s.walking){ armL=s.legPhase===0?30:-20; armR=s.legPhase===0?-20:30; }
  drawArm(ax-7,ay-36,armL,"#FF1493"); drawArm(ax+7,ay-36,armR,"#FF1493");
  drawRect(ax-8,ay-52,16,16,"#ffd9b3"); drawRect(ax-9,ay-56,18,7,"#8B4513");
  drawRect(ax-9,ay-52,3,10,"#8B4513"); drawRect(ax+6,ay-52,3,10,"#8B4513");
  drawRect(ax-12,ay-53,4,6,"#8B4513"); drawRect(ax+8,ay-53,4,6,"#8B4513");
  drawRect(ax-5,ay-44,3,3,"#2c2c54"); drawRect(ax+2,ay-44,3,3,"#2c2c54");
  drawRect(ax-6,ay-46,1,2,"#2c2c54"); drawRect(ax+5,ay-46,1,2,"#2c2c54");
  drawRect(ax-2,ay-39,5,2,"#a14a5c");
  ctx.fillStyle="rgba(255,150,150,0.4)"; ctx.fillRect(ax-7,ay-41,3,2); ctx.fillRect(ax+4,ay-41,3,2);
  if(SHOW_HEART){
    var hy=ay-68-Math.sin(tickCounter/10+1)*3,hx=ax-8;
    ctx.fillStyle="#ff6f91"; ctx.fillRect(hx,hy,3,3); ctx.fillRect(hx+4,hy,3,3); ctx.fillRect(hx-1,hy+3,9,3); ctx.fillRect(hx+1,hy+6,5,2);
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
  if(boy.walking){ boy.x+=2.2; if(boy.x>=boy.targetX){ boy.x=boy.targetX; boy.walking=false; } if(tickCounter%4===0) boy.legPhase=1-boy.legPhase; }
  if(girl.walking){ girl.x-=1.8; if(girl.x<=girl.targetX){ girl.x=girl.targetX; girl.walking=false; } if(tickCounter%4===0) girl.legPhase=1-girl.legPhase; }
  if(POSE==="talk"&&tickCounter%5===0) boy.mouthOpen=!boy.mouthOpen;
  if(boy.pocketRevealing){ boy.pocketItemY+=1.2; boy.pocketItemScale+=0.04; if(boy.pocketItemY>40) boy.pocketRevealing=false; }
  if((POSE==="hug"||POSE==="celebrate")&&tickCounter%15===0){
    var sw=document.querySelector('.scene-wrap'); if(sw){ var r=sw.getBoundingClientRect(); spawnHeart((boy.x/W)*r.width,(GROUND_Y/H)*r.height-40); }
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
window.triggerPocketReveal=function(){ boy.pocketRevealing=true; boy.pocketItemY=0; boy.pocketItemScale=0.3; };
</script>
</body>
</html>
"""

def render_rpg_scene(pose="idle", dialogue=None, show_heart=False, show_girl=False, scene_w=420, scene_h=260, canvas_w=140, canvas_h=110, scale=3):
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
    html = html.replace("DIALOGUE_VAL", json.dumps(dialogue) if dialogue else "null")
    html = html.replace("DBOX_DISPLAY", "block" if dialogue else "none")
    components.html(html, height=scene_h + 10, scrolling=False)

def render_step_indicator():
    dots = ""
    for i in range(1, 6):
        if i < st.session_state.current_step:
            cls, icon = "done", "✓"
        elif i == st.session_state.current_step:
            cls, icon = "active", str(i)
        else:
            cls, icon = "", str(i)
        dots += f'<div class="step-dot {cls}">{icon}</div>'
    st.markdown(f'<div class="step-indicator">{dots}</div>', unsafe_allow_html=True)

# Header
st.markdown('<div class="title-banner"><h1>Happy Birthday, Pikku!</h1></div>', unsafe_allow_html=True)
render_step_indicator()

# STEP 1
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

# STEP 2
elif st.session_state.current_step == 2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Step 2: Our Beautiful Memories")
    story_days = [
        ("Day 1", "The Arrival", "walk", False, "He walks in, a little nervous, and introduces himself for the first time."),
        ("Day 2", "The Gesture", "talk", True, "He shows up with a small gesture from the heart."),
        ("Day 3", "Getting Closer", "talk", False, "He shares a memory that means a lot to him."),
        ("Day 4", "Forever", "celebrate", True, "He is celebrating right beside you because forever starts with days like this."),
    ]
    row1 = st.columns(2)
    row2 = st.columns(2)
    positions = row1 + row2
    for col, (day, title, pose, heart, desc) in zip(positions, story_days):
        with col:
            st.markdown(f'<h4 style="text-align:center;">{day}</h4><h3 style="text-align:center;">{title}</h3>', unsafe_allow_html=True)
            render_rpg_scene(pose=pose, show_heart=heart, scene_w=320, scene_h=200, canvas_w=110, canvas_h=90, scale=2)
            st.markdown(f'<p style="text-align:center;font-size:14px;">{desc}</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Next Step", use_container_width=True, key="btn_step2_next"):
            st.session_state.current_step = 3
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 3
elif st.session_state.current_step == 3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Step 3: Pocket Surprise!")
    revealed = st.session_state.step3_pocket_revealed
    next_index = len(revealed)
    all_revealed = next_index >= len(POCKET_PHOTOS)
    pose = "reach" if not all_revealed else "celebrate"
    dlg = ["He reaches into his pocket..."] if not all_revealed else ["That is everything he had in there!"]
    render_rpg_scene(pose=pose, show_heart=all_revealed, dialogue=dlg)
    st.write("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if not all_revealed:
            if st.button("Pull photo from pocket", use_container_width=True, key="btn_pull"):
                st.session_state.step3_pocket_revealed.append(next_index)
                st.session_state.step3_just_revealed = True
                st.rerun()
        else:
            st.button("All memories found!", use_container_width=True, disabled=True)
    if st.session_state.step3_just_revealed:
        st.balloons()
        st.session_state.step3_just_revealed = False
    if revealed:
        st.write("")
        st.markdown("#### Revealed memories")
        newest_idx = revealed[-1]
        newest = POCKET_PHOTOS[newest_idx]
        st.markdown('<div class="pocket-photo-new">', unsafe_allow_html=True)
        safe_image(newest["path"], newest["caption"])
        st.markdown('</div>', unsafe_allow_html=True)
        if len(revealed) > 1:
            st.caption("Earlier finds:")
            older_cols = st.columns(3)
            for pos, idx in enumerate(revealed[:-1]):
                memory = POCKET_PHOTOS[idx]
                with older_cols[pos % 3]:
                    safe_image(memory["path"], memory["caption"])
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Next Step", use_container_width=True, key="btn_step3_next"):
            st.session_state.current_step = 4
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 4
elif st.session_state.current_step == 4:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Step 4: Cute Videos")
    vid_cols = st.columns(2)
    labels = ["Cute Clip 1", "Cute Clip 2"]
    for col, path, label in zip(vid_cols, VIDEO_PATHS, labels):
        with col:
            st.markdown(f"**{label}**")
            safe_video(path, label)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Reveal Final Surprise", use_container_width=True, key="btn_step4_next"):
            st.session_state.current_step = 5
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 5
elif st.session_state.current_step == 5:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Step 5: Thank You, Pikku!")
    phase = st.session_state.step5_phase
    if phase == "entry":
        render_rpg_scene(pose="hug", show_heart=True, show_girl=True, dialogue=["They walk toward each other..."], scene_w=500, canvas_w=180)
        st.write("")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Watch them hug!", use_container_width=True, key="btn_hug"):
                st.session_state.step5_phase = "hug"
                st.rerun()
    elif phase == "hug":
        render_rpg_scene(pose="hug", show_heart=True, show_girl=True, dialogue=["Thank you for being my favorite person in the entire universe!", "Happy Birthday! 🎉💖"], scene_w=500, canvas_w=180)
        st.balloons()
        st.markdown('<div class="glass-card" style="text-align:center;"><h2 class="glow-text">Happy Birthday, Pikku!</h2><p style="font-size:18px;">May this year bring you as much joy as you bring into everyone else is life. Here is to more days, more stories, and more reasons to smile together.</p></div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Celebrate Again!", use_container_width=True, key="btn_celebrate"):
                st.balloons()
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
