from flask import Flask, request  # Web Server / HTTP Request
import requests                   # HTTP Client
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# --- 根路径 Health Check ---
@app.route("/", methods=["GET"])
def home():
    return "Bot is running", 200


# --- Telegram Webhook Handler (Webhook Endpoint) ---
@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.json  # Incoming Update JSON (Telegram update)

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        # 回消息 (Send Message API)
        requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": f"你发了: {text}"
            }
        )

    return "OK", 200


if __name__ == "__main__":
    # Local Development Server
    app.run(host="0.0.0.0", port=8000)
