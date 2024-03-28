import sqlite3
import config

try:
    # Try to connect to the database
    connection = sqlite3.connect(config.DB_FILE)
    
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE assets (
            id INTEGER PRIMARY KEY,
            symbol TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            exchange TEXT NOT NULL
        )
    """)

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS asset_prices (
            id INTEGER PRIMARY KEY, 
            asset_id INTEGER,
            date NOT NULL,
            open NOT NULL,
            high NOT NULL,
            low NOT NULL,
            close NOT NULL,
            volume NOT NULL,
            FOREIGN KEY (asset_id) REFERENCES assets (id)
        )
    """) 

    connection.commit()            



except sqlite3.Error as error:
    print("Connection failed", error)
