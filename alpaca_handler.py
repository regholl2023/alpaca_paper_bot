import alpaca_trade_api as tradeapi
from alpaca_trade_api.common import URL
from config import API_KEY, API_SECRET, WS_HOST
from backtesting import Backtest, Strategy
import pandas_ta as ta

class AlpacaHandler:
    def __init__(self):
        self.api = tradeapi.REST(API_KEY, API_SECRET, base_url='https://paper-api.alpaca.markets')
        self.conn = tradeapi.stream.Stream(
            key_id=API_KEY,
            secret_key=API_SECRET,
            base_url='https://paper-api.alpaca.markets',
            data_feed='iex'  # replace with 'sip' if you're using the paid data feed
        )
        self.conn.subscribe_trades(self.on_trade_update, '*')  # subscribe to trade updates for all symbols

    async def on_trade_update(self, trade):
        print(f"Received new trade: {trade}")
        # Update indicators and make trading decision
        # This is a simplified example. You'll need to implement your own logic here.

    def fetch_data(self, symbol, timeframe, limit):
        return self.api.get_barset(symbol, timeframe, limit).df[symbol]

    def place_order(self, symbol, qty, side):
        try:
            self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side=side,
                type='market',
                time_in_force='gtc'
            )
            return True
        except Exception as e:
            print(f"Error placing order: {e}")
            return False
    
    def start_stream(self, symbols):
        @self.conn.on(r'^AM\..+$')
        def on_minute_bars(conn, channel, bar):
            print(f"Received new bar: {bar}")
            # Update indicators and make trading decision
            # This is a simplified example. You'll need to implement your own logic here.

        try:
            self.conn.run([f'AM.{symbol}' for symbol in symbols])
        except Exception as e:
            print(f"Error with WebSocket connection: {e}")
            raise
 
    def calculate_indicators(self, symbol, timeframe, limit):
        data = self.fetch_data(symbol, timeframe, limit)
        sma = ta.sma(data['close'], 14)
        ema = ta.ema(data['close'], 14)
        return sma, ema

    def crossover(self, series1, series2):
        return series1[-2] < series2[-2] and series1[-1] > series2[-1]

    def execute_strategy(self, symbol, qty):
        sma, ema = self.calculate_indicators(symbol, 'day', 100)
        if self.crossover(ema, sma):
            self.place_order(symbol, qty, 'buy')
        elif self.crossover(sma, ema):
            self.place_order(symbol, qty, 'sell')        
        
    def backtest(self, strategy_class):
        bt = Backtest(self.data, strategy_class)
        stats = bt.run()
        print(f"Backtest stats: {stats}")
    
    def get_account_info(self):
        return self.api.get_account()
    
    def get_order_info(self, order_id):
        return self.api.get_order(order_id)
    
    def cancel_order(self, order_id):
        self.api.cancel_order(order_id)