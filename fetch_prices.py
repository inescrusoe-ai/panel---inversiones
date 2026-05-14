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
        info = t.fast_info
        price = info.get("last_price") or info.get("previous_close")
        if price and price > 0:
            prices[ticker] = round(float(price), 2)
            print(f"OK {ticker}: ${price:.2f}")
        else:
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
print(f"Actualizado: {output['updated']}")
