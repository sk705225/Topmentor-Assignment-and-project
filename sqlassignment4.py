import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error

def get_conn():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="learnSQL",
        database="t20wc"
    )

def run_query(query: str, params=None, fetch=False):
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(query, params or ())
        if fetch:
            return cur.fetchall()
        conn.commit()
        return None
    finally:
        try:
            conn.close()
        except Exception:
            pass

st.set_page_config(page_title="T20 WC Match Entry", layout="wide")
st.title("Men's T20 World Cup – Match Data Entry")

# ---------- Helpers ----------
def get_dropdown(sql):
    rows = run_query(sql, fetch=True)
    return rows

def team_map():
    teams = get_dropdown("SELECT team_id, name FROM team ORDER BY name;")
    return {t["name"]: t["team_id"] for t in teams}

def venue_map():
    venues = get_dropdown("SELECT venue_id, CONCAT(name,' - ',city,', ',country) AS v FROM venue ORDER BY name;")
    return {v["v"]: v["venue_id"] for v in venues}

def tournament_map():
    tourn = get_dropdown("SELECT tournament_id, CONCAT(name,' ',year) AS t FROM tournament ORDER BY year DESC;")
    return {x["t"]: x["tournament_id"] for x in tourn}

# ---------- Sidebar: reference data ----------
st.sidebar.header("Reference Data")
st.sidebar.caption("Make sure teams/venues/players are loaded first.")

# ---------- Main: Match Entry ----------
tmap = tournament_map()
teams = team_map()
venues = venue_map()

col1, col2 = st.columns(2)

with col1:
    tournament_label = st.selectbox("Tournament", list(tmap.keys()))
    match_no = st.text_input("Match No", value="Match 1")
    stage = st.selectbox("Stage", ["Group","Super 8","Semi Final","Final","Qualifier","Other"])
    grp = st.text_input("Group (optional)", value="Group A")
    match_date = st.date_input("Match Date")
    venue_label = st.selectbox("Venue", list(venues.keys()))
with col2:
    team1 = st.selectbox("Team 1", list(teams.keys()))
    team2 = st.selectbox("Team 2", [t for t in teams.keys() if t != team1])
    toss_winner = st.selectbox("Toss Winner", [team1, team2])
    toss_decision = st.selectbox("Toss Decision", ["bat","bowl"])
    result_type = st.selectbox("Result Type", ["normal","tie","no_result","abandoned"])
    player_of_match = st.text_input("Player of Match (text)")

st.subheader("Result Details (if normal win)")
winner_team = st.selectbox("Winner Team", ["(none)"] + [team1, team2])
win_by_runs = st.number_input("Win by Runs", min_value=0, value=0)
win_by_wkts = st.number_input("Win by Wickets", min_value=0, value=0)
notes = st.text_area("Notes / Highlights", height=80)

if st.button("Save Match"):
    winner_id = None if winner_team == "(none)" else teams[winner_team]

    run_query("""
        INSERT INTO match_info
        (tournament_id, match_no, stage, grp, match_date, venue_id,
         team1_id, team2_id, toss_winner_id, toss_decision,
         result_type, winner_team_id, win_by_runs, win_by_wkts,
         player_of_match, notes)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
    """, (
        tmap[tournament_label], match_no, stage, grp, match_date, venues[venue_label],
        teams[team1], teams[team2], teams[toss_winner], toss_decision,
        result_type, winner_id, int(win_by_runs), int(win_by_wkts),
        player_of_match, notes
    ))
    st.success("Match saved! Now add innings + player stats using match_id from the list below.")

st.divider()

st.subheader("Recently Added Matches")
recent = run_query("""
    SELECT match_id, match_no, match_date,
           (SELECT name FROM team WHERE team_id=team1_id) AS team1,
           (SELECT name FROM team WHERE team_id=team2_id) AS team2,
           (SELECT name FROM team WHERE team_id=winner_team_id) AS winner
    FROM match_info
    ORDER BY match_id DESC
    LIMIT 10;
""", fetch=True)

st.dataframe(pd.DataFrame(recent), use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px
from add_data import run_query

st.set_page_config(page_title="T20 WC Dashboard", layout="wide")
st.title("📊 Men's T20 World Cup – Analytics Dashboard")

# Matches table
matches = run_query("""
    SELECT match_id, match_no, match_date,
           (SELECT name FROM team WHERE team_id=team1_id) AS team1,
           (SELECT name FROM team WHERE team_id=team2_id) AS team2,
           (SELECT name FROM team WHERE team_id=winner_team_id) AS winner,
           result_type
    FROM match_info;
""", fetch=True)

dfm = pd.DataFrame(matches)
if dfm.empty:
    st.warning("No match data yet. Add matches first.")
    st.stop()

st.subheader("All Matches")
st.dataframe(dfm.sort_values("match_date"), use_container_width=True)

st.divider()

# Team wins
wins = run_query("""
    SELECT t.name AS team, COUNT(*) AS wins
    FROM match_info m
    JOIN team t ON t.team_id = m.winner_team_id
    WHERE m.winner_team_id IS NOT NULL
    GROUP BY t.name
    ORDER BY wins DESC;
""", fetch=True)
dfw = pd.DataFrame(wins)

c1, c2 = st.columns(2)
with c1:
    st.subheader("Wins by Team")
    if not dfw.empty:
        fig = px.bar(dfw, x="team", y="wins", title="Wins by Team")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No winners recorded yet.")

# Top batters
top_batters = run_query("""
    SELECT p.full_name AS player, t.name AS team,
           SUM(runs_scored) AS runs, SUM(balls_faced) AS balls,
           ROUND(100 * SUM(runs_scored)/NULLIF(SUM(balls_faced),0), 2) AS sr
    FROM player_match_stats s
    JOIN player p ON p.player_id = s.player_id
    JOIN team t ON t.team_id = s.team_id
    GROUP BY p.full_name, t.name
    HAVING SUM(balls_faced) > 0
    ORDER BY runs DESC
    LIMIT 15;
""", fetch=True)
dfb = pd.DataFrame(top_batters)

with c2:
    st.subheader("Top Run-Scorers")
    if not dfb.empty:
        fig = px.bar(dfb, x="player", y="runs", title="Top 15 Run-Scorers")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No batting stats yet.")

st.divider()

# Top bowlers
top_bowlers = run_query("""
    SELECT p.full_name AS player, t.name AS team,
           SUM(wickets_taken) AS wkts,
           SUM(runs_conceded) AS runs,
           ROUND(SUM(runs_conceded)/NULLIF(SUM(overs_bowled),0), 2) AS eco
    FROM player_match_stats s
    JOIN player p ON p.player_id = s.player_id
    JOIN team t ON t.team_id = s.team_id
    GROUP BY p.full_name, t.name
    HAVING SUM(overs_bowled) > 0
    ORDER BY wkts DESC, eco ASC
    LIMIT 15;
""", fetch=True)
dfbo = pd.DataFrame(top_bowlers)

st.subheader("Top Wicket-Takers")
if not dfbo.empty:
    st.dataframe(dfbo, use_container_width=True)
else:
    st.info("No bowling stats yet.")

