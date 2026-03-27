HALAL = ["AAPL", "TSLA"]
HARAM = ["META", "NFLX"]

def check_halal(symbol):
    symbol = symbol.upper()

    if symbol in HALAL:
        return "HALAL"
    elif symbol in HARAM:
        return "HARAM"
    else:
        return "UNKNOWN"
