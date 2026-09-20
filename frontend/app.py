"""
IPL Cricket Data Analytics Dashboard — Streamlit Application
"""

import os
import sys
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IPL Cricket Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Paths ────────────────────────────────────────────────────────────────────
BASE      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC      = os.path.join(BASE, "processed_data")

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header{font-size:2.2rem;font-weight:700;color:#FF6B35;text-align:center;margin-bottom:0.3rem}
    .sub-header{font-size:1rem;color:#888;text-align:center;margin-bottom:1.5rem}
    .kpi-card{background:linear-gradient(135deg,#1a1a2e,#16213e);border-radius:12px;
              padding:1.2rem;text-align:center;border-left:4px solid #FF6B35}
    .kpi-value{font-size:2rem;font-weight:700;color:#FF6B35}
    .kpi-label{font-size:0.8rem;color:#aaa;margin-top:0.2rem}
    .section-header{font-size:1.3rem;font-weight:600;color:#FF6B35;
                    border-bottom:2px solid #FF6B35;padding-bottom:0.3rem;margin:1.2rem 0 0.8rem}
    div[data-testid="stMetricValue"]{font-size:1.8rem;color:#FF6B35}
</style>
""", unsafe_allow_html=True)

ACCENT = "#FF6B35"
BG_DARK = "#1a1a2e"

# ── Data loaders ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load(fname):
    path = os.path.join(PROC, fname)
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path, low_memory=False)


def fmt(n, decimals=0):
    if pd.isna(n):
        return "—"
    if isinstance(n, float) and decimals == 0:
        n = int(n)
    return f"{n:,.{decimals}f}"


def bar_chart(df, x, y, title, color=ACCENT, orientation="v", top_n=None):
    if top_n:
        df = df.head(top_n)
    if orientation == "h":
        fig = px.bar(df, x=y, y=x, orientation="h", title=title,
                     color_discrete_sequence=[color])
        fig.update_layout(yaxis=dict(autorange="reversed"))
    else:
        fig = px.bar(df, x=x, y=y, title=title,
                     color_discrete_sequence=[color])
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e0e0e0",
        title_font_size=14,
        margin=dict(l=10, r=10, t=40, b=10),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="#333")
    return fig


def line_chart(df, x, y, title, color=ACCENT):
    fig = px.line(df, x=x, y=y, title=title,
                  markers=True, color_discrete_sequence=[color])
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e0e0e0",
        title_font_size=14,
        margin=dict(l=10, r=10, t=40, b=10),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="#333")
    return fig


def pie_chart(df, names, values, title):
    fig = px.pie(df, names=names, values=values, title=title,
                 color_discrete_sequence=px.colors.qualitative.Bold)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#e0e0e0",
        title_font_size=14,
        margin=dict(l=10, r=10, t=40, b=10),
    )
    return fig


# ── Sidebar navigation ────────────────────────────────────────────────────────
pages = [
    "🏠 Home / Overview",
    "🏆 Team Analysis",
    "🏏 Player Analysis",
    "📊 Batting Analysis",
    "🎯 Bowling Analysis",
    "📅 Match & Season Analysis",
    "🏟️ Venue & Toss Analysis",
]

with st.sidebar:
    st.markdown("## 🏏 IPL Analytics")
    st.markdown("---")
    page = st.radio("Navigate", pages, label_visibility="collapsed")
    st.markdown("---")
    st.markdown("<small style='color:#888'>Data: IPL Ball-by-Ball Dataset<br>Built with Streamlit + Plotly</small>",
                unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 1 — HOME / OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════
if page == "🏠 Home / Overview":
    st.markdown('<div class="main-header">🏏 IPL Cricket Data Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">A comprehensive end-to-end analysis of Indian Premier League ball-by-ball data</div>', unsafe_allow_html=True)

    kpis       = load("kpis.csv")
    batting    = load("batting_analysis.csv")
    bowling    = load("bowling_analysis.csv")
    team_wins  = load("team_wins.csv")
    season_df  = load("season_analysis.csv")

    if kpis.empty:
        st.error("Processed data not found. Please run `analysis/data_analysis.py` first.")
        st.stop()

    k = kpis.iloc[0]

    # KPI cards
    cols = st.columns(7)
    kpi_data = [
        ("Total Matches",    fmt(k["total_matches"])),
        ("Seasons",          fmt(k["total_seasons"])),
        ("Teams",            fmt(k["total_teams"])),
        ("Players",          fmt(k["total_players"])),
        ("Total Runs",       fmt(k["total_runs"])),
        ("Total Wickets",    fmt(k["total_wickets"])),
        ("Valid Balls",      fmt(k["total_valid_balls"])),
    ]
    for col, (label, val) in zip(cols, kpi_data):
        col.markdown(
            f'<div class="kpi-card"><div class="kpi-value">{val}</div><div class="kpi-label">{label}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-header">📈 Season-wise Run Trend</div>', unsafe_allow_html=True)
        if not season_df.empty:
            season_df_s = season_df.sort_values("season_year")
            st.plotly_chart(line_chart(season_df_s, "season_year", "total_runs", "Total Runs by Season"), use_container_width=True)

    with c2:
        st.markdown('<div class="section-header">🏆 Top Teams by Wins</div>', unsafe_allow_html=True)
        if not team_wins.empty:
            st.plotly_chart(bar_chart(team_wins.head(10), "team", "wins", "Top 10 Teams by Wins"), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="section-header">🏏 Top 10 Run Scorers</div>', unsafe_allow_html=True)
        if not batting.empty:
            st.plotly_chart(bar_chart(batting.head(10), "batter", "total_runs", "Top 10 Batsmen", orientation="h"), use_container_width=True)

    with c4:
        st.markdown('<div class="section-header">🎯 Top 10 Wicket Takers</div>', unsafe_allow_html=True)
        if not bowling.empty:
            st.plotly_chart(bar_chart(bowling.head(10), "bowler", "wickets", "Top 10 Bowlers", color="#7B2D8B", orientation="h"), use_container_width=True)

    st.markdown("---")
    st.markdown('<div class="section-header">📋 Key Insights</div>', unsafe_allow_html=True)

    if not batting.empty and not bowling.empty and not team_wins.empty:
        top_bat = batting.iloc[0]
        top_bowl= bowling.iloc[0]
        top_team= team_wins.iloc[0]
        avg_sr  = batting["strike_rate"].median()
        hi_score= load("highest_scores.csv")

        insights = [
            f"🏏 **{top_bat['batter']}** is the all-time leading run scorer with **{fmt(top_bat['total_runs'])} runs** across {fmt(top_bat['innings_played'])} matches.",
            f"🎯 **{top_bowl['bowler']}** leads wicket takers with **{fmt(top_bowl['wickets'])} wickets** (economy: {top_bowl['economy']:.2f}).",
            f"🏆 **{top_team['team']}** has the most IPL wins: **{fmt(top_team['wins'])} wins** ({top_team['win_pct']:.1f}% win rate).",
            f"📊 Median batter strike rate across all innings: **{avg_sr:.1f}**.",
            f"📈 Total runs scored across all IPL seasons: **{fmt(k['total_runs'])}**.",
        ]
        if not hi_score.empty:
            hs = hi_score.iloc[0]
            insights.append(f"⭐ Highest individual innings: **{fmt(hs['score'])} runs** by **{hs['batter']}**.")
        for ins in insights:
            st.markdown(f"- {ins}")

    st.markdown("---")
    st.markdown('<div class="section-header">📂 Dataset Summary</div>', unsafe_allow_html=True)
    dd = load("data_dictionary.csv")
    if not dd.empty:
        st.dataframe(dd, use_container_width=True, height=300)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 2 — TEAM ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
elif page == "🏆 Team Analysis":
    st.markdown('<div class="main-header">🏆 Team Analysis</div>', unsafe_allow_html=True)

    team_wins     = load("team_wins.csv")
    team_runs     = load("team_runs.csv")
    season_wins   = load("team_season_wins.csv")
    batting_full  = load("batting_season.csv")

    if team_wins.empty:
        st.error("Processed data not found. Please run the analysis script first.")
        st.stop()

    all_teams = sorted(team_wins["team"].dropna().unique().tolist())
    sel_team = st.selectbox("Select a Team", ["All Teams"] + all_teams)

    st.markdown("---")

    if sel_team == "All Teams":
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="section-header">Wins by Team</div>', unsafe_allow_html=True)
            st.plotly_chart(bar_chart(team_wins.sort_values("wins", ascending=False),
                                      "team", "wins", "Total IPL Wins per Team", orientation="h"), use_container_width=True)
        with c2:
            st.markdown('<div class="section-header">Win Percentage</div>', unsafe_allow_html=True)
            st.plotly_chart(bar_chart(team_wins.sort_values("win_pct", ascending=False),
                                      "team", "win_pct", "Win % per Team", color="#4CAF50", orientation="h"), use_container_width=True)

        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<div class="section-header">Total Runs by Team</div>', unsafe_allow_html=True)
            st.plotly_chart(bar_chart(team_runs.sort_values("total_runs", ascending=False),
                                      "batting_team", "total_runs", "Total Runs Scored", color="#FFC107", orientation="h"), use_container_width=True)
        with c4:
            st.markdown('<div class="section-header">Wins vs Losses</div>', unsafe_allow_html=True)
            fig = go.Figure()
            tw = team_wins.sort_values("wins", ascending=False).head(12)
            fig.add_trace(go.Bar(name="Wins",   x=tw["team"], y=tw["wins"],   marker_color="#4CAF50"))
            fig.add_trace(go.Bar(name="Losses", x=tw["team"], y=tw["losses"], marker_color="#F44336"))
            fig.update_layout(barmode="group", paper_bgcolor="rgba(0,0,0,0)",
                               plot_bgcolor="rgba(0,0,0,0)", font_color="#e0e0e0",
                               title="Wins vs Losses (Top 12 Teams)",
                               margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig, use_container_width=True)

        st.markdown('<div class="section-header">Full Team Statistics Table</div>', unsafe_allow_html=True)
        st.dataframe(team_wins.sort_values("wins", ascending=False).reset_index(drop=True), use_container_width=True)

    else:
        # Single team view
        tw_row = team_wins[team_wins["team"] == sel_team]
        if not tw_row.empty:
            r = tw_row.iloc[0]
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Matches Played", fmt(r.get("matches_played", 0)))
            c2.metric("Wins",           fmt(r.get("wins", 0)))
            c3.metric("Losses",         fmt(r.get("losses", 0)))
            c4.metric("Win %",          f"{r.get('win_pct',0):.1f}%")

        st.markdown('<div class="section-header">Season-wise Wins</div>', unsafe_allow_html=True)
        team_sw = season_wins[season_wins["team"] == sel_team].sort_values("season_year")
        if not team_sw.empty:
            st.plotly_chart(line_chart(team_sw, "season_year", "wins", f"{sel_team} — Wins per Season"), use_container_width=True)
        else:
            st.info("No season win data for this team.")

        st.markdown('<div class="section-header">Total Runs Scored</div>', unsafe_allow_html=True)
        tr_row = team_runs[team_runs["batting_team"] == sel_team]
        if not tr_row.empty:
            st.metric("Total Runs", fmt(tr_row.iloc[0]["total_runs"]))


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 3 — PLAYER ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
elif page == "🏏 Player Analysis":
    st.markdown('<div class="main-header">🏏 Player Analysis</div>', unsafe_allow_html=True)

    batting       = load("batting_analysis.csv")
    bowling       = load("bowling_analysis.csv")
    bat_season    = load("batting_season.csv")
    bowl_season   = load("bowling_season.csv")
    potm          = load("player_of_match.csv")

    all_batters  = sorted(batting["batter"].dropna().unique().tolist())
    all_bowlers  = sorted(bowling["bowler"].dropna().unique().tolist())
    all_players  = sorted(set(all_batters + all_bowlers))

    sel_player = st.selectbox("Select a Player", all_players)
    st.markdown("---")

    # Batting stats
    bat_row = batting[batting["batter"] == sel_player]
    bowl_row= bowling[bowling["bowler"] == sel_player]

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-header">Batting Statistics</div>', unsafe_allow_html=True)
        if not bat_row.empty:
            r = bat_row.iloc[0]
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Runs",          fmt(r["total_runs"]))
            m2.metric("Balls Faced",   fmt(r["balls_faced"]))
            m3.metric("Strike Rate",   f"{r['strike_rate']:.1f}")
            m4.metric("Innings",       fmt(r["innings_played"]))
            st.metric("Fours", fmt(r["fours"]))
            st.metric("Sixes", fmt(r["sixes"]))
        else:
            st.info("No batting data for this player.")

    with c2:
        st.markdown('<div class="section-header">Bowling Statistics</div>', unsafe_allow_html=True)
        if not bowl_row.empty:
            r = bowl_row.iloc[0]
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Wickets",       fmt(r["wickets"]))
            m2.metric("Balls Bowled",  fmt(r["balls_bowled"]))
            m3.metric("Economy",       f"{r['economy']:.2f}")
            m4.metric("Matches",       fmt(r["matches"]))
            if pd.notna(r["avg"]):
                st.metric("Bowling Avg", f"{r['avg']:.2f}")
        else:
            st.info("No bowling data for this player.")

    # Season-wise batting
    st.markdown('<div class="section-header">Season-wise Batting Performance</div>', unsafe_allow_html=True)
    pb = bat_season[bat_season["batter"] == sel_player].sort_values("season_year")
    if not pb.empty:
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Runs per Season", "Strike Rate per Season"))
        fig.add_trace(go.Bar(x=pb["season_year"], y=pb["runs"], marker_color=ACCENT, name="Runs"), row=1, col=1)
        fig.add_trace(go.Scatter(x=pb["season_year"], y=pb["strike_rate"], mode="lines+markers",
                                  marker_color="#4CAF50", name="SR"), row=1, col=2)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font_color="#e0e0e0", showlegend=False,
                           margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No season-wise batting data.")

    # Season-wise bowling
    st.markdown('<div class="section-header">Season-wise Bowling Performance</div>', unsafe_allow_html=True)
    pw = bowl_season[bowl_season["bowler"] == sel_player].sort_values("season_year")
    if not pw.empty:
        fig2 = make_subplots(rows=1, cols=2, subplot_titles=("Wickets per Season", "Economy per Season"))
        fig2.add_trace(go.Bar(x=pw["season_year"], y=pw["wickets"], marker_color="#7B2D8B", name="Wickets"), row=1, col=1)
        fig2.add_trace(go.Scatter(x=pw["season_year"], y=pw["economy"], mode="lines+markers",
                                   marker_color="#FF9800", name="Economy"), row=1, col=2)
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                            font_color="#e0e0e0", showlegend=False,
                            margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig2, use_container_width=True)

    # Player of the match
    if not potm.empty:
        potm_row = potm[potm["player"] == sel_player]
        if not potm_row.empty:
            st.success(f"🏅 Player of the Match awards: **{potm_row.iloc[0]['awards']}**")


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 4 — BATTING ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
elif page == "📊 Batting Analysis":
    st.markdown('<div class="main-header">📊 Batting Analysis</div>', unsafe_allow_html=True)

    batting    = load("batting_analysis.csv")
    hi_scores  = load("highest_scores.csv")
    bat_season = load("batting_season.csv")

    if batting.empty:
        st.error("Processed data not found.")
        st.stop()

    top_n = st.slider("Show Top N Batsmen", 5, 30, 10)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-header">Top Run Scorers</div>', unsafe_allow_html=True)
        st.plotly_chart(bar_chart(batting.head(top_n), "batter", "total_runs",
                                   f"Top {top_n} Run Scorers", orientation="h"), use_container_width=True)
    with c2:
        st.markdown('<div class="section-header">Top Strike Rates (min 200 balls)</div>', unsafe_allow_html=True)
        sr_df = batting[batting["balls_faced"] >= 200].sort_values("strike_rate", ascending=False).head(top_n)
        st.plotly_chart(bar_chart(sr_df, "batter", "strike_rate",
                                   f"Top {top_n} Strike Rates", color="#4CAF50", orientation="h"), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="section-header">Top Boundary Hitters (Sixes)</div>', unsafe_allow_html=True)
        six_df = batting.sort_values("sixes", ascending=False).head(top_n)
        st.plotly_chart(bar_chart(six_df, "batter", "sixes",
                                   f"Top {top_n} Six Hitters", color="#9C27B0", orientation="h"), use_container_width=True)
    with c4:
        st.markdown('<div class="section-header">Top Boundary Hitters (Fours)</div>', unsafe_allow_html=True)
        four_df = batting.sort_values("fours", ascending=False).head(top_n)
        st.plotly_chart(bar_chart(four_df, "batter", "fours",
                                   f"Top {top_n} Four Hitters", color="#2196F3", orientation="h"), use_container_width=True)

    st.markdown('<div class="section-header">Highest Individual Innings Scores</div>', unsafe_allow_html=True)
    if not hi_scores.empty:
        st.dataframe(hi_scores[["batter", "match_id", "score", "balls"]].head(20).reset_index(drop=True),
                      use_container_width=True)

    st.markdown('<div class="section-header">Runs Distribution (Runs vs Strike Rate scatter)</div>', unsafe_allow_html=True)
    scatter_df = batting[batting["balls_faced"] >= 100].copy()
    fig = px.scatter(scatter_df, x="total_runs", y="strike_rate", hover_name="batter",
                     size="balls_faced", color="sixes",
                     color_continuous_scale="Oranges",
                     title="Runs vs Strike Rate (bubble size = balls faced, colour = sixes)")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       font_color="#e0e0e0", margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">Full Batting Stats Table</div>', unsafe_allow_html=True)
    st.dataframe(batting.reset_index(drop=True), use_container_width=True, height=350)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 5 — BOWLING ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
elif page == "🎯 Bowling Analysis":
    st.markdown('<div class="main-header">🎯 Bowling Analysis</div>', unsafe_allow_html=True)

    bowling      = load("bowling_analysis.csv")
    bowl_season  = load("bowling_season.csv")
    season_df    = load("season_analysis.csv")

    if bowling.empty:
        st.error("Processed data not found.")
        st.stop()

    top_n = st.slider("Show Top N Bowlers", 5, 30, 10)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-header">Top Wicket Takers</div>', unsafe_allow_html=True)
        st.plotly_chart(bar_chart(bowling.head(top_n), "bowler", "wickets",
                                   f"Top {top_n} Wicket Takers", color="#7B2D8B", orientation="h"), use_container_width=True)
    with c2:
        st.markdown('<div class="section-header">Best Economy Rates (min 200 valid balls)</div>', unsafe_allow_html=True)
        eco_df = bowling[bowling["balls_bowled"] >= 200].sort_values("economy").head(top_n)
        st.plotly_chart(bar_chart(eco_df, "bowler", "economy",
                                   f"Top {top_n} Economy Rates", color="#FF9800", orientation="h"), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="section-header">Best Bowling Averages (min 30 wickets)</div>', unsafe_allow_html=True)
        avg_df = bowling[(bowling["wickets"] >= 30) & bowling["avg"].notna()].sort_values("avg").head(top_n)
        st.plotly_chart(bar_chart(avg_df, "bowler", "avg",
                                   f"Best Bowling Averages", color="#2196F3", orientation="h"), use_container_width=True)
    with c4:
        st.markdown('<div class="section-header">Wickets by Season (all bowlers)</div>', unsafe_allow_html=True)
        if not season_df.empty:
            sdf = season_df.sort_values("season_year")
            st.plotly_chart(line_chart(sdf, "season_year", "total_wickets",
                                        "Total Wickets per Season", color="#9C27B0"), use_container_width=True)

    st.markdown('<div class="section-header">Wickets vs Economy (scatter)</div>', unsafe_allow_html=True)
    scatter_b = bowling[bowling["balls_bowled"] >= 60].copy()
    fig = px.scatter(scatter_b, x="wickets", y="economy", hover_name="bowler",
                     size="balls_bowled", color="wickets",
                     color_continuous_scale="Purples",
                     title="Wickets vs Economy (bubble size = balls bowled)")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       font_color="#e0e0e0", margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">Full Bowling Stats Table</div>', unsafe_allow_html=True)
    st.dataframe(bowling.reset_index(drop=True), use_container_width=True, height=350)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 6 — MATCH & SEASON ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
elif page == "📅 Match & Season Analysis":
    st.markdown('<div class="main-header">📅 Match & Season Analysis</div>', unsafe_allow_html=True)

    season_df    = load("season_analysis.csv")
    match_runs   = load("match_runs.csv")
    team_sw      = load("team_season_wins.csv")

    if season_df.empty:
        st.error("Processed data not found.")
        st.stop()

    seasons_avail = sorted(season_df["season_year"].dropna().unique().astype(int).tolist())
    sel_season = st.selectbox("Filter by Season", ["All Seasons"] + [str(s) for s in seasons_avail])

    st.markdown("---")

    sdf = season_df.sort_values("season_year")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Matches", fmt(sdf["matches"].sum()))
    c2.metric("Total Runs",    fmt(sdf["total_runs"].sum()))
    c3.metric("Total Wickets", fmt(sdf["total_wickets"].sum()))
    c4.metric("Seasons",       str(len(sdf)))

    c5, c6 = st.columns(2)
    with c5:
        st.markdown('<div class="section-header">Matches per Season</div>', unsafe_allow_html=True)
        st.plotly_chart(bar_chart(sdf, "season_year", "matches", "Matches per Season"), use_container_width=True)
    with c6:
        st.markdown('<div class="section-header">Avg Runs per Match by Season</div>', unsafe_allow_html=True)
        st.plotly_chart(line_chart(sdf, "season_year", "avg_runs_per_match",
                                    "Avg Runs per Match per Season", color="#4CAF50"), use_container_width=True)

    c7, c8 = st.columns(2)
    with c7:
        st.markdown('<div class="section-header">Total Runs per Season</div>', unsafe_allow_html=True)
        st.plotly_chart(bar_chart(sdf, "season_year", "total_runs", "Total Runs per Season", color="#FFC107"), use_container_width=True)
    with c8:
        st.markdown('<div class="section-header">Total Wickets per Season</div>', unsafe_allow_html=True)
        st.plotly_chart(bar_chart(sdf, "season_year", "total_wickets", "Total Wickets per Season", color="#9C27B0"), use_container_width=True)

    # Season-filtered match table
    st.markdown('<div class="section-header">Match Details</div>', unsafe_allow_html=True)
    if sel_season != "All Seasons":
        mr = match_runs[match_runs["season_year"] == int(sel_season)]
    else:
        mr = match_runs.copy()

    if not mr.empty:
        st.markdown(f"**Top Scoring Matches {'in ' + sel_season if sel_season != 'All Seasons' else '(All Seasons)'}**")
        st.dataframe(mr[["match_id","season_year","batting_team","bowling_team","venue","total_runs","total_wickets"]]
                     .sort_values("total_runs", ascending=False).head(20).reset_index(drop=True),
                     use_container_width=True)

    # Season-wise team wins heatmap
    st.markdown('<div class="section-header">Season × Team Wins Heatmap</div>', unsafe_allow_html=True)
    if not team_sw.empty:
        pivot = team_sw.pivot_table(index="team", columns="season_year", values="wins", fill_value=0)
        fig_h = px.imshow(pivot, color_continuous_scale="YlOrRd",
                           title="Season × Team Wins Heatmap",
                           labels=dict(x="Season Year", y="Team", color="Wins"))
        fig_h.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                             font_color="#e0e0e0", margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_h, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 7 — VENUE & TOSS ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
elif page == "🏟️ Venue & Toss Analysis":
    st.markdown('<div class="main-header">🏟️ Venue & Toss Analysis</div>', unsafe_allow_html=True)

    venue_df     = load("venue_analysis.csv")
    toss_summary = load("toss_summary.csv")
    toss_decision= load("toss_decision.csv")
    toss_outcome = load("toss_outcome.csv")

    if venue_df.empty:
        st.error("Processed data not found.")
        st.stop()

    tab1, tab2 = st.tabs(["🏟️ Venue Analysis", "🎲 Toss Analysis"])

    with tab1:
        top_venues = st.slider("Show Top N Venues", 5, 30, 15)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="section-header">Matches by Venue</div>', unsafe_allow_html=True)
            st.plotly_chart(bar_chart(venue_df.head(top_venues), "venue", "matches",
                                       f"Top {top_venues} Venues by Matches", orientation="h"), use_container_width=True)
        with c2:
            st.markdown('<div class="section-header">Avg Runs per Match by Venue</div>', unsafe_allow_html=True)
            run_venue = venue_df.sort_values("avg_runs_per_match", ascending=False).head(top_venues)
            st.plotly_chart(bar_chart(run_venue, "venue", "avg_runs_per_match",
                                       f"Avg Runs per Match by Venue", color="#FFC107", orientation="h"), use_container_width=True)

        st.markdown('<div class="section-header">Venue Statistics Table</div>', unsafe_allow_html=True)
        st.dataframe(venue_df.reset_index(drop=True), use_container_width=True, height=350)

    with tab2:
        st.markdown('<div class="section-header">Toss Summary</div>', unsafe_allow_html=True)
        if not toss_summary.empty:
            for _, row in toss_summary.iterrows():
                st.metric(row["metric"], str(row["value"]))

        st.markdown("---")
        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<div class="section-header">Toss Decision Distribution</div>', unsafe_allow_html=True)
            if not toss_decision.empty:
                st.plotly_chart(pie_chart(toss_decision, "decision", "count",
                                           "Bat vs Field — Toss Decisions"), use_container_width=True)
        with c4:
            st.markdown('<div class="section-header">Win % by Toss Decision</div>', unsafe_allow_html=True)
            if not toss_outcome.empty:
                fig = go.Figure(go.Bar(
                    x=toss_outcome["toss_decision"],
                    y=toss_outcome["win_pct"],
                    marker_color=[ACCENT, "#4CAF50"],
                    text=toss_outcome["win_pct"].apply(lambda x: f"{x:.1f}%"),
                    textposition="outside",
                ))
                fig.update_layout(
                    title="Win % for Toss Winner — by Decision",
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#e0e0e0", yaxis_title="Win %",
                    margin=dict(l=10, r=10, t=40, b=10),
                )
                st.plotly_chart(fig, use_container_width=True)

        st.markdown('<div class="section-header">Toss Winner vs Match Winner Insight</div>', unsafe_allow_html=True)
        if not toss_outcome.empty:
            total_matches  = toss_outcome["total"].sum()
            total_toss_wins= toss_outcome["wins"].sum()
            pct = round(total_toss_wins / total_matches * 100, 1) if total_matches > 0 else 0
            if pct > 50:
                st.info(f"📊 Toss winners win **{pct}%** of matches — winning the toss provides a **slight advantage**.")
            else:
                st.info(f"📊 Toss winners win only **{pct}%** of matches — the toss has **limited impact** on match outcome.")
