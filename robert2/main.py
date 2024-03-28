import sqlite3
import config
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates

# Set up logging
logging.basicConfig(filename='app.log', level=logging.ERROR)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/") #defines route for url
def index(request: Request):
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT id, symbol, name, exchange FROM assets ORDER BY symbol
        """)
        rows = cursor.fetchall()
    except sqlite3.Error as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    return templates.TemplateResponse("index.html", {"request": request, "assets": rows})

@app.get("/stonk/{symbol}") #defines route for url
def asset_detail(request: Request, symbol):
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT id, symbol, name FROM assets WHERE symbol = ?
        """, (symbol,))
        row = cursor.fetchone()

        if row is None:
            raise HTTPException(status_code=404, detail="Asset not found")

        cursor.execute("""
            SELECT * FROM asset_prices WHERE asset_id = ?
        """, (row['id'],))
        prices = cursor.fetchall()
    except sqlite3.Error as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    return templates.TemplateResponse("asset_detail.html", {"request": request, "assets": row, "bars": prices})