from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import requests
import time
import re

# 🔥 TELEGRAM
from telethon import TelegramClient

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
# 🕌 HALAL SYSTEM (IMPROVED)
# =============================
FALLBACK_HALAL = ["AAPL","MSFT","NVDA","AMD","GOOGL","META","TSLA","AMZN"]
FALLBACK_HARAM = ["JPM","BAC","C","GS","WFC"]

@app.get("/halal/{symbol}")
def halal(symbol: str):
    sym = symbol.upper().replace("-USD", "")

    if sym in FALLBACK_HALAL:
        return {"status": "HALAL"}

    if sym in FALLBACK_HARAM:
        return {"status": "HARAM"}

    # fallback logic using sector (simple AI)
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
# 📰 NEWS (UPGRADED WITH IMAGE)
# =============================
FINNHUB_API = "d726mspr01qjeeeg4ll0d726mspr01qjeeeg4llg"

@app.get("/news")
def news():
    url = f"https://finnhub.io/api/v1/news?category=general&token={FINNHUB_API}"

    try:
        res = requests.get(url)
        data = res.json()

        result = []

        for n in data[:10]:
            result.append({
                "title": n.get("headline"),
                "summary": n.get("summary"),
                "image": n.get("image"),  # 🔥 NEW
                "url": n.get("url"),
                "source": n.get("source")
            })

        return result

    except:
        return []


# =============================
# 📡 TELEGRAM LIVE SIGNALS
# =============================

api_id = 30062420
api_hash = "0a408d6c4588a5235a6c194e31c77bcf"

CHANNEL = "buysellalert_ai_bot"  # ⚠️ CHANGE THIS

client = TelegramClient("session", api_id, api_hash)


@app.get("/signals-live")
async def signals_live():
    await client.start()

    signals = []

    async for msg in client.iter_messages(CHANNEL, limit=10):
        if msg.text:

            text = msg.text

            symbol = None
            action = None
            price = None

            # 🔍 SYMBOL
            try:
                symbol = re.search(r'Alert:(\w+)', text).group(1)
            except:
                pass

            # 🔍 ACTION
            if "Buy" in text:
                action = "BUY"
            elif "Sell" in text:
                action = "SELL"

            # 🔍 PRICE
            try:
                price = re.search(r'\$(\d+\.?\d*)', text).group(1)
            except:
                pass

            signals.append({
                "symbol": symbol,
                "action": action,
                "price": price,
                "raw": text
            })

    return signals
