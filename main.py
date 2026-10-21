import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = "8326164521:AAGFNKRlVxV57ul4KXUSFcPYCfh8aaHJAJs"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}"


def send_telegram_message(chat_id, text):
  payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
  requests.post(f"{TELEGRAM_API_URL}/sendMessage", json=payload)


@app.route("/")
def home():
  return "JamesAutoTradeBot is active and running on Render!"


# Endpoint that receives updates from Telegram when you chat with the bot
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
          "📊 *Account Status*\n\nYour Telegram bot is live via Render.\nBroker:"
          " JustMarkets (Connected via Webhook)"
      )
    elif text == "/status":
      reply_text = (
          "🟢 *System Status*\n\n- Render Server: Online\n- Telegram Webhook:"
          " Active\n- Bot Status: Listening for signals"
      )
    else:
      reply_text = f"Received your command: {text}"

    send_telegram_message(chat_id, reply_text)

  return "OK", 200


# Optional endpoint where external trading alerts can send signals to your bot
@app.route("/signal", methods=["POST"])
def signal():
  signal_data = request.get_json()
  # You can pass your Telegram chat ID here to receive automated alerts
  # (Replace CHAT_ID with your actual Telegram user chat ID if you want direct push alerts)
  chat_id = signal_data.get("chat_id")
  message = signal_data.get(
      "message", "⚡ New Trading Signal Received from JustMarkets setup."
  )

  if chat_id:
    send_telegram_message(chat_id, message)
    return "Signal sent to Telegram", 200

  return "No chat_id provided", 400


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
