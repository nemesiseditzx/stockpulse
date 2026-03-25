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
        hist = ticker.history(period="1d")

        if not hist.empty:
            price = float(hist["Close"].iloc[-1])
            data[symbol] = round(price, 2)

    return data
