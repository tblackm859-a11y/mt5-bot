from flask import Flask, jsonify
from flask_cors import CORS
from metaapi_cloud_sdk import MetaApi
import asyncio
import threading

app = Flask(__name__)
CORS(app)  # Connects your GitHub Pages dashboard to Render

# Your credentials
API_TOKEN = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiJmYmY3N2YwZTFmYzI4OTlmZmRkYjhmYjFkODNmYTU0MyIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVzdC1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcnBjLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVhbC10aW1lLXN0cmVhbWluZy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtZXRhc3RhdHMtYXBpIiwibWV0aG9kcyI6WyJtZXRhc3RhdHMtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6InJpc2stbWFuYWdlbWVudC1hcGkiLCJtZXRob2RzIjpbInJpc2stbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoiY29weWZhY3RvcnktYXBpIiwibWV0aG9kcyI6WyJjb3B5ZmFjdG9yeS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibXQtbWFuYWdlci1hcGkiLCJtZXRob2RzIjpbIm10LW1hbmFnZXItYXBpOnJlc3Q6ZGVhbGluZzoqOioiLCJtdC1tYW5hZ2VyLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6ImJpbGxpbmctYXBpIiwibWV0aG9kcyI6WyJiaWxsaW5nLWFwaS5yZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19XSwiaWdub3JlUmF0ZUxpbWl0cyI6ZmFsc2UsInRva2VuSWQiOiIyMDIxMDIxMyIsImltcGVyc29uYXRlZCI6ZmFsc2UsInJlYWxVc2VySWQiOiJmYmY3N2YwZTFmYzI4OTlmZmRkYjhmYjFkODNmYTU0MyIsImlhdCI6MTc5MzM3MzkwOH0uankyLXRmMVBpRmhrcWwzZ0NIa2R0bTdIU1EtTEJDdC1Ddk1aQlFicTVCbTdqM0ZlaHVZZnZiUVdIM2xQUUhkdVZsZGdxWmd4c0o3QlRHSWdKM1F4OFdad3c3YjVjb3BFN01ha3Q5eXAxX3pHTVNRRUNTMGRvV0lESFBKSkF4ajBDdU5BdlNkUHVIZjVvTW9CYzZwLTFsYlcwX3VpRlZEbnZOekVBZ2pMRHhjOTVXeDRpV1lxVXJkQlN3V1pHdXR3RHpxS3FhcnNpRGlJR2NGRFZJNWNUNWcySjd4eGhabVNoWVJ0QzhyQktlU09TTWxmX2RQaXlxUmIyNWVONFFocmZIVm4tOUN3ZDRTTUxqRjBLSWVCdzhUSi1rWTE4UDdZaHA3Wm0td3kxZzhfdzBtekNKbFJ6c1RCejhvNk5tTEZhZHJrZHJWdjQ1SkpTOTdfOWVsalFvcFd1QnhzdzR0FFhxY2xCcDBYOGVsU2VCbXVHTUtwR2RjMXp5QzY2YXpGcHFxMGIxY0Y4V1JRWWIteWdJOG1aemJxSFljeTlZMWpub3lyV3U0b21Kb0dkYVlaMnRVSXFBVjhfV2JiLWlLaE55WFpwdGVYX2dIbmh5ZFdPeHp6bGpndHVsQ1B2Tm1sUGNGYVhMbW1pbjhTUVVaTW53WUJocjA0QjNFSGY0Q2VYZTJSZVNsaW94anRaeVdHjdUwMDBpWm95ZnZwVjg3SElNbXBDWXlHjDB4TVNwblNaS3VjSnVfZ212RFUzMUw0V1o5LWNNWXVvZmlzMHBBNFdlZlMxeUkzSm42eUdkazNkZXVzTDY5T052eXBlQUVlb2NaNGJHN09FNEFwam9kZVhXTm9IMlR3bmdiMkpyamVvQ3QwMFxldEd1R0hZ"
ACCOUNT_ID = "ad531acb-5260-4c48-ab1c-9542482132b4"

bot_running = False
latest_status = {"status": "STOPPED", "balance": 0, "market_structure": "Idle"}

def run_metaapi_bot():
    global bot_running, latest_status
    async def bot_loop():
        api = MetaApi(API_TOKEN)
        account = await api.metatrader_account_api.get_account(ACCOUNT_ID)
        connection = account.get_rpc_connection()
        await connection.connect()
        await connection.wait_synchronized()
        
        latest_status["status"] = "RUNNING"
        
        while bot_running:
            info = await connection.get_account_information()
            latest_status["balance"] = info.get('balance', 0)
            latest_status["market_structure"] = "Analyzing Gold (XAUUSD)..."
            
            await asyncio.sleep(3)

    asyncio.run(bot_loop())

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify(latest_status)

@app.route('/start', methods=['POST', 'GET'])
def start_bot():
    global bot_running
    if not bot_running:
        bot_running = True
        thread = threading.Thread(target=run_metaapi_bot)
        thread.daemon = True
        thread.start()
        return jsonify({"message": "Bot execution started"})
    return jsonify({"message": "Bot is already running"})

@app.route('/stop', methods=['POST', 'GET'])
def stop_bot():
    global bot_running
    bot_running = False
    latest_status["status"] = "STOPPED"
    return jsonify({"message": "Bot execution stopped"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
        
