import alpaca_trade_api as tradeapi
import pandas_ta as ta
from backtesting import Backtest, Strategy
from config import API_KEY, API_SECRET, WS_HOST
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

class MyStrategy(Strategy):
    def init(self):
        self.sma = self.I(ta.sma, self.data.Close, 14)
        self.ema = self.I(ta.ema, self.data.Close, 14)
        self.rsi = self.I(ta.rsi, self.data.Close, 14)

    def next(self):
        if crossover(self.ema, self.sma) and self.rsi[-1] < 30:
            self.buy()
        if crossover(self.sma, self.ema) and self.rsi[-1] > 70:
            self.sell()

def crossover(series1, series2):
    return series1[-2] < series2[-2] and series1[-1] > series2[-1]

# Connect to Alpaca
api = tradeapi.REST(API_KEY, API_SECRET, base_url=WS_HOST)

# Fetch historical data
try:
    data = api.get_barset('AAPL', 'day', limit=1000).df['AAPL']
except Exception as e:
    logging.error(f"Error fetching historical data: {e}")
    raise

# Backtest the strategy
bt = Backtest(data, MyStrategy)
stats = bt.run()
logging.info(f"Backtest stats: {stats}")

# Connect to Alpaca's WebSocket for live data
conn = tradeapi.stream2.StreamConn(API_KEY, API_SECRET, base_url=WS_HOST)

# Define the handler function
@conn.on(r'^AM\..+$')
def on_minute_bars(conn, channel, bar):
    logging.info(f"Received new bar: {bar}")
    # Update indicators and make trading decision
    # This is a simplified example. You'll need to implement your own logic here.
    data = data.append(bar)
    sma = ta.sma(data['close'], 14)
    ema = ta.ema(data['close'], 14)
    rsi = ta.rsi(data['close'], 14)
    if crossover(ema, sma) and rsi[-1] < 30:
        logging.info("Placing buy order")
        try:
            api.submit_order(
                symbol='AAPL',
                qty=1,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
        except Exception as e:
            logging.error(f"Error placing buy order: {e}")
    elif crossover(sma, ema) and rsi[-1] > 70:
        logging.info("Placing sell order")
        try:
            api.submit_order(
                symbol='AAPL',
                qty=1,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
        except Exception as e:
            logging.error(f"Error placing sell order: {e}")

# Start the WebSocket connection
try:
    conn.run(['AM.AAPL'])
except Exception as e:
    logging.error(f"Error with WebSocket connection: {e}")
    raise
