import config, sqlite3, time, logging
import alpaca_trade_api as tradeapi
from datetime import datetime, timedelta
from time import sleep

# Set up logging
logging.basicConfig(level=logging.INFO)

connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("""
    SELECT id, symbol, name FROM asset
""")
rows = cursor.fetchall()

symbols = [row['symbol'] for row in rows]
asset_dict = {row['symbol']: row['id'] for row in rows}

api = tradeapi.REST(config.ALPACA_API_KEY, config.ALPACA_SECRET_KEY, base_url=config.ALPACA_URL_BASE)

# Set date range for one day
start_date = datetime.now() - timedelta(days=1)
end_date = datetime.now()

chunk_size = 200
for i in range(0, len(symbols), chunk_size):
    symbol_chunk = symbols[i: i + chunk_size]

    # Add delay/retry mechanism
    retries = 3
    for j in range(retries):
        try:
            barsets = api.get_bars(symbol_chunk, '15Min', start=start_date, end=end_date)
            break
        except Exception as e:
            if j < retries - 1:  # i is zero indexed
                sleep(3)  # wait a bit before trying again
                continue
            else:
                raise

    for symbol in symbol_chunk:
        bars = barsets[symbol]
        total_bars = len(bars)
        for bar in bars:
            asset_id = asset_dict[symbol]
            cursor.execute("""
                INSERT INTO asset_prices (asset_id, date, open, high, low, close, volume)
                VALUES (?,?,?,?,?,?,?)
            """, (asset_id, bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v))

    logging.info(f"Received {total_bars} prices for symbol {symbol}")
    connection.commit()