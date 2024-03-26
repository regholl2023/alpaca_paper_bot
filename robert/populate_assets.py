import sqlite3
import alpaca_trade_api as tradeapi
import config


try:
    
    connection = sqlite3.connect(config.DB_FILE)
    print("Connection successful")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT symbol, name, exchange FROM asset
    """)

    rows = cursor.fetchall()
    symbols = [row['symbol'] for row in rows]
   


    api = tradeapi.REST(config.ALPACA_API_KEY, config.ALPACA_SECRET_KEY, base_url=config.ALPACA_URL_BASE)
  
    assets = api.list_assets()

    new_symbols_added = False

    for asset in assets:
        try:
             if asset.status == 'active' and asset.tradable and asset.symbol not in symbols and asset.exchange != 'CRYPTO':
                    print(f"Added a new asset {asset.symbol} {asset.name}")
                    cursor.execute("INSERT OR IGNORE INTO asset (symbol, name, exchange) VALUES (?, ?, ?)", (asset.symbol, asset.name, asset.exchange))
                    new_symbols_added = True
        except Exception as e:
            print(asset.symbol)
            print(e)

    if not new_symbols_added:
        print("There are no new symbols to add")


    connection.commit()
    print("Transaction committed to the DB")

except sqlite3.Error as error:
    print("Connection failed", error)