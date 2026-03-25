# -----------------------------
# HARAM SECTORS
# -----------------------------
HARAM_SECTORS = [
    "Banks",
    "Financial Services",
    "Insurance",
    "Gambling",
    "Alcohol",
    "Tobacco"
]

# -----------------------------
# FETCH STOCK DATA (SAFE)
# -----------------------------
def get_stock_data(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        return {
            "symbol": symbol.upper(),
            "sector": info.get("sector", ""),
            "industry": info.get("industry", ""),
            "market_cap": info.get("marketCap", 0) or 0,
            "total_debt": info.get("totalDebt", 0) or 0,
            "total_revenue": info.get("totalRevenue", 1) or 1,
            "interest_expense": info.get("interestExpense", 0) or 0
        }
    except:
        return {
            "symbol": symbol.upper(),
            "sector": "",
            "industry": "",
            "market_cap": 0,
            "total_debt": 0,
            "total_revenue": 1,
            "interest_expense": 0
        }

# -----------------------------
# BUSINESS FILTER
# -----------------------------
def is_haram_business(sector: str, industry: str):
    text = (sector + " " + industry).lower()

    for haram in HARAM_SECTORS:
        if haram.lower() in text:
            return True

    return False

# -----------------------------
# FINANCIAL SCREEN
# -----------------------------
def financial_screen(data):
    try:
        if data["market_cap"] == 0:
            return "UNKNOWN"

        debt_ratio = data["total_debt"] / data["market_cap"]
        interest_ratio = data["interest_expense"] / data["total_revenue"]

        if debt_ratio < 0.33 and interest_ratio < 0.05:
            return "HALAL"
        else:
            return "DOUBTFUL"

    except:
        return "UNKNOWN"

# -----------------------------
# CLASSIFIER
# -----------------------------
def classify_stock(data):
    if is_haram_business(data["sector"], data["industry"]):
        return "HARAM"

    return financial_screen(data)

# -----------------------------
# HALAL API (FINAL)
# -----------------------------
@app.get("/halal/{symbol}")
def halal_check(symbol: str):
    data = get_stock_data(symbol)
    status = classify_stock(data)

    return {
        "symbol": data["symbol"],
        "sector": data["sector"],
        "status": status
    }
