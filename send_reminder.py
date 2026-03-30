import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_reminder():
    gmail = os.environ["GMAIL"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]
    recipient = os.environ["RECIPIENT_EMAIL"]
    app_url = os.environ["APP_URL"]

    msg = MIMEMultipart()
    msg["From"] = gmail
    msg["To"] = recipient
    msg["Subject"] = "💰 Time to log your weekly expenses!"

    body = f"""
    Hi there!

    This is your weekly reminder to log your expenses.

    Click the link below to open your Finance Tracker and log this week's spending:

    {app_url}

    Happy tracking!
    """

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail, app_password)
        server.sendmail(gmail, recipient, msg.as_string())
        print("✅ Reminder email sent successfully!")

if __name__ == "__main__":
    send_reminder()