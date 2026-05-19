import math
import pandas as pd
import pytest
from utils.metrics import (
    era_summary,
    score_gap,
    peak_interest_month,
    interest_decline_pct,
    player_peak_by_title,
    yoy_player_change,
)


# ── era_summary ───────────────────────────────────────────────────────────────

def test_era_summary_avg_correct():
    df = pd.DataFrame([
        {"title": "A", "year": 2007, "era": "Classic", "metacritic_score": 94.0, "user_score": 8.7},
        {"title": "B", "year": 2010, "era": "Classic", "metacritic_score": 87.0, "user_score": 7.6},
        {"title": "C", "year": 2013, "era": "Transitional", "metacritic_score": 68.0, "user_score": 2.4},
    ])
    result = era_summary(df)
    classic = result[result["era"] == "Classic"]["avg_metacritic"].values[0]
    assert abs(classic - 90.5) < 0.1


def test_era_summary_title_count():
    df = pd.DataFrame([
        {"title": "A", "year": 2007, "era": "Classic", "metacritic_score": 94.0, "user_score": 8.7},
        {"title": "B", "year": 2010, "era": "Classic", "metacritic_score": 87.0, "user_score": 7.6},
    ])
    result = era_summary(df)
    assert result[result["era"] == "Classic"]["title_count"].values[0] == 2


def test_era_summary_drops_null_scores():
    df = pd.DataFrame([
        {"title": "BO7", "year": 2025, "era": "Live Service", "metacritic_score": None, "user_score": None},
    ])
    result = era_summary(df)
    assert len(result) == 0


# ── score_gap ─────────────────────────────────────────────────────────────────

def test_score_gap_positive_gap():
    df = pd.DataFrame([
        {"title": "MW2", "year": 2009, "era": "Classic",
         "metacritic_score": 86.0, "user_score": 5.1, "developer": "IW"},
    ])
    result = score_gap(df)
    # gap = 86 - (5.1 * 10) = 86 - 51 = 35
    assert abs(result["gap"].values[0] - 35.0) < 0.1


def test_score_gap_drops_nulls():
    df = pd.DataFrame([
        {"title": "BO7", "year": 2025, "era": "Live Service",
         "metacritic_score": None, "user_score": None, "developer": "Treyarch"},
    ])
    result = score_gap(df)
    assert len(result) == 0


def test_score_gap_columns():
    df = pd.DataFrame([
        {"title": "CoD4", "year": 2007, "era": "Classic",
         "metacritic_score": 94.0, "user_score": 8.7, "developer": "IW"},
    ])
    result = score_gap(df)
    assert set(["title", "year", "metacritic_score", "user_score", "gap"]).issubset(result.columns)


# ── peak_interest_month ───────────────────────────────────────────────────────

def test_peak_interest_month_correct():
    df = pd.DataFrame([
        {"keyword": "Call of Duty", "date": "2020-03-01", "interest": 100},
        {"keyword": "Call of Duty", "date": "2021-01-01", "interest": 60},
        {"keyword": "Call of Duty", "date": "2022-01-01", "interest": 40},
    ])
    result = peak_interest_month(df, "Call of Duty")
    assert result == "2020-03-01"


def test_peak_interest_month_empty_returns_empty_string():
    df = pd.DataFrame(columns=["keyword", "date", "interest"])
    result = peak_interest_month(df, "Call of Duty")
    assert result == ""


def test_peak_interest_month_wrong_keyword_returns_empty_string():
    df = pd.DataFrame([
        {"keyword": "Warzone", "date": "2020-03-01", "interest": 100},
    ])
    result = peak_interest_month(df, "Call of Duty")
    assert result == ""


# ── interest_decline_pct ──────────────────────────────────────────────────────

def test_interest_decline_pct_correct():
    df = pd.DataFrame([
        {"keyword": "Call of Duty", "date": "2020-03-01", "interest": 100},
        {"keyword": "Call of Duty", "date": "2024-01-01", "interest": 30},
    ])
    result = interest_decline_pct(df, "Call of Duty")
    assert abs(result - 0.70) < 0.01


def test_interest_decline_pct_empty_returns_zero():
    df = pd.DataFrame(columns=["keyword", "date", "interest"])
    result = interest_decline_pct(df, "Call of Duty")
    assert result == 0.0


# ── player_peak_by_title ──────────────────────────────────────────────────────

def test_player_peak_by_title_correct():
    df = pd.DataFrame([
        {"title": "MW2", "date": "2022-11-01", "app_id": 1938090,
         "avg_players": 50000, "peak_players": 120000},
        {"title": "MW2", "date": "2022-12-01", "app_id": 1938090,
         "avg_players": 45000, "peak_players": 95000},
        {"title": "MW3", "date": "2023-11-01", "app_id": 2519060,
         "avg_players": 30000, "peak_players": 80000},
    ])
    result = player_peak_by_title(df)
    assert result[result["title"] == "MW2"]["peak_players"].values[0] == 120000


def test_player_peak_by_title_sorted_descending():
    df = pd.DataFrame([
        {"title": "MW3", "date": "2023-11-01", "app_id": 2519060,
         "avg_players": 30000, "peak_players": 80000},
        {"title": "MW2", "date": "2022-11-01", "app_id": 1938090,
         "avg_players": 50000, "peak_players": 120000},
    ])
    result = player_peak_by_title(df)
    assert result.iloc[0]["title"] == "MW2"


# ── yoy_player_change ─────────────────────────────────────────────────────────

def test_yoy_player_change_decline():
    df = pd.DataFrame([
        {"title": "MW2", "date": "2022-11-01", "app_id": 1938090,
         "avg_players": 50000, "peak_players": 120000},
        {"title": "MW3", "date": "2023-11-01", "app_id": 2519060,
         "avg_players": 25000, "peak_players": 80000},
    ])
    result = yoy_player_change(df)
    row_2023 = result[result["year"] == 2023]
    assert abs(row_2023["yoy_pct"].values[0] - (-0.50)) < 0.01


def test_yoy_player_change_first_year_is_nan():
    df = pd.DataFrame([
        {"title": "MW2", "date": "2022-11-01", "app_id": 1938090,
         "avg_players": 50000, "peak_players": 120000},
    ])
    result = yoy_player_change(df)
    assert math.isnan(result.iloc[0]["yoy_pct"])
