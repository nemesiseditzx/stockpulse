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

# 🕌 HALAL SYSTEM (STRICT)
HALAL = ["AAPL","MSFT","NVDA","TSLA","GOOGL","AMD","META"]
HARAM = ["JPM","BAC","C","GS","WFC"]

@app.get("/")
def data():
    d={}
    for s in STOCKS:
        t=yf.Ticker(s)
        h=t.history(period="2d")

        if len(h)>=2:
            l=h["Close"].iloc[-1]
            p=h["Close"].iloc[-2]

            c=((l-p)/p)*100

            signal="HOLD"
            if c>1.5: signal="STRONG BUY 🚀"
            elif c>0.5: signal="BUY"
            elif c<-1.5: signal="STRONG SELL ⚠️"
            elif c<-0.5: signal="SELL"

            d[s]={
                "price":round(float(l),2),
                "change":round(float(c),2),
                "signal":signal
            }
    return d


# 🌍 NEWS ENGINE (CAUSE + EFFECT)
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
            effect="📉 Market crash risk"

        elif "trump" in t:
            reason="Political action"
            effect="⚡ High volatility"

        elif "fed" in t:
            reason="Interest rate decision"
            effect="📉 Stocks drop"

        elif "profit" in t:
            reason="Strong earnings"
            effect="📈 Bullish move"

        out.append({
            "title":a["title"][:70],
            "reason":reason,
            "effect":effect
        })

    return out


# 🐦 TWITTER-LIKE FEED (WITH LINKS)
@app.get("/tweets")
def tweets():
    return [
        {
            "text":"🚨 Trump speech causing market reaction",
            "impact":"⚡ VOLATILITY",
            "link":"https://x.com/realDonaldTrump"
        },
        {
            "text":"⚔️ War news shaking oil + stocks",
            "impact":"📉 BEARISH",
            "link":"https://www.wsj.com"
        },
        {
            "text":"📊 Tech stocks reacting after Fed news",
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
