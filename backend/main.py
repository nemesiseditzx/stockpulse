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
    "BTC-USD","ETH-USD","JPM","BAC","C","GS"
]

# 🕌 HALAL DATABASE (CLEAR LIST SYSTEM)
HALAL_STOCKS = [
    "AAPL","MSFT","NVDA","TSLA","GOOGL","AMD","META","INTC"
]

HARAM_STOCKS = [
    "JPM","BAC","C","GS","WFC"
]

# 📊 STOCK DATA
@app.get("/")
def data():
    d={}
    for s in STOCKS:
        t=yf.Ticker(s)
        h=t.history(period="2d")

        if len(h)>=2:
            l=h["Close"].iloc[-1]
            p=h["Close"].iloc[-2]

            change=((l-p)/p)*100

            signal="HOLD"
            if change>1: signal="BUY"
            elif change<-1: signal="SELL"

            d[s]={
                "price":round(float(l),2),
                "change":round(float(change),2),
                "signal":signal
            }
    return d


# 🕌 HALAL CHECK (ACCURATE LIST)
@app.get("/halal/{symbol}")
def halal(symbol:str):
    s=symbol.upper()

    if s in HALAL_STOCKS:
        return {"status":"✅ HALAL"}

    if s in HARAM_STOCKS:
        return {"status":"❌ HARAM"}

    return {"status":"❌ HARAM"}
