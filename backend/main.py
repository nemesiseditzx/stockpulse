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

# 📊 MARKET + AI SIGNAL ENGINE
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

            # 🔥 SIGNAL
            signal = "HOLD"
            if percent > 1.5:
                signal = "STRONG BUY 🚀"
            elif percent > 0.5:
                signal = "BUY"
            elif percent < -1.5:
                signal = "STRONG SELL ⚠️"
            elif percent < -0.5:
                signal = "SELL"

            # 🧠 AI PREDICTION (SIMULATED)
            confidence = min(abs(percent) * 20, 95)

            if percent > 0:
                prediction = "📈 Bullish"
            elif percent < 0:
                prediction = "📉 Bearish"
            else:
                prediction = "⚖️ Neutral"

            volatility = "LOW"
            if abs(percent) > 2:
                volatility = "HIGH ⚡"
            elif abs(percent) > 1:
                volatility = "MEDIUM"

            data[symbol] = {
                "price": round(float(latest), 2),
                "change": round(float(percent), 2),
                "signal": signal,
                "prediction": prediction,
                "confidence": round(confidence, 1),
                "volatility": volatility
            }

    return data


# 🌍 NEWS + SENTIMENT ENGINE
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

        summary = title[:80] + "..."

        news.append({
            "title": title,
            "summary": summary,
            "impact": impact,
            "direction": direction,
            "url": article["url"]
        })

    return news
