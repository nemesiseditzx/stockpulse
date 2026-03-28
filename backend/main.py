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

    except:
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
            summary = n.get("summary", "")

            effect = "Market impact expected"
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

messages_db = load_messages()

@app.post("/telegram-webhook")
async def telegram_webhook(req: Request):
    global messages_db

    data = await req.json()

    try:
        message = data.get("channel_post") or data.get("message")

        if not message:
            return {"ok": True}

        text = message.get("text") or message.get("caption", "")

        if text:
            messages_db.insert(0, {
                "text": text,
                "time": int(time.time())
            })

            save_messages(messages_db)

    except Exception as e:
        print("SIGNAL ERROR:", e)

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
    return [m for m in messages_db if now - m["time"] < 86400]


@app.get("/signals-previous")
def previous():
    clean_old()
    now = time.time()
    return [m for m in messages_db if 86400 <= now - m["time"] < 604800]

# =============================
# 🔔 ALERT SYSTEM (FINAL PRO)
# =============================

ALERT_FILE = "alerts.json"


# 📸 TELEGRAM IMAGE HELPER
def get_telegram_file_url(file_id):
    TOKEN = "8729117748:AAG7XRR9SYVW47g7oEtBrHdmtrk5iRmm7L4"  # 🔥  bot token 

    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}"
        res = requests.get(url).json()

        if res.get("ok"):
            file_path = res["result"]["file_path"]
            return f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
    except Exception as e:
        print("IMAGE ERROR:", e)

    return None


# 📂 LOAD / SAVE
def load_alerts():
    if not os.path.exists(ALERT_FILE):
        return []
    with open(ALERT_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return []


def save_alerts(data):
    with open(ALERT_FILE, "w") as f:
        json.dump(data, f)


alerts_db = load_alerts()


# 📩 TELEGRAM WEBHOOK
@app.post("/alert-webhook")
async def alert_webhook(req: Request):
    global alerts_db

    data = await req.json()

    try:
        message = data.get("message") or data.get("channel_post")

        if not message:
            return {"ok": True}

        # ✅ TEXT + CAPTION
        text = message.get("text") or message.get("caption")

        image = None

        # 📸 IMAGE
        if "photo" in message:
            photo = message["photo"][-1]
            file_id = photo["file_id"]

            image = get_telegram_file_url(file_id)

        # ✅ SAVE
        if text or image:
            alerts_db.insert(0, {
                "text": text,
                "image": image,
                "time": int(time.time())
            })

            save_alerts(alerts_db)

            print("✅ ALERT SAVED")

    except Exception as e:
        print("❌ ALERT ERROR:", e)

    return {"ok": True}


# 🔥 TODAY ALERTS (24h)
@app.get("/alerts-today")
def alerts_today():
    now = time.time()

    return [
        a for a in alerts_db
        if now - a["time"] < 86400
    ]


# 🔥 PREVIOUS ALERTS (PERMANENT)
@app.get("/alerts-previous")
def alerts_previous():
    now = time.time()

    return [
        a for a in alerts_db
        if now - a["time"] >= 86400
    ]
    
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
            await manager.broadcast(get_stocks())
            await asyncio.sleep(5)
    except:
        manager.disconnect(ws)

# =============================
# 🧠 HEALTH
# =============================
@app.get("/")
def home():
    return {
        "status": "StockPulse PRO running",
        "powered_by": "Badhon EditZX"
    }
