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
# 🕌 HALAL SYSTEM (SMART)
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

    try:
        stock = yf.Ticker(sym)
        sector = stock.info.get("sector", "").lower()

        if any(x in sector for x in ["bank", "finance", "insurance"]):
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

        return [{
            "title": n.get("headline"),
            "summary": n.get("summary"),
            "image": n.get("image"),
            "url": n.get("url"),
            "source": n.get("source")
        } for n in data[:12]]

    except:
        return []


# =============================
# 📡 TELEGRAM SIGNAL SYSTEM
# =============================
messages_db = []

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


@app.get("/signals-live")
def signals_live():
    return messages_db[:20]


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
