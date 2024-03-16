import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

class MyStrategy(Strategy):
    def __init__(self, sma, ema, rsi):
        self.sma = sma
        self.ema = ema
        self.rsi = rsi

    def crossover(self, series1, series2):
        return series1[-2] < series2[-2] and series1[-1] > series2[-1]

    def next(self):
        if self.crossover(self.ema, self.sma) and self.rsi[-1] < 30:
            self.buy()
        if self.crossover(self.sma, self.ema) and self.rsi[-1] > 70:
            self.sell()