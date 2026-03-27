import yfinance as yf

SYMBOLS = ["AAPL", "TSLA", "BTC-USD"]

def get_stock_data():
    data = []

    for symbol in SYMBOLS:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d", interval="1m")

        if not hist.empty:
            price = hist["Close"].iloc[-1]
            prev = hist["Close"].iloc[-2] if len(hist) > 1 else price
            change = ((price - prev) / prev) * 100
        else:
            price = 0
            change = 0

        data.append({
            "symbol": symbol,
            "price": round(price, 2),
            "change": round(change, 2),
            "signal": "BUY" if change > 0 else "SELL"
        })

    return data
