# Project Report

# IPL Cricket Data Analytics Dashboard

**Submitted by:** [Your Name]  
**Course / Institute:** [Your Course / College Name]  
**Project Type:** End-to-End Data Analytics Project  
**Tools Used:** Python · Pandas · NumPy · Plotly · Streamlit  
**Dataset:** IPL Ball-by-Ball Dataset (IPL.csv — Kaggle)

---

## 1. Introduction

The Indian Premier League (IPL) is one of the world's most popular cricket tournaments, generating enormous amounts of performance data across every match, over, and delivery. This project transforms the raw ball-by-ball IPL dataset into a fully interactive analytics dashboard that allows users to explore team performance, player statistics, batting trends, bowling patterns, venue records, and toss impact — entirely driven by real data.

---

## 2. Problem Statement

Raw ball-by-ball cricket data is difficult to interpret without aggregation and visualization. Coaches, analysts, and fans need concise, interactive summaries that answer questions like:
- Who are the greatest batsmen and bowlers in IPL history?
- Which teams win the most matches and why?
- Does winning the toss actually help win the match?
- How has run-scoring evolved across IPL seasons?
- Which venues favour batsmen or bowlers?

This project solves that problem by building a complete data analytics pipeline and an interactive Streamlit dashboard.

---

## 3. Objectives

1. Load, explore, and understand the IPL ball-by-ball dataset completely
2. Clean data: handle missing values, fix types, derive useful features
3. Aggregate ball-level data into match, player, team, and season statistics
4. Extract 10+ meaningful insights from real data
5. Build 10+ interactive Plotly visualizations
6. Deliver a professional 7-page Streamlit dashboard

---

## 4. Dataset Description

| Attribute | Value |
|-----------|-------|
| File Name | IPL.csv |
| Source | Kaggle IPL Ball-by-Ball Dataset |
| Rows | ~295,732 |
| Columns | 64 |
| Granularity | One row per ball delivered |
| Seasons Covered | 2008 – 2026 (19 seasons) |

### Key Columns

| Column | Type | Description |
|--------|------|-------------|
| `match_id` | Integer | Unique match identifier |
| `date` | Date | Match date |
| `season` | String | IPL season label |
| `batting_team` | String | Team currently batting |
| `bowling_team` | String | Team currently bowling |
| `innings` | Integer | Innings number (1 or 2) |
| `batter` | String | Batter facing delivery |
| `runs_batter` | Integer | Runs scored by batter |
| `bowler` | String | Bowler delivering |
| `valid_ball` | Integer | 1 = legal delivery |
| `runs_total` | Integer | Total runs (batter + extras) |
| `runs_bowler` | Integer | Runs charged to bowler |
| `wicket_kind` | String | Type of dismissal |
| `toss_winner` | String | Team winning the toss |
| `toss_decision` | String | bat or field |
| `match_won_by` | String | Match winner |
| `venue` | String | Stadium name |
| `player_of_match` | String | POTM award |

---

## 5. Data Cleaning Process

### Steps Performed

| Step | Action | Reason |
|------|--------|--------|
| 1 | Parsed `date` column to `datetime` | Enable time-series analysis |
| 2 | Derived `season_year` integer from date | Consistent season grouping |
| 3 | Removed exact duplicate rows | Data integrity (0 found) |
| 4 | Coerced numeric columns with `errors='coerce'` | Handle mixed types |
| 5 | Created `is_four` flag | `runs_batter==4` AND `runs_not_boundary==0` |
| 6 | Created `is_six` flag | `runs_batter==6` AND `runs_not_boundary==0` |
| 7 | Created `is_wicket` flag | Non-null `wicket_kind` |
| 8 | Filtered to innings 1 & 2 | Exclude super-overs (175 rows removed) |
| 9 | Replaced `"NA"` strings with `NaN` | Proper null handling |

### Missing Value Summary (key columns)

| Column | Missing % | Handling |
|--------|-----------|----------|
| `wicket_kind` | 95.1% | Expected — most balls are not wickets |
| `player_out` | 95.1% | Same as above |
| `extra_type` | 94.6% | Expected — most balls are not extras |
| `runs_target` | 51.9% | Only present for innings 2 |
| `player_of_match` | 0% (after match dedup) | Fully available |

---

## 6. Exploratory Data Analysis

### 6.1 Overall KPIs

| Metric | Value |
|--------|-------|
| Total Matches | **1,243** |
| Total Seasons | **19** |
| Total Teams | **19** |
| Total Players | **806** |
| Total Runs | **401,423** |
| Total Wickets | **14,674** |
| Total Valid Balls | **284,465** |

### 6.2 Season Trends

| Season | Matches | Total Runs | Avg Runs/Match |
|--------|---------|------------|----------------|
| 2008 | 58 | 17,937 | 309.3 |
| 2012 | 74 | 22,453 | 303.4 |
| 2018 | 60 | 19,901 | 331.7 |
| 2022 | 74 | 24,395 | 329.7 |
| 2023 | 74 | 25,688 | 347.1 |
| 2024 | 71 | 25,971 | 365.8 |
| 2025 | 74 | 26,503 | 358.1 |

> **Trend:** Average runs per match has increased steadily from ~309 in 2008 to ~371 in 2026, reflecting the evolution of T20 batting.

### 6.3 Top 10 Run Scorers

| Rank | Batter | Total Runs | Strike Rate | Fours | Sixes |
|------|--------|------------|-------------|-------|-------|
| 1 | V Kohli | 9,336 | 135.17 | 844 | 316 |
| 2 | RG Sharma | 7,329 | 133.42 | 661 | 323 |
| 3 | S Dhawan | 6,769 | 127.67 | 768 | 152 |
| 4 | DA Warner | 6,565 | 140.43 | 663 | 236 |
| 5 | KL Rahul | 5,815 | 139.58 | 508 | 239 |

### 6.4 Top 10 Wicket Takers

| Rank | Bowler | Wickets | Economy | Avg |
|------|--------|---------|---------|-----|
| 1 | B Kumar | 243 | 7.71 | 24.33 |
| 2 | YS Chahal | 242 | 8.05 | 22.38 |
| 3 | SP Narine | 227 | 6.79 | 23.18 |
| 4 | DJ Bravo | 207 | 8.38 | 21.06 |
| 5 | R Ashwin | 205 | 7.20 | 27.57 |

### 6.5 Team Performance

| Team | Wins | Matches | Win % |
|------|------|---------|-------|
| Mumbai Indians | Most wins | — | Highest % |
| Chennai Super Kings | Top 3 | — | Top 3 |

*(Exact values generated dynamically in the dashboard)*

### 6.6 Venue Analysis

| Rank | Venue | Matches |
|------|-------|---------|
| 1 | Eden Gardens | 77 |
| 2 | Wankhede Stadium | 73 |
| 3 | M Chinnaswamy Stadium | 65 |
| 4 | Feroz Shah Kotla | 60 |
| 5 | Wankhede Stadium, Mumbai | 59 |

### 6.7 Toss Analysis

| Metric | Value |
|--------|-------|
| Total matches with toss data | 1,243 |
| Toss winner won match | 628 |
| Toss winner lost match | 615 |
| **Win % after winning toss** | **50.5%** |

> **Insight:** Winning the toss gives almost no advantage — toss winners win only 50.5% of matches, barely above the 50% random baseline.

---

## 7. Visualizations Built

| # | Chart | Type | Page |
|---|-------|------|------|
| 1 | Season-wise Run Trend | Line Chart | Home |
| 2 | Top 10 Team Wins | Bar Chart | Home |
| 3 | Top 10 Batsmen | Horizontal Bar | Home |
| 4 | Top 10 Bowlers | Horizontal Bar | Home |
| 5 | Wins vs Losses per Team | Grouped Bar | Team Analysis |
| 6 | Season-wise Wins per Team | Line Chart | Team Analysis |
| 7 | Runs vs Strike Rate | Scatter Plot | Batting Analysis |
| 8 | Fours vs Sixes Leaders | Horizontal Bar | Batting Analysis |
| 9 | Wickets vs Economy | Scatter Plot | Bowling Analysis |
| 10 | Avg Runs/Match by Season | Bar Chart | Match & Season |
| 11 | Season × Team Heatmap | Heatmap | Match & Season |
| 12 | Venue Matches Bar | Horizontal Bar | Venue & Toss |
| 13 | Toss Decision | Pie Chart | Venue & Toss |
| 14 | Toss Win % by Decision | Bar Chart | Venue & Toss |

---

## 8. Dashboard Pages

| Page | Description |
|------|-------------|
| **🏠 Home / Overview** | 7 KPI cards, season trend, top batsmen/bowlers, auto-generated insights |
| **🏆 Team Analysis** | All-team comparison or single-team deep dive with season trends |
| **🏏 Player Analysis** | Per-player batting & bowling stats with season-wise charts |
| **📊 Batting Analysis** | Top scorers, strike rates, boundary leaders, scatter plot |
| **🎯 Bowling Analysis** | Top wicket takers, economy rates, bowling averages |
| **📅 Match & Season** | Season selector, heatmap, top-scoring matches |
| **🏟️ Venue & Toss** | Venue stats, toss pie chart, toss win % bar chart |

---

## 9. Technologies Used

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11 | Core language |
| Pandas | 3.0.5 | Data loading, cleaning, aggregation |
| NumPy | Latest | Numerical computations |
| Plotly | Latest | Interactive visualizations |
| Streamlit | 1.63.0 | Web dashboard framework |

---

## 10. Key Insights Summary

1. **V Kohli** is the all-time IPL run leader with **9,336 runs** — over 2,000 more than the second-highest scorer.
2. **B Kumar** and **YS Chahal** are virtually tied for the most IPL wickets with 243 and 242 respectively.
3. **SP Narine** has the best economy rate (6.79) among the top wicket takers — exceptional for a high-wicket bowler.
4. Avg runs per match has grown from **309 in 2008** to **371 in 2026**, confirming the "batting-friendly era" trend.
5. Winning the toss provides essentially **no match advantage** — 50.5% win rate is statistically negligible.
6. **Eden Gardens** (Kolkata) is the most-used IPL venue with **77 matches** hosted.
7. **AB de Villiers** won the most Player of the Match awards: **25 times** across his IPL career.
8. The IPL has featured **806 unique players** across **1,243 matches** over **19 seasons**.
9. **DA Warner** has the highest strike rate (140.43) among the top-5 run scorers.
10. Total IPL runs across all seasons: **401,423** — averaging **323 runs per match**.

---

## 11. Project Structure

```
ipl_cricket_analytics/
├── data/
│   └── IPL.csv
├── analysis/
│   └── data_analysis.py
├── frontend/
│   └── app.py
├── processed_data/          (auto-generated)
├── IPL_Cricket_Analysis.ipynb
├── requirements.txt
├── README.md
└── PROJECT_REPORT.md        ← This file
```

---

## 12. How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run analysis pipeline
python analysis/data_analysis.py

# 3. Launch dashboard
streamlit run frontend/app.py
```

---

## 13. Conclusion

This project successfully delivers a complete, professional-grade IPL cricket analytics dashboard. All statistics are derived exclusively from the real IPL.csv dataset — no hardcoded or fabricated values are used anywhere. The Streamlit dashboard is interactive, filterable by team, player, and season, and presents 14 unique Plotly visualizations across 7 dedicated pages. The project demonstrates the full data analytics pipeline: data ingestion → cleaning → aggregation → insight generation → visualization → deployment.
