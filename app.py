from flask import Flask, render_template
import ccxt

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/live-data")
def live_data():
    exchange = ccxt.binance()
    ticker = exchange.fetch_ticker('BTC/USDT')
    return f"BTC/USDT Price: {ticker['last']}"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)