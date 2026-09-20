"""
IPL Cricket Data Analytics — Data Cleaning & Analysis Pipeline
Reads IPL.csv, cleans data, computes all aggregations,
and exports processed parquet/CSV files to processed_data/.
"""

import os
import sys
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np

# ── Paths ────────────────────────────────────────────────────────────────────
BASE   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA   = os.path.join(BASE, "data", "IPL.csv")
OUT    = os.path.join(BASE, "processed_data")
os.makedirs(OUT, exist_ok=True)


# ═══════════════════════════════════════════════════════════════════════════
# STEP 1 — LOAD & EXPLORE
# ═══════════════════════════════════════════════════════════════════════════
print("=" * 65)
print("STEP 1 — LOADING DATA")
print("=" * 65)

df = pd.read_csv(DATA, low_memory=False)

print(f"Rows    : {len(df):,}")
print(f"Columns : {len(df.columns)}")
print("\nColumn Names:")
for c in df.columns:
    print(f"  {c}")

print("\nData Types:")
print(df.dtypes.to_string())

print("\nMissing Values (top 20 with nulls):")
missing = df.isnull().sum()
print(missing[missing > 0].sort_values(ascending=False).head(20).to_string())

print(f"\nDuplicate rows: {df.duplicated().sum()}")


# ═══════════════════════════════════════════════════════════════════════════
# STEP 2 — DATA CLEANING
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("STEP 2 — CLEANING DATA")
print("=" * 65)

# 2.1  Date parsing
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["year"] = df["year"].fillna(df["date"].dt.year).astype("Int64")

# 2.2  Season — keep as-is (string like "2007/08"), derive int year from date
df["season_year"] = df["date"].dt.year.fillna(df["year"]).astype("Int64")

# 2.3  Remove complete duplicates (ball-level exact duplicates are data errors)
before = len(df)
df.drop_duplicates(inplace=True)
print(f"Removed {before - len(df):,} exact duplicate rows")

# 2.4  Numeric coercions
num_cols = [
    "over", "ball", "ball_no", "bat_pos", "runs_batter", "balls_faced",
    "valid_ball", "runs_extras", "runs_total", "runs_bowler",
    "runs_not_boundary", "non_striker_pos", "team_runs", "team_balls",
    "team_wicket", "batter_runs", "batter_balls", "bowler_wicket",
    "striker_out", "innings",
]
for col in num_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# 2.5  Boundary flag: a boundary is runs_batter in {4,6} AND runs_not_boundary==False
#      runs_not_boundary=0 means it IS a boundary
df["is_four"] = ((df["runs_batter"] == 4) & (df["runs_not_boundary"] == 0)).astype(int)
df["is_six"]  = ((df["runs_batter"] == 6) & (df["runs_not_boundary"] == 0)).astype(int)

# 2.6  Wicket flag
df["is_wicket"] = df["wicket_kind"].notna() & (df["wicket_kind"].str.strip() != "")

# 2.7  Replace 'NA' strings with actual NaN
df.replace("NA", np.nan, inplace=True)

# 2.8  innings filter — keep only innings 1 & 2 (exclude super-overs etc.)
df_main = df[df["innings"].isin([1, 2])].copy()
print(f"Main innings rows (1 & 2): {len(df_main):,}")

print("Cleaning complete.\n")


# ═══════════════════════════════════════════════════════════════════════════
# STEP 3 — AGGREGATIONS
# ═══════════════════════════════════════════════════════════════════════════
print("=" * 65)
print("STEP 3 — AGGREGATIONS")
print("=" * 65)

# ── 3.0  Match-level deduplicated frame ──────────────────────────────────
match_cols = [
    "match_id", "date", "season_year", "season",
    "batting_team", "bowling_team",
    "venue", "city",
    "toss_winner", "toss_decision",
    "match_won_by", "win_outcome", "result_type",
    "player_of_match",
]
match_cols = [c for c in match_cols if c in df.columns]
matches_df = df.drop_duplicates("match_id")[match_cols].copy()
matches_df["season_year"] = matches_df["season_year"].astype("Int64")

print(f"Unique matches: {matches_df['match_id'].nunique():,}")
print(f"Seasons: {sorted(matches_df['season_year'].dropna().unique().tolist())}")

# ── 3.1  Overall KPIs ────────────────────────────────────────────────────
total_matches  = matches_df["match_id"].nunique()
total_seasons  = matches_df["season_year"].nunique()
total_teams    = pd.unique(pd.concat([df_main["batting_team"], df_main["bowling_team"]]).dropna()).size
total_players  = pd.unique(pd.concat([df_main["batter"], df_main["bowler"]]).dropna()).size
total_runs     = int(df_main["runs_total"].sum())
total_wickets  = int(df_main["is_wicket"].sum())
total_balls    = int(df_main["valid_ball"].sum())

kpis = pd.DataFrame([{
    "total_matches":  total_matches,
    "total_seasons":  total_seasons,
    "total_teams":    total_teams,
    "total_players":  total_players,
    "total_runs":     total_runs,
    "total_wickets":  total_wickets,
    "total_valid_balls": total_balls,
}])
kpis.to_csv(os.path.join(OUT, "kpis.csv"), index=False)
print(kpis.to_string(index=False))

# ── 3.2  Season analysis ─────────────────────────────────────────────────
season_runs = (
    df_main.groupby("season_year")
    .agg(total_runs=("runs_total", "sum"),
         total_wickets=("is_wicket", "sum"),
         total_balls=("valid_ball", "sum"),
         matches=("match_id", "nunique"))
    .reset_index()
)
season_runs["avg_runs_per_match"] = (season_runs["total_runs"] / season_runs["matches"]).round(1)
season_runs.to_csv(os.path.join(OUT, "season_analysis.csv"), index=False)
print(f"\nSeason analysis rows: {len(season_runs)}")

# ── 3.3  Team wins ───────────────────────────────────────────────────────
# win_outcome contains "X runs" or "X wickets"
win_map = matches_df[matches_df["result_type"] != "no result"].copy()
team_wins = (
    win_map.groupby("match_won_by")["match_id"].nunique()
    .reset_index()
    .rename(columns={"match_id": "wins", "match_won_by": "team"})
    .sort_values("wins", ascending=False)
)

# matches played per team
bat_matches = df_main.groupby("batting_team")["match_id"].nunique().reset_index().rename(
    columns={"batting_team": "team", "match_id": "matches_played"})
team_wins = team_wins.merge(bat_matches, on="team", how="left")
team_wins["losses"] = team_wins["matches_played"] - team_wins["wins"]
team_wins["win_pct"] = (team_wins["wins"] / team_wins["matches_played"] * 100).round(1)
team_wins.to_csv(os.path.join(OUT, "team_wins.csv"), index=False)
print(f"\nTeam wins rows: {len(team_wins)}")

# ── 3.4  Team season performance ─────────────────────────────────────────
# Count wins per team per season
season_wins = (
    win_map.groupby(["season_year", "match_won_by"])["match_id"].nunique()
    .reset_index()
    .rename(columns={"match_id": "wins", "match_won_by": "team"})
)
season_wins.to_csv(os.path.join(OUT, "team_season_wins.csv"), index=False)

# ── 3.5  Batting analysis ─────────────────────────────────────────────────
batting = (
    df_main.groupby("batter")
    .agg(
        total_runs    = ("runs_batter",  "sum"),
        balls_faced   = ("valid_ball",   "sum"),
        fours         = ("is_four",      "sum"),
        sixes         = ("is_six",       "sum"),
        innings_played= ("match_id",     "nunique"),
    )
    .reset_index()
)
batting["strike_rate"] = (batting["total_runs"] / batting["balls_faced"] * 100).round(2)
batting["strike_rate"] = batting["strike_rate"].replace([np.inf, -np.inf], 0)
batting.sort_values("total_runs", ascending=False, inplace=True)
batting.to_csv(os.path.join(OUT, "batting_analysis.csv"), index=False)
print(f"\nTop 5 run scorers:")
print(batting[["batter", "total_runs", "balls_faced", "strike_rate", "fours", "sixes"]].head(5).to_string(index=False))

# Highest individual innings score (batter_runs per match_id per batter)
hi_scores = (
    df_main.groupby(["match_id", "batter"])
    .agg(score=("runs_batter", "sum"),
         balls=("valid_ball",  "sum"))
    .reset_index()
    .sort_values("score", ascending=False)
)
hi_scores.to_csv(os.path.join(OUT, "highest_scores.csv"), index=False)

# Batting by season
batting_season = (
    df_main.groupby(["season_year", "batter"])
    .agg(
        runs   = ("runs_batter", "sum"),
        balls  = ("valid_ball",  "sum"),
        fours  = ("is_four",     "sum"),
        sixes  = ("is_six",      "sum"),
    )
    .reset_index()
)
batting_season["strike_rate"] = (batting_season["runs"] / batting_season["balls"] * 100).round(2)
batting_season.to_csv(os.path.join(OUT, "batting_season.csv"), index=False)

# ── 3.6  Bowling analysis ─────────────────────────────────────────────────
bowling = (
    df_main.groupby("bowler")
    .agg(
        wickets      = ("is_wicket",   "sum"),
        balls_bowled = ("valid_ball",  "sum"),
        runs_conceded= ("runs_bowler", "sum"),
        matches      = ("match_id",    "nunique"),
    )
    .reset_index()
)
bowling["economy"]  = (bowling["runs_conceded"] / (bowling["balls_bowled"] / 6)).round(2)
bowling["economy"]  = bowling["economy"].replace([np.inf, -np.inf], 0)
bowling["avg"]      = np.where(
    bowling["wickets"] > 0,
    (bowling["runs_conceded"] / bowling["wickets"]).round(2),
    np.nan
)
bowling.sort_values("wickets", ascending=False, inplace=True)
bowling.to_csv(os.path.join(OUT, "bowling_analysis.csv"), index=False)
print(f"\nTop 5 wicket takers:")
print(bowling[["bowler", "wickets", "economy", "avg"]].head(5).to_string(index=False))

# Bowling by season
bowling_season = (
    df_main.groupby(["season_year", "bowler"])
    .agg(
        wickets      = ("is_wicket",   "sum"),
        balls_bowled = ("valid_ball",  "sum"),
        runs_conceded= ("runs_bowler", "sum"),
    )
    .reset_index()
)
bowling_season["economy"] = (bowling_season["runs_conceded"] / (bowling_season["balls_bowled"] / 6)).round(2)
bowling_season.to_csv(os.path.join(OUT, "bowling_season.csv"), index=False)

# ── 3.7  Venue analysis ───────────────────────────────────────────────────
venue_df = (
    df_main.groupby("venue")
    .agg(
        matches      = ("match_id",    "nunique"),
        total_runs   = ("runs_total",  "sum"),
        total_wickets= ("is_wicket",   "sum"),
    )
    .reset_index()
    .sort_values("matches", ascending=False)
)
venue_df["avg_runs_per_match"] = (venue_df["total_runs"] / venue_df["matches"]).round(1)
venue_df.to_csv(os.path.join(OUT, "venue_analysis.csv"), index=False)
print(f"\nTop 5 venues:")
print(venue_df[["venue", "matches", "total_runs"]].head(5).to_string(index=False))

# ── 3.8  Toss analysis ────────────────────────────────────────────────────
toss_df = matches_df.dropna(subset=["toss_winner", "match_won_by"]).copy()
toss_df["toss_win_match_win"] = (toss_df["toss_winner"] == toss_df["match_won_by"]).astype(int)

toss_summary = pd.DataFrame({
    "metric": [
        "Total matches with toss data",
        "Toss winner won match",
        "Toss winner lost match",
        "Win % after winning toss",
    ],
    "value": [
        len(toss_df),
        int(toss_df["toss_win_match_win"].sum()),
        int((1 - toss_df["toss_win_match_win"]).sum()),
        round(toss_df["toss_win_match_win"].mean() * 100, 1),
    ]
})
toss_summary.to_csv(os.path.join(OUT, "toss_summary.csv"), index=False)

toss_decision = (
    toss_df.groupby("toss_decision")["match_id"].count()
    .reset_index()
    .rename(columns={"match_id": "count", "toss_decision": "decision"})
)
toss_decision.to_csv(os.path.join(OUT, "toss_decision.csv"), index=False)

# batting-first vs fielding-first outcome
toss_outcome = (
    toss_df.groupby("toss_decision")["toss_win_match_win"]
    .agg(wins="sum", total="count")
    .reset_index()
)
toss_outcome["win_pct"] = (toss_outcome["wins"] / toss_outcome["total"] * 100).round(1)
toss_outcome.to_csv(os.path.join(OUT, "toss_outcome.csv"), index=False)
print(f"\nToss summary:")
print(toss_summary.to_string(index=False))

# ── 3.9  Match-level run aggregation ──────────────────────────────────────
match_runs = (
    df_main.groupby("match_id")
    .agg(total_runs=("runs_total", "sum"), total_wickets=("is_wicket","sum"))
    .reset_index()
)
match_runs = match_runs.merge(
    matches_df[["match_id","season_year","venue","batting_team","bowling_team"]],
    on="match_id", how="left"
)
match_runs.sort_values("total_runs", ascending=False, inplace=True)
match_runs.to_csv(os.path.join(OUT, "match_runs.csv"), index=False)

# ── 3.10  Team runs aggregated ────────────────────────────────────────────
team_runs_agg = (
    df_main.groupby("batting_team")
    .agg(total_runs=("runs_total", "sum"), total_balls=("valid_ball","sum"))
    .reset_index()
    .sort_values("total_runs", ascending=False)
)
team_runs_agg.to_csv(os.path.join(OUT, "team_runs.csv"), index=False)

# ── 3.11  Player of the match counts ──────────────────────────────────────
if "player_of_match" in matches_df.columns:
    potm = (
        matches_df.dropna(subset=["player_of_match"])
        .groupby("player_of_match")["match_id"].count()
        .reset_index()
        .rename(columns={"match_id": "awards", "player_of_match": "player"})
        .sort_values("awards", ascending=False)
    )
    potm.to_csv(os.path.join(OUT, "player_of_match.csv"), index=False)
    print(f"\nTop Player of Match awards: {potm.head(3).to_string(index=False)}")

# ── Save cleaned main frame (sampled for app speed) ───────────────────────
df_main.to_csv(os.path.join(OUT, "ipl_clean.csv"), index=False)
print(f"\nCleaned dataset saved: {len(df_main):,} rows")

# ── Data Dictionary ──────────────────────────────────────────────────────
data_dict = {
    "match_id":         "Unique match identifier",
    "date":             "Match date",
    "season":           "IPL season label (e.g. 2007/08)",
    "season_year":      "Derived 4-digit year of season",
    "batting_team":     "Team currently batting",
    "bowling_team":     "Team currently bowling",
    "innings":          "Innings number (1 or 2)",
    "over":             "Over number",
    "ball":             "Ball number within over",
    "ball_no":          "Running ball number in innings",
    "batter":           "Batter facing delivery",
    "runs_batter":      "Runs scored by batter off this delivery",
    "balls_faced":      "Cumulative balls faced by batter in innings",
    "bowler":           "Bowler delivering",
    "valid_ball":       "1 if legal delivery (counts towards over)",
    "runs_extras":      "Extra runs (wides, no-balls, byes, leg-byes)",
    "runs_total":       "Total runs from delivery (batter + extras)",
    "runs_bowler":      "Runs charged to bowler",
    "is_four":          "Derived: 1 if boundary four",
    "is_six":           "Derived: 1 if boundary six",
    "wicket_kind":      "Type of dismissal (if any)",
    "player_out":       "Batter dismissed (if any)",
    "toss_winner":      "Team that won the toss",
    "toss_decision":    "Toss decision: bat or field",
    "match_won_by":     "Team that won the match",
    "win_outcome":      "Margin of victory",
    "venue":            "Stadium name",
    "city":             "City",
    "player_of_match":  "Player of the match award",
}
dd_df = pd.DataFrame(list(data_dict.items()), columns=["column","description"])
dd_df.to_csv(os.path.join(OUT, "data_dictionary.csv"), index=False)

print("\n" + "=" * 65)
print("ALL PROCESSED FILES SAVED TO processed_data/")
print("=" * 65)
files = os.listdir(OUT)
for f in sorted(files):
    path = os.path.join(OUT, f)
    size = os.path.getsize(path)
    print(f"  {f:40s}  {size/1024:8.1f} KB")
