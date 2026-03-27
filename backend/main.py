from fastapi import FastAPI, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import requests
import time
import asyncio

app = FastAPI()

# =============================
# 🌐 CORS
# =============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================
# 📊 STOCK SYSTEM (FIXED)
# =============================
STOCKS = [
    "AAPL","TSLA","MSFT","NVDA","AMZN",
    "META","GOOGL","AMD","INTC",
    "BTC-USD","ETH-USD","JPM","BAC","C","GS"
]

HALAL_BLOCK = {"JPM","BAC","C","GS"}  # ❌ remove haram

cache = {}
cache_time = 0

def get_stocks():
    global cache, cache_time

    if time.time() - cache_time < 10:
        return cache

    data = {}

    for s in STOCKS:
        try:
            # ✅ HALAL FILTER
            if s in HALAL_BLOCK:
                continue

            t = yf.Ticker(s)
            h = t.history(period="2d")

            if len(h) >= 2:
                l = float(h["Close"].iloc[-1])
                p = float(h["Close"].iloc[-2])

                change = ((l - p) / p) * 100

                signal = "HOLD"
                if change > 1:
                    signal = "BUY"
                elif change < -1:
                    signal = "SELL"

                data[s] = {
                    "price": round(l, 2),
                    "change": round(change, 2),
                    "signal": signal
                }

        except:
            continue

    cache = data
    cache_time = time.time()
    return data


@app.get("/stocks")
def stocks():
    return {
        "data": get_stocks(),
        "powered_by": "Badhon EditZX"
    }

# =============================
# 🕌 HALAL SYSTEM (PRO)
# =============================
HALAL_LIST = {
    "AAPL","MSFT","NVDA","AMD","GOOGL","META","TSLA","AMZN","NFLX"
}

HARAM_LIST = {
    "JPM","BAC","C","GS","WFC","MS","AXP"
}

@app.get("/halal/{symbol}")
def halal(symbol: str):
    sym = symbol.upper().replace("-USD", "")

    if sym in HALAL_LIST:
        return {"status": "HALAL"}

    if sym in HARAM_LIST:
        return {"status": "HARAM"}

    try:
        stock = yf.Ticker(sym)
        info = stock.info

        sector = str(info.get("sector", "")).lower()
        industry = str(info.get("industry", "")).lower()

        haram_keywords = [
            "bank", "financial", "insurance",
            "credit", "lending", "capital markets"
        ]

        if any(k in sector for k in haram_keywords) or any(k in industry for k in haram_keywords):
            return {"status": "HARAM"}

        return {"status": "HALAL"}

    except:
        return {"status": "UNKNOWN"}

# =============================
# 📰 NEWS SYSTEM (PRO)
# =============================
@app.get("/news")
def news():
    url = f"https://finnhub.io/api/v1/news?category=general&token=d726mspr01qjeeeg4ll0d726mspr01qjeeeg4llg"

    try:
        res = requests.get(url)
        data = res.json()

        news_list = []

        for n in data[:12]:
            title = (n.get("headline") or "").lower()
            summary = n.get("summary", "")

            # ======================
            # 🧠 AI LOGIC
            # ======================

            effect = "General market movement expected"
            sentiment = "Neutral"
            sector = "Overall Market"

            if any(x in title for x in ["fed","interest","inflation"]):
                effect = "Interest-sensitive stocks affected"
                sentiment = "Bearish"
                sector = "Tech / Growth"

            elif any(x in title for x in ["oil","energy"]):
                effect = "Energy stocks may rise"
                sentiment = "Bullish"
                sector = "Energy"

            elif any(x in title for x in ["war","conflict","china","iran"]):
                effect = "Market volatility expected"
                sentiment = "Bearish"
                sector = "Global Markets"

            elif any(x in title for x in ["ai","chip","nvidia","tech"]):
                effect = "Tech sector momentum"
                sentiment = "Bullish"
                sector = "Technology"

            elif any(x in title for x in ["crypto","bitcoin"]):
                effect = "Crypto price movement"
                sentiment = "Volatile"
                sector = "Crypto"

            news_list.append({
                "title": n.get("headline"),
                "summary": summary,
                "image": n.get("image"),
                "url": n.get("url"),
                "effect": effect,
                "sentiment": sentiment,
                "sector": sector
            })

        return news_list

    except:
        return []

# =============================
# 📡 SIGNAL SYSTEM (24h + 7d)
# =============================
import json
import os

SIGNAL_FILE = "signals.json"

# load existing
def load_messages():
    if not os.path.exists(SIGNAL_FILE):
        return []

    with open(SIGNAL_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return []

# save
def save_messages(data):
    with open(SIGNAL_FILE, "w") as f:
        json.dump(data, f)

messages_db = load_messages()


@app.post("/telegram-webhook")
async def telegram_webhook(req: Request):
    global messages_db

    data = await req.json()

    try:
        message = data.get("message") or data.get("channel_post")

        if not message:
            return {"ok": True}

        text = message.get("text", "")

        if text:
            new_msg = {
                "text": text,
                "time": int(time.time())
            }

            messages_db.insert(0, new_msg)

            # 🔥 SAVE TO FILE
            save_messages(messages_db)

    except Exception as e:
        print("ERROR:", e)

    return {"ok": True}


def clean_old():
    global messages_db

    now = time.time()

    messages_db = [
        m for m in messages_db
        if now - m["time"] < 604800
    ]

    save_messages(messages_db)


@app.get("/signals-current")
def current():
    clean_old()
    now = time.time()

    return [
        m for m in messages_db
        if now - m["time"] < 86400
    ]


@app.get("/signals-previous")
def previous():
    clean_old()
    now = time.time()

    return [
        m for m in messages_db
        if 86400 <= now - m["time"] < 604800
    ]

# =============================
# 🔌 WEBSOCKET (LIVE)
# =============================
class ConnectionManager:
    def __init__(self):
        self.connections = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.connections.append(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.connections:
            self.connections.remove(ws)

    async def broadcast(self, data):
        for conn in self.connections:
            try:
                await conn.send_json({
                    "data": data,
                    "powered_by": "Badhon EditZX"
                })
            except:
                pass


manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)

    try:
        while True:
            data = get_stocks()
            await manager.broadcast(data)
            await asyncio.sleep(5)

    except:
        manager.disconnect(ws)

# =============================
# 🧠 HEALTH CHECK
# =============================
@app.get("/")
def home():
    return {
        "status": "StockPulse PRO running",
        "powered_by": "Badhon EditZX"
    }
