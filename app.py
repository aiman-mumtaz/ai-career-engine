import streamlit as st
import json
import os
import time
import uuid
import base64
from utils.parser import extract_text_from_pdf
from utils.ai_engine import identify_persona, generate_email
from utils.mailer import send_email

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
    except Exception: pass

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
        }

        .mario-ground {
            position: fixed; bottom: 0; left: 0; width: 100%; height: 40px;
            background-color: #E7693E;
            background-image: url('https://www.transparenttextures.com/patterns/brick-wall.png');
            border-top: 4px solid #000; z-index: 1000;
        }

        /* YELLOW QUESTION BLOCKS - Force Color & Kill Overlap */
        [data-testid="stStatus"], [data-testid="stStatusContainer"], [data-testid="stStatus"] > details {
            background-color: #f7d016 !important; 
            border: 4px solid #000 !important;
            box-shadow: 4px 4px 0px #000 !important;
        }
        [data-testid="stStatus"] summary { background-color: #f7d016 !important; }
        
        /* Hides the 'arrow' and 'Running/Success' icons */
        [data-testid="stStatus"] summary svg, 
        [data-testid="stStatus"] summary div[role="img"],
        [data-testid="stStatus"] summary span:not(:first-child) {
            display: none !important;
            visibility: hidden !important;
        }

        [data-testid="stStatus"] * {
            color: black !important;
            text-shadow: none !important;
            font-family: 'Press Start 2P', cursive !important;
        }

        h1, h2, h3, p, label, .stMarkdown span {
            font-family: 'Press Start 2P', cursive !important;
            color: white !important;
            text-shadow: 2px 2px 0px #000 !important;
        }

        .stButton>button {
            background-color: #E7693E !important;
            border: 4px solid #000 !important;
            box-shadow: 6px 6px 0px #000;
            color: white !important;
            font-family: 'Press Start 2P';
        }
    </style>
    <div class="mario-ground"></div>
    """, unsafe_allow_html=True)

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
    # st.markdown('<div class="controller-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("🎮 CONTROLLER")
        testing_mode = st.toggle("TEST MODE", value=True)
        if testing_mode:
            # st.markdown(":small[Power-up active: Emails are redirected to you.]")
            st.markdown('<p style="font-size: 8px; text-align: left; font-color: black">Power-up active: Emails are redirected to you.</p>', unsafe_allow_html=True)
    with col2:
        test_email = st.text_input("TEST PLAYER EMAIL", value="aimanmumtaz001@gmail.com", disabled=not testing_mode)
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
    # uploaded_resume.seek(0)
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
            play_mario_sound(SND_POWER_UP)
            # matches = [c for c in master_list if c['name'] in matched_names]
            matches = [
            c for c in master_list 
            if 'roles' in c and identified_persona in c['roles']
        ]
            # print(master_list)
        # print(f"Matches: {[m['name'] for m in matches]}")
        if not matches:
            st.warning("GAME OVER: NO MATCHES FOUND IN THIS WORLD.")
            play_mario_sound(SND_GAME_OVER)
        else:
            # st.write(f"### MISSION TYPE: {identified_persona}")
            st.write(f"Found **{len(matches)}** suitable companies for you.")
            
            play_mario_sound(SND_POWER_UP)
            for i, company in enumerate(matches):
    
                with st.status(f"🍄 FOUND MATCH: {company['name']}", expanded=False):
                    st.write("Generating Fireball (Email)...")
                    subject, body = generate_email(resume_text, company['name'], company['industry'])
                    # st.write(f"**Subject:** {subject}")
                    target_recipient = test_email if testing_mode else company['email']
                    try:
                        send_email(target_recipient, subject, body, resume_bytes, uploaded_resume.name)
                        st.write(f"✅ Fireball sent to {target_recipient}!")
                        play_mario_sound(SND_FIREBALL)
                        time.sleep(0.5)
                        if testing_mode:
                            st.info(f"TEST MODE: Email sent to {target_recipient}. Check your inbox!")
                            play_mario_sound(SND_CLEAR)
                            st.stop()
                    except Exception as e:
                        st.error(f"Mission Failed: {e}")
                        play_mario_sound(SND_GAME_OVER)
                        st.stop()
            
            st.write("### LEVEL COMPLETE")
            play_mario_sound(SND_CLEAR)
            st.balloons()