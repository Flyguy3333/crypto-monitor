from flask import Flask, render_template_string
import ccxt
import time

app = Flask(__name__)
exchange = ccxt.binance()

@app.route('/')
def home():
    try:
        btc = exchange.fetch_ticker('BTC/USDT')
        eth = exchange.fetch_ticker('ETH/USDT')
        return render_template_string('''
            <html>
                <head>
                    <title>Crypto Monitor</title>
                    <style>
                        body { font-family: Arial; margin: 40px; background: #f0f0f0; }
                        .price { font-size: 24px; margin: 20px; padding: 20px; background: white; border-radius: 8px; }
                    </style>
                </head>
                <body>
                    <h1>Crypto Price Monitor</h1>
                    <div class="price">BTC/USDT: ${{ "{:,.2f}".format(btc_price) }}</div>
                    <div class="price">ETH/USDT: ${{ "{:,.2f}".format(eth_price) }}</div>
                    <script>
                        setTimeout(() => location.reload(), 5000);
                    </script>
                </body>
            </html>
        ''', btc_price=btc['last'], eth_price=eth['last'])
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    print("Server starting at http://64.226.91.151:8080")
    app.run(host='0.0.0.0', port=8080)
