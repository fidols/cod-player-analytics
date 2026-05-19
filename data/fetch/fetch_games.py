"""
Writes hardcoded franchise data to data/games.csv.
Metacritic and user scores sourced from metacritic.com (PC platform where available).
Run: python data/fetch/fetch_games.py
"""
import pandas as pd
from pathlib import Path

OUT = Path(__file__).parent.parent / "games.csv"

GAMES = [
    ("Call of Duty",                    2003, "Infinity Ward",      "Classic",      91,  8.5, None),
    ("Call of Duty 2",                  2005, "Infinity Ward",      "Classic",      86,  8.2, None),
    ("Call of Duty 3",                  2006, "Treyarch",           "Classic",      82,  7.1, None),
    ("Call of Duty 4: Modern Warfare",  2007, "Infinity Ward",      "Classic",      94,  8.7, None),
    ("Call of Duty: World at War",      2008, "Treyarch",           "Classic",      83,  7.8, None),
    ("Call of Duty: Modern Warfare 2",  2009, "Infinity Ward",      "Classic",      86,  5.1, None),
    ("Call of Duty: Black Ops",         2010, "Treyarch",           "Classic",      87,  7.6, None),
    ("Call of Duty: Modern Warfare 3",  2011, "Infinity Ward",      "Classic",      78,  2.7, None),
    ("Call of Duty: Black Ops II",      2012, "Treyarch",           "Classic",      83,  7.1, None),
    ("Call of Duty: Ghosts",            2013, "Infinity Ward",      "Transitional", 68,  2.4, None),
    ("Call of Duty: Advanced Warfare",  2014, "Sledgehammer Games", "Transitional", 74,  4.7, None),
    ("Call of Duty: Black Ops III",     2015, "Treyarch",           "Transitional", 73,  5.1, None),
    ("Call of Duty: Infinite Warfare",  2016, "Infinity Ward",      "Transitional", 76,  2.6, None),
    ("Call of Duty: WWII",              2017, "Sledgehammer Games", "Transitional", 77,  5.4, None),
    ("Call of Duty: Black Ops 4",       2018, "Treyarch",           "Live Service", 83,  5.3, None),
    ("Call of Duty: Modern Warfare",    2019, "Infinity Ward",      "Live Service", 81,  6.2, None),
    ("Call of Duty: Black Ops Cold War",2020, "Treyarch",           "Live Service", 76,  5.0, None),
    ("Call of Duty: Vanguard",          2021, "Sledgehammer Games", "Live Service", 63,  2.2, None),
    ("Call of Duty: Modern Warfare II", 2022, "Infinity Ward",      "Live Service", 73,  4.2, 1938090),
    ("Call of Duty: Modern Warfare III",2023, "Infinity Ward",      "Live Service", 56,  3.7, 2519060),
    ("Call of Duty: Black Ops 6",       2024, "Treyarch",           "Live Service", 75,  6.3, None),
    ("Call of Duty: Black Ops 7",       2025, "Treyarch",           "Live Service", None, None, None),
]

df = pd.DataFrame(GAMES, columns=[
    "title", "year", "developer", "era",
    "metacritic_score", "user_score", "steam_app_id",
])
df.to_csv(OUT, index=False)
print(f"Wrote {len(df)} rows to {OUT}")
