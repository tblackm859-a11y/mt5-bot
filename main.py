import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = "8326164521:AAGFNKRlVxV57ul4KXUSFcPYCfh8aaHJAJs"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}"


@app.route("/")
def home():
  return "JamesAutoTradeBot is active and running on Render!"


@app.route("/webhook", methods=["POST"])
def webhook():
  data = request.get_json()

  if data and "message" in data:
    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "").strip().lower()

    if text == "/start":
      reply_text = (
          "🤖 *JamesAutoTradeBot* is connected and active.\nReady for your"
          " JustMarkets trading signals!"
      )
    elif text == "/balance":
      reply_text = (
          "📊 *Account Status*\n\nYour Telegram bot is live via Render.\nTo pull"
          " live broker account data directly on mobile, ensure your broker"
          " webhooks or alerts are configured to push signals here."
      )
    else:
      reply_text = f"Received your command: {text}"

    send_url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": reply_text, "parse_mode": "Markdown"}
    requests.post(send_url, json=payload)

  return "OK", 200


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
        
