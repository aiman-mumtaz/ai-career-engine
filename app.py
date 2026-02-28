import streamlit as st
import json
import os
import time
import uuid
from utils.parser import extract_text_from_pdf
from utils.ai_engine import identify_persona, generate_email
from utils.mailer import send_email
import base64

def play_mario_sound(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            
        unique_id = str(uuid.uuid4())
        sound_html = f"""
            <audio id="{unique_id}" autoplay="true" style="display:none;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            <script>
                var audio = document.getElementById('{unique_id}');
                audio.volume = 0.5;
                audio.play().catch(function(error) {{
                    console.log("Autoplay blocked by browser. User must interact first.");
                }});
            </script>
        """
        st.components.v1.html(sound_html, height=0)
    except FileNotFoundError:
        st.error(f"Sound file not found: {file_path}")

SND_COIN = "sounds/super-mario-coin-sound.mp3"
SND_FIREBALL = "sounds/mario-fireball.mp3"
SND_POWER_UP = "sounds/01-power-up-mario.mp3"
SND_CLEAR = "sounds/super-mario-kart-mario-wins.mp3"
SND_GAME_OVER = "sounds/super-mario-death-sound-sound-effect.mp3"
SND_BEGIN = "sounds/super-mario-bros-music.mp3"


st.set_page_config(page_title="Super Liaison World", page_icon="🍄", layout="wide")
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

        .stApp {
            background-color: #5C94FC !important;
            background-image: url('https://www.transparenttextures.com/patterns/8-bit-mario.png') !important;
        }

        header, [data-testid="stHeader"], [data-testid="collapsedControl"], [data-testid="stSidebar"] {
            display: none !important;
            visibility: hidden !important;
        }
        .mario-ground {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 40px;
            background-color: #E7693E;
            background-image: url('https://www.transparenttextures.com/patterns/brick-wall.png');
            border-top: 4px solid #000;
            z-index: 1000;
        }

        /* 4. YELLOW QUESTION BLOCKS (Mission Results) */
        /* Targets the status boxes for company matches */
        div[data-testid="stStatusContainer"], 
        div[data-testid="stStatus"] {
            background-color: #f7d016 !important; 
            border: 4px solid #000 !important;
            border-radius: 0px !important;
            box-shadow: 4px 4px 0px #000 !important;
        }

        /* Ensure text inside Yellow Blocks is black for readability */
        div[data-testid="stStatus"] * {
            color: black !important;
            text-shadow: none !important;
            font-family: 'Press Start 2P', cursive !important;
            font-size: 10px !important;
        }

        /* 5. NATIVE UPLOADER (Restored to White) */
        [data-testid="stFileUploadDropzone"] {
            background-color: #FFFFFF !important;
            border: 2px dashed #999 !important;
            border-radius: 10px !important;
        }

        /* 6. GLOBAL TEXT STYLING */
        h1, h2, h3, p, label, .stMarkdown span {
            font-family: 'Press Start 2P', cursive !important;
            color: white !important;
            text-shadow: 2px 2px 0px #000 !important;
        }

        /* 7. BRICK BUTTONS */
        .stButton>button {
            background-color: #E7693E !important;
            border: 4px solid #000 !important;
            box-shadow: 6px 6px 0px #000;
            color: white !important;
            font-family: 'Press Start 2P';
            border-radius: 0px !important;
        }
    </style>
    
    <div class="mario-ground"></div>
    """, unsafe_allow_html=True)

# if 'game_started' not in st.session_state:
#     st.session_state.game_started = False

# if not st.session_state.game_started:
#     # Center the start button
#     st.write("# 🍄 SUPER LIAISON WORLD")
#     st.write("### [ PRESS START TO BEGIN ]")
    
#     if st.button("🕹️ START MISSION"):
#         play_mario_sound(SND_BEGIN)
#         st.session_state.game_started = True
#         st.info("Level Loading... Click again to enter.") 
#     st.stop()
if 'game_started' not in st.session_state:
    st.session_state.game_started = False

if not st.session_state.game_started:
    st.write("# 🍄 SUPER LIAISON WORLD")
    st.write("### [ PRESS START TO BEGIN ]")
    
    if st.button("🕹️ START MISSION"):
        play_mario_sound(SND_BEGIN)
    # play_mario_sound(SND_BEGIN)
        st.session_state.game_started = True
    st.stop()
# st.sidebar.markdown("### 🎮 Controller")
# testing_mode = st.sidebar.toggle("Testing Mode (Safety Bubble)", value=True)
# test_email = st.sidebar.text_input("Player Email", value="your@email.com")

# if testing_mode:
#     st.sidebar.info("Power-up active: Emails are redirected to you.")

st.title("Super Liason")


with st.container():
    st.markdown('<div class="controller-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("🎮 CONTROLLER")
        testing_mode = st.toggle("TEST MODE", value=True)
        if testing_mode:
            # st.markdown(":small[Power-up active: Emails are redirected to you.]")
            st.markdown('<p style="font-size: 8px; text-align: left; font-color: black">Power-up active: Emails are redirected to you.</p>', unsafe_allow_html=True)
    with col2:
        test_email = st.text_input("TEST PLAYER EMAIL", value="your@email.com", disabled=not testing_mode)
    st.markdown('</div>', unsafe_allow_html=True)



st.subheader("Level 1-1: The Job Hunt")

if os.path.exists("company_db.json"):
    with open("company_db.json", "r") as f:
        master_list = json.load(f)
else:
    st.error("MISSING DATABASE! GO TO BOWSER'S CASTLE.")
    st.stop()

uploaded_resume = st.file_uploader("📥 DROP YOUR WARP PIPE (RESUME)", type="pdf")

if uploaded_resume:
    if 'powerup_played' not in st.session_state:
        play_mario_sound(SND_POWER_UP)
        st.session_state.powerup_played = True

# if uploaded_resume and 'audio_played' not in st.session_state:
#     play_mario_sound(SND_POWER_UP)
#     st.session_state.audio_played = True
    uploaded_resume.seek(0)
    resume_bytes = uploaded_resume.read()
    resume_text = extract_text_from_pdf(resume_bytes)
    st.success("🍄 POWER-UP INGESTED : RESUME PARSED!")
    # print(resume_text[:500])
    if st.button("START MISSION (Match & Send)"):
        play_mario_sound(SND_COIN)
        # st.session_state.matches_found = True
        with st.spinner("🍄 EATING MUSHROOMS... ANALYSING PROFILE..."):
            identified_persona = identify_persona(resume_text)
            # print(f"Identified Persona: {matched_names}")
            st.write(f"### MISSION TYPE: {identified_persona}")
            # play_mario_sound(SND_POWER_UP)
            # matches = [c for c in master_list if c['name'] in matched_names]
            matches = [
            c for c in master_list 
            if 'roles' in c and identified_persona in c['roles']
        ]
            # print(master_list)
        # print(f"Matches: {[m['name'] for m in matches]}")
        if not matches:
            st.warning("GAME OVER: NO MATCHES FOUND IN THIS WORLD.")
        else:
            # st.write(f"### MISSION TYPE: {identified_persona}")
            st.write(f"Found **{len(matches)}** suitable companies for you.")
            
        
            for i, company in enumerate(matches):
    
                with st.status(f"❓ BLOCK: {company['name']}", expanded=False):
                    st.write("Generating Fireball (Email)...")
                    
                    subject, body = generate_email(resume_text, company['name'], company['industry'])
                    # st.write(f"**Subject:** {subject}")
                    target_recipient = test_email if testing_mode else company['email']
                    try:
                        send_email(target_recipient, subject, body, resume_bytes, uploaded_resume.name)
                        st.write(f"✅ Fireball sent to {target_recipient}!")
                        play_mario_sound(SND_FIREBALL)
                        time.sleep(0.5)
                    except Exception as e:
                        st.error(f"Mission Failed: {e}")
                        play_mario_sound(SND_GAME_OVER)
                        st.stop()
            
            st.write("### LEVEL COMPLETE")
            play_mario_sound(SND_CLEAR)
            st.balloons()