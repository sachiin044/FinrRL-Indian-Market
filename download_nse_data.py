import yfinance as yf
import pandas as pd
from pathlib import Path

# Add NSE symbols here (Yahoo format usually uses .NS)
symbols = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "LT.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "AXISBANK.NS",
    # proxy ETFs / defensive names you may use:
    "NIFTYBEES.NS", "GOLDBEES.NS"
]

out_dir = Path("data/fmp_daily")
out_dir.mkdir(parents=True, exist_ok=True)

start = "2017-01-01"
failed = []

for sym in symbols:
    try:
        df = yf.download(sym, start=start, progress=False, auto_adjust=False)
        if df.empty:
            failed.append(sym)
            print(f"FAIL empty: {sym}")
            continue

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df.reset_index()
        df.columns = [c.lower() for c in df.columns]
        df = df[["date", "open", "high", "low", "close", "volume"]]
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
        df.to_csv(out_dir / f"{sym}_daily.csv", index=False)

        print(f"OK: {sym} ({len(df)} rows)")
    except Exception as e:
        failed.append(sym)
        print(f"FAIL: {sym} - {e}")

print(f"\nDone. Success={len(symbols)-len(failed)}, Failed={len(failed)}")
if failed:
    print("Failed symbols:", failed)


