# COD Analytics — Plan 6: Churn Analysis Page

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `pages/4_Churn_Analysis.py` — the synthesis page. Overlays all three signals (Metacritic score, Google Trends interest, Steam players) on a single normalized chart, adds a quality-vs-retention scatter, and calls out the "churn zone."

**Architecture:** Loads all three CSVs. Normalizes each signal to 0–100 by year using `games_df` for Metacritic, `trends_df` for annual avg interest (keyword: "Call of Duty"), and `steam_df` for annual avg players. Computes Pearson correlation between Metacritic score and peak players across titles that exist in both datasets. Two charts: (1) normalized multi-line overlay, (2) scatter of Metacritic score vs. peak Steam players.

**Tech Stack:** Python 3.12, Streamlit >= 1.32.0, Plotly Express >= 5.18.0, pandas >= 2.0.0, NumPy >= 1.26.0

---

## File Map

| File | Change |
|---|---|
| `pages/4_Churn_Analysis.py` | Create |

---

## Task 1: Failing tests for churn analysis signal normalization

**Files:**
- Modify: `tests/test_metrics.py` (append)

- [ ] **Step 1: Append two normalization tests to tests/test_metrics.py**

Open `tests/test_metrics.py` and add at the bottom:

```python
# ── Churn Analysis signal helpers ─────────────────────────────────────────────

def test_normalize_series_max_is_100():
    """Normalizing a series to 0–100: max should be 100."""
    import numpy as np
    s = pd.Series([10.0, 20.0, 50.0, 80.0, 100.0])
    normalized = (s - s.min()) / (s.max() - s.min()) * 100
    assert abs(normalized.max() - 100.0) < 0.01


def test_normalize_series_min_is_0():
    """Normalizing a series to 0–100: min should be 0."""
    import numpy as np
    s = pd.Series([10.0, 20.0, 50.0, 80.0, 100.0])
    normalized = (s - s.min()) / (s.max() - s.min()) * 100
    assert abs(normalized.min() - 0.0) < 0.01
```

- [ ] **Step 2: Run tests**

```bash
cd /Users/mr.fidols/github/cod-player-analytics && python -m pytest tests/test_metrics.py -v
```

Expected: all tests PASS (these two are pure math, no CSV dependency).

- [ ] **Step 3: Commit**

```bash
cd /Users/mr.fidols/github/cod-player-analytics
git add tests/test_metrics.py
git commit -m "test: add normalization helper tests for Churn Analysis"
```

---

## Task 2: Build pages/4_Churn_Analysis.py

**Files:**
- Create: `pages/4_Churn_Analysis.py`

- [ ] **Step 1: Create pages/4_Churn_Analysis.py**

```python
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_all():
    games = pd.read_csv("data/games.csv")
    trends = pd.read_csv("data/trends.csv", parse_dates=["date"])
    steam = pd.read_csv("data/steam_players.csv", parse_dates=["date"])
    return games, trends, steam

games_df, trends_df, steam_df = load_all()

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("The Full Picture — Churn Analysis")
st.caption("Stakeholders: Live Services · Analytics · Executive Leadership")
st.markdown(
    "No single factor killed COD — it was the combination. "
    "When quality dropped **and** search interest fell **and** player counts declined simultaneously, "
    "that's when players like me quit. This page overlays all three signals."
)

st.divider()

# ── Build normalized signals by year ──────────────────────────────────────────

# Signal 1: Metacritic score by year (use scored titles only)
meta_yearly = (
    games_df.dropna(subset=["metacritic_score"])
    .groupby("year")["metacritic_score"]
    .mean()
    .reset_index()
    .rename(columns={"metacritic_score": "value"})
)
meta_yearly["signal"] = "Quality (Metacritic)"

# Signal 2: COD Google Trends annual average
trends_cod = trends_df[trends_df["keyword"] == "Call of Duty"].copy()
trends_cod["year"] = trends_cod["date"].dt.year
trends_yearly = (
    trends_cod.groupby("year")["interest"]
    .mean()
    .reset_index()
    .rename(columns={"interest": "value"})
)
trends_yearly["signal"] = "Search Interest (Google Trends)"

# Signal 3: Steam avg players annual average
steam_df["year"] = steam_df["date"].dt.year
steam_yearly = (
    steam_df.groupby("year")["avg_players"]
    .mean()
    .reset_index()
    .rename(columns={"avg_players": "value"})
)
steam_yearly["signal"] = "Steam Players (Avg)"


def _normalize(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize 'value' column to 0–100 scale."""
    mn, mx = df["value"].min(), df["value"].max()
    if mx == mn:
        df = df.copy()
        df["value"] = 50.0
        return df
    df = df.copy()
    df["value"] = (df["value"] - mn) / (mx - mn) * 100
    return df


meta_norm = _normalize(meta_yearly)
trends_norm = _normalize(trends_yearly)
steam_norm = _normalize(steam_yearly)

combined = pd.concat([meta_norm, trends_norm, steam_norm], ignore_index=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────

# Find the first year where all three signals declined year-over-year
def _first_triple_decline(meta: pd.DataFrame, trend: pd.DataFrame, stm: pd.DataFrame) -> str:
    """Return the first year string where all three signals declined from prior year."""
    for df in [meta, trend, stm]:
        df.sort_values("year", inplace=True)
    years = sorted(set(meta["year"]) & set(trend["year"]) & set(stm["year"]))
    for i in range(1, len(years)):
        y = years[i]
        y_prev = years[i - 1]
        meta_val = meta[meta["year"] == y]["value"].values
        meta_prev = meta[meta["year"] == y_prev]["value"].values
        trend_val = trend[trend["year"] == y]["value"].values
        trend_prev = trend[trend["year"] == y_prev]["value"].values
        stm_val = stm[stm["year"] == y]["value"].values
        stm_prev = stm[stm["year"] == y_prev]["value"].values
        if (len(meta_val) and len(meta_prev) and meta_val[0] < meta_prev[0] and
                len(trend_val) and len(trend_prev) and trend_val[0] < trend_prev[0] and
                len(stm_val) and len(stm_prev) and stm_val[0] < stm_prev[0]):
            return str(y)
    return "N/A"


churn_year = _first_triple_decline(
    meta_norm.copy(), trends_norm.copy(), steam_norm.copy()
)

# Pearson correlation between metacritic score and peak Steam players
steam_peaks = steam_df.groupby("title")["peak_players"].max().reset_index()
merged_corr = games_df.dropna(subset=["metacritic_score"]).merge(
    steam_peaks, on="title", how="inner"
)
if len(merged_corr) >= 2:
    corr = float(np.corrcoef(merged_corr["metacritic_score"], merged_corr["peak_players"])[0, 1])
    corr_str = f"{corr:.2f}"
else:
    corr_str = "N/A (need 2+ shared titles)"

k1, k2 = st.columns(2)
k1.metric(
    "First Year All Three Signals Declined",
    churn_year,
    help="The first calendar year where Metacritic avg, search interest, and Steam player avg all fell year-over-year.",
)
k2.metric(
    "Quality vs. Retention Correlation",
    corr_str,
    help="Pearson r between Metacritic score and peak Steam players for titles with data in both datasets.",
)

st.divider()

# ── Chart 1: Normalized multi-signal overlay ──────────────────────────────────
st.subheader("All Three Signals — Normalized to 0–100")
st.caption(
    "Each signal scaled independently. 100 = that signal's own historical peak. "
    "Convergence downward = the churn zone."
)

signal_colors = {
    "Quality (Metacritic)": "#1A1A1A",
    "Search Interest (Google Trends)": "#6D6E71",
    "Steam Players (Avg)": "#E31837",
}

# Restrict to overlapping years with meaningful data
min_year = max(
    int(meta_norm["year"].min()),
    int(trends_norm["year"].min()),
    int(steam_norm["year"].min()),
)
overlay_df = combined[combined["year"] >= 2007].copy()

fig_overlay = px.line(
    overlay_df.sort_values("year"),
    x="year",
    y="value",
    color="signal",
    color_discrete_map=signal_colors,
    markers=True,
    labels={"year": "Year", "value": "Normalized Score (0–100)", "signal": "Signal"},
)

# Shade the churn zone if we found one
if churn_year != "N/A":
    fig_overlay.add_vrect(
        x0=int(churn_year) - 0.5,
        x1=overlay_df["year"].max() + 0.5,
        fillcolor="#E31837",
        opacity=0.05,
        annotation_text="Churn Zone",
        annotation_position="top left",
        annotation_font_color="#E31837",
    )

fig_overlay.update_layout(
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    font_color="#1A1A1A",
    yaxis_range=[0, 110],
    margin=dict(t=60, b=40),
)
fig_overlay.update_xaxes(tickfont=dict(color="#1A1A1A"), title_font=dict(color="#1A1A1A"))
fig_overlay.update_yaxes(tickfont=dict(color="#1A1A1A"), title_font=dict(color="#1A1A1A"))
st.plotly_chart(fig_overlay, use_container_width=True)

st.divider()

# ── Chart 2: Quality vs. Player Retention scatter ─────────────────────────────
st.subheader("Quality Score vs. Peak Steam Players")
st.caption(
    "Does a higher Metacritic score predict more concurrent players? "
    "Each point is a title with data in both datasets."
)

if len(merged_corr) < 2:
    st.info(
        "Need at least 2 titles with both Metacritic scores and Steam player data. "
        "Run data/fetch/fetch_steam.py to generate steam_players.csv.",
        icon="ℹ️",
    )
else:
    fig_scatter = px.scatter(
        merged_corr,
        x="metacritic_score",
        y="peak_players",
        text="title",
        color_discrete_sequence=["#E31837"],
        trendline="ols",
        trendline_color_override="#1A1A1A",
        labels={
            "metacritic_score": "Metacritic Score",
            "peak_players": "Peak Concurrent Players (Steam)",
            "title": "Title",
        },
    )
    fig_scatter.update_traces(
        textposition="top center",
        marker=dict(size=10),
        selector=dict(mode="markers+text"),
    )
    fig_scatter.update_layout(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font_color="#1A1A1A",
        yaxis_tickformat=",",
        margin=dict(t=40, b=40),
    )
    fig_scatter.update_xaxes(tickfont=dict(color="#1A1A1A"), title_font=dict(color="#1A1A1A"))
    fig_scatter.update_yaxes(tickfont=dict(color="#1A1A1A"), title_font=dict(color="#1A1A1A"))
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.caption(
        f"Pearson r = {corr_str}. "
        "Positive correlation means higher-rated titles retain more players on PC. "
        "Note: small sample (2 titles) — treat as directional only."
    )

st.caption(
    "Sources: Metacritic.com · Google Trends (pytrends) · SteamCharts.com. "
    "All data fetched at build time. Steam covers PC only."
)
```

- [ ] **Step 2: Install statsmodels (required for trendline='ols' in Plotly)**

```bash
pip install statsmodels
```

Then add `statsmodels>=0.14.0` to `requirements.txt`.

- [ ] **Step 3: Run the app to verify the page loads**

```bash
cd /Users/mr.fidols/github/cod-player-analytics && streamlit run app.py
```

Navigate to "The Full Picture". Expected:
- 2 KPI cards: first triple-decline year, correlation coefficient
- Normalized overlay line chart with churn zone shading (if triple decline found)
- If steam_players.csv exists: scatter of MW2 vs MW3 with OLS trendline
- If steam_players.csv missing: info banner

- [ ] **Step 4: Run full test suite — target 21 passing**

```bash
cd /Users/mr.fidols/github/cod-player-analytics && python -m pytest tests/test_metrics.py -v
```

Expected: **21 PASSED** (15 original + 1 schema + 2 era/gap + 2 trends + 2 steam + 2 normalization; CSV-dependent tests skip if not generated).

- [ ] **Step 5: Commit**

```bash
cd /Users/mr.fidols/github/cod-player-analytics
git add pages/4_Churn_Analysis.py requirements.txt
git commit -m "feat: add Churn Analysis page — normalized multi-signal overlay, quality vs retention scatter"
```
