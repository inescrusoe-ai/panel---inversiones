import yfinance as yf
import json
from datetime import datetime, timezone

TICKERS = [
    "SM", "MRVL", "LLY", "MSFT", "AMZN", "SNDK", "PBR", "FN", "MRK",
    "GS", "CSCO", "NOW", "PANW", "IREN", "CRDO", "ASTS",
    "MXL", "KRYS", "GH", "BSX", "META", "CACI", "CAT", "NEM"
]

prices = {}
errors = []

for ticker in TICKERS:
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="2d")
        if not hist.empty:
            price = float(hist['Close'].iloc[-1])
            if price > 0:
                prices[ticker] = round(price, 2)
                print(f"OK {ticker}: ${price:.2f}")
                continue
        try:
            fi = t.fast_info
            price = getattr(fi, 'last_price', None) or getattr(fi, 'previous_close', None)
            if price and float(price) > 0:
                prices[ticker] = round(float(price), 2)
                print(f"OK {ticker} (fast_info): ${price:.2f}")
                continue
        except Exception:
            pass
        try:
            info = t.info
            price = info.get('regularMarketPrice') or info.get('previousClose') or info.get('currentPrice')
            if price and float(price) > 0:
                prices[ticker] = round(float(price), 2)
                print(f"OK {ticker} (info): ${price:.2f}")
                continue
        except Exception:
            pass
        errors.append(ticker)
        print(f"ERROR {ticker}: no price found")
    except Exception as e:
        errors.append(ticker)
        print(f"ERROR {ticker}: {e}")

output = {
    "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    "prices": prices,
    "errors": errors
}

with open("prices.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\nGuardados {len(prices)}/{len(TICKERS)} precios en prices.json")
if errors:
    print(f"Errores: {errors}")
