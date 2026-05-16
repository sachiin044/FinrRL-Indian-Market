import yfinance as yf
import pandas as pd
from pathlib import Path

out = Path("data/fmp_daily")
out.mkdir(parents=True, exist_ok=True)

symbols = [
    ("^GSPC", "^GSPC"),
    ("^VIX", "^VIX"),
    ("QQQ", "QQQ")
]

for ticker, filename in symbols:
    print(f"Downloading {ticker}...")

    df = yf.download(
        ticker,
        start="2017-01-01",
        progress=False,
        auto_adjust=False
    )

    df = df.reset_index()

    df.columns = [
        c[0].lower() if isinstance(c, tuple) else str(c).lower()
        for c in df.columns
    ]

    df = df[["date", "open", "high", "low", "close", "volume"]]

    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

    output_file = out / f"{filename}_daily.csv"

    df.to_csv(output_file, index=False)

    print("Saved:", output_file)