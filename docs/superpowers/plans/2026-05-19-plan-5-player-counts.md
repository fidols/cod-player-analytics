# COD Analytics — Plan 5: Player Counts Page

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `pages/3_Player_Counts.py` — Steam concurrent player data showing MW2 (2022) and MW3 (2023) monthly averages, peak bar chart, and YoY change.

**Architecture:** Loads `data/steam_players.csv` with `@st.cache_data`. Uses `player_peak_by_title` and `yoy_player_change` from `utils/metrics.py`. Three charts: (1) overlapping line chart of monthly avg players per title, (2) bar chart of peak concurrent players per title, (3) YoY average player change bar. Includes a disclaimer about PC-only coverage.

**Tech Stack:** Python 3.12, Streamlit >= 1.32.0, Plotly Express >= 5.18.0, pandas >= 2.0.0

---

## File Map

| File | Change |
|---|---|
| `pages/3_Player_Counts.py` | Create |

---

## Task 1: Failing tests for steam player metrics

**Files:**
- Modify: `tests/test_metrics.py` (append)

- [ ] **Step 1: Append tests to tests/test_metrics.py**

Open `tests/test_metrics.py` and add at the bottom:

```python
# ── steam_players.csv integration (Player Counts assertions) ──────────────────

def test_steam_csv_mw2_has_higher_peak_than_mw3():
    """MW2 (2022) should have a higher peak player count than MW3 (2023)."""
    from pathlib import Path
    import pandas as pd
    csv_path = Path(__file__).parent.parent / "data" / "steam_players.csv"
    if not csv_path.exists():
        pytest.skip("data/steam_players.csv not yet generated")
    df = pd.read_csv(csv_path)
    from utils.metrics import player_peak_by_title
    peaks = player_peak_by_title(df)
    mw2_peak = peaks[peaks["title"] == "Call of Duty: Modern Warfare II"]["peak_players"].values
    mw3_peak = peaks[peaks["title"] == "Call of Duty: Modern Warfare III"]["peak_players"].values
    assert len(mw2_peak) == 1 and len(mw3_peak) == 1
    assert mw2_peak[0] > mw3_peak[0], "MW2 should have higher peak than MW3"


def test_yoy_player_change_returns_correct_years():
    """yoy_player_change output should contain both 2022 and 2023."""
    from pathlib import Path
    import pandas as pd
    csv_path = Path(__file__).parent.parent / "data" / "steam_players.csv"
    if not csv_path.exists():
        pytest.skip("data/steam_players.csv not yet generated")
    df = pd.read_csv(csv_path)
    from utils.metrics import yoy_player_change
    yoy = yoy_player_change(df)
    assert 2022 in yoy["year"].values
    assert 2023 in yoy["year"].values
```

- [ ] **Step 2: Run tests**

```bash
cd /Users/mr.fidols/github/cod-player-analytics && python -m pytest tests/test_metrics.py -v
```

Expected: all tests PASS or SKIP.

- [ ] **Step 3: Commit**

```bash
cd /Users/mr.fidols/github/cod-player-analytics
git add tests/test_metrics.py
git commit -m "test: add Player Counts integration assertions for MW2/MW3 peak comparison"
```

---

## Task 2: Build pages/3_Player_Counts.py

**Files:**
- Create: `pages/3_Player_Counts.py`

- [ ] **Step 1: Create pages/3_Player_Counts.py**

```python
import pandas as pd
import plotly.express as px
import streamlit as st

from utils.metrics import player_peak_by_title, yoy_player_change

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_steam():
    df = pd.read_csv("data/steam_players.csv", parse_dates=["date"])
    return df

steam_df = load_steam()

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("Player Counts")
st.caption("Stakeholders: Live Services · Analytics · Executive Leadership")
st.markdown(
    "Steam concurrent player data for titles with PC releases. "
    "Each new title since MW2 (2022) has launched with a lower peak and faster drop-off. "
    "The live service model that was supposed to retain players has instead accelerated churn."
)
st.info(
    "**Note:** Steam covers PC only. Console player counts are not publicly available. "
    "Data covers MW2 (2022, AppID 1938090) and MW3 (2023, AppID 2519060).",
    icon="ℹ️",
)

st.divider()

# ── KPI Cards ─────────────────────────────────────────────────────────────────
peaks = player_peak_by_title(steam_df)
yoy = yoy_player_change(steam_df)

total_peak = int(peaks["peak_players"].max()) if len(peaks) else 0
peak_title_name = peaks.iloc[0]["title"] if len(peaks) else "N/A"

latest_avg = int(steam_df.sort_values("date").groupby("title")["avg_players"].last().mean()) if len(steam_df) else 0

yoy_row = yoy.dropna(subset=["yoy_pct"])
latest_yoy = float(yoy_row.iloc[-1]["yoy_pct"]) if len(yoy_row) else 0.0

k1, k2, k3 = st.columns(3)
k1.metric("Peak Concurrent Players", f"{total_peak:,}", help=peak_title_name)
k2.metric("Latest Monthly Avg", f"{latest_avg:,}")
k3.metric(
    "YoY Player Change",
    f"{latest_yoy:.0%}",
    delta=f"{latest_yoy:.0%}",
)

st.divider()

# ── Chart 1: Monthly avg players per title ────────────────────────────────────
st.subheader("Monthly Average Players — All Tracked Titles")
st.caption("Overlapping lines show how each title's player base grew and declined over its lifecycle.")

title_colors = {
    "Call of Duty: Modern Warfare II": "#1A1A1A",
    "Call of Duty: Modern Warfare III": "#E31837",
}

fig_line = px.line(
    steam_df.sort_values("date"),
    x="date",
    y="avg_players",
    color="title",
    color_discrete_map=title_colors,
    markers=True,
    labels={"date": "Month", "avg_players": "Avg Concurrent Players", "title": "Title"},
)
fig_line.update_layout(
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    font_color="#1A1A1A",
    yaxis_tickformat=",",
    margin=dict(t=40, b=40),
)
fig_line.update_xaxes(tickfont=dict(color="#1A1A1A"), title_font=dict(color="#1A1A1A"))
fig_line.update_yaxes(tickfont=dict(color="#1A1A1A"), title_font=dict(color="#1A1A1A"))
st.plotly_chart(fig_line, use_container_width=True)

st.divider()

# ── Chart 2: Peak concurrent players bar ──────────────────────────────────────
st.subheader("Peak Concurrent Players by Title")
st.caption("All-time peak concurrent players recorded on Steam for each title.")

fig_peak = px.bar(
    peaks,
    x="title",
    y="peak_players",
    color_discrete_sequence=["#E31837"],
    text="peak_players",
    labels={"title": "Title", "peak_players": "Peak Concurrent Players"},
)
fig_peak.update_traces(texttemplate="%{text:,}", textposition="outside")
fig_peak.update_layout(
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    font_color="#1A1A1A",
    yaxis_tickformat=",",
    xaxis_tickangle=-15,
    margin=dict(t=60, b=80),
)
fig_peak.update_xaxes(tickfont=dict(color="#1A1A1A"), title_font=dict(color="#1A1A1A"))
fig_peak.update_yaxes(tickfont=dict(color="#1A1A1A"), title_font=dict(color="#1A1A1A"))
st.plotly_chart(fig_peak, use_container_width=True)

st.divider()

# ── Chart 3: YoY player change ─────────────────────────────────────────────────
st.subheader("Year-over-Year Average Player Change")
st.caption("Average concurrent players across all tracked titles per calendar year.")

yoy_display = yoy.copy()
yoy_display["year"] = yoy_display["year"].astype(str)

fig_yoy = px.bar(
    yoy_display,
    x="year",
    y="avg_players",
    color_discrete_sequence=["#1A1A1A"],
    text="avg_players",
    labels={"year": "Year", "avg_players": "Avg Concurrent Players"},
)
fig_yoy.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
fig_yoy.update_layout(
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    font_color="#1A1A1A",
    yaxis_tickformat=",",
    margin=dict(t=60, b=40),
)
fig_yoy.update_xaxes(tickfont=dict(color="#1A1A1A"), title_font=dict(color="#1A1A1A"))
fig_yoy.update_yaxes(tickfont=dict(color="#1A1A1A"), title_font=dict(color="#1A1A1A"))
st.plotly_chart(fig_yoy, use_container_width=True)

st.caption(
    "Source: SteamCharts.com — monthly average and peak concurrent player data. "
    "Fetched at build time via SteamCharts JSON API. PC platform only."
)
```

- [ ] **Step 2: Run the app to verify the page loads**

```bash
cd /Users/mr.fidols/github/cod-player-analytics && streamlit run app.py
```

Navigate to "Player Counts". Expected: info banner about PC-only, 3 KPI cards, monthly avg line chart with 2 overlapping title lines, peak concurrent bar chart, YoY bar chart. All text black.

If `data/steam_players.csv` doesn't exist, run `python data/fetch/fetch_steam.py` first.

- [ ] **Step 3: Commit**

```bash
cd /Users/mr.fidols/github/cod-player-analytics
git add pages/3_Player_Counts.py
git commit -m "feat: add Player Counts page — monthly avg, peak players, YoY change"
```
