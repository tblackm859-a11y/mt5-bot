import asyncio
import os
from flask import Flask, jsonify, request
from metaapi_cloud_sdk import MetaApi
import requests

app = Flask(__name__)

# Your MetaApi Credentials
TOKEN = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiJmYmY3N2YwZTFmYzI4OTlmZmRkYjhmYjFkODNmYTU0MyIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVzdC1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcnBjLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVhbC10aW1lLXN0cmVhbWluZy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc2VyY2VzIjpbIio6JRVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFastRhdHMtYXBpIiwibWV0aG9kcyI6WyJtZXRhc3RhdHMtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6InJpc2stbWFuYWdlbWVudC1hcGkiLCJtZXRob2RzIjpbInJpc2stbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoiY29weWZhY3RvcnktYXBpIiwibWV0aG9kcyI6WyJjb3B5ZmFjdG9yeS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibXQtbWFuYWdlci1hcGkiLCJtZXRob2RzIjpbIm10LW1hbmFnZXItYXBpOnJlc3Q6ZGVhbGluZzoqOioiLCJtdC1tYW5hZ2VyLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJiaWxsaW5nLWFwaSIsIm1ldGhvZHMiOlsiYmlsbGluZy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfV0sImlnbm9yZVJhdGVMaW1pdHMiOmZhbHNlLCJ0b2tlbklkIjoiMjAyMTAyMTMiLCJpbXBlcnNvbmF0ZWQiOmZhbHNlLCJyZWFsVXNlcklkIjoiZmJmNzdmMGUxZmMyODk5ZmZkZGI4ZmIxZDgzZmE1NDMiLCJpYXQiOjE3OTMyNzkwNzl9.eX-K8828aTWh8-93iwRwbZ23DpMpGFgzXqe450vRwG0Y7KU4LXFB0WQFBrluIHn-47BZAcfr_pQuBAwISajtcSpPxWYAX4LAVkM_xbueYO6BoYPFLOGLMFA-2xd0i9gZ_-hFK5Y1ulDp4qIXZad386NYxpxmfvPk9AbamJ36r1HJdHEoWbOry28xl5gMGxfaGpOyiCXigMM1pXx67qbpGJN_gofc2yomwjlCXNCFFN9tHfibnv0QQ_aAbFlKyiMncrQafwKIpt5FgvbX6hNesgLUYHozZIMYGasvco1g6ShoBrPV4Tv8JHYS20x3lV9eH-rURq71nuGB4VUxfIGOqyi6S_RnMLFokv0sXgnJjSPlOMjYQFStj0PG38zeOazEnfQ5_CviZNgH14JCucNQSaRZW_9ISzh2VJpa-h-gbXlAA_dzFDzHXxPOHT0J-ygo1EjW4YQ-VPlEOBr_HqDmH1vxH8wW-svy2-Ed_5tx-t0QvwF71AbMP8asgpChokzPKSp8HVJe5h1qffkycypozxVlZcAJNtdWeoPb4D_9jIGAdc3PmxSTfbALbKhWzmytlBAjO6saOkkaekS5OLrhc9YwejE4Ol7JqGSXM3hKDZbhLv_FvjNROBLN3OVwlz9gKZWtx8tcEdUwauhaaor3gVumnPj9xp8fXBH5x2jiuO0"
ACCOUNT_ID = "Ad531acb-5260-4c48-ab1c-9542482132b4"


@app.route("/")
def home():
  return "JamesAutoTradeBot is active and running!"


# Endpoint triggered when you tap START BOT on your mobile dashboard
@app.route("/api/bot/start", methods=["POST"])
def start_bot():
  try:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def execute_trade_logic():
      api = MetaApi(token=TOKEN)
      account = await api.metatrader_account_api.get_account(ACCOUNT_ID)

      if account.state != "DEPLOYED":
        await account.deploy()

      await account.wait_connected()
      connection = account.get_rpc_connection()
      await connection.connect()
      await connection.wait_synchronized()

      result = await connection.create_market_order(
          symbol="XAUUSDm",
          order_type="ORDER_TYPE_SELL",
          volume=0.01,
          stop_loss=2700.0,
          take_profit=2600.0,
      )
      return result

    trade_result = loop.run_until_complete(execute_trade_logic())
    return jsonify({
        "success": True,
        "message": "Bot started and order executed via MetaApi!",
        "details": str(trade_result),
    })

  except Exception as e:
    return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/bot/stop", methods=["POST"])
def stop_bot():
  return jsonify({"success": True, "message": "Bot stopped."})


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=10000)
  
