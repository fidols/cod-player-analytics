# COD Analytics — Plan 1: Foundation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scaffold the project, generate all data CSVs, and implement + test all utility functions in `utils/metrics.py`.

**Architecture:** `data/fetch/` scripts generate CSVs committed to `data/`. `games.csv` is hardcoded (static historical data). `trends.csv` is fetched via pytrends. `steam_players.csv` is scraped from SteamCharts. `utils/metrics.py` provides pure aggregation functions with no I/O. All functions are unit-tested before any UI work.

**Tech Stack:** Python 3.12, pandas >= 2.0.0, NumPy >= 1.26.0, pytrends, requests, pytest

---

## File Map

| File | Change |
|---|---|
| `requirements.txt` | Create |
| `.gitignore` | Create |
| `data/fetch/fetch_games.py` | Create — writes hardcoded games.csv |
| `data/fetch/fetch_trends.py` | Create — pulls Google Trends via pytrends |
| `data/fetch/fetch_steam.py` | Create — scrapes SteamCharts |
| `data/games.csv` | Create (generated) |
| `data/trends.csv` | Create (generated) |
| `data/steam_players.csv` | Create (generated) |
| `utils/__init__.py` | Create (empty) |
| `utils/metrics.py` | Create — 6 pure aggregation functions |
| `tests/__init__.py` | Create (empty) |
| `tests/test_metrics.py` | Create — 15 unit tests |

---

## Task 1: Project scaffold

**Files:**
- Create: `requirements.txt`
- Create: `.gitignore`
- Create: `utils/__init__.py`
- Create: `tests/__init__.py`

- [ ] **Step 1: Create requirements.txt**

```
streamlit>=1.32.0
pandas>=2.0.0
numpy>=1.26.0
plotly>=5.18.0
pytrends>=4.9.2
requests>=2.31.0
beautifulsoup4>=4.12.0
pytest>=8.0.0
```

- [ ] **Step 2: Create .gitignore**

```
__pycache__/
*.pyc
.venv/
venv/
.env
.DS_Store
```

- [ ] **Step 3: Create empty init files**

```bash
touch /Users/mr.fidols/github/cod-player-analytics/utils/__init__.py
touch /Users/mr.fidols/github/cod-player-analytics/tests/__init__.py
```

- [ ] **Step 4: Install dependencies**

```bash
cd /Users/mr.fidols/github/cod-player-analytics && pip install -r requirements.txt
```

- [ ] **Step 5: Commit**

```bash
cd /Users/mr.fidols/github/cod-player-analytics
git add requirements.txt .gitignore utils/__init__.py tests/__init__.py
git commit -m "feat: project scaffold — requirements, gitignore, package structure"
```

---

## Task 2: games.csv — franchise timeline

**Files:**
- Create: `data/fetch/fetch_games.py`
- Create: `data/games.csv` (generated)

- [ ] **Step 1: Create data/fetch/ directory**

```bash
mkdir -p /Users/mr.fidols/github/cod-player-analytics/data/fetch
touch /Users/mr.fidols/github/cod-player-analytics/data/__init__.py
touch /Users/mr.fidols/github/cod-player-analytics/data/fetch/__init__.py
```

- [ ] **Step 2: Create data/fetch/fetch_games.py**

```python
"""
Writes hardcoded franchise data to data/games.csv.
Metacritic and user scores sourced from metacritic.com (PC platform where available).
Run: python data/fetch/fetch_games.py
"""
import pandas as pd
from pathlib import Path

OUT = Path(__file__).parent.parent / "games.csv"

GAMES = [
    ("Call of Duty",                    2003, "Infinity Ward",      "Classic",      91,  8.5, None),
    ("Call of Duty 2",                  2005, "Infinity Ward",      "Classic",      86,  8.2, None),
    ("Call of Duty 3",                  2006, "Treyarch",           "Classic",      82,  7.1, None),
    ("Call of Duty 4: Modern Warfare",  2007, "Infinity Ward",      "Classic",      94,  8.7, None),
    ("Call of Duty: World at War",      2008, "Treyarch",           "Classic",      83,  7.8, None),
    ("Call of Duty: Modern Warfare 2",  2009, "Infinity Ward",      "Classic",      86,  5.1, None),
    ("Call of Duty: Black Ops",         2010, "Treyarch",           "Classic",      87,  7.6, None),
    ("Call of Duty: Modern Warfare 3",  2011, "Infinity Ward",      "Classic",      78,  2.7, None),
    ("Call of Duty: Black Ops II",      2012, "Treyarch",           "Classic",      83,  7.1, None),
    ("Call of Duty: Ghosts",            2013, "Infinity Ward",      "Transitional", 68,  2.4, None),
    ("Call of Duty: Advanced Warfare",  2014, "Sledgehammer Games", "Transitional", 74,  4.7, None),
    ("Call of Duty: Black Ops III",     2015, "Treyarch",           "Transitional", 73,  5.1, None),
    ("Call of Duty: Infinite Warfare",  2016, "Infinity Ward",      "Transitional", 76,  2.6, None),
    ("Call of Duty: WWII",              2017, "Sledgehammer Games", "Transitional", 77,  5.4, None),
    ("Call of Duty: Black Ops 4",       2018, "Treyarch",           "Live Service", 83,  5.3, None),
    ("Call of Duty: Modern Warfare",    2019, "Infinity Ward",      "Live Service", 81,  6.2, None),
    ("Call of Duty: Black Ops Cold War",2020, "Treyarch",           "Live Service", 76,  5.0, None),
    ("Call of Duty: Vanguard",          2021, "Sledgehammer Games", "Live Service", 63,  2.2, None),
    ("Call of Duty: Modern Warfare II", 2022, "Infinity Ward",      "Live Service", 73,  4.2, 1938090),
    ("Call of Duty: Modern Warfare III",2023, "Infinity Ward",      "Live Service", 56,  3.7, 2519060),
    ("Call of Duty: Black Ops 6",       2024, "Treyarch",           "Live Service", 75,  6.3, None),
    ("Call of Duty: Black Ops 7",       2025, "Treyarch",           "Live Service", None, None, None),
]

df = pd.DataFrame(GAMES, columns=[
    "title", "year", "developer", "era",
    "metacritic_score", "user_score", "steam_app_id",
])
df.to_csv(OUT, index=False)
print(f"Wrote {len(df)} rows to {OUT}")
```

- [ ] **Step 3: Run to generate games.csv**

```bash
cd /Users/mr.fidols/github/cod-player-analytics && python data/fetch/fetch_games.py
```

Expected: `Wrote 22 rows to .../data/games.csv`

- [ ] **Step 4: Commit**

```bash
cd /Users/mr.fidols/github/cod-player-analytics
git add data/fetch/fetch_games.py data/games.csv data/__init__.py data/fetch/__init__.py
git commit -m "feat: add franchise timeline data — 22 titles, World at War through Black Ops 7"
```

---

## Task 3: trends.csv — Google Trends data

**Files:**
- Create: `data/fetch/fetch_trends.py`
- Create: `data/trends.csv` (generated)

- [ ] **Step 1: Create data/fetch/fetch_trends.py**

```python
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
```

- [ ] **Step 2: Run to generate trends.csv**

```bash
cd /Users/mr.fidols/github/cod-player-analytics && python data/fetch/fetch_trends.py
```

Expected: `Wrote ~2500 rows to .../data/trends.csv` (3 keywords × ~240 months × ~monthly granularity)

- [ ] **Step 3: Commit**

```bash
cd /Users/mr.fidols/github/cod-player-analytics
git add data/fetch/fetch_trends.py data/trends.csv
git commit -m "feat: add Google Trends data for Call of Duty, Warzone, Black Ops"
```

---

## Task 4: steam_players.csv — SteamCharts data

**Files:**
- Create: `data/fetch/fetch_steam.py`
- Create: `data/steam_players.csv` (generated)

- [ ] **Step 1: Create data/fetch/fetch_steam.py**

```python
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

frames = []
for app_id, title in TITLES:
    print(f"Fetching Steam data for {title} (AppID {app_id})")
    url = f"https://steamcharts.com/app/{app_id}/chart-data.json"
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    # Each entry: [timestamp_ms, avg_players, peak_players]
    rows = []
    for entry in data:
        if entry[1] is None:
            continue
        rows.append({
            "date": pd.Timestamp(entry[0], unit="ms").strftime("%Y-%m-%d"),
            "app_id": str(app_id),
            "title": title,
            "avg_players": int(entry[1]),
            "peak_players": int(entry[2]) if entry[2] else int(entry[1]),
        })
    df = pd.DataFrame(rows)
    frames.append(df)
    print(f"  {len(df)} months of data")
    time.sleep(2)

result = pd.concat(frames, ignore_index=True)
result.to_csv(OUT, index=False)
print(f"Wrote {len(result)} rows to {OUT}")
```

- [ ] **Step 2: Run to generate steam_players.csv**

```bash
cd /Users/mr.fidols/github/cod-player-analytics && python data/fetch/fetch_steam.py
```

Expected: `Wrote ~50+ rows` (2 titles × ~25 months each)

- [ ] **Step 3: Commit**

```bash
cd /Users/mr.fidols/github/cod-player-analytics
git add data/fetch/fetch_steam.py data/steam_players.csv
git commit -m "feat: add Steam player count data for MW2 and MW3"
```

---

## Task 5: utils/metrics.py — failing tests first

**Files:**
- Create: `tests/test_metrics.py`
- Create: `utils/metrics.py`

- [ ] **Step 1: Create tests/test_metrics.py with all 15 failing tests**

```python
import math
import pandas as pd
import pytest
from utils.metrics import (
    era_summary,
    score_gap,
    peak_interest_month,
    interest_decline_pct,
    player_peak_by_title,
    yoy_player_change,
)


# ── era_summary ───────────────────────────────────────────────────────────────

def test_era_summary_avg_correct():
    df = pd.DataFrame([
        {"title": "A", "year": 2007, "era": "Classic", "metacritic_score": 94.0, "user_score": 8.7},
        {"title": "B", "year": 2010, "era": "Classic", "metacritic_score": 87.0, "user_score": 7.6},
        {"title": "C", "year": 2013, "era": "Transitional", "metacritic_score": 68.0, "user_score": 2.4},
    ])
    result = era_summary(df)
    classic = result[result["era"] == "Classic"]["avg_metacritic"].values[0]
    assert abs(classic - 90.5) < 0.1


def test_era_summary_title_count():
    df = pd.DataFrame([
        {"title": "A", "year": 2007, "era": "Classic", "metacritic_score": 94.0, "user_score": 8.7},
        {"title": "B", "year": 2010, "era": "Classic", "metacritic_score": 87.0, "user_score": 7.6},
    ])
    result = era_summary(df)
    assert result[result["era"] == "Classic"]["title_count"].values[0] == 2


def test_era_summary_drops_null_scores():
    df = pd.DataFrame([
        {"title": "BO7", "year": 2025, "era": "Live Service", "metacritic_score": None, "user_score": None},
    ])
    result = era_summary(df)
    assert len(result) == 0


# ── score_gap ─────────────────────────────────────────────────────────────────

def test_score_gap_positive_gap():
    df = pd.DataFrame([
        {"title": "MW2", "year": 2009, "era": "Classic",
         "metacritic_score": 86.0, "user_score": 5.1, "developer": "IW"},
    ])
    result = score_gap(df)
    # gap = 86 - (5.1 * 10) = 86 - 51 = 35
    assert abs(result["gap"].values[0] - 35.0) < 0.1


def test_score_gap_drops_nulls():
    df = pd.DataFrame([
        {"title": "BO7", "year": 2025, "era": "Live Service",
         "metacritic_score": None, "user_score": None, "developer": "Treyarch"},
    ])
    result = score_gap(df)
    assert len(result) == 0


def test_score_gap_columns():
    df = pd.DataFrame([
        {"title": "CoD4", "year": 2007, "era": "Classic",
         "metacritic_score": 94.0, "user_score": 8.7, "developer": "IW"},
    ])
    result = score_gap(df)
    assert set(["title", "year", "metacritic_score", "user_score", "gap"]).issubset(result.columns)


# ── peak_interest_month ───────────────────────────────────────────────────────

def test_peak_interest_month_correct():
    df = pd.DataFrame([
        {"keyword": "Call of Duty", "date": "2020-03-01", "interest": 100},
        {"keyword": "Call of Duty", "date": "2021-01-01", "interest": 60},
        {"keyword": "Call of Duty", "date": "2022-01-01", "interest": 40},
    ])
    result = peak_interest_month(df, "Call of Duty")
    assert result == "2020-03-01"


def test_peak_interest_month_empty_returns_empty_string():
    df = pd.DataFrame(columns=["keyword", "date", "interest"])
    result = peak_interest_month(df, "Call of Duty")
    assert result == ""


def test_peak_interest_month_wrong_keyword_returns_empty_string():
    df = pd.DataFrame([
        {"keyword": "Warzone", "date": "2020-03-01", "interest": 100},
    ])
    result = peak_interest_month(df, "Call of Duty")
    assert result == ""


# ── interest_decline_pct ──────────────────────────────────────────────────────

def test_interest_decline_pct_correct():
    df = pd.DataFrame([
        {"keyword": "Call of Duty", "date": "2020-03-01", "interest": 100},
        {"keyword": "Call of Duty", "date": "2024-01-01", "interest": 30},
    ])
    result = interest_decline_pct(df, "Call of Duty")
    assert abs(result - 0.70) < 0.01


def test_interest_decline_pct_empty_returns_zero():
    df = pd.DataFrame(columns=["keyword", "date", "interest"])
    result = interest_decline_pct(df, "Call of Duty")
    assert result == 0.0


# ── player_peak_by_title ──────────────────────────────────────────────────────

def test_player_peak_by_title_correct():
    df = pd.DataFrame([
        {"title": "MW2", "date": "2022-11-01", "app_id": "1938090",
         "avg_players": 50000, "peak_players": 120000},
        {"title": "MW2", "date": "2022-12-01", "app_id": "1938090",
         "avg_players": 45000, "peak_players": 95000},
        {"title": "MW3", "date": "2023-11-01", "app_id": "2519060",
         "avg_players": 30000, "peak_players": 80000},
    ])
    result = player_peak_by_title(df)
    assert result[result["title"] == "MW2"]["peak_players"].values[0] == 120000


def test_player_peak_by_title_sorted_descending():
    df = pd.DataFrame([
        {"title": "MW3", "date": "2023-11-01", "app_id": "2519060",
         "avg_players": 30000, "peak_players": 80000},
        {"title": "MW2", "date": "2022-11-01", "app_id": "1938090",
         "avg_players": 50000, "peak_players": 120000},
    ])
    result = player_peak_by_title(df)
    assert result.iloc[0]["title"] == "MW2"


# ── yoy_player_change ─────────────────────────────────────────────────────────

def test_yoy_player_change_decline():
    df = pd.DataFrame([
        {"title": "MW2", "date": "2022-11-01", "app_id": "1938090",
         "avg_players": 50000, "peak_players": 120000},
        {"title": "MW3", "date": "2023-11-01", "app_id": "2519060",
         "avg_players": 25000, "peak_players": 80000},
    ])
    result = yoy_player_change(df)
    row_2023 = result[result["year"] == 2023]
    assert abs(row_2023["yoy_pct"].values[0] - (-0.50)) < 0.01


def test_yoy_player_change_first_year_is_nan():
    df = pd.DataFrame([
        {"title": "MW2", "date": "2022-11-01", "app_id": "1938090",
         "avg_players": 50000, "peak_players": 120000},
    ])
    result = yoy_player_change(df)
    assert math.isnan(result.iloc[0]["yoy_pct"])
```

- [ ] **Step 2: Run to confirm all 15 tests fail**

```bash
cd /Users/mr.fidols/github/cod-player-analytics && python -m pytest tests/test_metrics.py -v
```

Expected: 15 FAILED with `ImportError: cannot import name 'era_summary' from 'utils.metrics'`

---

## Task 6: utils/metrics.py — implement all 6 functions

**Files:**
- Create: `utils/metrics.py`

- [ ] **Step 1: Create utils/metrics.py**

```python
import pandas as pd


def era_summary(games_df: pd.DataFrame) -> pd.DataFrame:
    """Average Metacritic score and title count per era. Drops rows with null metacritic_score."""
    return (
        games_df.dropna(subset=["metacritic_score"])
        .groupby("era")
        .agg(
            avg_metacritic=("metacritic_score", "mean"),
            title_count=("title", "count"),
        )
        .reset_index()
    )


def score_gap(games_df: pd.DataFrame) -> pd.DataFrame:
    """
    Critic score minus (user_score × 10) per title.
    Positive = critics liked it more than players. Drops rows missing either score.
    Returns columns: title, year, metacritic_score, user_score, gap.
    """
    df = games_df.dropna(subset=["metacritic_score", "user_score"]).copy()
    df["gap"] = df["metacritic_score"] - (df["user_score"] * 10)
    return df[["title", "year", "metacritic_score", "user_score", "gap"]].reset_index(drop=True)


def peak_interest_month(trends_df: pd.DataFrame, keyword: str) -> str:
    """Date string of the month with peak Google Trends interest for a keyword. Returns '' if no data."""
    df = trends_df[trends_df["keyword"] == keyword]
    if df.empty:
        return ""
    return str(df.loc[df["interest"].idxmax(), "date"])


def interest_decline_pct(trends_df: pd.DataFrame, keyword: str) -> float:
    """
    Fractional decline from peak interest to the most recent month.
    Returns 0.0 if fewer than 2 data points or keyword not found.
    """
    df = trends_df[trends_df["keyword"] == keyword].sort_values("date")
    if len(df) < 2:
        return 0.0
    peak = df["interest"].max()
    if peak == 0:
        return 0.0
    return float((peak - df.iloc[-1]["interest"]) / peak)


def player_peak_by_title(steam_df: pd.DataFrame) -> pd.DataFrame:
    """
    Peak and mean concurrent players per title, sorted by peak descending.
    Returns columns: title, peak_players, avg_players.
    """
    return (
        steam_df.groupby("title")
        .agg(
            peak_players=("peak_players", "max"),
            avg_players=("avg_players", "mean"),
        )
        .reset_index()
        .sort_values("peak_players", ascending=False)
        .reset_index(drop=True)
    )


def yoy_player_change(steam_df: pd.DataFrame) -> pd.DataFrame:
    """
    Year-over-year % change in average concurrent players across all tracked titles.
    Returns columns: year, avg_players, yoy_pct (NaN for first year).
    """
    df = steam_df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    yearly = (
        df.groupby("year")["avg_players"]
        .mean()
        .reset_index()
    )
    yearly["yoy_pct"] = yearly["avg_players"].pct_change()
    return yearly
```

- [ ] **Step 2: Run full test suite**

```bash
cd /Users/mr.fidols/github/cod-player-analytics && python -m pytest tests/test_metrics.py -v
```

Expected: **15 PASSED**

- [ ] **Step 3: Commit**

```bash
cd /Users/mr.fidols/github/cod-player-analytics
git add utils/metrics.py tests/test_metrics.py
git commit -m "feat: add utils/metrics.py with 6 functions — 15 tests passing"
```
