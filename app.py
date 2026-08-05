"""
Pikku's Birthday Web App - Complete with All Animations
Walking, Talking, Hugging, Kissing - All Working
"""

import os
import json
import base64
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Happy Birthday, Pikku!", page_icon="🎂", layout="wide", initial_sidebar_state="collapsed")

ASSETS_DIR = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)
BG_MUSIC_PATH = os.path.join(ASSETS_DIR, "bg_music.mp3")
VIDEO_PATHS = [os.path.join(ASSETS_DIR, "video1.mp4"), os.path.join(ASSETS_DIR, "video2.mp4")]
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
                b64 = base64.b64encode(f.read()).decode()
            st.markdown(f'<audio autoplay loop><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
        except: pass
    else: st.caption("Add bg_music.mp3 to assets folder")

def safe_video(path, label):
    if os.path.exists(path):
        try: st.video(path)
        except: st.info(f"Add video at {path}")
    else: st.info(f"Add clip at {path}")

def safe_image(path, caption="", use_container_width=True):
    if os.path.exists(path):
        try: st.image(path, caption=caption, use_container_width=use_container_width)
        except: st.markdown(f'<div style="text-align:center;padding:20px;background:white;border-radius:20px;"><p>{caption}</p></div>', unsafe_allow_html=True)
    else: st.markdown(f'<div style="text-align:center;padding:20px;background:white;border-radius:20px;"><p>{caption}</p></div>', unsafe_allow_html=True)

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
.glow-text { animation: glowPulse 2s infinite; }
@keyframes glowPulse { 0%,100% { text-shadow: 0 0 10px #ff6b9d; } 50% { text-shadow: 0 0 30px #ff6b9d; } }
</style>
""", unsafe_allow_html=True)

if "current_step" not in st.session_state: st.session_state.current_step = 1
if "step1_stage" not in st.session_state: st.session_state.step1_stage = "walk"
if "step2_idx" not in st.session_state: st.session_state.step2_idx = 0
if "step2_show" not in st.session_state: st.session_state.step2_show = False
if "step2_just" not in st.session_state: st.session_state.step2_just = False
if "step4_phase" not in st.session_state: st.session_state.step4_phase = "entry"

def render_scene(pose, show_girl=False, show_heart=False, holding_photo=False):
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
body{{margin:0;padding:0;background:transparent;display:flex;justify-content:center;}}
canvas{{border:3px solid #7a4a3a;border-radius:14px;display:block;}}
</style></head><body>
<canvas id="c" width="420" height="260"></canvas>
<script>
var c=document.getElementById('c');var ctx=c.getContext('2d');var W=420,H=260,GY=238;
var POSE='{pose}';var SH={str(show_heart).lower()};var SG={str(show_girl).lower()};var HP={str(holding_photo).lower()};
var boy={{x:-40,tx:180,y:GY,w:true,lp:0,aw:0,ht:0,mo:false,kf:0,ki:false}};
var girl={{x:460,tx:240,y:GY,w:false,lp:1,aw:0,ht:0,kf:0,ki:false}};
var tc=0,hearts=[];

function dr(x,y,w,h,cl){{ctx.fillStyle=cl;ctx.fillRect(Math.round(x),Math.round(y),w,h);}}
function arm(sx,sy,a,cl){{ctx.save();ctx.translate(sx,sy);ctx.rotate(a*Math.PI/180);ctx.fillStyle=cl;ctx.fillRect(-2,0,5,15);ctx.restore();}}

function dB(ax,gy,s){{
  var bob=0;
  if(POSE=='celebrate')bob=Math.sin(s.ht)*5;
  else if(!s.w&&POSE!='walk')bob=Math.sin(tc/6)*1.8;
  var ay=gy+bob;
  ctx.fillStyle='rgba(0,0,0,0.2)';ctx.beginPath();ctx.ellipse(ax,ay+18,12,4,0,0,Math.PI*2);ctx.fill();
  var ll=0,lr=0;
  if(s.w){{ll=s.lp?-5:0;lr=s.lp?0:-5;}}
  else if(POSE=='celebrate'){{ll=Math.sin(s.ht)>0?-3:0;lr=Math.sin(s.ht)>0?0:-3;}}
  dr(ax-7,ay-16+ll,6,16,'#333');dr(ax-7,ay-1+ll,6,4,'#222');
  dr(ax+1,ay-16+lr,6,16,'#333');dr(ax+1,ay-1+lr,6,4,'#222');
  dr(ax-9,ay-34,18,20,'#4f8ecb');dr(ax-9,ay-34,18,3,'#33618f');
  dr(ax+3,ay-20,5,5,'#1a2538');
  var al=8,ar=-8;
  if(POSE=='talk')ar=-60+Math.sin(s.aw)*40;
  else if(POSE=='reach')ar=75;
  else if(POSE=='celebrate'){{al=150+Math.sin(s.ht)*15;ar=-150-Math.sin(s.ht)*15;}}
  else if(POSE=='hug'){{al=-55;ar=55;}}
  else if(POSE=='kiss'){{al=-50;ar=50;}}
  else if(s.w){{al=s.lp?30:-20;ar=s.lp?-20:30;}}
  arm(ax-9,ay-32,al,'#33618f');arm(ax+9,ay-32,ar,'#33618f');
  if(HP&&POSE=='reach'){{
    var px=ax+14,py=ay-38;
    ctx.fillStyle='#fff';ctx.fillRect(px-8,py-10,16,20);
    ctx.strokeStyle='#f0c0d0';ctx.lineWidth=1;ctx.strokeRect(px-8,py-10,16,20);
    ctx.fillStyle='#f66';ctx.fillRect(px-4,py-4,3,3);ctx.fillRect(px+3,py-4,3,3);ctx.fillRect(px-4,py,10,3);
  }}
  dr(ax-8,ay-50,16,16,'#ffd9b3');
  dr(ax-9,ay-54,18,6,'#4a2c17');dr(ax-9,ay-50,3,10,'#4a2c17');dr(ax+6,ay-50,3,10,'#4a2c17');
  if(POSE=='kiss'&&s.ki){{dr(ax-4,ay-42,2,2,'#333');dr(ax+2,ay-42,1,1,'#333');dr(ax-2,ay-36,4,2,'#a14a5c');}}
  else{{dr(ax-5,ay-42,2,2,'#333');dr(ax+3,ay-42,2,2,'#333');var mh=(POSE=='talk'&&s.mo)?3:1;dr(ax-3,ay-37,6,mh,'#a14a5c');}}
  if(SH){{var hy=ay-66-Math.sin(tc/5)*6,hx=ax+12;ctx.fillStyle='#ff6f91';dr(hx,hy,3,3);dr(hx+4,hy,3,3);dr(hx-1,hy+3,9,3);dr(hx+1,hy+6,5,2);}}
}}

function dG(ax,gy,s){{
  var bob=Math.sin(tc/6)*1.8,ay=gy+bob;
  ctx.fillStyle='rgba(0,0,0,0.2)';ctx.beginPath();ctx.ellipse(ax,ay+18,12,4,0,0,Math.PI*2);ctx.fill();
  var ll=0,lr=0;
  if(s.w){{ll=s.lp?-5:0;lr=s.lp?0:-5;}}
  dr(ax-5,ay-8+ll,4,10,'#ffd9b3');dr(ax+1,ay-8+lr,4,10,'#ffd9b3');
  dr(ax-5,ay,4,3,'#FF1493');dr(ax+1,ay,4,3,'#FF1493');
  dr(ax-9,ay-26,18,20,'#FF69B4');dr(ax-9,ay-26,18,3,'#FF1493');
  dr(ax-7,ay-38,14,14,'#FF69B4');
  var al=8,ar=-8;
  if(POSE=='hug'){{al=-45;ar=45;}}
  else if(POSE=='kiss'){{al=-40;ar=40;}}
  else if(s.w){{al=s.lp?30:-20;ar=s.lp?-20:30;}}
  arm(ax-7,ay-36,al,'#FF1493');arm(ax+7,ay-36,ar,'#FF1493');
  dr(ax-8,ay-52,16,16,'#ffd9b3');
  dr(ax-9,ay-56,18,7,'#8B4513');dr(ax-9,ay-52,3,10,'#8B4513');dr(ax+6,ay-52,3,10,'#8B4513');
  dr(ax-10,ay-53,4,5,'#8B4513');dr(ax+6,ay-53,4,5,'#8B4513');
  if(POSE=='kiss'&&s.ki){{dr(ax-3,ay-44,2,2,'#333');dr(ax+1,ay-44,1,1,'#333');dr(ax-2,ay-38,4,2,'#a14a5c');}}
  else{{dr(ax-5,ay-44,3,3,'#333');dr(ax+2,ay-44,3,3,'#333');dr(ax-2,ay-39,5,2,'#a14a5c');}}
  ctx.fillStyle='rgba(255,150,150,0.4)';dr(ax-7,ay-41,3,2);dr(ax+4,ay-41,3,2);
  if(SH){{var hy=ay-68-Math.sin(tc/5+1)*5,hx=ax-8;ctx.fillStyle='#ff6f91';dr(hx,hy,3,3);dr(hx+4,hy,3,3);dr(hx-1,hy+3,9,3);dr(hx+1,hy+6,5,2);}}
}}

function tick(){{
  tc++;boy.aw+=0.4;boy.ht+=0.3;girl.aw+=0.35;girl.ht+=0.28;
  if(POSE=='kiss'){{boy.kf++;girl.kf++;if(boy.kf>50){{boy.ki=true;girl.ki=true;}}}}
  if(boy.w){{boy.x+=2.5;if(boy.x>=boy.tx){{boy.x=boy.tx;boy.w=false;}}if(tc%3==0)boy.lp=1-boy.lp;}}
  if(girl.w){{girl.x-=2.5;if(girl.x<=girl.tx){{girl.x=girl.tx;girl.w=false;}}if(tc%3==0)girl.lp=1-girl.lp;}}
  if(POSE=='talk'&&tc%4==0)boy.mo=!boy.mo;
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle='#c8e6ff';ctx.fillRect(0,0,W,H*0.55);
  ctx.fillStyle='rgba(255,255,255,0.8)';ctx.fillRect(15,8,35,9);ctx.fillRect(25,4,25,7);
  ctx.fillStyle='rgba(255,255,255,0.6)';ctx.fillRect(W-55,12,30,7);
  ctx.fillStyle='#7fc97f';ctx.fillRect(0,H*0.55,W,H*0.45);
  dB(boy.x,boy.y,boy);
  if(SG)dG(girl.x,girl.y,girl);
}}
setInterval(tick,1000/30);tick();
</script></body></html>"""
    components.html(html, height=280, scrolling=False)

def step_dots():
    dots = ""
    for i in range(1, 5):
        if i < st.session_state.current_step: c, icon = "done", "✓"
        elif i == st.session_state.current_step: c, icon = "active", str(i)
        else: c, icon = "", str(i)
        dots += f'<div class="step-dot {c}">{icon}</div>'
    st.markdown(f'<div class="step-indicator">{dots}</div>', unsafe_allow_html=True)

st.markdown('<h1>🎀 Happy Birthday, Pikku! 🎂</h1>', unsafe_allow_html=True)
step_dots()

# STEP 1 - BOY WALKS IN
if st.session_state.current_step == 1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 💬 A Special Visitor Arrives")
    safe_audio(BG_MUSIC_PATH)
    s = st.session_state.step1_stage
    if s == "walk":
        render_scene(pose="walk")
        st.markdown('<div style="background:#fff8ec;border:3px solid #2c2c54;border-radius:8px;padding:10px;text-align:center;margin-top:5px;">...</div>', unsafe_allow_html=True)
        c1,c2,c3 = st.columns([1,2,1])
        with c2:
            if st.button("💬 Talk to him", use_container_width=True, key="b1"):
                st.session_state.step1_stage = "talk"
                st.rerun()
    elif s == "talk":
        render_scene(pose="talk")
        st.markdown(f'<div style="background:#fff8ec;border:3px solid #2c2c54;border-radius:8px;padding:10px;text-align:center;margin-top:5px;">{GREETING_LINE}</div>', unsafe_allow_html=True)
        c1,c2,c3 = st.columns([1,2,1])
        with c2:
            if st.button("Next ➡️", use_container_width=True, key="b1n"):
                st.session_state.current_step = 2
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 2 - POCKET PHOTOS
elif st.session_state.current_step == 2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🎁 Pocket Surprise!")
    idx = st.session_state.step2_idx
    total = len(POCKET_PHOTOS)
    done = idx >= total
    if not done:
        ph = POCKET_PHOTOS[idx]
        render_scene(pose="reach", holding_photo=True)
        st.markdown(f'<div style="background:#fff8ec;border:3px solid #2c2c54;border-radius:8px;padding:10px;text-align:center;margin-top:5px;">Photo {idx+1}/{total}: {ph["caption"]}</div>', unsafe_allow_html=True)
        c1,c2,c3 = st.columns([1,2,1])
        with c2:
            if idx == 0 and not st.session_state.step2_show:
                if st.button("🎁 Pull photo", use_container_width=True, key="bp"):
                    st.session_state.step2_show = True
                    st.session_state.step2_just = True
                    st.rerun()
            elif st.session_state.step2_show:
                lab = "📸 Next Photo" if idx < total-1 else "📸 Final Photo"
                if st.button(lab, use_container_width=True, key=f"bn{idx}"):
                    st.session_state.step2_idx += 1
                    st.session_state.step2_just = True
                    st.rerun()
        if st.session_state.step2_just:
            st.balloons()
            st.session_state.step2_just = False
        if st.session_state.step2_show:
            safe_image(ph["path"], ph["caption"])
    else:
        render_scene(pose="celebrate", show_heart=True)
        st.markdown('<div style="background:#fff8ec;border:3px solid #2c2c54;border-radius:8px;padding:10px;text-align:center;">All done! 💗</div>', unsafe_allow_html=True)
        cols = st.columns(min(total,4))
        for i, ph in enumerate(POCKET_PHOTOS):
            with cols[i%len(cols)]: safe_image(ph["path"], ph["caption"])
        c1,c2,c3 = st.columns([1,2,1])
        with c2:
            if st.button("Next Step ➡️", use_container_width=True, key="b2n"):
                st.session_state.current_step = 3
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 3 - VIDEOS
elif st.session_state.current_step == 3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🎬 Cute Videos")
    vc = st.columns(2)
    for col, path, lab in zip(vc, VIDEO_PATHS, ["Clip 1", "Clip 2"]):
        with col:
            st.markdown(f"**{lab}**")
            safe_video(path, lab)
    c1,c2,c3 = st.columns([1,2,1])
    with c2:
        if st.button("💖 Final Surprise ➡️", use_container_width=True, key="b3n"):
            st.session_state.current_step = 4
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 4 - FINALE HUG & KISS
elif st.session_state.current_step == 4:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 💕 Grand Finale")
    ph = st.session_state.step4_phase
    if ph == "entry":
        render_scene(pose="hug", show_heart=True, show_girl=True)
        st.markdown('<div style="background:#fff8ec;border:3px solid #2c2c54;border-radius:8px;padding:10px;text-align:center;">They meet! 💓</div>', unsafe_allow_html=True)
        c1,c2,c3 = st.columns([1,2,1])
        with c2:
            if st.button("🤗 Watch Hug!", use_container_width=True, key="bh"):
                st.session_state.step4_phase = "hug"
                st.rerun()
    elif ph == "hug":
        render_scene(pose="hug", show_heart=True, show_girl=True)
        st.markdown('<div style="background:#fff8ec;border:3px solid #2c2c54;border-radius:8px;padding:10px;text-align:center;">Warm embrace! 🤗</div>', unsafe_allow_html=True)
        c1,c2,c3 = st.columns([1,2,1])
        with c2:
            if st.button("💋 Watch Kiss!", use_container_width=True, key="bk"):
                st.session_state.step4_phase = "kiss"
                st.rerun()
    elif ph == "kiss":
        render_scene(pose="kiss", show_heart=True, show_girl=True)
        st.balloons()
        st.markdown('<div style="background:#fff8ec;border:3px solid #2c2c54;border-radius:8px;padding:10px;text-align:center;">Thank you for being my favorite person! 🎉💖</div>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card" style="text-align:center;"><h2 class="glow-text">💝 Happy Birthday, Pikku! 💝</h2><p style="font-size:18px;">Thank you for being my favorite person in the entire universe! 🎉💖</p></div>', unsafe_allow_html=True)
        c1,c2,c3 = st.columns([1,2,1])
        with c2:
            if st.button("🎉 Celebrate Again!", use_container_width=True, key="bcel"):
                st.balloons()
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
