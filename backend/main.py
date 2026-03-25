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

# 📊 MARKET + SIGNAL ENGINE
@app.get("/")
def get_data():
    data = {}

    for symbol in STOCKS:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="2d")

        if len(hist) >= 2:
            latest = hist["Close"].iloc[-1]
            previous = hist["Close"].iloc[-2]

            change = latest - previous
            percent = (change / previous) * 100

            # 🔥 SMART SIGNAL LOGIC
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


# 🌍 NEWS + IMPACT ENGINE
@app.get("/news")
def get_news():
    url = "https://newsapi.org/v2/top-headlines?category=business&language=en&pageSize=6&apiKey=4a92eeeadf4a49d292083c9fae812c47"

    response = requests.get(url)
    articles = response.json().get("articles", [])

    news = []

    for article in articles:
        title_lower = article["title"].lower()

        impact = "🟡 Neutral"

        if "war" in title_lower or "conflict" in title_lower:
            impact = "🔴 HIGH IMPACT"
        elif "trump" in title_lower or "fed" in title_lower or "interest rate" in title_lower:
            impact = "🟠 MARKET MOVING"

        news.append({
            "title": article["title"],
            "url": article["url"],
            "impact": impact
        })

    return news
