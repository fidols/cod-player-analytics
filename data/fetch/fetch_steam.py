"""
Fetches monthly player data from SteamCharts for COD titles available on Steam.
Run: python data/fetch/fetch_steam.py
Output: data/steam_players.csv
"""
import time
import requests
import pandas as pd
from pathlib import Path

OUT = Path(__file__).parent.parent / "steam_players.csv"

TITLES = [
    (1938090, "Call of Duty: Modern Warfare II"),
    (2519060, "Call of Duty: Modern Warfare III"),
]

HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}


def fetch_title(app_id: int, title: str, retries: int = 3) -> pd.DataFrame:
    """Fetch monthly player data from SteamCharts JSON endpoint.

    The chart-data.json endpoint returns entries as [timestamp_ms, avg_players].
    peak_players is not available via this endpoint, so it mirrors avg_players.
    """
    url = f"https://steamcharts.com/app/{app_id}/chart-data.json"
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            # Each entry: [timestamp_ms, avg_players]
            rows = []
            for entry in data:
                if entry[1] is None or entry[1] == 0:
                    continue
                avg = int(entry[1])
                peak = int(entry[2]) if len(entry) > 2 and entry[2] else avg
                rows.append({
                    "date": pd.Timestamp(entry[0], unit="ms").strftime("%Y-%m-%d"),
                    "app_id": str(app_id),
                    "title": title,
                    "avg_players": avg,
                    "peak_players": peak,
                })
            df = pd.DataFrame(rows)
            print(f"  {len(df)} months of data: {df['date'].min()} – {df['date'].max()}")
            return df
        except Exception as exc:
            wait = 10 * attempt
            print(f"  Error on attempt {attempt}/{retries}: {exc}. Waiting {wait}s...")
            time.sleep(wait)
    print(f"  Failed to fetch AppID {app_id} after {retries} attempts.")
    return pd.DataFrame()


if __name__ == "__main__":
    frames = []
    for app_id, title in TITLES:
        print(f"Fetching Steam data for {title} (AppID {app_id})")
        df = fetch_title(app_id, title)
        if not df.empty:
            frames.append(df)
        time.sleep(2)

    if not frames:
        raise RuntimeError("No Steam data fetched — check network access.")

    result = pd.concat(frames, ignore_index=True)
    result.to_csv(OUT, index=False)
    print(f"Wrote {len(result)} rows to {OUT}")
