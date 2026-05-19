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


def fetch_keyword(pytrends: TrendReq, kw: str, retries: int = 3) -> pd.DataFrame:
    """Fetch interest_over_time for one keyword with basic retry on 429."""
    for attempt in range(1, retries + 1):
        try:
            pytrends.build_payload([kw], timeframe="all", geo="")
            df = pytrends.interest_over_time()
            if df.empty:
                print(f"  No data returned for '{kw}'")
                return pd.DataFrame()
            df = df[[kw]].reset_index()
            df.columns = ["date", "interest"]
            df["keyword"] = kw
            df["date"] = df["date"].dt.strftime("%Y-%m-%d")
            print(f"  {len(df)} rows: {df['date'].min()} – {df['date'].max()}")
            return df
        except Exception as exc:
            if "429" in str(exc) or "Too Many Requests" in str(exc):
                wait = 30 * attempt
                print(f"  Rate limited on attempt {attempt}/{retries}. Waiting {wait}s...")
                time.sleep(wait)
            else:
                raise
    print(f"  Failed to fetch '{kw}' after {retries} attempts.")
    return pd.DataFrame()


if __name__ == "__main__":
    pytrends = TrendReq(hl="en-US", tz=0)
    frames = []
    for kw in KEYWORDS:
        print(f"Fetching: {kw}")
        df = fetch_keyword(pytrends, kw)
        if not df.empty:
            frames.append(df)
        time.sleep(5)

    if not frames:
        raise RuntimeError("No data fetched for any keyword — check network/API access.")

    result = pd.concat(frames, ignore_index=True)
    result.to_csv(OUT, index=False)
    print(f"Wrote {len(result)} rows to {OUT}")
