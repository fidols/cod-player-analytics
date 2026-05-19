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
