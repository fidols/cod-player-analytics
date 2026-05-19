# COD Analytics — Plan 4: Search Interest Page

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `pages/2_Search_Interest.py` — Google Trends area chart for "Call of Duty" 2004–present with key release annotations, plus a multi-keyword comparison line chart.

**Architecture:** Loads `data/trends.csv` with `@st.cache_data`. Uses `peak_interest_month` and `interest_decline_pct` from `utils/metrics.py`. Two charts: (1) area chart for "Call of Duty" with release date annotations, (2) line chart comparing all three keywords. Key event dates hardcoded as constants (Warzone launch March 2020, Ricochet Nov 2021, BO6 on Game Pass Oct 2024).

**Tech Stack:** Python 3.12, Streamlit >= 1.32.0, Plotly Express >= 5.18.0, pandas >= 2.0.0

---

## File Map

| File | Change |
|---|---|
| `pages/2_Search_Interest.py` | Create |

---

## Task 1: Failing tests for trends metrics

**Files:**
- Modify: `tests/test_metrics.py` (append)

- [ ] **Step 1: Append tests to tests/test_metrics.py**

Open `tests/test_metrics.py` and add at the bottom:

```python
# ── trends.csv integration (Search Interest assertions) ───────────────────────

def test_trends_csv_warzone_peak_in_2020():
    """Warzone's peak interest should be in 2020 (COVID/launch spike)."""
    from pathlib import Path
    import pandas as pd
    csv_path = Path(__file__).parent.parent / "data" / "trends.csv"
    if not csv_path.exists():
        pytest.skip("data/trends.csv not yet generated")
    df = pd.read_csv(csv_path)
    from utils.metrics import peak_interest_month
    peak = peak_interest_month(df, "Warzone")
    assert peak.startswith("2020"), f"Expected 2020 peak, got {peak}"


def test_trends_csv_cod_decline_positive():
    """Call of Duty search interest should show a positive decline from peak."""
    from pathlib import Path
    import pandas as pd
    csv_path = Path(__file__).parent.parent / "data" / "trends.csv"
    if not csv_path.exists():
        pytest.skip("data/trends.csv not yet generated")
    df = pd.read_csv(csv_path)
    from utils.metrics import interest_decline_pct
    decline = interest_decline_pct(df, "Call of Duty")
    assert decline > 0.0
```

- [ ] **Step 2: Run tests**

```bash
cd /Users/mr.fidols/github/cod-player-analytics && python -m pytest tests/test_metrics.py -v
```

Expected: all tests PASS or SKIP (skip only if CSVs not generated yet).

- [ ] **Step 3: Commit**

```bash
cd /Users/mr.fidols/github/cod-player-analytics
git add tests/test_metrics.py
git commit -m "test: add Search Interest integration assertions for Warzone peak and COD decline"
```

---

## Task 2: Build pages/2_Search_Interest.py

**Files:**
- Create: `pages/2_Search_Interest.py`

- [ ] **Step 1: Create pages/2_Search_Interest.py**

```python
import pandas as pd
import plotly.express as px
import streamlit as st

from utils.metrics import interest_decline_pct, peak_interest_month

# ── Key event dates ────────────────────────────────────────────────────────────
_EVENTS = [
    ("2020-03-10", "Warzone Launch", "#E31837"),
    ("2021-10-05", "Ricochet Anti-Cheat", "#6D6E71"),
    ("2024-10-25", "BO6 on Game Pass", "#1A1A1A"),
]

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_trends():
    df = pd.read_csv("data/trends.csv", parse_dates=["date"])
    return df

trends_df = load_trends()

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("Search Interest")
st.caption("Stakeholders: Live Services · Marketing · Analytics")
st.markdown(
    "Google Trends for 'Call of Duty' shows a dramatic spike with Warzone's launch "
    "(March 2020, coinciding with COVID lockdowns), followed by a steep and sustained decline. "
    "The franchise never recovered to pre-Warzone organic interest levels."
)

st.divider()

# ── KPI Cards ─────────────────────────────────────────────────────────────────
peak_month = peak_interest_month(trends_df, "Call of Duty")
decline = interest_decline_pct(trends_df, "Call of Duty")
warzone_peak = peak_interest_month(trends_df, "Warzone")

k1, k2, k3 = st.columns(3)
k1.metric("COD Peak Interest Month", peak_month if peak_month else "N/A")
k2.metric("Decline from Peak", f"{decline:.0%}" if decline else "N/A",
          delta=f"-{decline:.0%}" if decline else None)
k3.metric("Warzone Peak Month", warzone_peak if warzone_peak else "N/A")

st.divider()

# ── Chart 1: COD area chart with event annotations ────────────────────────────
st.subheader("'Call of Duty' Search Interest — 2004 to Present")
st.caption(
    "Google Trends normalized interest (0–100). 100 = peak search volume for that term. "
    "Annotated: Warzone Launch, Ricochet Anti-Cheat, BO6 on Game Pass."
)

cod_df = trends_df[trends_df["keyword"] == "Call of Duty"].sort_values("date")

fig_area = px.area(
    cod_df,
    x="date",
    y="interest",
    labels={"date": "Month", "interest": "Search Interest (0–100)"},
    color_discrete_sequence=["#E31837"],
)

for event_date, label, color in _EVENTS:
    fig_area.add_vline(
        x=event_date,
        line_dash="dot",
        line_color=color,
        annotation_text=label,
        annotation_position="top right",
        annotation_font_color=color,
        annotation_font_size=11,
    )

fig_area.update_layout(
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    font_color="#1A1A1A",
    margin=dict(t=60, b=40),
)
fig_area.update_xaxes(tickfont=dict(color="#1A1A1A"), title_font=dict(color="#1A1A1A"))
fig_area.update_yaxes(tickfont=dict(color="#1A1A1A"), title_font=dict(color="#1A1A1A"))
st.plotly_chart(fig_area, use_container_width=True)

st.divider()

# ── Chart 2: Multi-keyword comparison ─────────────────────────────────────────
st.subheader("Keyword Comparison — 'Call of Duty' vs. 'Warzone' vs. 'Black Ops'")
st.caption(
    "Each keyword normalized independently. Shows how Warzone dominated search share, "
    "then collapsed — pulling the franchise brand down with it."
)

keyword_colors = {
    "Call of Duty": "#1A1A1A",
    "Warzone": "#E31837",
    "Black Ops": "#6D6E71",
}

fig_compare = px.line(
    trends_df.sort_values("date"),
    x="date",
    y="interest",
    color="keyword",
    color_discrete_map=keyword_colors,
    labels={"date": "Month", "interest": "Search Interest (0–100)", "keyword": "Keyword"},
    markers=False,
)
fig_compare.update_layout(
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    font_color="#1A1A1A",
    margin=dict(t=40, b=40),
)
fig_compare.update_xaxes(tickfont=dict(color="#1A1A1A"), title_font=dict(color="#1A1A1A"))
fig_compare.update_yaxes(tickfont=dict(color="#1A1A1A"), title_font=dict(color="#1A1A1A"))
st.plotly_chart(fig_compare, use_container_width=True)

st.caption(
    "Source: Google Trends via pytrends. Data fetched at build time. "
    "Normalized 0–100 relative to each keyword's own peak — not comparable across keywords in absolute terms."
)
```

- [ ] **Step 2: Run the app to verify the page loads**

```bash
cd /Users/mr.fidols/github/cod-player-analytics && streamlit run app.py
```

Navigate to "Search Interest". Expected: 3 KPI cards (peak month, decline %, Warzone peak), area chart with Warzone/Ricochet/BO6 vertical annotations, multi-keyword comparison line chart. All text black.

If `data/trends.csv` doesn't exist yet, the page will error with a FileNotFoundError — run `python data/fetch/fetch_trends.py` first.

- [ ] **Step 3: Commit**

```bash
cd /Users/mr.fidols/github/cod-player-analytics
git add pages/2_Search_Interest.py
git commit -m "feat: add Search Interest page — COD trends area chart, keyword comparison"
```
