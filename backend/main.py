from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import requests
import time

app = FastAPI()

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================
# 📊 STOCK SYSTEM
# =============================
STOCKS = [
    "AAPL","TSLA","MSFT","NVDA","AMZN",
    "META","GOOGL","NFLX","AMD","INTC",
    "BTC-USD","ETH-USD","JPM","BAC","C","GS"
]

cache = {}
cache_time = 0

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


# =============================
# 🕌 HALAL SYSTEM (FIXED)
# =============================

FALLBACK_HALAL = ["AAPL","MSFT","NVDA","AMD","GOOGL","META"]
FALLBACK_HARAM = ["JPM","BAC","C","GS"]

# (Optional Zoya – safe placeholder)
ZOYA_API_KEY = ""
ZOYA_URL = "https://sandbox-api.zoya.finance/graphql"


@app.get("/halal/{symbol}")
def halal(symbol: str):
    sym = symbol.upper().replace("-USD", "")

    # 🔥 fallback (main working system)
    if sym in FALLBACK_HALAL:
        return {"status": "HALAL"}

    if sym in FALLBACK_HARAM:
        return {"status": "HARAM"}

    # 🔥 Zoya optional (won't break if empty key)
    try:
        if ZOYA_API_KEY:
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

            res = requests.post(ZOYA_URL, json=query, headers=headers)
            data = res.json()

            if "data" in data and data["data"]["screening"]:
                if data["data"]["screening"]["shariahCompliant"]:
                    return {"status": "HALAL"}
                else:
                    return {"status": "HARAM"}

    except:
        pass

    return {"status": "UNKNOWN"}


# =============================
# 📰 NEWS
# =============================
@app.get("/news")
def news():
    return [
        {
            "title": "Tesla rally",
            "cause": "EV demand surge",
            "effect": "Bullish momentum",
            "impact": "HIGH"
        },
        {
            "title": "Bitcoin spike",
            "cause": "ETF inflow",
            "effect": "Market bullish",
            "impact": "HIGH"
        }
    ]
