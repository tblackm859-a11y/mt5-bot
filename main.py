import os
from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def home():
  return "MT5 Trading Bot is active and running!"


@app.route("/webhook", methods=["POST"])
def webhook():
  json_data = request.get_json()
  return "OK", 200


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
    
