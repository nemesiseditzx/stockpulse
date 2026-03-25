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

# 🕌 STRICT HALAL LOGIC
HALAL = ["AAPL","MSFT","NVDA","TSLA","GOOGL","AMD"]
HARAM = ["JPM","BAC","C","GS"]

@app.get("/")
def data():
    d = {}
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


# 🌍 BETTER NEWS ENGINE
@app.get("/news")
def news():
    url="https://newsapi.org/v2/top-headlines?category=business&language=en&pageSize=6&apiKey=4a92eeeadf4a49d292083c9fae812c47"
    res=requests.get(url).json()

    out=[]

    for a in res.get("articles",[]):
        title=a["title"].lower()

        effect="Market stable"

        if "war" in title:
            effect="📉 Crash risk"
        elif "trump" in title:
            effect="⚡ Big volatility"
        elif "fed" in title:
            effect="📉 Stocks drop"
        elif "growth" in title:
            effect="📈 Bullish"

        out.append({
            "title":a["title"][:60],
            "effect":effect
        })

    return out


# 🕌 HALAL FIX
@app.get("/halal/{symbol}")
def halal(symbol:str):
    s=symbol.upper()

    if s in HALAL:
        return {"status":"✅ HALAL"}

    if s in HARAM:
        return {"status":"❌ HARAM"}

    return {"status":"❌ HARAM"}  # strict
