import smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import streamlit as st

def send_email(to_email, subject, body, pdf_bytes, filename):

    # server = smtplib.SMTP("smtp.gmail.com", 587)
    # server.starttls()


    # server.login(SENDER_EMAIL, SENDER_PASSWORD)

    msg = MIMEMultipart()
    msg['From'] = st.secrets["smtp"]["email"]
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    part = MIMEApplication(pdf_bytes, _subtype="pdf")
    part.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(part)

    with smtplib.SMTP(st.secrets["smtp"]["server"], int(st.secrets["smtp"]["port"])) as server:
        server.starttls()
        server.login(st.secrets["smtp"]["email"], st.secrets["smtp"]["password"])
        server.send_message(msg)