# Alpaca API credentials
import os

API_KEY = os.environ.get('alpaca_id')
API_SECRET = os.environ.get('alpaca_sec')
VARIABLE = ""
WS_HOST = "https://paper-api.alpaca.markets/v2"
WEBHOOK_PASSPHRASE = ""
# Exchange details
EXCHANGE = "alpaca"  # Or any other supported exchange by CCXT
SYMBOL = "BTC/USDT"  # Or any other symbol you<