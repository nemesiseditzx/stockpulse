from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import requests
import time
import re

app = FastAPI()

# =============================
# 🌐 CORS (FRONTEND CONNECT)
# =============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================
# 📊 STOCK SYSTEM (OPTIMIZED)
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

    # 🔥 caching (performance boost)
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
# 🕌 HALAL SYSTEM (SMART FIX)
# =============================
FALLBACK_HALAL = ["AAPL","MSFT","NVDA","AMD","GOOGL","META","TSLA","AMZN"]
FALLBACK_HARAM = ["JPM","BAC","C","GS","WFC"]

@app.get("/halal/{symbol}")
def halal(symbol: str):
    sym = symbol.upper().replace("-USD", "")

    # 🔥 fallback fast result
    if sym in FALLBACK_HALAL:
        return {"status": "HALAL"}

    if sym in FALLBACK_HARAM:
        return {"status": "HARAM"}

    # 🔥 smart sector detection
    try:
        stock = yf.Ticker(sym)
        info = stock.info

        sector = info.get("sector", "").lower()

        if any(x in sector for x in ["bank", "finance", "insurance"]):
            return {"status": "HARAM"}

        return {"status": "HALAL"}

    except:
        return {"status": "UNKNOWN"}


# =============================
# 📰 NEWS (WITH IMAGE + CLEAN)
# =============================
FINNHUB_API = "d726mspr01qjeeeg4ll0d726mspr01qjeeeg4llg"

@app.get("/news")
def news():
    url = f"https://finnhub.io/api/v1/news?category=general&token={FINNHUB_API}"

    try:
        res = requests.get(url)
        data = res.json()

        result = []

        for n in data[:12]:
            result.append({
                "title": n.get("headline"),
                "summary": n.get("summary"),
                "image": n.get("image"),
                "url": n.get("url"),
                "source": n.get("source"),
                "time": n.get("datetime")
            })

        return result

    except:
        return [{"title": "News loading error"}]


# =============================
# 📡 SIGNAL SYSTEM (UPGRADE READY)
# =============================

@app.get("/signals-live")
def signals_live():

    # 🔥 CURRENT: STATIC (STABLE)
    # 🔥 FUTURE: TELEGRAM / DB REPLACE HERE

    sample_messages = [
        "🚨 Trading Alert: META 🚨 Recommendation: Buy Suggested Price: $594.19",
        "🚨 Trading Alert: AAPL 🚨 Recommendation: Sell Suggested Price: $252.62"
    ]

    signals = []

    for text in sample_messages:

        symbol = None
        action = None
        price = None

        # 🔍 symbol detect
        try:
            symbol = re.search(r'Alert:\s*(\w+)', text).group(1)
        except:
            pass

        # 🔍 action detect
        if "Buy" in text:
            action = "BUY"
        elif "Sell" in text:
            action = "SELL"

        # 🔍 price detect
        try:
            price = re.search(r'\$(\d+\.?\d*)', text).group(1)
        except:
            pass

        signals.append({
            "symbol": symbol,
            "action": action,
            "price": price
        })

    return signals
