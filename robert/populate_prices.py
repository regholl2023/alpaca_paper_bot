import config, sqlite3
import alpaca_trade_api as tradeapi
import time

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

chunk_size = 200
for i in range(0, len(symbols), chunk_size):
    symbol_chunk = symbols[i: i + chunk_size]
    print(f"Querying API for symbols: {', '.join(symbol_chunk)}")

    barsets = api.get_bars(symbol_chunk, '15Min') 

    for bar in barsets:
        print(f"Processing symbol {bar.S}")
        asset_id = asset_dict[bar.S]
        print(bar.t, bar.o, bar.h, bar.l, bar.c, bar.v)
        cursor.execute("""
            INSERT INTO asset_prices (asset_id, date, open, high, low, close, volume)
            VALUES (?,?,?,?,?,?,?)
        """, (asset_id, bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v))

    connection.commit()