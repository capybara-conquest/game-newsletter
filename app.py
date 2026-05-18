from flask import Flask, render_template, request
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv("/home/chestnutcapybara/newsletter/.env")
print("SMTP_SERVER =", os.getenv("SMTP_SERVER"))
app = Flask(__name__)

SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/subscribe", methods=["POST"])
def subscribe():
    user_email = request.form["email"]

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

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

    return render_template("success.html", email=user_email)

if __name__ == "__main__":
    app.run(debug=True)