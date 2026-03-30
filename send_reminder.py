import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_reminder():
    gmail = os.environ["GMAIL"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]
    recipient = os.environ["RECIPIENT_EMAIL"]

    msg = MIMEMultipart()
    msg["From"] = gmail
    msg["To"] = recipient
    msg["Subject"] = "💰 Time to log your weekly expenses!"

    body = """
    Hi Nick!

    This is your weekly reminder to log your expenses.

    To get started:
    1. Open VS Code
    2. Activate your virtual environment: venv\\Scripts\\activate
    3. Switch to your private branch: git checkout private
    4. Run the app: streamlit run app.py
    5. Log this week's expenses

    Stay on track this week!

    — Finance Tracker
    """

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail, app_password)
        server.sendmail(gmail, recipient, msg.as_string())
        print("✅ Reminder email sent successfully!")

if __name__ == "__main__":
    send_reminder()