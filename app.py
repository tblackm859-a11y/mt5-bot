from flask import Flask, jsonify
from flask_cors import CORS
import os
import threading

app = Flask(__name__)
# Allows your GitHub Pages dashboard to send requests to Render
CORS(app)

bot_running = False

def run_trading_loop():
    global bot_running
    while bot_running:
        # Your MetaApi / MT5 trading execution logic goes here
        pass

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        "status": "RUNNING" if bot_running else "STOPPED",
        "account": "Connected"
    })

@app.route('/start', methods=['POST'])
def start_bot():
    global bot_running
    if not bot_running:
        bot_running = True
        thread = threading.Thread(target=run_trading_loop)
        thread.start()
    return jsonify({"message": "Bot started", "status": "RUNNING"})

@app.route('/stop', methods=['POST'])
def stop_bot():
    global bot_running
    bot_running = False
    return jsonify({"message": "Bot stopped", "status": "STOPPED"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
    
