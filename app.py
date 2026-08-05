"""
Pikku's Birthday Web App - Simple Working Version
==================================================
Characters visible immediately - tested and working.
"""

import os
import json
import base64
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Happy Birthday, Pikku!",
    page_icon="🎂",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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


def safe_audio(path):
    if os.path.exists(path):
        try:
            with open(path, "rb") as f:
                audio_bytes = f.read()
            b64 = base64.b64encode(audio_bytes).decode()
            st.markdown(f'<audio autoplay loop><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
        except:
            pass


def safe_video(path, label):
    if os.path.exists(path):
        try:
            st.video(path)
        except:
            st.info(f"Add video at {path}")
    else:
        st.info(f"Add clip at {path}")


def safe_image(path, caption="", use_container_width=True):
    if os.path.exists(path):
        try:
            st.image(path, caption=caption, use_container_width=use_container_width)
        except:
            st.markdown(f'<div style="text-align:center;padding:30px;background:white;border-radius:20px;"><div style="font-size:64px;">🌸</div><p>{caption}</p></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align:center;padding:30px;background:white;border-radius:20px;"><div style="font-size:64px;">🌸</div><p>{caption}</p></div>', unsafe_allow_html=True)


st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #ffdde1 0%, #ee9ca7 100%); }
#MainMenu, header, footer {visibility: hidden;}
h1, h2, h3 { color: #a14a5c !important; text-align: center; }
.glass-card { background: rgba(255,255,255,0.85); border-radius: 22px; padding: 20px; margin: 10px 0; }
.stButton > button { background: #ffb6c1; color: #6b2c3a; border: none; border-radius: 30px; padding: 12px 24px; font-weight: 700; font-size: 16px; width: 100%; cursor: pointer; }
.step-indicator { display: flex; justify-content: center; gap: 10px; margin: 15px 0; }
.step-dot { width: 35px; height: 35px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; background: rgba(255,255,255,0.5); color: #c98a97; border: 2px solid #ee9ca7; }
.step-dot.active { background: #ee9ca7; color: white; }
.step-dot.done { background: #c44569; color: white; }
@keyframes popIn { from { transform: scale(0); opacity: 0; } to { transform: scale(1); opacity: 1; } }
.pocket-photo-new { animation: popIn 0.6s ease-out forwards; }
.glow-text { animation: glowPulse 2s infinite; }
@keyframes glowPulse { 0%,100% { text-shadow: 0 0 10px #ff6b9d; } 50% { text-shadow: 0 0 30px #ff6b9d; } }
</style>
""", unsafe_allow_html=True)

if "current_step" not in st.session_state:
    st.session_state.current_step = 1
if "step1_stage" not in st.session_state:
    st.session_state.step1_stage = "idle"
if "step2_idx" not in st.session_state:
    st.session_state.step2_idx = 0
if "step2_show" not in st.session_state:
    st.session_state.step2_show = False
if "step2_just" not in st.session_state:
    st.session_state.step2_just = False
if "step4_phase" not in st.session_state:
    st.session_state.step4_phase = "entry"


def get_canvas_html(pose, show_girl=False, show_heart=False, holding_photo=False, dialogue=None):
    dialogue_json = json.dumps(dialogue) if dialogue else "null"
    sh = "true" if show_heart else "false"
    sg = "true" if show_girl else "false"
    hp = "true" if holding_photo else "false"
    
    html = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
body{margin:0;padding:0;background:transparent;display:flex;justify-content:center;}
canvas{border:3px solid #7a4a3a;border-radius:14px;background:linear-gradient(#87CEEB 0%,#87CEEB 55%,#4CAF50 55%);display:block;}
</style></head><body>
<canvas id="c" width="420" height="260"></canvas>
<script>
var c=document.getElementById('c');
var ctx=c.getContext('2d');
var W=420,H=260,GY=238;
var boy={x:210,y:GY,w:false,lp:0,aw:0,ht:0,mo:false};
var girl={x:250,y:GY,w:false,lp:0};
var tc=0;
var POSE='""" + pose + """';
var SH=""" + sh + """;
var SG=""" + sg + """;
var HP=""" + hp + """;

function dr(x,y,w,h,cl){ctx.fillStyle=cl;ctx.fillRect(Math.round(x),Math.round(y),w,h);}
function arm(sx,sy,a,cl){ctx.save();ctx.translate(sx,sy);ctx.rotate(a*Math.PI/180);ctx.fillStyle=cl;ctx.fillRect(-2,0,5,15);ctx.restore();}

function drawBoy(ax,ay,s){
  var bob=Math.sin(tc/8)*1.5,ay2=ay+bob;
  ctx.fillStyle='rgba(0,0,0,0.2)';ctx.beginPath();ctx.ellipse(ax,ay2+18,12,4,0,0,Math.PI*2);ctx.fill();
  var ll=0,lr=0;
  if(s.w){ll=s.lp?-4:0;lr=s.lp?0:-4;}
  dr(ax-7,ay2-16+ll,6,16,'#333');dr(ax-7,ay2+ll,6,4,'#222');
  dr(ax+1,ay2-16+lr,6,16,'#333');dr(ax+1,ay2+lr,6,4,'#222');
  dr(ax-9,ay2-34,18,20,'#4f8ecb');dr(ax-9,ay2-34,18,3,'#33618f');
  var al=8,ar=-8;
  if(POSE=='talk')ar=-60+Math.sin(s.aw)*35;
  else if(POSE=='reach')ar=70;
  else if(POSE=='celebrate'){al=150;ar=-150;}
  else if(POSE=='hug'){al=-55;ar=55;}
  else if(POSE=='kiss'){al=-50;ar=50;}
  arm(ax-9,ay2-32,al,'#33618f');arm(ax+9,ay2-32,ar,'#33618f');
  if(HP&&POSE=='reach'){
    var px=ax+14,py=ay2-38;
    ctx.fillStyle='#fff';ctx.fillRect(px-8,py-10,16,20);
    ctx.strokeStyle='#f0c0d0';ctx.lineWidth=1;ctx.strokeRect(px-8,py-10,16,20);
    ctx.fillStyle='#f66';ctx.fillRect(px-4,py-3,3,3);ctx.fillRect(px+3,py-3,3,3);ctx.fillRect(px-4,py,10,3);
  }
  dr(ax-8,ay2-50,16,16,'#ffd9b3');
  dr(ax-9,ay2-54,18,6,'#4a2c17');
  dr(ax-9,ay2-50,3,10,'#4a2c17');dr(ax+6,ay2-50,3,10,'#4a2c17');
  dr(ax-5,ay2-42,2,2,'#333');dr(ax+3,ay2-42,2,2,'#333');
  var mh=(POSE=='talk'&&s.mo)?3:1;
  dr(ax-3,ay2-37,6,mh,'#a14a5c');
  if(SH){
    var hy=ay2-66-Math.sin(tc/7)*5,hx=ax+12;
    ctx.fillStyle='#ff6f91';
    dr(hx,hy,3,3);dr(hx+4,hy,3,3);dr(hx-1,hy+3,9,3);dr(hx+1,hy+6,5,2);
  }
}

function drawGirl(ax,ay,s){
  var bob=Math.sin(tc/8)*1.5,ay2=ay+bob;
  ctx.fillStyle='rgba(0,0,0,0.2)';ctx.beginPath();ctx.ellipse(ax,ay2+18,12,4,0,0,Math.PI*2);ctx.fill();
  var ll=0,lr=0;
  if(s.w){ll=s.lp?-4:0;lr=s.lp?0:-4;}
  dr(ax-5,ay2-8+ll,4,10,'#ffd9b3');dr(ax+1,ay2-8+lr,4,10,'#ffd9b3');
  dr(ax-5,ay2-2+ll,4,3,'#FF1493');dr(ax+1,ay2-2+lr,4,3,'#FF1493');
  dr(ax-9,ay2-26,18,20,'#FF69B4');dr(ax-9,ay2-26,18,3,'#FF1493');
  dr(ax-7,ay2-38,14,14,'#FF69B4');
  var al=8,ar=-8;
  if(POSE=='hug'){al=-45;ar=45;}
  else if(POSE=='kiss'){al=-40;ar=40;}
  arm(ax-7,ay2-36,al,'#FF1493');arm(ax+7,ay2-36,ar,'#FF1493');
  dr(ax-8,ay2-52,16,16,'#ffd9b3');
  dr(ax-9,ay2-56,18,7,'#8B4513');
  dr(ax-9,ay2-52,3,10,'#8B4513');dr(ax+6,ay2-52,3,10,'#8B4513');
  dr(ax-5,ay2-44,3,3,'#333');dr(ax+2,ay2-44,3,3,'#333');
  dr(ax-2,ay2-39,5,2,'#a14a5c');
  ctx.fillStyle='rgba(255,150,150,0.4)';dr(ax-7,ay2-41,3,2);dr(ax+4,ay2-41,3,2);
  if(SH){
    var hy=ay2-68-Math.sin(tc/7+1)*4,hx=ax-8;
    ctx.fillStyle='#ff6f91';
    dr(hx,hy,3,3);dr(hx+4,hy,3,3);dr(hx-1,hy+3,9,3);dr(hx+1,hy+6,5,2);
  }
}

function tick(){
  tc++;boy.aw+=0.35;boy.ht+=0.28;
  if(POSE=='talk'&&tc%4==0)boy.mo=!boy.mo;
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle='#c8e6ff';ctx.fillRect(0,0,W,H*0.55);
  ctx.fillStyle='rgba(255,255,255,0.8)';ctx.fillRect(20,10,40,10);ctx.fillRect(30,5,30,8);
  ctx.fillStyle='rgba(255,255,255,0.6)';ctx.fillRect(W-60,15,35,8);
  ctx.fillStyle='#7fc97f';ctx.fillRect(0,H*0.55,W,H*0.45);
  drawBoy(boy.x,boy.y,boy);
  if(SG)drawGirl(girl.x,girl.y,girl);
}
setInterval(tick,1000/30);
tick();
</script></body></html>"""
    return html


def render_scene(pose="idle", dialogue=None, show_heart=False, show_girl=False, holding_photo=False):
    html = get_canvas_html(pose, show_girl, show_heart, holding_photo, dialogue)
    components.html(html, height=280, scrolling=False)


def step_dots():
    dots = ""
    for i in range(1, 5):
        if i < st.session_state.current_step:
            c, icon = "done", "✓"
        elif i == st.session_state.current_step:
            c, icon = "active", str(i)
        else:
            c, icon = "", str(i)
        dots += f'<div class="step-dot {c}">{icon}</div>'
    st.markdown(f'<div class="step-indicator">{dots}</div>', unsafe_allow_html=True)


st.markdown('<h1>🎀 Happy Birthday, Pikku! 🎂</h1>', unsafe_allow_html=True)
step_dots()

# STEP 1
if st.session_state.current_step == 1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 💬 A Special Visitor")
    safe_audio(BG_MUSIC_PATH)
    s = st.session_state.step1_stage
    if s == "idle":
        render_scene(pose="idle")
    elif s == "talking":
        render_scene(pose="talk")
    st.write("")
    c1, c2, c3 = st.columns([1, 2, 1])
    if s == "idle":
        with c2:
            if st.button("💬 Talk to him", use_container_width=True, key="b1"):
                st.session_state.step1_stage = "talking"
                st.rerun()
    elif s == "talking":
        st.markdown(f'<div style="background:#fff8ec;border:3px solid #2c2c54;border-radius:8px;padding:12px;text-align:center;font-size:16px;">{GREETING_LINE}</div>', unsafe_allow_html=True)
        with c2:
            if st.button("Next ➡️", use_container_width=True, key="b1n"):
                st.session_state.current_step = 2
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 2
elif st.session_state.current_step == 2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🎁 Pocket Surprise!")
    idx = st.session_state.step2_idx
    total = len(POCKET_PHOTOS)
    done = idx >= total
    if not done:
        ph = POCKET_PHOTOS[idx]
        cap = ph['caption']
        render_scene(pose="reach", holding_photo=True)
        st.markdown(f'<div style="background:#fff8ec;border:3px solid #2c2c54;border-radius:8px;padding:10px;text-align:center;margin-top:5px;">Photo {idx+1}/{total}: {cap}</div>', unsafe_allow_html=True)
        st.write("")
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if idx == 0 and not st.session_state.step2_show:
                if st.button("🎁 Pull photo", use_container_width=True, key="bp"):
                    st.session_state.step2_show = True
                    st.session_state.step2_just = True
                    st.rerun()
            elif st.session_state.step2_show:
                lab = "📸 Next Photo" if idx < total - 1 else "📸 Final Photo"
                if st.button(lab, use_container_width=True, key=f"bn{idx}"):
                    st.session_state.step2_idx += 1
                    st.session_state.step2_just = True
                    st.rerun()
        if st.session_state.step2_just:
            st.balloons()
            st.session_state.step2_just = False
        if st.session_state.step2_show:
            st.markdown('<div class="pocket-photo-new">', unsafe_allow_html=True)
            safe_image(ph["path"], cap)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        render_scene(pose="celebrate", show_heart=True)
        st.markdown('<div style="background:#fff8ec;border:3px solid #2c2c54;border-radius:8px;padding:10px;text-align:center;">All memories shown! 💗</div>', unsafe_allow_html=True)
        cols = st.columns(min(total, 4))
        for i, ph in enumerate(POCKET_PHOTOS):
            with cols[i % len(cols)]:
                safe_image(ph["path"], ph["caption"])
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("Next Step ➡️", use_container_width=True, key="b2n"):
                st.session_state.current_step = 3
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 3
elif st.session_state.current_step == 3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🎬 Cute Videos")
    vc = st.columns(2)
    for col, path, lab in zip(vc, VIDEO_PATHS, ["Clip 1", "Clip 2"]):
        with col:
            st.markdown(f"**{lab}**")
            safe_video(path, lab)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("💖 Final Surprise ➡️", use_container_width=True, key="b3n"):
            st.session_state.current_step = 4
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 4
elif st.session_state.current_step == 4:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 💕 Grand Finale")
    ph = st.session_state.step4_phase
    if ph == "entry":
        render_scene(pose="hug", show_heart=True, show_girl=True)
        st.markdown('<div style="background:#fff8ec;border:3px solid #2c2c54;border-radius:8px;padding:10px;text-align:center;">They meet! 💓</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("🤗 Watch Hug!", use_container_width=True, key="bh"):
                st.session_state.step4_phase = "hug"
                st.rerun()
    elif ph == "hug":
        render_scene(pose="hug", show_heart=True, show_girl=True)
        st.markdown('<div style="background:#fff8ec;border:3px solid #2c2c54;border-radius:8px;padding:10px;text-align:center;">Warm embrace! 🤗</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("💋 Watch Kiss!", use_container_width=True, key="bk"):
                st.session_state.step4_phase = "kiss"
                st.rerun()
    elif ph == "kiss":
        render_scene(pose="kiss", show_heart=True, show_girl=True)
        st.balloons()
        st.markdown('<div class="glass-card" style="text-align:center;"><h2 class="glow-text">💝 Happy Birthday, Pikku! 💝</h2><p style="font-size:18px;">Thank you for being my favorite person in the entire universe! 🎉💖</p></div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("🎉 Celebrate Again!", use_container_width=True, key="bcel"):
                st.balloons()
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
