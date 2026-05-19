import pandas as pd
import plotly.express as px
import streamlit as st

from utils.metrics import era_summary, score_gap

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_games():
    return pd.read_csv("data/games.csv")

games_df = load_games()
scored_df = games_df.dropna(subset=["metacritic_score"]).copy()

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("Quality Arc")
st.caption("Stakeholders: Live Services · Analytics · Executive Leadership")
st.markdown(
    "Metacritic scores tell the story of a franchise that peaked in 2007–2010, "
    "stumbled through the jetpack era, partially recovered with MW2019, "
    "then declined to its lowest point with Modern Warfare III (2023, score: 56)."
)

st.divider()

# ── KPI Cards ─────────────────────────────────────────────────────────────────
summary = era_summary(games_df)
peak_score = int(scored_df["metacritic_score"].max())
peak_title = scored_df.loc[scored_df["metacritic_score"].idxmax(), "title"]
lowest_score = int(scored_df["metacritic_score"].min())
lowest_title = scored_df.loc[scored_df["metacritic_score"].idxmin(), "title"]

live_service_avg = summary[summary["era"] == "Live Service"]["avg_metacritic"].values
classic_avg = summary[summary["era"] == "Classic"]["avg_metacritic"].values

k1, k2, k3 = st.columns(3)
k1.metric("Peak Score", str(peak_score), help=peak_title)
k2.metric("Lowest Score", str(lowest_score), help=lowest_title)
if len(classic_avg) and len(live_service_avg):
    delta = round(live_service_avg[0] - classic_avg[0], 1)
    k3.metric(
        "Live Service vs. Classic Avg",
        f"{live_service_avg[0]:.1f}",
        delta=f"{delta:+.1f} vs Classic",
    )

st.divider()

# ── Chart 1: Score over time with era background bands ─────────────────────────
st.subheader("Metacritic Score by Release Year")
st.caption("Era bands: Classic (2003–2012) · Transitional (2013–2017) · Live Service (2018–present)")

fig_line = px.line(
    scored_df.sort_values("year"),
    x="year",
    y="metacritic_score",
    markers=True,
    hover_data={"title": True, "developer": True, "metacritic_score": True},
    labels={"year": "Release Year", "metacritic_score": "Metacritic Score"},
    color_discrete_sequence=["#E31837"],
)

# Era background shapes
fig_line.add_vrect(x0=2002.5, x1=2012.5, fillcolor="#1A1A1A", opacity=0.05,
                   annotation_text="Classic", annotation_position="top left",
                   annotation_font_color="#1A1A1A")
fig_line.add_vrect(x0=2012.5, x1=2017.5, fillcolor="#6D6E71", opacity=0.07,
                   annotation_text="Transitional", annotation_position="top left",
                   annotation_font_color="#6D6E71")
fig_line.add_vrect(x0=2017.5, x1=2026, fillcolor="#E31837", opacity=0.04,
                   annotation_text="Live Service", annotation_position="top left",
                   annotation_font_color="#E31837")

# Personal quit-point annotation
fig_line.add_vline(
    x=2025,
    line_dash="dot",
    line_color="#E31837",
    annotation_text="← I quit here",
    annotation_position="top right",
    annotation_font_color="#E31837",
)

fig_line.update_layout(
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    font_color="#1A1A1A",
    yaxis_range=[40, 100],
    margin=dict(t=60, b=40),
)
fig_line.update_xaxes(tickfont=dict(color="#1A1A1A"), title_font=dict(color="#1A1A1A"))
fig_line.update_yaxes(tickfont=dict(color="#1A1A1A"), title_font=dict(color="#1A1A1A"))
st.plotly_chart(fig_line, use_container_width=True)

st.divider()

# ── Chart 2: Critic score vs. user score side-by-side ─────────────────────────
st.subheader("Critic Score vs. Player Score")
st.caption(
    "User score scaled to 0–100 (original 0–10 × 10). "
    "A growing gap between press and players is a churn predictor."
)

gap_df = score_gap(games_df).sort_values("year")
# Melt for grouped bar
melted = gap_df.melt(
    id_vars=["title", "year"],
    value_vars=["metacritic_score", "user_score"],
    var_name="source",
    value_name="score",
)
melted["source"] = melted["source"].map({
    "metacritic_score": "Metacritic (Critics)",
    "user_score": "User Score (×10)",
})
melted.loc[melted["source"] == "User Score (×10)", "score"] *= 10

fig_bar = px.bar(
    melted,
    x="title",
    y="score",
    color="source",
    barmode="group",
    color_discrete_map={
        "Metacritic (Critics)": "#1A1A1A",
        "User Score (×10)": "#E31837",
    },
    labels={"title": "Title", "score": "Score (0–100)", "source": ""},
)
fig_bar.update_layout(
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    font_color="#1A1A1A",
    xaxis_tickangle=-45,
    margin=dict(t=40, b=120),
)
fig_bar.update_xaxes(tickfont=dict(color="#1A1A1A"), title_font=dict(color="#1A1A1A"))
fig_bar.update_yaxes(tickfont=dict(color="#1A1A1A"), title_font=dict(color="#1A1A1A"))
st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# ── Chart 3: Average Metacritic score by era ──────────────────────────────────
st.subheader("Average Score by Era")

era_order = ["Classic", "Transitional", "Live Service"]
era_colors = {"Classic": "#1A1A1A", "Transitional": "#6D6E71", "Live Service": "#E31837"}
summary_ordered = summary.copy()
summary_ordered["era"] = pd.Categorical(summary_ordered["era"], categories=era_order, ordered=True)
summary_ordered = summary_ordered.sort_values("era")

fig_era = px.bar(
    summary_ordered,
    x="era",
    y="avg_metacritic",
    color="era",
    color_discrete_map=era_colors,
    text="avg_metacritic",
    labels={"era": "Era", "avg_metacritic": "Avg Metacritic Score"},
)
fig_era.update_traces(texttemplate="%{text:.1f}", textposition="outside")
fig_era.update_layout(
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    font_color="#1A1A1A",
    showlegend=False,
    yaxis_range=[0, 110],
    margin=dict(t=40, b=40),
)
fig_era.update_xaxes(tickfont=dict(color="#1A1A1A"), title_font=dict(color="#1A1A1A"))
fig_era.update_yaxes(tickfont=dict(color="#1A1A1A"), title_font=dict(color="#1A1A1A"))
st.plotly_chart(fig_era, use_container_width=True)

st.caption("Source: Metacritic.com — PC scores where available, console otherwise.")
