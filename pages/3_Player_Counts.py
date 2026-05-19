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
