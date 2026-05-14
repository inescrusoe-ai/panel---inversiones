import yfinance as yf
import json
from datetime import datetime, timezone

TICKERS = [
    "META", "MSFT", "MRK", "JNJ", "BSX", "CACI",
    "WDC", "JBL", "ADI", "CRDO", "CAT", "NEM",
    "GGAL", "SOLS", "ORCL", "CRS", "KTOS", "MARA"
]

prices = {}
errors = []

for ticker in TICKERS:
    try:
        t = yf.Ticker(ticker)
        
        # Method 1: history (most reliable)
        hist = t.history(period="2d")
        if not hist.empty:
            price = float(hist['Close'].iloc[-1])
            if price > 0:
                prices[ticker] = round(price, 2)
                print(f"OK {ticker}: ${price:.2f}")
                continue
        
        # Method 2: fast_info
        try:
            fi = t.fast_info
            price = getattr(fi, 'last_price', None) or getattr(fi, 'previous_close', None)
            if price and float(price) > 0:
                prices[ticker] = round(float(price), 2)
                print(f"OK {ticker} (fast_info): ${price:.2f}")
                continue
        except Exception:
            pass

        # Method 3: info dict
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
