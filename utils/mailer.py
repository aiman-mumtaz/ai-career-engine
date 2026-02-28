import smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def send_email(to_email, subject, body, pdf_bytes, filename):
    msg = MIMEMultipart()
    msg['From'] = os.getenv("SENDER_EMAIL")
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    part = MIMEApplication(pdf_bytes, _subtype="pdf")
    part.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(part)

    with smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))) as server:
        server.starttls()
        server.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
        server.send_message(msg)