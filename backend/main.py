import yfinance as yf
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STOCKS = [
    "AAPL","TSLA","MSFT","NVDA","AMZN",
    "META","GOOGL","NFLX","AMD","INTC",
    "BTC-USD","ETH-USD","JPM","BAC","C","GS"
]

# 🔐 ZOYA CONFIG
ZOYA_API_KEY = "sandbox-48a6a43f-dcdc-48e2-86b1-f113ebaf8d25"
ZOYA_URL = "https://sandbox-api.zoya.finance/graphql"

cache = {}
cache_time = 0

# ⚡ STOCK CACHE
def get_stocks():
    global cache, cache_time

    if time.time() - cache_time < 10:
        return cache

    data = {}

    for s in STOCKS:
        try:
            t = yf.Ticker(s)
            h = t.history(period="2d")

            if len(h) >= 2:
                l = h["Close"].iloc[-1]
                p = h["Close"].iloc[-2]

                change = ((l - p) / p) * 100

                signal = "HOLD"
                if change > 1:
                    signal = "BUY"
                elif change < -1:
                    signal = "SELL"

                data[s] = {
                    "price": round(float(l), 2),
                    "change": round(float(change), 2),
                    "signal": signal
                }
        except:
            continue

    cache = data
    cache_time = time.time()
    return data


@app.get("/stocks")
def stocks():
    return get_stocks()


# 🕌 ZOYA HALAL CHECK (REAL)
@app.get("/halal/{symbol}")
def halal(symbol: str):
    query = {
        "query": """
        query Screening($ticker: String!) {
          screening(ticker: $ticker) {
            shariahCompliant
            status
          }
        }
        """,
        "variables": {"ticker": symbol.upper()}
    }

    headers = {
        "Authorization": f"Bearer {ZOYA_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        res = requests.post(ZOYA_URL, json=query, headers=headers)
        data = res.json()

        screening = data["data"]["screening"]

        if screening["shariahCompliant"]:
            return {"status": "HALAL"}

        return {"status": "HARAM"}

    except:
        return {"status": "ERROR"}


# 📰 NEWS (KEEP SIMPLE FOR NOW)
@app.get("/news")
def news():
    return [
        {
            "title": "Tesla rallies",
            "cause": "EV demand surge",
            "effect": "Bullish sentiment",
            "impact": "HIGH"
        },
        {
            "title": "Bitcoin spike",
            "cause": "ETF inflow",
            "effect": "Market bullish",
            "impact": "HIGH"
        }
    ]
