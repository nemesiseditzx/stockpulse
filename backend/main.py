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

# 🔐 ZOYA
ZOYA_API_KEY = "sandbox-48a6a43f-dcdc-48e2-86b1-f113ebaf8d25"
ZOYA_URL = "https://sandbox-api.zoya.finance/graphql"

cache = {}
cache_time = 0

def get_data():
    global cache, cache_time

    if time.time() - cache_time < 10:
        return cache

    d = {}

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

                d[s] = {
                    "price": round(float(l),2),
                    "change": round(float(change),2),
                    "signal": signal
                }
        except:
            continue

    cache = d
    cache_time = time.time()
    return d


@app.get("/stocks")
def stocks():
    return get_data()


@app.get("/halal/{symbol}")
def halal(symbol: str):
    sym = symbol.upper().replace("-USD", "")

    query = {
        "query": """
        query ($ticker: String!) {
          screening(ticker: $ticker) {
            shariahCompliant
          }
        }
        """,
        "variables": {"ticker": sym}
    }

    headers = {
        "Authorization": f"Bearer {ZOYA_API_KEY}"
    }

    try:
        res = requests.post(ZOYA_URL, json=query, headers=headers)
        data = res.json()

        if "data" not in data or data["data"]["screening"] is None:
            return {"status": "UNKNOWN"}

        if data["data"]["screening"]["shariahCompliant"]:
            return {"status": "HALAL"}

        return {"status": "HARAM"}

    except Exception as e:
        print("ERROR:", e)
        return {"status": "ERROR"}


@app.get("/news")
def news():
    return [
        {"title":"Tesla rally","cause":"EV demand","effect":"Bullish","impact":"HIGH"},
        {"title":"Bitcoin spike","cause":"ETF","effect":"Market up","impact":"HIGH"}
    ]
