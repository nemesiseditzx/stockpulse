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
    "AAPL", "TSLA", "MSFT", "NVDA", "AMZN",
    "META", "GOOGL", "NFLX", "AMD", "INTC",
    "BTC-USD", "ETH-USD"
]

# 📊 MARKET DATA + SIGNAL
@app.get("/")
def get_data():
    data = {}

    for symbol in STOCKS:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="2d")

        if len(hist) >= 2:
            latest = hist["Close"].iloc[-1]
            previous = hist["Close"].iloc[-2]

            percent = ((latest - previous) / previous) * 100

            signal = "HOLD"
            if percent > 1.5:
                signal = "STRONG BUY 🚀"
            elif percent > 0.5:
                signal = "BUY"
            elif percent < -1.5:
                signal = "STRONG SELL ⚠️"
            elif percent < -0.5:
                signal = "SELL"

            data[symbol] = {
                "price": round(float(latest), 2),
                "change": round(float(percent), 2),
                "signal": signal
            }

    return data


# 🌍 ADVANCED NEWS ENGINE
@app.get("/news")
def get_news():
    url = "https://newsapi.org/v2/top-headlines?category=business&language=en&pageSize=8&apiKey=4a92eeeadf4a49d292083c9fae812c47"

    res = requests.get(url)
    articles = res.json().get("articles", [])

    news = []

    for article in articles:
        title = article["title"]
        lower = title.lower()

        impact = "🟡 LOW"
        direction = "⚖️ NEUTRAL"

        # 🔥 IMPACT DETECTION
        if "war" in lower or "conflict" in lower:
            impact = "🔴 HIGH"
            direction = "📉 BEARISH"

        elif "trump" in lower:
            impact = "🟠 HIGH"
            direction = "⚡ VOLATILE"

        elif "fed" in lower or "interest rate" in lower:
            impact = "🔴 HIGH"
            direction = "📉 BEARISH"

        elif "growth" in lower or "profit" in lower:
            impact = "🟢 MEDIUM"
            direction = "📈 BULLISH"

        # 🧠 SIMPLE SUMMARY (AI-like)
        summary = title[:80] + "..."

        news.append({
            "title": title,
            "summary": summary,
            "impact": impact,
            "direction": direction,
            "url": article["url"]
        })

    return news
