import yfinance as yf
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    "BTC-USD","ETH-USD"
]

# 🕌 HALAL DATABASE (simple)
HALAL_STOCKS = ["AAPL","MSFT","NVDA","TSLA","GOOGL","AMD"]

# 📊 MARKET ENGINE
@app.get("/")
def get_data():
    data = {}

    for s in STOCKS:
        t = yf.Ticker(s)
        h = t.history(period="2d")

        if len(h) >= 2:
            latest = h["Close"].iloc[-1]
            prev = h["Close"].iloc[-2]

            change = ((latest - prev) / prev) * 100

            signal = "HOLD"
            if change > 1.5: signal = "STRONG BUY 🚀"
            elif change > 0.5: signal = "BUY"
            elif change < -1.5: signal = "STRONG SELL ⚠️"
            elif change < -0.5: signal = "SELL"

            prediction = "📈 Bullish" if change > 0 else "📉 Bearish"
            confidence = min(abs(change)*20,95)

            vol = "LOW"
            if abs(change) > 2: vol = "HIGH ⚡"
            elif abs(change) > 1: vol = "MEDIUM"

            data[s] = {
                "price": round(float(latest),2),
                "change": round(float(change),2),
                "signal": signal,
                "prediction": prediction,
                "confidence": round(confidence,1),
                "volatility": vol
            }

    return data


# 🌍 SMART NEWS ENGINE
@app.get("/news")
def news():
    url = "https://newsapi.org/v2/top-headlines?category=business&language=en&pageSize=8&apiKey=4a92eeeadf4a49d292083c9fae812c47"
    res = requests.get(url).json()

    out = []

    for a in res.get("articles",[]):
        title = a["title"].lower()

        impact = "LOW"
        reason = "General market update"
        effect = "Minimal movement expected"

        if "trump" in title:
            impact="HIGH"
            reason="Political statement"
            effect="Market volatility spike"

        elif "war" in title or "conflict" in title:
            impact="HIGH"
            reason="Geopolitical tension"
            effect="Market drop likely"

        elif "fed" in title or "interest rate" in title:
            impact="HIGH"
            reason="Interest rate decision"
            effect="Stocks may fall"

        elif "profit" in title or "growth" in title:
            impact="MEDIUM"
            reason="Company performance"
            effect="Bullish movement possible"

        out.append({
            "title": a["title"],
            "impact": impact,
            "reason": reason,
            "effect": effect
        })

    return out


# 🕌 HALAL CHECK (FIXED)
@app.get("/halal/{symbol}")
def halal(symbol: str):
    s = symbol.upper().replace("-USD","")

    if s in HALAL_STOCKS:
        return {"status":"✅ Halal"}

    if s in ["JPM","BAC","C","GS"]:
        return {"status":"❌ Not Halal"}

    return {"status":"⚠️ Needs Scholar Review"}
