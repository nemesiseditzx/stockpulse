from fastapi import FastAPI, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import requests
import time
import asyncio
import json
import os

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
# 📊 STOCK SYSTEM
# =============================
STOCKS = [
    "AAPL","TSLA","MSFT","NVDA","AMZN",
    "META","GOOGL","AMD","INTC",
    "BTC-USD","ETH-USD","JPM","BAC","C","GS"
]

HALAL_BLOCK = {"JPM","BAC","C","GS"}

cache = {}
cache_time = 0

def get_stocks():
    global cache, cache_time

    if time.time() - cache_time < 10:
        return cache

    data = {}

    for s in STOCKS:
        try:
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

        except Exception as e:
            print("STOCK ERROR:", e)

    cache = data
    cache_time = time.time()
    return data


@app.get("/stocks")
def stocks():
    return {"data": get_stocks()}


# =============================
# 🕌 HALAL SYSTEM
# =============================
HALAL_LIST = {"AAPL","MSFT","NVDA","AMD","GOOGL","META","TSLA","AMZN","NFLX"}
HARAM_LIST = {"JPM","BAC","C","GS","WFC","MS","AXP"}

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

        if "bank" in sector or "finance" in sector:
            return {"status": "HARAM"}

        return {"status": "HALAL"}

    except Exception as e:
        print("HALAL ERROR:", e)
        return {"status": "UNKNOWN"}


# =============================
# 📰 NEWS SYSTEM
# =============================
@app.get("/news")
def news():
    url = "https://finnhub.io/api/v1/news?category=general&token=d726mspr01qjeeeg4ll0d726mspr01qjeeeg4llg"

    try:
        res = requests.get(url)
        data = res.json()

        news_list = []

        for n in data[:12]:
            title = (n.get("headline") or "").lower()

            sentiment = "Neutral"
            sector = "General"

            if "fed" in title or "interest" in title:
                sentiment = "Bearish"
                sector = "Tech"
            elif "ai" in title or "chip" in title:
                sentiment = "Bullish"
                sector = "Technology"

            news_list.append({
                "title": n.get("headline"),
                "summary": n.get("summary"),
                "image": n.get("image"),
                "url": n.get("url"),
                "sentiment": sentiment,
                "sector": sector
            })

        return news_list

    except Exception as e:
        print("NEWS ERROR:", e)
        return []


# =============================
# 📡 SIGNAL SYSTEM
# =============================
SIGNAL_FILE = "signals.json"

def load_messages():
    if not os.path.exists(SIGNAL_FILE):
        return []
    try:
        with open(SIGNAL_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_messages(data):
    with open(SIGNAL_FILE, "w") as f:
        json.dump(data, f)

@app.post("/telegram-webhook")
async def telegram_webhook(req: Request):
    data = await req.json()

    try:
        message = data.get("channel_post") or data.get("message")

        if not message:
            return {"ok": True}

        text = message.get("text") or message.get("caption", "")

        if text:
            messages = load_messages()

            messages.insert(0, {
                "text": text,
                "time": int(time.time())
            })

            save_messages(messages)

    except Exception as e:
        print("SIGNAL ERROR:", e)

    return {"ok": True}


@app.get("/signals-current")
def current():
    now = time.time()
    return [m for m in load_messages() if now - m["time"] < 86400]


@app.get("/signals-previous")
def previous():
    now = time.time()
    return [m for m in load_messages() if 86400 <= now - m["time"] < 604800]


# =============================
# 🔔 ALERT SYSTEM (FINAL FIXED)
# =============================
ALERT_FILE = "alerts.json"

def load_alerts():
    if not os.path.exists(ALERT_FILE):
        return []
    try:
        with open(ALERT_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_alerts(data):
    with open(ALERT_FILE, "w") as f:
        json.dump(data, f)

def get_telegram_file_url(file_id):
    TOKEN = "YOUR_BOT_TOKEN"

    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}"
        res = requests.get(url).json()

        if res.get("ok"):
            path = res["result"]["file_path"]
            return f"https://api.telegram.org/file/bot{TOKEN}/{path}"
    except Exception as e:
        print("IMAGE ERROR:", e)

    return None


@app.post("/alert-webhook")
async def alert_webhook(req: Request):
    data = await req.json()

    try:
        message = data.get("message") or data.get("channel_post")

        if not message:
            return {"ok": True}

        text = message.get("text") or message.get("caption", "")
        image = None

        if "photo" in message:
            file_id = message["photo"][-1]["file_id"]
            image = get_telegram_file_url(file_id)

        if text or image:
            alerts = load_alerts()

            alerts.insert(0, {
                "text": text,
                "image": image,
                "time": int(time.time())
            })

            save_alerts(alerts)

            print("ALERT SAVED")

    except Exception as e:
        print("ALERT ERROR:", e)

    return {"ok": True}


@app.get("/alerts-today")
def alerts_today():
    now = time.time()
    return [a for a in load_alerts() if now - a["time"] < 86400]


@app.get("/alerts-previous")
def alerts_previous():
    now = time.time()
    return [a for a in load_alerts() if now - a["time"] >= 86400]


# =============================
# 🔌 WEBSOCKET
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
                await conn.send_json({"data": data})
            except:
                pass


manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)

    try:
        while True:
            await manager.broadcast(get_stocks())
            await asyncio.sleep(5)
    except:
        manager.disconnect(ws)


# =============================
# 🧠 HEALTH
# =============================
@app.get("/")
def home():
    return {"status": "StockPulse PRO running"}
