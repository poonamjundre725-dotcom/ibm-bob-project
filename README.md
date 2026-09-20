# 🏏 IPL Cricket Data Analytics Dashboard

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Streamlit-1.63-FF4B4B?style=for-the-badge&logo=streamlit" />
  <img src="https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=for-the-badge&logo=plotly" />
  <img src="https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas" />
  <img src="https://img.shields.io/badge/Dataset-IPL%20Ball--by--Ball-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit" />
</p>

<p align="center">
  <a href="https://ibm-bob-project-qtwc5yupyozvkmsamuz9il.streamlit.app/" target="_blank">
    <strong>🚀 LIVE DEMO → https://ibm-bob-project-qtwc5yupyozvkmsamuz9il.streamlit.app/</strong>
  </a>
</p>

> **A complete end-to-end Data Analytics project on the IPL Cricket Ball-by-Ball dataset — built with Python, Pandas, Plotly, and Streamlit.**
https://www.kaggle.com/datasets/chaitu20/ipl-dataset2008-2025
---

## 📥 Dataset

| | |
|---|---|
| **Dataset Name** | IPL Dataset 2008–2025 (Ball-by-Ball) |
| **Source** | Kaggle |
| **Direct Link** | 🔗 [https://www.kaggle.com/datasets/chaitu20/ipl-dataset2008-2025](https://www.kaggle.com/datasets/chaitu20/ipl-dataset2008-2025) |
| **Rows** | ~295,732 (one row per ball delivered) |
| **Columns** | 64 |
| **Seasons** | 2008 – 2026 (19 seasons) |

> ⚠️ Download `IPL.csv` from the Kaggle link above and place it at `ipl_cricket_analytics/data/IPL.csv` before running the project.

---

## 📌 Problem Statement

The Indian Premier League generates vast amounts of ball-by-ball cricket data. Raw data in this form is difficult to interpret. This project transforms the IPL dataset into an interactive analytics dashboard that enables comprehensive analysis of matches, teams, players, batting, bowling, venues, toss patterns, and seasons.

---

## 🎯 Objectives

- Load, explore, and understand the IPL ball-by-ball dataset (295,732 rows × 64 columns)
- Clean data: handle missing values, derive boundary/wicket flags, standardise types
- Aggregate ball-level records into match, player, team, and season statistics
- Generate 10+ meaningful, data-backed insights
- Build 14 interactive Plotly charts
- Deliver a professional 7-page Streamlit dashboard

---

## 📂 Project Structure

```
ipl_cricket_analytics/
│
├── data/
│   └── IPL.csv                      ← Source dataset (ball-by-ball)
│
├── analysis/
│   └── data_analysis.py             ← Data cleaning & aggregation pipeline
│
├── frontend/
│   └── app.py                       ← Streamlit dashboard (7 pages)
│
├── processed_data/                  ← Auto-generated CSVs (run pipeline first)
│   ├── kpis.csv
│   ├── season_analysis.csv
│   ├── team_wins.csv
│   ├── team_season_wins.csv
│   ├── team_runs.csv
│   ├── batting_analysis.csv
│   ├── batting_season.csv
│   ├── bowling_analysis.csv
│   ├── bowling_season.csv
│   ├── venue_analysis.csv
│   ├── toss_summary.csv
│   ├── toss_decision.csv
│   ├── toss_outcome.csv
│   ├── match_runs.csv
│   ├── highest_scores.csv
│   ├── player_of_match.csv
│   ├── ipl_clean.csv
│   └── data_dictionary.csv
│
├── IPL_Cricket_Analysis.ipynb       ← Jupyter notebook (full walkthrough)
├── PROJECT_REPORT.md                ← Detailed project report
├── requirements.txt                 ← Python dependencies
└── README.md
```

---

## 📊 Dataset Description

| Attribute | Value |
|-----------|-------|
| File | `IPL.csv` |
| Source | Kaggle IPL Ball-by-Ball Dataset |
| Rows | ~295,732 |
| Columns | 64 |
| Granularity | One row per ball delivered |
| Seasons | 2008 – 2026 (19 seasons) |

### Key Columns

| Column | Description |
|--------|-------------|
| `match_id` | Unique match identifier |
| `date` | Match date |
| `batting_team` / `bowling_team` | Teams for each delivery |
| `batter` / `bowler` | Player names |
| `runs_batter` | Runs scored by batter |
| `valid_ball` | 1 = legal delivery |
| `runs_total` | Total runs (batter + extras) |
| `wicket_kind` | Type of dismissal |
| `toss_winner` / `toss_decision` | Toss details |
| `match_won_by` | Match winner |
| `venue` | Stadium |
| `player_of_match` | POTM award |

---

## 🧹 Data Cleaning

| Step | Action |
|------|--------|
| Date parsing | `date` → `datetime`, derived `season_year` |
| Duplicates | 0 exact duplicates found |
| Numeric coercion | All numeric columns cast with `errors='coerce'` |
| Boundary flags | `is_four`, `is_six` derived from `runs_batter` + `runs_not_boundary` |
| Wicket flag | `is_wicket` from non-null `wicket_kind` |
| Innings filter | Only innings 1 & 2 used (super-overs excluded) |

---

## 📈 Key Insights (from actual IPL.csv data)

| # | Insight |
|---|---------|
| 1 | **V Kohli** — all-time IPL run leader with **9,336 runs** |
| 2 | **B Kumar** — most wickets: **243** (economy 7.71) |
| 3 | Toss winners win only **50.5%** of matches — minimal toss advantage |
| 4 | Avg runs/match grew from **309 (2008)** to **371 (2026)** |
| 5 | **Eden Gardens** most-used venue: **77 matches** |
| 6 | **AB de Villiers** — most POTM awards: **25** |
| 7 | Total runs across all IPL seasons: **401,423** |
| 8 | **SP Narine** — best economy among top wicket-takers: **6.79** |
| 9 | **DA Warner** — highest strike rate in top-5 run scorers: **140.43** |
| 10 | IPL has featured **806 unique players** in **1,243 matches** |

---

## 🖥️ Dashboard Pages

| Page | What You'll Find |
|------|-----------------|
| 🏠 **Home / Overview** | 7 KPI cards · Season run trend · Top batsmen & bowlers · Key insights |
| 🏆 **Team Analysis** | Wins / losses / win% · Season trends · Runs per team · Heatmap |
| 🏏 **Player Analysis** | Per-player batting & bowling stats · Season-wise charts |
| 📊 **Batting Analysis** | Top scorers · Strike rates · Boundary leaders · Scatter plot |
| 🎯 **Bowling Analysis** | Top wicket-takers · Economy rates · Bowling averages |
| 📅 **Match & Season** | Season selector · Matches/runs/wickets trend · Top-scoring matches |
| 🏟️ **Venue & Toss** | Venue stats · Toss decision pie · Toss win % bar chart |

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python 3.11 | Core language |
| Pandas | Data loading, cleaning, aggregation |
| NumPy | Numerical operations |
| Plotly | 14 interactive charts |
| Streamlit | 7-page web dashboard |

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/poonamjundre725-dotcom/ibm-bob-project.git
cd ibm-bob-project/ipl_cricket_analytics
```

### 2. Download the Dataset

> ⚠️ **IPL.csv is not included in this repo** (file size > 100 MB — GitHub limit).
> Download it from Kaggle and place it at `data/IPL.csv`:
>
> 📥 **[Download IPL.csv from Kaggle](https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020)**

```
ipl_cricket_analytics/
└── data/
    └── IPL.csv     ← place the downloaded file here
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the data pipeline
```bash
python analysis/data_analysis.py
```

### 5. Launch the dashboard
```bash
streamlit run frontend/app.py
```

Open **http://localhost:8501** in your browser.

---

## 📓 Jupyter Notebook

Open `IPL_Cricket_Analysis.ipynb` in Jupyter or VS Code to walk through the complete analysis step-by-step with inline outputs and charts.

```bash
jupyter notebook IPL_Cricket_Analysis.ipynb
```

---

## 📄 Project Report

See [`PROJECT_REPORT.md`](PROJECT_REPORT.md) for the full written report including problem statement, objectives, dataset description, data cleaning process, EDA, visualizations, and conclusions.

---

## 📜 License

This project is for educational purposes. Dataset sourced from Kaggle.

---

<p align="center">Built with ❤️ using Python · Pandas · Plotly · Streamlit | IBM Bob Project</p>
