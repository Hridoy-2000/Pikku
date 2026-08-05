import streamlit as st
import requests
from streamlit_lottie import st_lottie

# 1. Page Configuration
st.set_page_config(page_title="Happy Birthday My Love! 💕", page_icon="💖", layout="centered")

# 2. Pink Aesthetic & Custom Styling
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #ffdde1 0%, #ee9ca7 100%) !important;
    background-attachment: fixed !important;
}
.cute-card {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 18px;
    box-shadow: 0 8px 20px rgba(238, 156, 167, 0.3);
    border: 2px solid #ffb6c1;
}
.cute-card h4 {
    color: #d63384 !important;
    margin-bottom: 8px;
    font-size: 20px;
}
.cute-card p {
    color: #4a4a4a !important;
    font-size: 16px;
}
.speech-bubble {
    position: relative;
    background: #ff69b4;
    border-radius: 25px;
    padding: 18px 25px;
    color: white;
    font-size: 19px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0 6px 15px rgba(255, 105, 180, 0.4);
}
.speech-bubble:after {
    content: '';
    position: absolute;
    bottom: -15px;
    left: 50%;
    width: 0;
    height: 0;
    border: 15px solid transparent;
    border-top-color: #ff69b4;
    border-bottom: 0;
    margin-left: -15px;
}
h1 {
    color: #c71585 !important;
    text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.8);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Helper function to load Lottie animations
def load_lottieurl(url: str):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

# Load 2D Character Poses & Animations
char_idle = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_cK18G1.json")
char_happy = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_dn3m9zxb.json")
lottie_bear = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_u4yrau.json")

st.title("🎂 Happy Birthday My Love! 💕✨")

# Navigation Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎮 1. RPG Intro", 
    "📜 2. Our 4 Days", 
    "📸 3. Surprise Screen", 
    "🎬 4. Cute Videos", 
    "💌 5. Thank You"
])

# --- TAB 1: 2D RPG Character Dialogue System ---
with tab1:
    if "step" not in st.session_state:
        st.session_state.step = 0

    dialogues = [
        {
            "anim": char_idle,
            "text": "Hey there! Ready to start our special birthday quest? 🎮",
            "options": [("Yes, let's go! ✨", 1), ("Tell me more first! 🤔", 1)]
        },
        {
            "anim": char_happy,
            "text": "Yay! I created this entire world just for you today! 💕",
            "options": [("Aww, thank you! ❤️", 2), ("Show me the surprises! 🎁", 2)]
        },
        {
            "anim": char_idle,
            "text": "Explore all the tabs above to see our memory story, photos, and videos!",
            "options": [("Restart Story 🔄", 0)]
        }
    ]

    current = dialogues[st.session_state.step]

    # Speech Bubble & Animated Character
    st.markdown(f'<div class="speech-bubble">"{current["text"]}"</div>', unsafe_allow_html=True)
    if current["anim"]:
        st_lottie(current["anim"], height=220, key=f"rpg_char_{st.session_state.step}")

    # Interactive Choice Buttons
    st.write("---")
    cols = st.columns(len(current["options"]))
    for idx, (label, next_step) in enumerate(current["options"]):
        if cols[idx].button(label, key=f"btn_{st.session_state.step}_{idx}"):
            st.session_state.step = next_step
            st.rerun()

    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

# --- TAB 2: Love Story & 4 Special Days ---
with tab2:
    st.subheader("💖 Why You Mean The World To Me")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="cute-card">
            <h4>🌸 Day 1: First Impression</h4>
            <p>The moment you entered my life, everything instantly felt brighter and happier.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="cute-card">
            <h4>🌷 Day 2: Getting Closer</h4>
            <p>Every conversation made me realize how uniquely caring you are.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="cute-card">
            <h4>🌺 Day 3: Falling In Love</h4>
            <p>I knew right here that you were the person I want to hold close forever.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="cute-card">
            <h4>🎀 Day 4: Always & Forever</h4>
            <p>No matter what, I am standing right beside you with all my heart!</p>
        </div>
        """, unsafe_allow_html=True)

# --- TAB 3: Pull Slider Screen ---
with tab3:
    st.subheader("📸 Pull the Slider to Unlock Memories!")
    pull_slider = st.slider("Drag to pull open the curtain! 💖 👉", 0, 100, 0)
    
    if pull_slider >= 50:
        st.success("🎉 Surprise Unlocked!")
        st.balloons()
        st.image("https://images.unsplash.com/photo-1518199266791-5375a83190b7?w=600", caption="Reason #1: Your gorgeous smile that lights up every room.")
        st.image("https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?w=600", caption="Reason #2: The way you care about every little detail.")
    else:
        st.warning("Slide to at least 50% to pull open the surprise!")

# --- TAB 4: Cute Videos ---
with tab4:
    st.subheader("🎬 Cute Clips & Music")
    st.video("https://www.w3schools.com/html/mov_bbb.mp4")

# --- TAB 5: Thank You ---
with tab5:
    st.subheader("💖 Thank You For Being You!")
    if lottie_bear:
        st_lottie(lottie_bear, height=200, key="bear")
    st.balloons()
    st.markdown("### You are my favorite person in the entire universe. Happy Birthday! 🎉💖")import streamlit as st
import requests
from streamlit_lottie import st_lottie

# Page setup
st.set_page_config(page_title="Happy Birthday My Love! ❤️", page_icon="🎂", layout="centered")

# Custom CSS for Speech Bubbles & Cards
st.markdown("""
<style>
.speech-bubble {
    position: relative;
    background: #ff4b4b;
    border-radius: 15px;
    padding: 15px 20px;
    color: white;
    font-size: 18px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}
.speech-bubble:after {
    content: '';
    position: absolute;
    bottom: -15px;
    left: 50%;
    width: 0;
    height: 0;
    border: 15px solid transparent;
    border-top-color: #ff4b4b;
    border-bottom: 0;
    margin-left: -15px;
}
.card {
    background-color: #ffffff;
    border-left: 5px solid #ff4b4b;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# Helper function to load animations
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load cute animations
lottie_cute = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_cK18G1.json")
lottie_heart = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_dn3m9zxb.json")

st.title("🎂 Happy Birthday My Love! 🎉")

# Interactive Multi-Stage Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎭 1. The Welcome", 
    "📜 2. Our 4 Days", 
    "📸 3. Photo Gallery", 
    "🎬 4. Cute Videos", 
    "💌 5. Thank You"
])

# --- TAB 1: Animated Character & Speech Bubble ---
with tab1:
    st.write("### A special voice message for you!")
    
    # Speech bubble above the character
    st.markdown('<div class="speech-bubble">"Hey there! I have a super special message for you today. Press play on the audio below to hear me!"</div>', unsafe_allow_html=True)
    
    # Animated Character
    if lottie_cute:
        st_lottie(lottie_cute, height=220, key="character")
    
    # Audio / Voice Recording
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

# --- TAB 2: Love Story & 4 Special Days ---
with tab2:
    st.subheader("How Much You Mean To Me ❤️")
    st.write("Here is what makes you so special every single day:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="card">
            <h4>Day 1: The First Impression</h4>
            <p style="color: black;">The moment you came into my life, everything felt brighter and happier.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h4>Day 2: Getting Closer</h4>
            <p style="color: black;">I realized how sweet, caring, and amazingly genuine you really are.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <h4>Day 3: Growing Love</h4>
            <p style="color: black;">Every conversation with you showed me how much you truly mean to me.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h4>Day 4: Forever & Always</h4>
            <p style="color: black;">I will always be right here by your side, supporting and loving you.</p>
        </div>
        """, unsafe_allow_html=True)

# --- TAB 3: Pull-to-Reveal Photo Screen ---
with tab3:
    st.subheader("📸 Pull the Slider to Unlock Memories!")
    
    pull_slider = st.slider("Drag the slider to pull open the curtain! 👉", 0, 100, 0)
    
    if pull_slider >= 50:
        st.success("🎉 Memories Unlocked!")
        st.balloons()
        
        st.image("https://images.unsplash.com/photo-1518199266791-5375a83190b7?w=600", caption="Reason #1: Your gorgeous smile that lights up every room.")
        st.image("https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?w=600", caption="Reason #2: How kind and thoughtful you are to everyone.")
    else:
        st.warning("Slide to at least 50% to pull open the screen!")

# --- TAB 4: Cute Videos & Music ---
with tab4:
    st.subheader("🎬 Favorite Clips & Music")
    st.video("https://www.w3schools.com/html/mov_bbb.mp4")
    st.caption("A cute special video dedicated to you! ❤️")

# --- TAB 5: Thank You ---
with tab5:
    st.subheader("💖 Thank You For Everything!")
    if lottie_heart:
        st_lottie(lottie_heart, height=200, key="heart")
    st.balloons()
    st.markdown("### You are the most precious person in my life. Happy Birthday! 🎉")
