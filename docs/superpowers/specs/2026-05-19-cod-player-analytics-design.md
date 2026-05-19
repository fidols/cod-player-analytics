# Call of Duty Player Analytics — Design Spec

## Overview

A Streamlit BI dashboard that traces the rise and decline of the Call of Duty franchise through real public data. The narrative anchor is personal: the analyst started playing at age 8 with World at War and quit around Black Ops 7 — this dashboard is an attempt to understand why through data.

Built as a portfolio project for the Activision Data Analyst, Analytics Insights role (Req R027533). Demonstrates player engagement analysis, trend identification, and the ability to translate complex data into a compelling story for both technical and non-technical audiences.

**Audience:** Activision hiring team, Live Services analytics stakeholders

**Decisions it supports:**
- Identifying where in the franchise lifecycle player engagement began to decline
- Understanding which signals (quality, interest, concurrent players) predict churn
- Connecting the player experience to measurable engagement outcomes

---

## Tech Stack

- Python 3.12
- Streamlit >= 1.32.0
- Plotly Express >= 5.18.0
- pandas >= 2.0.0
- NumPy >= 1.26.0
- pytrends (Google Trends API client)
- pytest

---

## Data Sources

All data is fetched at build time by scripts in `data/fetch/` and committed as CSVs to `data/`. No API keys are required at runtime.

| File | Source | Fetch method |
|---|---|---|
| `data/games.csv` | Wikipedia / manual | Hand-curated from public sources |
| `data/metacritic.csv` | Metacritic | `data/fetch/fetch_metacritic.py` (requests + BeautifulSoup) |
| `data/trends.csv` | Google Trends | `data/fetch/fetch_trends.py` (pytrends) |
| `data/steam_players.csv` | SteamDB (manual export) | `data/fetch/fetch_steam.py` or manual CSV |

### games.csv schema
```
title, year, developer, platform_focus, era, metacritic_score, steam_app_id
```

**Era classification:**
- Classic (2008–2012): World at War, MW1, MW2, Black Ops 1, MW3
- Transitional (2013–2017): Ghosts, Advanced Warfare, Black Ops 3, Infinite Warfare, WWII
- Live Service (2018–present): Black Ops 4, MW2019, Cold War, Vanguard, MW2, MW3, BO6, BO7

### metacritic.csv schema
```
title, year, metacritic_score, user_score, platform
```
Scores scraped for PC platform where available, console otherwise.

### trends.csv schema
```
date, interest (0–100 normalized), keyword
```
Keywords: "Call of Duty", "Warzone", "Black Ops"
Monthly granularity, 2004–present.

### steam_players.csv schema
```
date, app_id, title, avg_players, peak_players
```
Monthly averages. Covers: MW2019/Warzone (AppID 393080), Cold War, Vanguard, MW2 (1938090), MW3 (2519060), BO6.

---

## File Map

```
cod-player-analytics/
├── app.py                        # Entry point, overview page
├── requirements.txt
├── data/
│   ├── fetch/
│   │   ├── fetch_metacritic.py   # Scrape Metacritic scores
│   │   ├── fetch_trends.py       # Pull Google Trends via pytrends
│   │   └── fetch_steam.py        # Pull Steam player data
│   ├── games.csv                 # Hand-curated franchise timeline
│   ├── metacritic.csv            # Scraped scores
│   ├── trends.csv                # Google Trends export
│   └── steam_players.csv         # Steam concurrent players
├── utils/
│   └── metrics.py                # Pure aggregation functions
├── tests/
│   └── test_metrics.py           # pytest unit tests
└── pages/
    ├── 1_Quality_Arc.py
    ├── 2_Search_Interest.py
    ├── 3_Player_Counts.py
    └── 4_Churn_Analysis.py
```

---

## Pages

### app.py — Overview

**Personal narrative banner:**
> "I started playing Call of Duty at age 8 with World at War. I quit around Black Ops 7. This dashboard is my attempt to understand why — through data."

**Content:**
- Narrative banner with the personal story and context for the role
- Franchise timeline: horizontal bar or scatter of all titles by year, colored by era (Classic / Transitional / Live Service)
- Three KPI cards: Total titles (25+), Years of franchise history, Peak concurrent Steam players
- Caption: data sources and methodology note

---

### 1_Quality_Arc.py — Quality Over Time

**Story:** Metacritic scores show a clear quality peak in the MW2/Black Ops 1 era (~2009–2011), a dip during the jetpack era (~2014–2017), a recovery with MW2019, then inconsistency through the live service era.

**Charts:**
- Line chart: Metacritic score by release year, with era color bands as background shapes
- Bar chart: critic score vs. user score side-by-side — shows the growing gap between press and players
- Annotation: personal "quit point" marked on the timeline

**Metrics:** Peak score, lowest score, average by era

---

### 2_Search_Interest.py — Player Interest Over Time

**Story:** Google Trends for "Call of Duty" shows a dramatic spike with Warzone's launch (March 2020, COVID lockdowns), followed by a steep and sustained decline. The franchise never recovered to pre-Warzone organic interest.

**Charts:**
- Area chart: "Call of Duty" search interest 2004–present, with key release dates annotated
- Line chart: comparison of "Call of Duty" vs. "Warzone" vs. "Black Ops" as separate trends
- Annotation: Warzone launch, Ricochet anti-cheat launch, BO6 on Game Pass

**Metrics:** Peak interest month, current interest vs. peak (% decline), longest sustained decline period

---

### 3_Player_Counts.py — Steam Player Data

**Story:** Warzone drove an enormous concurrent player spike in 2020. Since then, each new title has launched with lower peaks and faster drop-offs. The live service model that was supposed to retain players has instead accelerated churn.

**Charts:**
- Line chart: monthly average players per title over time (overlapping lines)
- Bar chart: peak concurrent players per title (available titles only)
- Annotation: season launches, major patches, battle pass drops where dateable

**Metrics:** Peak players (Warzone), latest monthly average, YoY decline %

**Note:** BO7 included with available data; marked as "latest entry" if Metacritic/Steam data is incomplete at build time.

---

### 4_Churn_Analysis.py — The Full Picture

**Story:** No single factor killed COD — it was the combination. When quality dropped AND search interest fell AND player counts declined simultaneously, that's when players like me quit. This page overlays all three signals.

**Charts:**
- Normalized multi-line chart: Metacritic score (indexed), search interest, and Steam players all on the same 0–100 scale by year — shows the three signals converging downward
- Scatter plot: quality score vs. player retention (peak players for that title's lifecycle) — does higher Metacritic score predict better retention?
- Callout: the "churn zone" — the cluster of years where all three signals fell together

**Metrics:** Correlation between Metacritic score and player peak, year all three signals first declined simultaneously

---

## utils/metrics.py — Functions

| Function | Inputs | Output |
|---|---|---|
| `era_summary(games_df)` | games_df | DataFrame: era, avg_metacritic, title_count |
| `score_gap(metacritic_df)` | metacritic_df | DataFrame: title, year, gap (critic - user score) |
| `peak_interest_month(trends_df, keyword)` | trends_df, str | date of peak interest |
| `interest_decline_pct(trends_df, keyword)` | trends_df, str | float: % decline from peak to latest |
| `player_peak_by_title(steam_df)` | steam_df | DataFrame: title, peak_players, avg_players |
| `yoy_player_change(steam_df)` | steam_df | DataFrame: year, avg_players, yoy_pct |

---

## Testing

`tests/test_metrics.py` covers all 6 utility functions with unit tests using small hand-crafted DataFrames. Target: 15+ tests.

---

## Visual Style

Consistent with portfolio aesthetic:
- Background: `#FFFFFF`
- Primary accent: `#E31837` (COD red — also matches Activision brand)
- Era colors: Classic `#1A1A1A`, Transitional `#6D6E71`, Live Service `#E31837`
- All axis fonts explicitly set to `#1A1A1A`
- `use_container_width=True` on all charts

---

## Data Notes

- Metacritic scores are public and scrapable; if scraping is blocked, scores will be hand-entered from the public site
- Google Trends data is normalized (0–100 relative, not absolute search volume)
- Steam data covers only PC; console player counts are not public
- BO7 data included where available; missing fields marked clearly in the UI
- All data sources cited in page captions
