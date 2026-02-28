import streamlit as st
import json, os
from utils.parser import extract_text_from_pdf
from utils.ai_engine import identify_persona, generate_email
from utils.mailer import send_email

st.set_page_config(page_title="Liaison AI", page_icon="🤖")

st.title("🤖 Liaison AI Career Agent")

testing_mode = st.sidebar.toggle("Testing Mode", value=True)
test_email = st.sidebar.text_input("My Test Email", value="your-email@gmail.com")



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
    if st.button("Match & Send Emails"):
        with st.spinner("Analyzing resume and finding matches..."):
            identified_persona = identify_persona(resume_text)
            # print(f"Identified Persona: {matched_names}")
            # matches = [c for c in master_list if c['name'] in matched_names]
            matches = [
            c for c in master_list 
            if 'roles' in c and identified_persona in c['roles']
        ]
            print(master_list)
        print(f"Matches: {[m['name'] for m in matches]}")
        if not matches:
            st.warning("No suitable matches found in the database for your profile.")
        else:
            st.write(f"Found **{len(matches)}** suitable companies for you.")
            
            for company in matches:
                with st.status(f"Processing {company['name']}...", expanded=False):
                    
                    subject, body = generate_email(resume_text, company['name'], company['industry'])
                    st.write(f"**Subject:** {subject}")
                    target_recipient = test_email if testing_mode else company['email']
                    try:
                        send_email(target_recipient, subject, body, resume_bytes, uploaded_resume.name)
                        if testing_mode:
                            st.write(f"Email preview sent to {target_recipient}.")
                        else:
                            st.write("Email sent successfully.")
                    except Exception as e:
                        st.error(f"Failed to send: {e}")
            
            st.balloons()
            st.success("Campaign complete!")