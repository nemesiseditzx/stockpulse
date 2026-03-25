import yfinance as yf
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

# 🕌 STRUCTURED HALAL DATABASE
HALAL_DB = {
    "HALAL": ["AAPL","MSFT","NVDA","TSLA","GOOGL","AMD","META","INTC"],
    "HARAM": ["JPM","BAC","C","GS","WFC"]
}

cache_data = {}
cache_time = 0

# ⚡ SMART CACHE SYSTEM (10 sec)
def get_stock_data():
    global cache_data, cache_time

    if time.time() - cache_time < 10:
        return cache_data

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
                    "price": round(float(l), 2),
                    "change": round(float(change), 2),
                    "signal": signal
                }
        except:
            continue

    cache_data = d
    cache_time = time.time()
    return d


@app.get("/")
def data():
    return get_stock_data()


# 🕌 HALAL CHECK (STRICT SYSTEM)
@app.get("/halal/{symbol}")
def halal(symbol: str):
    s = symbol.upper()

    if s in HALAL_DB["HALAL"]:
        return {"status": "HALAL"}

    if s in HALAL_DB["HARAM"]:
        return {"status": "HARAM"}

    return {"status": "UNKNOWN"}


# 🕌 FULL LIST
@app.get("/halal-list")
def halal_list():
    return HALAL_DB


# 📰 MARKET NEWS (MOCK → upgrade later with API)
@app.get("/news")
def news():
    return [
        {
            "title": "Apple earnings beat expectations",
            "cause": "Strong iPhone sales",
            "effect": "Bullish momentum",
            "summary": "Apple reported higher-than-expected revenue."
        },
        {
            "title": "Bitcoin surges",
            "cause": "ETF inflows",
            "effect": "Market bullish",
            "summary": "Crypto market seeing strong inflows."
        }
    ]
