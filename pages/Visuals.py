# This creates the page for displaying data visualizations.

import streamlit as st
import json
import matplotlib.pyplot as plt

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")
 
with open("data.json", "r") as file:
    data = json.load(file)
data_points = data["data_points"]
# PART 1: GRAPHS FROM data.json
#static
st.header("Total Receiving Yards")

players = []
total_yards = []
for point in data_points:
    player = point["label"]
    if player not in players:
        players.append(player)
        total_yards.append(0)
    index = players.index(player)
    total_yards[index] += point["Yards"]

fig, ax = plt.subplots()
ax.bar(players,total_yards)
ax.set_title("Total Receiving Yards Across Six Games")
ax.set_xlabel("Wide Receiver")
ax.set_ylabel("Total Receiving Yards")
plt.xticks(rotation=15)
plt.tight_layout()

st.pyplot(fig)
plt.close(fig)

#Dynamic
st.header("Game-by-Game Performance")

if "receiver" not in st.session_state:
    st.session_state.receiver = "Jaxon Smith Njigba"

if "statistic" not in st.session_state:
    st.session_state.statistic = "Fantasy Points"
    
receiver = st.selectbox(
    "Choose a wide Receiver:",
    players,
    key = "receiver"
)
statistic = st.selectbox(
    "Choose a statistic:",
    ["Yards", "Receptions", "Touchdowns", "Fantasy Points"],
    key = "statistic"
)

game_numbers = []
stat_values = []

for point in data_points:
    if point["label"] == receiver:
        game_numbers.append(point["Game"])
        stat_values.append(point[statistic])

chart_data = {}

for i in range(len(game_numbers)):
    chart_data[game_numbers[i]] = stat_values[i]

st.line_chart(chart_data)
st.caption(f"{statistic} for {receiver}, by game")
# PART 2: GRAPHS FROM data.csv
import os
import pandas as pd
 
st.divider()
st.title("Survey Results 🏈")
 
if not os.path.exists("data.csv") or os.path.getsize("data.csv") == 0:
    st.info("No survey data yet. Fill out the Survey page first!")
else:
    df = pd.read_csv("data.csv")
    df["Category"] = df["Category"].astype(str).str.strip().str.title()
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df = df.dropna(subset=["Value"])
 
    # STATIC: pie chart (not affected by any widget)
    st.header("Favorite NFL Teams")
    team_counts = df["Category"].value_counts()
 
    fig2, ax2 = plt.subplots()
    ax2.pie(team_counts.values, labels=team_counts.index, autopct="%1.0f%%")
    ax2.set_title("Share of Survey Responses by Favorite Team")
    st.pyplot(fig2)
    plt.close(fig2)
 
    # DYNAMIC: bar chart controlled by user input
    st.header("Games Watched Per Season")
 
    if "agg_choice" not in st.session_state:
        st.session_state.agg_choice = "Average"
 
    agg_choice = st.radio(
        "How should the values be combined?",
        ["Average", "Total", "Maximum"],
        key="agg_choice",
        horizontal=True,
    )
    max_val = int(df["Value"].max()) if len(df) > 0 else 1
    min_games = st.slider(
        "Only include responses with at least this many games:",
        0, max(max_val, 1), 0,
    )
 
    filtered = df[df["Value"] >= min_games]
    if filtered.empty:
        st.warning("No responses match that filter.")
    else:
        agg_map = {"Average": "mean", "Total": "sum", "Maximum": "max"}
        grouped = filtered.groupby("Category")["Value"].agg(agg_map[agg_choice])
 
        fig3, ax3 = plt.subplots()
        ax3.bar(grouped.index, grouped.values)
        ax3.set_title(f"{agg_choice} Games Watched per Season by Favorite Team")
        ax3.set_xlabel("Favorite Team")
        ax3.set_ylabel(f"{agg_choice} Games Watched")
        plt.xticks(rotation=15)
        plt.tight_layout()
        st.pyplot(fig3)
        plt.close(fig3)
