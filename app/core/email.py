import smtplib
from email.message import EmailMessage

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_EMAIL = "venkatareddygeeda1998@gmail.com"
SMTP_PASSWORD = "hlmpppcufbaccprh"

def send_otp_email(to_email: str, otp: str):
    msg = EmailMessage()
    msg["Subject"] = "Your Login OTP"
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email
    msg.set_content(f"Hello, \n Your OTP is {otp}. Valid for 5 minutes.\n Please do not share it with anyone.")

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)
