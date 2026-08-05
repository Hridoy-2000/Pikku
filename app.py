import streamlit as st
import streamlit.components.v1 as components
import time
import random
import base64
from PIL import Image
import io

# Page configuration
st.set_page_config(
    page_title="Happy Birthday Pikku! 🎂",
    page_icon="🎉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for the entire app
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background: linear-gradient(135deg, #ffdde1 0%, #ee9ca7 100%);
    }
    
    /* Glassmorphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        border: 2px solid rgba(255, 182, 193, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b9d, #c44569);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 50px;
        font-size: 18px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 107, 157, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 157, 0.5);
    }
    
    /* Progress bar styling */
    .progress-container {
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'animation_triggered' not in st.session_state:
    st.session_state.animation_triggered = False
if 'photo_revealed' not in st.session_state:
    st.session_state.photo_revealed = False
if 'finale_triggered' not in st.session_state:
    st.session_state.finale_triggered = False

def generate_html5_canvas(step, action="idle"):
    """Generate HTML5 canvas with animated 2D sprites"""
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 0;
                overflow: hidden;
                background: transparent;
            }}
            #gameCanvas {{
                background: transparent;
                display: block;
            }}
            .speech-bubble {{
                position: absolute;
                top: 10%;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 20px 30px;
                border: 3px solid #ffb6c1;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                font-family: 'Comic Sans MS', cursive;
                font-size: 18px;
                color: #c44569;
                display: none;
                z-index: 100;
                max-width: 400px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <canvas id="gameCanvas"></canvas>
        <div class="speech-bubble" id="speechBubble"></div>
        
        <script>
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            const speechBubble = document.getElementById('speechBubble');
            
            // Set canvas size
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            
            // Animation state
            let boyX = -100;
            let boyY = canvas.height / 2 - 50;
            let girlX = canvas.width + 100;
            let girlY = canvas.height / 2 - 50;
            let frameCount = 0;
            let animationPhase = "{action}";
            let photoScale = 0;
            let photoY = canvas.height / 2;
            let particles = [];
            
            // Character drawing functions
            function drawBoy(x, y, frame, action) {{
                ctx.save();
                ctx.translate(x, y);
                
                // Body
                ctx.fillStyle = '#4A90E2';
                ctx.fillRect(15, 40, 30, 40);
                
                // Head
                ctx.fillStyle = '#FFE0BD';
                ctx.beginPath();
                ctx.arc(30, 25, 20, 0, Math.PI * 2);
                ctx.fill();
                
                // Hair
                ctx.fillStyle = '#2C1810';
                ctx.beginPath();
                ctx.arc(30, 20, 20, Math.PI, 0);
                ctx.fill();
                
                // Eyes
                ctx.fillStyle = '#000';
                ctx.beginPath();
                ctx.arc(22, 25, 3, 0, Math.PI * 2);
                ctx.arc(38, 25, 3, 0, Math.PI * 2);
                ctx.fill();
                
                // Mouth
                if (action === 'talking') {{
                    ctx.fillStyle = '#000';
                    ctx.beginPath();
                    ctx.ellipse(30, 32, 4, 3, 0, 0, Math.PI * 2);
                    ctx.fill();
                }} else {{
                    ctx.strokeStyle = '#000';
                    ctx.beginPath();
                    ctx.arc(30, 30, 5, 0, Math.PI);
                    ctx.stroke();
                }}
                
                // Arms
                ctx.strokeStyle = '#FFE0BD';
                ctx.lineWidth = 6;
                if (action === 'waving') {{
                    ctx.beginPath();
                    ctx.moveTo(15, 45);
                    ctx.lineTo(5, 20 + Math.sin(frameCount * 0.1) * 10);
                    ctx.stroke();
                }} else if (action === 'reaching') {{
                    ctx.beginPath();
                    ctx.moveTo(45, 45);
                    ctx.lineTo(55, 35);
                    ctx.stroke();
                }} else {{
                    ctx.beginPath();
                    ctx.moveTo(15, 45);
                    ctx.lineTo(5, 55);
                    ctx.stroke();
                    ctx.beginPath();
                    ctx.moveTo(45, 45);
                    ctx.lineTo(55, 55);
                    ctx.stroke();
                }}
                
                // Legs with walking animation
                ctx.strokeStyle = '#2C1810';
                ctx.lineWidth = 8;
                if (action === 'walking') {{
                    let legOffset = Math.sin(frameCount * 0.15) * 10;
                    ctx.beginPath();
                    ctx.moveTo(22, 80);
                    ctx.lineTo(22 - legOffset, 110);
                    ctx.stroke();
                    ctx.beginPath();
                    ctx.moveTo(38, 80);
                    ctx.lineTo(38 + legOffset, 110);
                    ctx.stroke();
                }} else {{
                    ctx.beginPath();
                    ctx.moveTo(22, 80);
                    ctx.lineTo(22, 110);
                    ctx.stroke();
                    ctx.beginPath();
                    ctx.moveTo(38, 80);
                    ctx.lineTo(38, 110);
                    ctx.stroke();
                }}
                
                // Shoes
                ctx.fillStyle = '#333';
                ctx.fillRect(12, 110, 20, 10);
                ctx.fillRect(28, 110, 20, 10);
                
                ctx.restore();
            }}
            
            function drawGirl(x, y, frame, action) {{
                ctx.save();
                ctx.translate(x, y);
                
                // Body
                ctx.fillStyle = '#FF69B4';
                ctx.fillRect(15, 40, 30, 40);
                
                // Head
                ctx.fillStyle = '#FFE0BD';
                ctx.beginPath();
                ctx.arc(30, 25, 20, 0, Math.PI * 2);
                ctx.fill();
                
                // Hair
                ctx.fillStyle = '#8B4513';
                ctx.beginPath();
                ctx.arc(30, 20, 20, Math.PI, 0);
                ctx.fill();
                // Ponytails
                ctx.beginPath();
                ctx.arc(12, 20, 8, 0, Math.PI * 2);
                ctx.arc(48, 20, 8, 0, Math.PI * 2);
                ctx.fill();
                
                // Eyes
                ctx.fillStyle = '#000';
                ctx.beginPath();
                ctx.arc(22, 25, 3, 0, Math.PI * 2);
                ctx.arc(38, 25, 3, 0, Math.PI * 2);
                ctx.fill();
                
                // Eyelashes
                ctx.strokeStyle = '#000';
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(19, 22);
                ctx.lineTo(17, 20);
                ctx.moveTo(25, 22);
                ctx.lineTo(24, 20);
                ctx.moveTo(35, 22);
                ctx.lineTo(34, 20);
                ctx.moveTo(41, 22);
                ctx.lineTo(43, 20);
                ctx.stroke();
                
                // Mouth
                ctx.fillStyle = '#FF6B9D';
                ctx.beginPath();
                ctx.arc(30, 32, 3, 0, Math.PI);
                ctx.fill();
                
                // Arms
                ctx.strokeStyle = '#FFE0BD';
                ctx.lineWidth = 6;
                if (action === 'hugging') {{
                    ctx.beginPath();
                    ctx.moveTo(15, 45);
                    ctx.lineTo(-10, 40);
                    ctx.stroke();
                    ctx.beginPath();
                    ctx.moveTo(45, 45);
                    ctx.lineTo(70, 40);
                    ctx.stroke();
                }} else {{
                    ctx.beginPath();
                    ctx.moveTo(15, 45);
                    ctx.lineTo(5, 55);
                    ctx.stroke();
                    ctx.beginPath();
                    ctx.moveTo(45, 45);
                    ctx.lineTo(55, 55);
                    ctx.stroke();
                }}
                
                // Dress
                ctx.fillStyle = '#FF69B4';
                ctx.beginPath();
                ctx.moveTo(15, 80);
                ctx.lineTo(45, 80);
                ctx.lineTo(55, 110);
                ctx.lineTo(5, 110);
                ctx.closePath();
                ctx.fill();
                
                // Legs
                ctx.strokeStyle = '#FFE0BD';
                ctx.lineWidth = 6;
                ctx.beginPath();
                ctx.moveTo(22, 80);
                ctx.lineTo(22, 110);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(38, 80);
                ctx.lineTo(38, 110);
                ctx.stroke();
                
                ctx.restore();
            }}
            
            function createParticle(x, y) {{
                return {{
                    x: x,
                    y: y,
                    vx: (Math.random() - 0.5) * 4,
                    vy: Math.random() * -8 - 2,
                    life: 1,
                    color: `hsl(${{Math.random() * 60 + 300}}, 100%, 75%)`,
                    size: Math.random() * 4 + 2
                }};
            }}
            
            function updateParticles() {{
                for (let i = particles.length - 1; i >= 0; i--) {{
                    let p = particles[i];
                    p.x += p.vx;
                    p.y += p.vy;
                    p.vy += 0.1;
                    p.life -= 0.02;
                    
                    if (p.life <= 0) {{
                        particles.splice(i, 1);
                    }}
                }}
            }}
            
            function drawParticles() {{
                particles.forEach(p => {{
                    ctx.save();
                    ctx.globalAlpha = p.life;
                    ctx.fillStyle = p.color;
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.restore();
                }});
            }}
            
            function drawPhoto(x, y, scale) {{
                ctx.save();
                ctx.translate(x, y);
                ctx.scale(scale, scale);
                
                // Photo frame
                ctx.fillStyle = '#FFF';
                ctx.fillRect(-50, -70, 100, 140);
                ctx.strokeStyle = '#FF69B4';
                ctx.lineWidth = 3;
                ctx.strokeRect(-50, -70, 100, 140);
                
                // Photo content (placeholder heart)
                ctx.fillStyle = '#FF6B9D';
                ctx.beginPath();
                let heartX = 0;
                let heartY = -10;
                ctx.moveTo(heartX, heartY);
                ctx.bezierCurveTo(heartX - 20, heartY - 20, heartX - 30, heartY + 10, heartX, heartY + 30);
                ctx.bezierCurveTo(heartX + 30, heartY + 10, heartX + 20, heartY - 20, heartX, heartY);
                ctx.fill();
                
                // "Memory" text
                ctx.fillStyle = '#C44569';
                ctx.font = '12px Comic Sans MS';
                ctx.textAlign = 'center';
                ctx.fillText('Memory ❤️', 0, 50);
                
                ctx.restore();
            }}
            
            // Animation loop
            function animate() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                frameCount++;
                
                // Draw gradient background
                let gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
                gradient.addColorStop(0, '#ffdde1');
                gradient.addColorStop(1, '#ee9ca7');
                ctx.fillStyle = gradient;
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                // Draw decorative elements
                for (let i = 0; i < 10; i++) {{
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
                    ctx.beginPath();
                    ctx.arc(Math.sin(frameCount * 0.02 + i) * 100 + canvas.width/2, 
                           Math.cos(frameCount * 0.02 + i) * 100 + canvas.height/2, 
                           5, 0, Math.PI * 2);
                    ctx.fill();
                }}
                
                // Animation logic based on phase
                switch(animationPhase) {{
                    case 'walking_in':
                        boyX += 2;
                        if (boyX >= canvas.width / 2 - 30) {{
                            boyX = canvas.width / 2 - 30;
                            animationPhase = 'idle';
                            // Notify Streamlit
                            window.parent.postMessage({{type: 'animation_complete', phase: 'walking_in'}}, '*');
                        }}
                        drawBoy(boyX, boyY, frameCount, 'walking');
                        break;
                        
                    case 'idle':
                        drawBoy(canvas.width / 2 - 30, boyY, frameCount, 'idle');
                        break;
                        
                    case 'talking':
                        drawBoy(canvas.width / 2 - 30, boyY, frameCount, 'talking');
                        speechBubble.style.display = 'block';
                        speechBubble.textContent = document.getElementById('dialogueText')?.value || '';
                        break;
                        
                    case 'reaching_pocket':
                        boyX = canvas.width / 2 - 50;
                        drawBoy(boyX, boyY, frameCount, 'reaching');
                        break;
                        
                    case 'photo_reveal':
                        drawBoy(canvas.width / 2 - 80, boyY, frameCount, 'idle');
                        if (photoScale < 1) {{
                            photoScale += 0.02;
                            photoY -= 2;
                        }}
                        drawPhoto(canvas.width / 2 + 50, photoY, photoScale);
                        
                        // Add celebration particles
                        if (Math.random() < 0.3) {{
                            particles.push(createParticle(canvas.width / 2, canvas.height / 2));
                        }}
                        break;
                        
                    case 'double_entry':
                        if (boyX < canvas.width / 3) boyX += 2;
                        if (girlX > canvas.width * 2/3) girlX -= 2;
                        drawBoy(boyX, boyY, frameCount, 'walking');
                        drawGirl(girlX, girlY, frameCount, 'walking');
                        
                        if (boyX >= canvas.width / 3 && girlX <= canvas.width * 2/3) {{
                            animationPhase = 'approaching';
                        }}
                        break;
                        
                    case 'approaching':
                        if (boyX < canvas.width / 2 - 30) boyX += 1.5;
                        if (girlX > canvas.width / 2 + 30) girlX -= 1.5;
                        drawBoy(boyX, boyY, frameCount, 'walking');
                        drawGirl(girlX, girlY, frameCount, 'walking');
                        
                        if (boyX >= canvas.width / 2 - 30 && girlX <= canvas.width / 2 + 30) {{
                            animationPhase = 'hugging';
                        }}
                        break;
                        
                    case 'hugging':
                        drawBoy(boyX, boyY, frameCount, 'idle');
                        drawGirl(girlX, girlY, frameCount, 'hugging');
                        
                        // Heart particles
                        if (Math.random() < 0.5) {{
                            let midX = (boyX + girlX) / 2;
                            let midY = boyY;
                            particles.push(createParticle(midX, midY));
                        }}
                        
                        speechBubble.style.display = 'block';
                        speechBubble.textContent = document.getElementById('finalMessage')?.textContent || '';
                        break;
                }}
                
                updateParticles();
                drawParticles();
                
                requestAnimationFrame(animate);
            }}
            
            // Start animation
            animate();
            
            // Handle messages from Streamlit
            window.addEventListener('message', function(event) {{
                if (event.data.type === 'set_phase') {{
                    animationPhase = event.data.phase;
                }}
                if (event.data.type === 'set_dialogue') {{
                    let dialogueEl = document.getElementById('dialogueText');
                    if (!dialogueEl) {{
                        dialogueEl = document.createElement('input');
                        dialogueEl.type = 'hidden';
                        dialogueEl.id = 'dialogueText';
                        document.body.appendChild(dialogueEl);
                    }}
                    dialogueEl.value = event.data.text;
                }}
            }});
            
            // Handle window resize
            window.addEventListener('resize', function() {{
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
            }});
        </script>
    </body>
    </html>
    """
    
    return html_content

# Main app header
st.markdown("""
<div style="text-align: center; padding: 50px 0;">
    <h1 style="color: #c44569; font-size: 48px; margin-bottom: 10px;">
        🎂 Happy Birthday Pikku! 🎉
    </h1>
    <p style="color: #ff6b9d; font-size: 20px;">
        A magical journey just for you 💖
    </p>
</div>
""", unsafe_allow_html=True)

# Progress indicator
progress_percentage = min((st.session_state.step - 1) * 25, 100)
st.markdown(f"""
<div class="progress-container">
    <div style="background: rgba(255,255,255,0.5); border-radius: 20px; height: 20px; margin: 0 50px;">
        <div style="background: linear-gradient(90deg, #ff6b9d, #c44569); width: {progress_percentage}%; 
                    height: 100%; border-radius: 20px; transition: width 0.5s ease;">
        </div>
    </div>
    <p style="text-align: center; color: #c44569; margin-top: 10px;">Step {st.session_state.step} of 5</p>
</div>
""", unsafe_allow_html=True)

# STEP 1: Boy Entrance & Greeting
if st.session_state.step == 1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display HTML5 canvas with walking animation
        if not st.session_state.animation_triggered:
            components.html(generate_html5_canvas(1, "walking_in"), height=400)
            st.session_state.animation_triggered = True
        else:
            components.html(generate_html5_canvas(1, "talking"), height=400)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding-top: 50px;">
            <h3 style="color: #c44569;">👋 A Special Visitor</h3>
            <p style="color: #666;">Someone wants to talk to you...</p>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💬 Talk to him / बात सुनो", key="talk_button", use_container_width=True):
            st.session_state.talking_started = True
            # Trigger talking animation
            dialogue_html = f"""
            <script>
                window.parent.postMessage({{type: 'set_phase', phase: 'talking'}}, '*');
                window.parent.postMessage({{type: 'set_dialogue', text: "Hi! Hey, I know your birthday is coming and you are very happy for that! 😊"}}, '*');
            </script>
            """
            components.html(dialogue_html, height=0)
            
            # Show speech bubble text
            st.markdown("""
            <div style="text-align: center; padding: 20px;">
                <div style="background: rgba(255,255,255,0.95); padding: 20px; border-radius: 20px; 
                            border: 3px solid #ffb6c1; display: inline-block; margin: 20px;">
                    <p style="font-size: 20px; color: #c44569; margin: 0;">
                        "Hi! Hey, I know your birthday is coming and you are very happy for that! 😊"
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Next step button
            if st.button("Next Step ➡️", key="next_step_1", use_container_width=True):
                st.session_state.step = 2
                st.session_state.animation_triggered = False
                st.session_state.photo_revealed = False
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 2: Interactive Story Milestones
elif st.session_state.step == 2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("""
    <h2 style="text-align: center; color: #c44569;">📖 Our Beautiful Memories</h2>
    """, unsafe_allow_html=True)
    
    # Story cards with animations
    memories = [
        {"title": "The First Hello 👋", "description": "Remember when we first met? That magical moment when our eyes met and everything changed forever...", "emoji": "✨"},
        {"title": "Laughter & Joy 😄", "description": "All those times we laughed until our stomachs hurt, creating memories that will last a lifetime.", "emoji": "💫"},
        {"title": "Adventures Together 🌟", "description": "Every adventure became special because you were there. From simple walks to grand journeys, you made everything better.", "emoji": "🌈"},
        {"title": "Birthday Magic 🎂", "description": "And now here we are, celebrating YOU - the most amazing person who deserves all the happiness in the world!", "emoji": "💝"}
    ]
    
    for i, memory in enumerate(memories):
        with st.container():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown(f"""
                <div style="text-align: center; padding: 20px;">
                    <div style="font-size: 50px;">{memory['emoji']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div style="padding: 15px; background: rgba(255,255,255,0.5); border-radius: 15px; margin: 10px 0;">
                    <h3 style="color: #c44569;">{memory['title']}</h3>
                    <p style="color: #666;">{memory['description']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Next Step ➡️", key="next_step_2", use_container_width=True):
            st.session_state.step = 3
            st.session_state.animation_triggered = False
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 3: Pocket Photo Reveal
elif st.session_state.step == 3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("""
    <h2 style="text-align: center; color: #c44569;">🎁 A Special Surprise</h2>
    """, unsafe_allow_html=True)
    
    # Display canvas with reaching animation
    if not st.session_state.photo_revealed:
        components.html(generate_html5_canvas(3, "reaching_pocket"), height=400)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 20px;">
                <p style="color: #666; font-size: 18px;">
                    He's reaching into his pocket... What could it be? 🤔
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🎁 Pull photo from pocket", key="pull_photo", use_container_width=True):
                st.session_state.photo_revealed = True
                st.balloons()
                st.rerun()
    else:
        # Photo reveal animation
        components.html(generate_html5_canvas(3, "photo_reveal"), height=500)
        
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <div style="background: rgba(255,255,255,0.95); padding: 30px; border-radius: 20px; 
                        border: 3px solid #ffb6c1; display: inline-block; margin: 20px; 
                        box-shadow: 0 10px 30px rgba(255,107,157,0.2);">
                <h2 style="color: #c44569;">📸 A Precious Memory</h2>
                <div style="font-size: 100px; padding: 20px;">💖</div>
                <p style="color: #666; font-size: 18px;">Every moment with you is worth cherishing forever!</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Next Step ➡️", key="next_step_3", use_container_width=True):
                st.session_state.step = 4
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 4: Video Showcase
elif st.session_state.step == 4:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("""
    <h2 style="text-align: center; color: #c44569;">🎬 Special Video Messages</h2>
    """, unsafe_allow_html=True)
    
    # Video placeholder with beautiful design
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
        <div style="background: rgba(0,0,0,0.05); border-radius: 20px; padding: 40px; 
                    text-align: center; min-height: 300px; display: flex; 
                    align-items: center; justify-content: center; flex-direction: column;">
            <div style="font-size: 80px;">🎥</div>
            <h3 style="color: #c44569; margin-top: 20px;">Your Birthday Video</h3>
            <p style="color: #666;">A special message from the heart 💝</p>
            <div style="margin-top: 20px;">
                <button style="background: linear-gradient(45deg, #ff6b9d, #c44569); 
                               color: white; border: none; padding: 15px 30px; 
                               border-radius: 50px; font-size: 18px; cursor: pointer;">
                    ▶️ Play Video
                </button>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Reveal Final Surprise 💖 ➡️", key="reveal_finale", use_container_width=True):
            st.session_state.step = 5
            st.session_state.animation_triggered = False
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 5: Final Finale Scene
elif st.session_state.step == 5:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    if not st.session_state.finale_triggered:
        # Double character entry animation
        components.html(generate_html5_canvas(5, "double_entry"), height=500)
        
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h2 style="color: #c44569;">💕 The Grand Finale</h2>
        </div>
        """, unsafe_allow_html=True)
        
        time.sleep(3)  # Wait for animation
        
        # Trigger hugging animation
        components.html(generate_html5_canvas(5, "approaching"), height=500)
        time.sleep(2)
        
        st.session_state.finale_triggered = True
        st.balloons()
        st.snow()
        st.rerun()
    
    else:
        # Final hugging scene with message
        components.html(generate_html5_canvas(5, "hugging"), height=500)
        
        st.markdown("""
        <div style="text-align: center; padding: 30px;">
            <div style="background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(255,220,220,0.95)); 
                        padding: 40px; border-radius: 30px; border: 3px solid #ffb6c1; 
                        box-shadow: 0 15px 40px rgba(255,107,157,0.3);
                        animation: glow 2s ease-in-out infinite alternate;">
                <h1 style="color: #c44569; font-size: 36px; margin-bottom: 20px;">
                    💖 Happy Birthday Pikku! 💖
                </h1>
                <p style="color: #666; font-size: 24px; line-height: 1.5;">
                    "Thank you for being my favorite person<br>
                    in the entire universe!<br>
                    Happy Birthday! 🎉💖"
                </p>
                <div style="font-size: 60px; margin-top: 20px;">
                    🎂 🎈 🎁 🎊 ✨
                </div>
            </div>
        </div>
        
        <style>
            @keyframes glow {{
                from {{ box-shadow: 0 0 20px rgba(255,107,157,0.3); }}
                to {{ box-shadow: 0 0 40px rgba(255,107,157,0.6); }}
            }}
        </style>
        """, unsafe_allow_html=True)
        
        # Additional celebration effects
        if st.button("🎉 Celebrate Again! 🎉", key="celebrate_again", use_container_width=True):
            st.balloons()
            st.snow()
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 30px; color: rgba(255,255,255,0.7);">
    <p>Made with 💖 specially for Pikku</p>
</div>
""", unsafe_allow_html=True)

# Auto-play background music (optional)
st.markdown("""
<script>
    // Background music can be added here if needed
    console.log('🎵 Happy Birthday Pikku! 🎵');
</script>
""", unsafe_allow_html=True)
