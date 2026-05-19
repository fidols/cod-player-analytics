"""
Fetches Google Trends data for COD keywords.
Run: python data/fetch/fetch_trends.py
Output: data/trends.csv
"""
import time
import pandas as pd
from pathlib import Path
from pytrends.request import TrendReq

OUT = Path(__file__).parent.parent / "trends.csv"

KEYWORDS = ["Call of Duty", "Warzone", "Black Ops"]

pytrends = TrendReq(hl="en-US", tz=0)

frames = []
for kw in KEYWORDS:
    print(f"Fetching: {kw}")
    pytrends.build_payload([kw], timeframe="all", geo="")
    df = pytrends.interest_over_time()
    if df.empty:
        print(f"  No data for {kw}")
        continue
    df = df[[kw]].reset_index()
    df.columns = ["date", "interest"]
    df["keyword"] = kw
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    frames.append(df)
    time.sleep(2)  # avoid rate limiting

result = pd.concat(frames, ignore_index=True)
result.to_csv(OUT, index=False)
print(f"Wrote {len(result)} rows to {OUT}")
