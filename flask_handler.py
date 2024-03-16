from config import API_KEY, API_SECRET, WS_HOST
import alpaca_trade_api as tradeapi
from flask import Flask, request, jsonify, render_template
from alpaca_handler import AlpacaHandler

app = Flask(__name__)

alpaca_handler = AlpacaHandler()

@app.route('/')
def index():
    account_info = alpaca_handler.get_account_info()
    return render_template('index.html', balances=account_info.portfolio_cash)

@app.route('/buy', methods=['POST'])
def buy():
    symbol = request.form.get('symbol')
    qty = request.form.get('quantity')
    if alpaca_handler.place_order(symbol, qty, 'buy'):
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error'})

@app.route('/sell', methods=['POST'])
def sell():
    symbol = request.form.get('symbol')
    qty = request.form.get('quantity')
    if alpaca_handler.place_order(symbol, qty, 'sell'):
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error'})

@app.route('/backtest', methods=['POST'])
def backtest():
    strategy_class = request.form.get('strategy_class')
    alpaca_handler.backtest(strategy_class)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)