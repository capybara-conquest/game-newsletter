from flask import Flask, render_template, request
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import threading

# Load env (safe fallback for local only)
load_dotenv()

app = Flask(__name__)

SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')


def send_email(user_email):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = user_email
        msg['Subject'] = "Welcome to Capybara Conquest"

        body = (
            "Thank you for subscribing to Capybara Conquest Newsletter.\n"
            "You will receive updates on the latest game news and updates.\n"
            "Stay tuned for more exciting content!\n\n"
            "Best regards,\n"
            "Capybara Conquest Team"
        )

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=15) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

    except Exception as e:
        print("Email failed:", e)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/subscribe", methods=["POST"])
def subscribe():
    user_email = request.form.get("email")

    if not user_email:
        return "Missing email", 400

    # 🚀 IMPORTANT: run email sending in background (prevents timeout)
    threading.Thread(target=send_email, args=(user_email,)).start()

    return render_template("success.html", email=user_email)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)