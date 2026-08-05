I'll upgrade the animation to **60 FPS** and add **3D-like effects** using CSS 3D transforms and enhanced rendering. Here's the complete `app.py`:

```python
"""
Pikku's Birthday Web App - 60 FPS 3D RPG Edition
=================================================
A guided 4-step Streamlit birthday experience with
60 FPS smooth animations and 3D-like effects.
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
            st.markdown(f'<audio autoplay loop style="display:none;"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
            st.caption("🎵 Music playing...")
        except:
            st.caption("🎵 Add MP3 to assets/bg_music.mp3")
    else:
        st.caption("🎵 Add song at assets/bg_music.mp3")


def safe_video(path, label):
    if os.path.exists(path):
        try:
            st.video(path)
        except:
            st.info(f"📹 Add video at {path}")
    else:
        st.info(f"📹 Add clip at {path}")


def safe_image(path, caption="", use_container_width=True):
    if os.path.exists(path):
        try:
            st.image(path, caption=caption, use_container_width=use_container_width)
        except:
            st.markdown(f'<div class="glass-card" style="text-align:center;padding:30px;"><div style="font-size:64px;">🌸</div><p style="font-weight:600;font-size:18px;color:#c44569;">{caption}</p></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="glass-card" style="text-align:center;padding:30px;"><div style="font-size:64px;">🌸</div><p style="font-weight:600;font-size:18px;color:#c44569;">{caption}</p></div>', unsafe_allow_html=True)


st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #ffdde1 0%, #ee9ca7 100%); background-attachment: fixed; }
#MainMenu, header, footer {visibility: hidden;}
h1, h2, h3, h4 { color: #a14a5c !important; text-shadow: 0 2px 6px rgba(255,255,255,0.4); }
p, span, label, div { color: #7a3b47; }
.glass-card { background: rgba(255,255,255,0.85); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-radius: 22px; border: 1.5px solid rgba(238,156,167,0.55); box-shadow: 0 8px 32px rgba(238,156,167,0.35); padding: 20px 24px; margin-bottom: 20px; transition: transform 0.25s ease, box-shadow 0.25s ease; }
.glass-card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(238,156,167,0.5); }
.stButton > button { background: linear-gradient(135deg, #ffb6c1 0%, #ee9ca7 100%); color: #6b2c3a; border: none; border-radius: 30px; padding: 10px 22px; font-weight: 700; box-shadow: 0 4px 14px rgba(238,156,167,0.5); transition: all 0.3s ease; }
.stButton > button:hover { transform: scale(1.05) translateY(-2px); box-shadow: 0 8px 25px rgba(238,156,167,0.7); }
.step-indicator { display: flex; justify-content: center; gap: 10px; margin: 15px 0 25px 0; }
.step-dot { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 18px; background: rgba(255,255,255,0.5); color: #c98a97; border: 2px solid #ee9ca7; transition: all 0.3s ease; }
.step-dot.active { background: #ee9ca7; color: white; border-color: #c44569; box-shadow: 0 0 20px rgba(238,156,167,0.6); animation: pulse 2s infinite; }
.step-dot.done { background: #c44569; color: white; border-color: #c44569; }
@keyframes pulse { 0%,100% { box-shadow: 0 0 20px rgba(238,156,167,0.6); } 50% { box-shadow: 0 0 35px rgba(238,156,167,0.9); } }
@keyframes popIn { 0% { transform: scale(0.05) rotateY(180deg); opacity: 0; } 60% { transform: scale(1.08) rotateY(0deg); opacity: 1; } 100% { transform: scale(1) rotateY(0deg); opacity: 1; } }
.pocket-photo-new { animation: popIn 0.8s cubic-bezier(.2,.9,.3,1.3) forwards; perspective: 1000px; }
@keyframes glowPulse { 0%,100% { text-shadow: 0 0 10px rgba(255,107,157,0.3); } 50% { text-shadow: 0 0 30px rgba(255,107,157,0.8), 0 0 60px rgba(255,107,157,0.4); } }
.glow-text { animation: glowPulse 2s ease-in-out infinite; }
@keyframes float3D { 0%,100% { transform: translateY(0px) rotateY(0deg); } 25% { transform: translateY(-10px) rotateY(5deg); } 75% { transform: translateY(-5px) rotateY(-5deg); } }
.float-3d { animation: float3D 4s ease-in-out infinite; }
@media (max-width: 768px) { .step-dot { width: 30px; height: 30px; font-size: 14px; } .glass-card { padding: 14px 16px; } }
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

RPG_HTML = """
<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
html,body{margin:0;padding:0;background:transparent;overflow:hidden;font-family:'Courier New',monospace;}
.scene-wrap{position:relative;width:SWpx;height:SHpx;margin:0 auto;border-radius:14px;overflow:hidden;border:3px solid #7a4a3a;box-shadow:0 10px 30px rgba(0,0,0,0.3),inset 0 0 50px rgba(255,255,255,0.1);background:linear-gradient(180deg,#bdeaff 0%,#a8d8ff 30%,#8ecf8e 55%,#7fc97f 100%);perspective:800px;transform-style:preserve-3d;}
.ground-strip{position:absolute;left:0;right:0;bottom:0;height:26px;background:repeating-linear-gradient(90deg,#6ab86a 0px,#6ab86a 8px,#5aa65a 8px,#5aa65a 16px);background-size:32px 26px;animation:gs 0.8s steps(4) infinite;opacity:0.9;z-index:1;box-shadow:0 -2px 10px rgba(0,0,0,0.2);}
@keyframes gs{from{background-position-x:0px;}to{background-position-x:-32px;}}
canvas#c{position:absolute;left:50%;top:8px;transform:translateX(-50%);image-rendering:pixelated;width:CWpx;height:CHpx;z-index:2;filter:drop-shadow(0 4px 8px rgba(0,0,0,0.3));}
.dw{position:absolute;left:6px;right:6px;bottom:6px;display:DD;z-index:10;}
.db{background:rgba(255,248,236,0.95);border:3px solid #2c2c54;border-radius:8px;box-shadow:inset 0 0 0 2px #ffe9c7,0 8px 20px rgba(0,0,0,0.3),0 0 30px rgba(255,182,193,0.3);padding:8px 30px 8px 10px;min-height:44px;font-size:13px;line-height:1.35;color:#2c2c54;position:relative;cursor:pointer;backdrop-filter:blur(5px);}
.da{position:absolute;right:10px;bottom:6px;width:0;height:0;border-left:6px solid transparent;border-right:6px solid transparent;border-top:8px solid #2c2c54;animation:ab 0.6s steps(1) infinite;}
@keyframes ab{0%,49%{opacity:1;}50%,100%{opacity:0;}}
.fh{position:absolute;top:0;left:0;right:0;bottom:0;pointer-events:none;z-index:3;perspective:500px;}
.hp{position:absolute;font-size:18px;animation:fu 3s ease-out forwards;pointer-events:none;transform-style:preserve-3d;}
@keyframes fu{0%{transform:translateY(0) scale(0.3) rotateY(0deg);opacity:1;}50%{transform:translateY(-100px) scale(1.2) rotateY(180deg);opacity:0.8;}100%{transform:translateY(-250px) scale(0.5) rotateY(360deg);opacity:0;}}
.particle{position:absolute;pointer-events:none;z-index:4;animation:sparkle 1.5s ease-out forwards;}
@keyframes sparkle{0%{transform:scale(1) rotate(0deg);opacity:1;}100%{transform:scale(0) rotate(180deg);opacity:0;}}
</style></head><body>
<div class="scene-wrap" id="sceneWrap">
<canvas id="c" width="CW2" height="CH2"></canvas>
<div class="ground-strip"></div>
<div class="fh" id="fh"></div>
<div class="dw"><div class="db" id="dca"><span id="dt"></span><div class="da" id="da" style="display:none;"></div></div></div>
</div>
<script>
var cv=document.getElementById('c'),ctx=cv.getContext('2d');
ctx.imageSmoothingEnabled=false;
var W=cv.width,H=cv.height,GY=H-22;
var POSE="PV",SH=SHV,SG=SGV,HP=HPV,DIA=DIAV;
var boy={x:-20,tx:SG?Math.round(W/2)-20:Math.round(W/2),w:true,lp:0,aw:0,ht:0,mo:false,kf:0,ki:false,scale:1,rotY:0};
var girl={x:W+40,tx:Math.round(W/2)+20,w:SG,lp:1,aw:0,ht:0,kf:0,ki:false,scale:1,rotY:0};
var tc=0,dl=DIA||[],cli=0,tt=null,tc2=false,sparkles=[];

function dr(x,y,w,h,c){ctx.fillStyle=c;ctx.fillRect(Math.round(x),Math.round(y),w,h);}
function da(sx,sy,an,c){ctx.save();ctx.translate(sx,sy);ctx.rotate(an*Math.PI/180);ctx.fillStyle=c;ctx.fillRect(-2,0,5,15);ctx.restore();}

function addSparkle(x,y){
  sparkles.push({x:x,y:y,life:1,size:Math.random()*3+1,vx:(Math.random()-0.5)*2,vy:Math.random()*-3-1});
  if(sparkles.length>50)sparkles.shift();
}

function drawSparkles(){
  for(var i=sparkles.length-1;i>=0;i--){
    var s=sparkles[i];
    s.x+=s.vx;s.y+=s.vy;s.life-=0.02;
    ctx.fillStyle='rgba(255,255,200,'+s.life+')';
    ctx.beginPath();ctx.arc(s.x,s.y,s.size,0,Math.PI*2);ctx.fill();
    if(s.life<=0)sparkles.splice(i,1);
  }
}

function draw3DShadow(ax,ay){
  ctx.fillStyle='rgba(0,0,0,0.15)';
  ctx.beginPath();ctx.ellipse(ax,ay+2,12,4,0,0,Math.PI*2);ctx.fill();
}

function dB(ax,gy,s){
  var bob=0;
  if(POSE==="celebrate")bob=Math.sin(s.ht)*4;
  else if(!s.w&&POSE!=="walk")bob=Math.sin(tc/8)*1.5;
  var ay=gy+bob;
  draw3DShadow(ax,ay+16);
  var ll=0,lr=0;
  if(s.w){ll=s.lp===0?-4:0;lr=s.lp===0?0:-4;}
  else if(POSE==="celebrate"){ll=Math.sin(s.ht)>0?-3:0;lr=Math.sin(s.ht)>0?0:-3;}
  // 3D legs with gradient
  var lgL=ctx.createLinearGradient(ax-7,ay-16,ax-1,ay);
  lgL.addColorStop(0,'#444466');lgL.addColorStop(1,'#222233');
  ctx.fillStyle=lgL;ctx.fillRect(Math.round(ax-7),Math.round(ay-16+ll),6,16);
  ctx.fillStyle='#22222a';ctx.fillRect(Math.round(ax-7),Math.round(ay-3+ll),6,3);
  var lgR=ctx.createLinearGradient(ax+1,ay-16,ax+7,ay);
  lgR.addColorStop(0,'#444466');lgR.addColorStop(1,'#222233');
  ctx.fillStyle=lgR;ctx.fillRect(Math.round(ax+1),Math.round(ay-16+lr),6,16);
  ctx.fillStyle='#22222a';ctx.fillRect(Math.round(ax+1),Math.round(ay-3+lr),6,3);
  // 3D body
  var bg=ctx.createLinearGradient(ax-9,ay-34,ax+9,ay-14);
  bg.addColorStop(0,'#5fa0e0');bg.addColorStop(0.5,'#4f8ecb');bg.addColorStop(1,'#3a6fa0');
  ctx.fillStyle=bg;ctx.fillRect(Math.round(ax-9),Math.round(ay-34),18,20);
  ctx.fillStyle='#33618f';ctx.fillRect(Math.round(ax-9),Math.round(ay-34),18,3);
  dr(ax+3,ay-20,5,5,'#1a2538');
  var al=8,ar=-8;
  if(POSE==="talk")ar=-60+Math.sin(s.aw)*35;
  else if(POSE==="reach")ar=70;
  else if(POSE==="celebrate"){al=150+Math.sin(s.ht)*10;ar=-150-Math.sin(s.ht)*10;}
  else if(POSE==="hug"){al=-55;ar=55;}
  else if(POSE==="kiss"){al=-50;ar=50;}
  else if(s.w){al=s.lp===0?30:-20;ar=s.lp===0?-20:30;}
  da(ax-9,ay-32,al,'#33618f');da(ax+9,ay-32,ar,'#33618f');
  if(HP&&POSE==="reach"){
    var px=ax+12,py=ay-40;
    ctx.fillStyle='#fffef5';ctx.fillRect(px-8,py-10,16,20);
    ctx.strokeStyle='#ffb6c1';ctx.lineWidth=1;ctx.strokeRect(px-8,py-10,16,20);
    ctx.fillStyle='#ff6f91';ctx.fillRect(px-3,py-3,3,3);ctx.fillRect(px+3,py-3,3,3);ctx.fillRect(px-4,py,10,3);ctx.fillRect(px-1,py+3,5,2);
    if(tc%3===0)addSparkle(px,py-10);
  }
  // 3D head
  var hg=ctx.createRadialGradient(ax,ay-46,2,ax,ay-42,12);
  hg.addColorStop(0,'#ffe8cc');hg.addColorStop(1,'#ffd9b3');
  ctx.fillStyle=hg;ctx.fillRect(Math.round(ax-8),Math.round(ay-50),16,16);
  dr(ax-9,ay-54,18,6,'#4a2c17');dr(ax-9,ay-50,3,10,'#4a2c17');dr(ax+6,ay-50,3,10,'#4a2c17');
  if(POSE==="kiss"&&s.ki){dr(ax-4,ay-46,2,2,'#2c2c54');dr(ax+2,ay-46,1,1,'#2c2c54');dr(ax-2,ay-40,4,2,'#a14a5c');}
  else{dr(ax-5,ay-42,2,2,'#2c2c54');dr(ax+3,ay-42,2,2,'#2c2c54');var mh=(POSE==="talk"&&s.mo)?3:1;dr(ax-3,ay-37,6,mh,'#a14a5c');}
  if(SH){
    var hy=ay-66-Math.sin(tc/7)*5,hx=ax+12;
    ctx.fillStyle='#ff6f91';ctx.fillRect(hx,hy,3,3);ctx.fillRect(hx+4,hy,3,3);ctx.fillRect(hx-1,hy+3,9,3);ctx.fillRect(hx+1,hy+6,5,2);
    if(tc%6===0)addSparkle(hx+3,hy);
  }
}

function dG(ax,gy,s){
  var bob=Math.sin(tc/8)*1.8,ay=gy+bob;
  draw3DShadow(ax,ay+16);
  var ll=0,lr=0;
  if(s.w){ll=s.lp===0?-4:0;lr=s.lp===0?0:-4;}
  dr(ax-5,ay-8+ll,4,10,'#ffd9b3');dr(ax+1,ay-8+lr,4,10,'#ffd9b3');
  dr(ax-5,ay-2+ll,4,3,'#FF1493');dr(ax+1,ay-2+lr,4,3,'#FF1493');
  var dg=ctx.createLinearGradient(ax-9,ay-26,ax+9,ay-6);
  dg.addColorStop(0,'#FF8cc4');dg.addColorStop(0.5,'#FF69B4');dg.addColorStop(1,'#e05590');
  ctx.fillStyle=dg;ctx.fillRect(Math.round(ax-9),Math.round(ay-26),18,20);
  ctx.fillStyle='#FF1493';ctx.fillRect(Math.round(ax-9),Math.round(ay-26),18,3);
  dr(ax-7,ay-38,14,14,'#FF69B4');dr(ax-7,ay-38,14,2,'#FF1493');
  var al=8,ar=-8;
  if(POSE==="hug"){al=-45;ar=45;}
  else if(POSE==="kiss"){al=-40;ar=40;}
  else if(s.w){al=s.lp===0?30:-20;ar=s.lp===0?-20:30;}
  da(ax-7,ay-36,al,'#FF1493');da(ax+7,ay-36,ar,'#FF1493');
  var hg=ctx.createRadialGradient(ax,ay-48,2,ax,ay-44,12);
  hg.addColorStop(0,'#ffe8cc');hg.addColorStop(1,'#ffd9b3');
  ctx.fillStyle=hg;ctx.fillRect(Math.round(ax-8),Math.round(ay-52),16,16);
  dr(ax-9,ay-56,18,7,'#8B4513');dr(ax-9,ay-52,3,10,'#8B4513');dr(ax+6,ay-52,3,10,'#8B4513');
  dr(ax-12,ay-53,4,6,'#8B4513');dr(ax+8,ay-53,4,6,'#8B4513');
  if(POSE==="kiss"&&s.ki){dr(ax-3,ay-46,2,2,'#2c2c54');dr(ax+1,ay-46,1,1,'#2c2c54');dr(ax-2,ay-40,4,2,'#a14a5c');}
  else{dr(ax-5,ay-44,3,3,'#2c2c54');dr(ax+2,ay-44,3,3,'#2c2c54');dr(ax-6,ay-46,1,2,'#2c2c54');dr(ax+5,ay-46,1,2,'#2c2c54');dr(ax-2,ay-39,5,2,'#a14a5c');}
  ctx.fillStyle='rgba(255,150,150,0.5)';ctx.fillRect(ax-7,ay-41,3,2);ctx.fillRect(ax+4,ay-41,3,2);
  if(SH){
    var hy=ay-68-Math.sin(tc/7+1)*4,hx=ax-8;
    ctx.fillStyle='#ff6f91';ctx.fillRect(hx,hy,3,3);ctx.fillRect(hx+4,hy,3,3);ctx.fillRect(hx-1,hy+3,9,3);ctx.fillRect(hx+1,hy+6,5,2);
  }
}

function sh(x,y){
  var c=document.getElementById('fh');if(!c)return;
  var h=document.createElement('div');h.className='hp';
  h.textContent=['❤️','💕','💖','💗','💝','✨','🌟','💫'][Math.floor(Math.random()*8)];
  h.style.left=x+'px';h.style.top=y+'px';
  c.appendChild(h);
  setTimeout(function(){if(h.parentNode)h.parentNode.removeChild(h);},3100);
}

function tick(){
  tc++;boy.aw+=0.45;boy.ht+=0.35;girl.aw+=0.42;girl.ht+=0.33;
  if(POSE==="kiss"){boy.kf++;girl.kf++;if(boy.kf>40){boy.ki=true;girl.ki=true;}}
  if(boy.w){boy.x+=2.4;if(boy.x>=boy.tx){boy.x=boy.tx;boy.w=false;}if(tc%2===0)boy.lp=1-boy.lp;}
  if(girl.w){girl.x-=2.0;if(girl.x<=girl.tx){girl.x=girl.tx;girl.w=false;}if(tc%2===0)girl.lp=1-girl.lp;}
  if(POSE==="talk"&&tc%3===0)boy.mo=!boy.mo;
  if((POSE==="hug"||POSE==="kiss"||POSE==="celebrate")&&tc%5===0){
    var sw=document.getElementById('sceneWrap');if(sw){var r=sw.getBoundingClientRect();sh((boy.x/W)*r.width,(GY/H)*r.height-40);sh((girl.x/W)*r.width,(GY/H)*r.height-40);}
  }
  ctx.clearRect(0,0,W,H);
  // 3D sky gradient
  var sky=ctx.createLinearGradient(0,0,0,H*0.55);
  sky.addColorStop(0,'#d4eeff');sky.addColorStop(1,'#a3d5f0');
  ctx.fillStyle=sky;ctx.fillRect(0,0,W,H*0.55);
  // Clouds with shadow
  ctx.fillStyle='rgba(255,255,255,0.7)';ctx.fillRect(15,10,30,8);ctx.fillRect(20,5,20,6);
  ctx.fillStyle='rgba(255,255,255,0.5)';ctx.fillRect(W-50,18,28,7);ctx.fillRect(W-45,13,18,6);
  dB(boy.x,GY,boy);if(SG)dG(girl.x,GY,girl);
  drawSparkles();
}
setInterval(tick,1000/60);

var te=document.getElementById('dt'),ae=document.getElementById('da'),dca=document.getElementById('dca');
function tl(line){te.textContent="";ae.style.display="none";tc2=false;var i=0;if(tt)clearInterval(tt);tt=setInterval(function(){te.textContent+=line.charAt(i);i++;if(i>=line.length){clearInterval(tt);tt=null;tc2=true;ae.style.display="block";}},22);}
function ad(){if(!tc2){if(tt)clearInterval(tt);tt=null;te.textContent=dl[cli];tc2=true;ae.style.display="block";return;}if(cli<dl.length-1){cli++;tl(dl[cli]);}}
if(dl&&dl.length>0)tl(dl[0]);if(dca)dca.addEventListener('click',ad);
</script></body></html>
"""

def render_scene(pose="idle", dialogue=None, show_heart=False, show_girl=False, holding_photo=False, scene_w=420, scene_h=260, canvas_w=140, canvas_h=110, scale=3):
    if isinstance(dialogue, str):
        dialogue = [dialogue]
    html = RPG_HTML
    html = html.replace("SW", str(scene_w))
    html = html.replace("SH", str(scene_h))
    html = html.replace("CW2", str(canvas_w))
    html = html.replace("CH2", str(canvas_h))
    html = html.replace("CW", str(canvas_w * scale))
    html = html.replace("CH", str(canvas_h * scale))
    html = html.replace("PV", pose)
    html = html.replace("SHV", "true" if show_heart else "false")
    html = html.replace("SGV", "true" if show_girl else "false")
    html = html.replace("HPV", "true" if holding_photo else "false")
    html = html.replace("DIAV", json.dumps(dialogue) if dialogue else "null")
    html = html.replace("DD", "block" if dialogue else "none")
    components.html(html, height=scene_h + 10, scrolling=False)

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

st.markdown('<div class="title-banner"><h1 class="float-3d">🎀 Happy Birthday, Pikku! 🎂</h1></div>', unsafe_allow_html=True)
step_dots()

# ===== STEP 1 =====
if st.session_state.current_step == 1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 💬 A Special Visitor Arrives")
    safe_audio(BG_MUSIC_PATH)
    s = st.session_state.step1_stage
    if s == "idle":
        render_scene(pose="walk", dialogue=["...", "Click the button below to talk to him!"])
    elif s == "talking":
        render_scene(pose="talk", dialogue=[GREETING_LINE])
    st.write("")
    c1, c2, c3 = st.columns([1, 2, 1])
    if s == "idle":
        with c2:
            if st.button("💬 Talk to him", use_container_width=True, key="b1"):
                st.session_state.step1_stage = "talking"
                st.rerun()
    elif s == "talking":
        with c2:
            if st.button("Next Step ➡️", use_container_width=True, key="b1n"):
                st.session_state.current_step = 2
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ===== STEP 2 =====
elif st.session_state.current_step == 2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🎁 Pocket Photo Surprise!")
    idx = st.session_state.step2_idx
    total = len(POCKET_PHOTOS)
    done = idx >= total
    if not done:
        ph = POCKET_PHOTOS[idx]
        cap = ph['caption']
        render_scene(pose="reach", holding_photo=True, dialogue=[f"Photo {idx+1} of {total}: {cap}"])
        st.write("")
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if idx == 0 and not st.session_state.step2_show:
                if st.button("🎁 Pull photo from pocket", use_container_width=True, key="bp"):
                    st.session_state.step2_show = True
                    st.session_state.step2_just = True
                    st.rerun()
            elif st.session_state.step2_show:
                lab = "📸 Show Next Photo" if idx < total - 1 else "📸 View Final Photo"
                if st.button(lab, use_container_width=True, key=f"bn{idx}"):
                    st.session_state.step2_idx += 1
                    st.session_state.step2_just = True
                    st.rerun()
        if st.session_state.step2_just:
            st.balloons()
            st.session_state.step2_just = False
        if st.session_state.step2_show:
            st.write("")
            st.markdown(f"#### Photo {idx+1}: {cap}")
            st.markdown('<div class="pocket-photo-new">', unsafe_allow_html=True)
            safe_image(ph["path"], cap)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        render_scene(pose="celebrate", show_heart=True, dialogue=["That's all the memories!", "What a beautiful collection! 💗"])
        st.write("")
        st.markdown("#### ✨ All Photos Shown! ✨")
        cols = st.columns(min(total, 4))
        for i, ph in enumerate(POCKET_PHOTOS):
            with cols[i % len(cols)]:
                safe_image(ph["path"], ph["caption"])
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("Proceed to Next Step ➡️", use_container_width=True, key="b2n"):
                st.session_state.current_step = 3
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ===== STEP 3 =====
elif st.session_state.current_step == 3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🎬 Cute Videos")
    vc = st.columns(2)
    for col, path, lab in zip(vc, VIDEO_PATHS, ["Cute Clip 1", "Cute Clip 2"]):
        with col:
            st.markdown(f"**{lab}**")
            safe_video(path
