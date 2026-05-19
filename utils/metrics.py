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
