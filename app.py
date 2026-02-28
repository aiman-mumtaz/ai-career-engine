import streamlit as st
import json, os
from utils.parser import extract_text_from_pdf
from utils.ai_engine import identify_persona, generate_email
from utils.mailer import send_email

st.set_page_config(page_title="Career Agent")
st.markdown("""
    <style>
        /* Retro Gaming Font */
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

        .stApp {
            background-color: #5C94FC; /* Classic Mario Sky Blue */
            background-image: url('https://www.transparenttextures.com/patterns/8-bit-mario.png');
        }

        /* Sidebar - The Underground Level */
        section[data-testid="stSidebar"] {
            background-color: #000000 !important;
            border-right: 5px solid #E7693E;
            color: white;
        }

        /* Pixel Labels */
        h1, h2, h3, p, label {
            font-family: 'Press Start 2P', cursive !important;
            color: #ffffff;
            text-shadow: 2px 2px #000000;
        }

        /* The "Brick" Button */
        .stButton>button {
            background-color: #E7693E !important; /* Brick Red */
            color: #ffffff !important;
            border: 4px solid #000000 !important;
            box-shadow: 4px 4px #000000;
            font-family: 'Press Start 2P', cursive;
            font-size: 12px;
            padding: 15px;
            width: 100%;
        }

        .stButton>button:hover {
            background-color: #f7d016 !important; /* Coin Gold */
            color: #000000 !important;
        }

        /* Match Cards (The Question Blocks) */
        .stExpander {
            background-color: #f7d016 !important; 
            border: 4px solid #000000 !important;
            border-radius: 0px !important;
            color: #000000 !important;
        }
        
        /* Success Message (Level Clear) */
        .stAlert {
            background-color: #4FB06D !important;
            border: 3px solid #000000;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

st.title("Super Career")
st.subheader("Level 1-1: The Job Hunt")

st.sidebar.markdown("### 🎮 Controller")

testing_mode = st.sidebar.toggle("Testing Mode (Safety Bubble)", value=True)
test_email = st.sidebar.text_input("Player Email", value="your@email.com")

if testing_mode:
    st.sidebar.info("🍄 Power-up active: Emails are redirected to you.")

if os.path.exists("company_db.json"):
    with open("company_db.json", "r") as f:
        master_list = json.load(f)
else:
    st.error("Company database not found!")
    master_list = []

uploaded_resume = st.file_uploader("Upload your Resume (PDF)", type="pdf")

if uploaded_resume:
    resume_bytes = uploaded_resume.read()
    resume_text = extract_text_from_pdf(resume_bytes)
    
    st.success("Resume parsed successfully.")
    # print(resume_text[:500])
    if st.button("START MISSION (Match & Send)"):
        with st.spinner("🍄 Eating Mushrooms... Matching your skills..."):
            identified_persona = identify_persona(resume_text)
            # print(f"Identified Persona: {matched_names}")
            st.write(f"### MISSION TYPE: {identified_persona}")
            # matches = [c for c in master_list if c['name'] in matched_names]
            matches = [
            c for c in master_list 
            if 'roles' in c and identified_persona in c['roles']
        ]
            # print(master_list)
        print(f"Matches: {[m['name'] for m in matches]}")
        if not matches:
            st.warning("No suitable matches found in the database for your profile.")
        else:
            st.write(f"Found **{len(matches)}** suitable companies for you.")
            
            for company in matches:
                with st.status(f"❓ QUESTION BLOCK: {company['name']}", expanded=False):
                    st.write("Generating Fireball (Email)...")
                    
                    subject, body = generate_email(resume_text, company['name'], company['industry'])
                    st.write(f"**Subject:** {subject}")
                    target_recipient = test_email if testing_mode else company['email']
                    try:
                        send_email(target_recipient, subject, body, resume_bytes, uploaded_resume.name)
                        if testing_mode:
                            st.write(f"Email preview sent to {target_recipient}.")
                        else:
                            if st.button(f"FIRE! To {company['name']}", key=company['name']):
                                st.success("🏁 LEVEL CLEAR! Email Sent.")
                    except Exception as e:
                        st.error(f"Mission Failed: {e}")
            
            st.balloons()