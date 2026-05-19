# COD Analytics — Plan 2: Overview Page (app.py)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Streamlit entry point (`app.py`) — personal narrative banner, franchise timeline scatter, and three KPI cards.

**Architecture:** `app.py` loads `data/games.csv` directly with pandas (no session state needed for static data). The franchise timeline is a Plotly scatter chart colored by era. KPI cards use `st.metric`. No utility functions are needed for this page — all aggregation is inline and trivial.

**Tech Stack:** Python 3.12, Streamlit >= 1.32.0, Plotly Express >= 5.18.0, pandas >= 2.0.0

---

## File Map

| File | Change |
|---|---|
| `app.py` | Create — entry point with narrative, timeline, KPI cards |
| `pages/__init__.py` | Create (empty, marks pages as package directory) |

---

## Task 1: Failing test for data loading contract

**Files:**
- Modify: `tests/test_metrics.py` (append new test at end)

The Overview page depends on `data/games.csv` having specific columns. This test verifies the schema contract so if fetch_games.py is ever changed, the test catches it.

- [ ] **Step 1: Append the schema test to tests/test_metrics.py**

Open `tests/test_metrics.py` and add at the bottom:

```python
# ── games.csv schema contract ─────────────────────────────────────────────────

def test_games_csv_schema():
    """Verify games.csv has the expected columns and row count."""
    from pathlib import Path
    import pandas as pd
    csv_path = Path(__file__).parent.parent / "data" / "games.csv"
    if not csv_path.exists():
        pytest.skip("data/games.csv not yet generated — run data/fetch/fetch_games.py first")
    df = pd.read_csv(csv_path)
    expected_cols = {"title", "year", "developer", "era", "metacritic_score", "user_score", "steam_app_id"}
    assert expected_cols.issubset(df.columns)
    assert len(df) == 22
```

- [ ] **Step 2: Run to confirm test passes (or skips if CSV not generated yet)**

```bash
cd /Users/mr.fidols/github/cod-player-analytics && python -m pytest tests/test_metrics.py::test_games_csv_schema -v
```

Expected: PASSED (or SKIPPED if games.csv not present)

- [ ] **Step 3: Commit**

```bash
cd /Users/mr.fidols/github/cod-player-analytics
git add tests/test_metrics.py
git commit -m "test: add games.csv schema contract test"
```

---

## Task 2: Create app.py — Overview page

**Files:**
- Create: `app.py`
- Create: `pages/__init__.py`

- [ ] **Step 1: Create pages/__init__.py**

```bash
mkdir -p /Users/mr.fidols/github/cod-player-analytics/pages
touch /Users/mr.fidols/github/cod-player-analytics/pages/__init__.py
```

- [ ] **Step 2: Create app.py**

```python
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Call of Duty Player Analytics",
    page_icon="🎮",
    layout="wide",
)

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_games():
    return pd.read_csv("data/games.csv")

games_df = load_games()

# ── Narrative Banner ──────────────────────────────────────────────────────────
st.title("Call of Duty Player Analytics")
st.caption("Portfolio project for Activision Data Analyst, Analytics Insights — Req R027533")

st.markdown(
    """
    > *"I started playing Call of Duty at age 8 with World at War. I quit around Black Ops 7.
    > This dashboard is my attempt to understand why — through data."*

    **What this is:** A BI dashboard tracing the rise and decline of the Call of Duty franchise
    through public data — Metacritic scores, Google Trends interest, and Steam concurrent player counts.

    **Audience:** Activision hiring team and Live Services analytics stakeholders.

    **Decisions it supports:**
    - Identifying where in the franchise lifecycle player engagement began to decline
    - Understanding which signals (quality, interest, concurrent players) predict churn
    - Connecting the player experience to measurable engagement outcomes
    """
)

st.divider()

# ── KPI Cards ─────────────────────────────────────────────────────────────────
st.subheader("Franchise at a Glance")

scored = games_df.dropna(subset=["metacritic_score"])
peak_score = int(scored["metacritic_score"].max())
peak_title = scored.loc[scored["metacritic_score"].idxmax(), "title"]
total_titles = len(games_df)
years_span = int(games_df["year"].max()) - int(games_df["year"].min())

k1, k2, k3 = st.columns(3)
k1.metric("Total Titles", str(total_titles))
k2.metric("Years of History", f"{years_span}+")
k3.metric("Peak Metacritic Score", f"{peak_score}", help=peak_title)

st.caption(
    f"Peak score: **{peak_title}** ({peak_score}). "
    "Data: Metacritic (PC platform), Google Trends, SteamCharts."
)

st.divider()

# ── Franchise Timeline ─────────────────────────────────────────────────────────
st.subheader("Franchise Timeline — All Titles by Era")
st.caption(
    "Each point is a released title. Color = era. "
    "Classic (2003–2012) · Transitional (2013–2017) · Live Service (2018–present)"
)

era_colors = {
    "Classic": "#1A1A1A",
    "Transitional": "#6D6E71",
    "Live Service": "#E31837",
}

fig = px.scatter(
    games_df,
    x="year",
    y="metacritic_score",
    color="era",
    color_discrete_map=era_colors,
    hover_data={"title": True, "year": True, "developer": True,
                "metacritic_score": True, "era": False},
    labels={"year": "Release Year", "metacritic_score": "Metacritic Score", "era": "Era"},
    size_max=12,
)

# Personal annotation: quit point
fig.add_vline(
    x=2025,
    line_dash="dot",
    line_color="#E31837",
    annotation_text="← I quit here",
    annotation_position="top right",
    annotation_font_color="#E31837",
)

fig.update_traces(marker=dict(size=10, opacity=0.85))
fig.update_layout(
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    font_color="#1A1A1A",
    margin=dict(t=40, b=40),
    yaxis_range=[40, 100],
)
fig.update_xaxes(tickfont=dict(color="#1A1A1A"), title_font=dict(color="#1A1A1A"))
fig.update_yaxes(tickfont=dict(color="#1A1A1A"), title_font=dict(color="#1A1A1A"))
st.plotly_chart(fig, use_container_width=True)

st.caption(
    "Sources: Metacritic.com (scores verified manually) · "
    "Google Trends (pytrends) · SteamCharts.com. "
    "All data fetched at build time. BO7 (2025) excluded from score chart — no Metacritic score yet."
)
```

- [ ] **Step 3: Run the app to verify it loads**

```bash
cd /Users/mr.fidols/github/cod-player-analytics && streamlit run app.py
```

Expected: App launches with narrative banner, 3 KPI cards, and franchise timeline scatter. BO7 (2025) appears on the x-axis but has no y-value (NaN) and is not plotted on the score chart. Quit annotation appears at x=2025.

- [ ] **Step 4: Commit**

```bash
cd /Users/mr.fidols/github/cod-player-analytics
git add app.py pages/__init__.py
git commit -m "feat: add Overview page — narrative banner, franchise timeline, KPI cards"
```
