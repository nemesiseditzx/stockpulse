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
    "BTC-USD","ETH-USD","JPM","BAC"
]

HALAL = ["AAPL","MSFT","NVDA","TSLA","GOOGL","AMD","META"]
HARAM = ["JPM","BAC","C","GS","WFC"]

# 📊 MARKET + AI SENTIMENT
@app.get("/")
def data():
    d={}
    total_score=0
    count=0

    for s in STOCKS:
        t=yf.Ticker(s)
        h=t.history(period="2d")

        if len(h)>=2:
            l=h["Close"].iloc[-1]
            p=h["Close"].iloc[-2]

            change=((l-p)/p)*100

            score=0
            if change>1: score=1
            elif change<-1: score=-1

            total_score+=score
            count+=1

            signal="BUY" if change>0 else "SELL"

            d[s]={
                "price":round(float(l),2),
                "change":round(float(change),2),
                "signal":signal
            }

    sentiment="NEUTRAL"
    confidence=50

    if count>0:
        avg=total_score/count
        confidence=abs(avg)*100

        if avg>0:
            sentiment="📈 BULLISH"
        elif avg<0:
            sentiment="📉 BEARISH"

    return {
        "stocks":d,
        "sentiment":sentiment,
        "confidence":round(confidence,1)
    }


# 🌍 NEWS (CAUSE + EFFECT)
@app.get("/news")
def news():
    url="https://newsapi.org/v2/top-headlines?category=business&language=en&pageSize=6&apiKey=4a92eeeadf4a49d292083c9fae812c47"
    res=requests.get(url).json()

    out=[]

    for a in res.get("articles",[]):
        t=a["title"].lower()

        reason="General update"
        effect="Market stable"

        if "war" in t:
            reason="War tension"
            effect="📉 Crash risk"
        elif "trump" in t:
            reason="Political move"
            effect="⚡ Volatility"
        elif "fed" in t:
            reason="Interest rate"
            effect="📉 Stocks fall"
        elif "profit" in t:
            reason="Company earnings"
            effect="📈 Bullish"

        out.append({
            "title":a["title"][:70],
            "reason":reason,
            "effect":effect
        })

    return out


# 🐦 TWEETS
@app.get("/tweets")
def tweets():
    return [
        {
            "text":"🚨 Trump speech affecting markets",
            "impact":"⚡ VOLATILITY",
            "link":"https://x.com/realDonaldTrump"
        },
        {
            "text":"⚔️ War news impacting oil + stocks",
            "impact":"📉 BEARISH",
            "link":"https://www.wsj.com"
        },
        {
            "text":"📊 Fed decision moving tech stocks",
            "impact":"⚡ SPIKE",
            "link":"https://www.marketwatch.com"
        }
    ]


# 🕌 HALAL CHECK
@app.get("/halal/{symbol}")
def halal(symbol:str):
    s=symbol.upper()

    if s in HALAL:
        return {"status":"✅ HALAL"}

    return {"status":"❌ HARAM"}
