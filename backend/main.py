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
# 📊 STOCK SYSTEM (IMPROVED)
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

    # ⚡ cache for performance
    if time.time() - cache_time < 10:
        return cache

    data = {}

    for s in STOCKS:
        try:
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
    return get_stocks()

# =============================
# 🕌 PREMIUM HALAL SYSTEM
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

    # 1️⃣ Hard rule
    if sym in HALAL_LIST:
        return {"status": "HALAL"}

    if sym in HARAM_LIST:
        return {"status": "HARAM"}

    # 2️⃣ Smart sector detection
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
# 📰 NEWS SYSTEM (REAL API)
# =============================
FINNHUB_API = "d726mspr01qjeeeg4ll0d726mspr01qjeeeg4llg"   # 🔥 replace later

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

            # 🎯 DEFAULT
            effect = "General market movement expected"

            # 🔥 SMART IMPACT ENGINE
            if any(x in title for x in ["oil", "energy"]):
                effect = "Energy stocks may move"

            elif any(x in title for x in ["fed", "interest rate", "inflation"]):
                effect = "Interest-sensitive stocks may react"

            elif any(x in title for x in ["war", "iran", "china", "military"]):
                effect = "Global markets may become volatile"

            elif any(x in title for x in ["tech", "chip", "ai"]):
                effect = "Tech stocks may be affected"

            elif any(x in title for x in ["crypto", "bitcoin"]):
                effect = "Crypto market may move"

            news_list.append({
                "title": n.get("headline"),
                "summary": summary,
                "image": n.get("image"),
                "url": n.get("url"),
                "source": n.get("source"),
                "effect": effect  # ✅ always defined
            })

        return news_list

    except:
        return []
# =============================
# 📡 SIGNAL STORAGE (UPGRADED)
# =============================

messages_db = []

EXPIRY_TIME = 86400  # 1 day (seconds)


@app.post("/telegram-webhook")
async def telegram_webhook(req: Request):

    data = await req.json()

    try:
        message = data.get("message") or data.get("channel_post")

        if not message:
            return {"ok": True}

        text = message.get("text", "")

        if text:
            messages_db.insert(0, {
                "text": text,
                "time": time.time()
            })

    except Exception as e:
        print("ERROR:", e)

    return {"ok": True}


# =============================
# 🎯 CURRENT SIGNALS (last 24h)
# =============================
@app.get("/signals-current")
def signals_current():
    now = time.time()

    return [
        m for m in messages_db
        if now - m["time"] <= EXPIRY_TIME
    ]


# =============================
# 🕓 PREVIOUS SIGNALS (old)
# =============================
@app.get("/signals-previous")
def signals_previous():
    now = time.time()

    return [
        m for m in messages_db
        if now - m["time"] > EXPIRY_TIME
    ]

# =============================
# 🔌 WEBSOCKET (LIVE ENGINE)
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
                await conn.send_json(data)
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
    return {"status": "StockPulse PRO running"}
