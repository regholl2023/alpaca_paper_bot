# Alpaca API credentials
import os

API_KEY = os.environ.get('ALPACA_ID')
API_SECRET = os.environ.get('ALPACA_SECRET')

WS_HOST = "https://paper-api.alpaca.markets/v2"
WEBHOOK_PASSPHRASE = ""
# Exchange details
EXCHANGE = "alpaca"  # Or any other supported exchange by CCXT
SYMBOL = "BTC/USDT"  # Or any other symbol you<