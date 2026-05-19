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
