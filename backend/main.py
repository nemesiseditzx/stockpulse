import yfinance as yf
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STOCKS = ["AAPL", "TSLA", "BTC-USD"]

@app.get("/")
def get_data():
    data = {}

    for symbol in STOCKS:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="2d")

        if len(hist) >= 2:
            latest = hist["Close"].iloc[-1]
            previous = hist["Close"].iloc[-2]

            change = latest - previous
            percent = (change / previous) * 100

            data[symbol] = {
                "price": round(float(latest), 2),
                "change": round(float(percent), 2)
            }

    return data
