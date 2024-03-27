import sqlite3, config

try:
    # Try to connect to the database
    connection = sqlite3.connect(config.DB_FILE)
    
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE asset (
            id INTEGER PRIMARY KEY,
            symbol TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            exchange TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        ALTER TABLE asset ADD COLUMN tradable BOOLEAN;
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS asset_prices (
            id INTEGER PRIMARY KEY,
            asset_id INTEGER,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            FOREIGN KEY (asset_id) REFERENCES asset (id)
        )
    """)

    connection.commit()            



except sqlite3.Error as error:
    print("Connection failed", error)
