"""
Script to generate the IPL (Indian Premier League) dataset used in this project.
Run this once to create the CSV files in the /data directory.
"""

import pandas as pd
import numpy as np
import os

np.random.seed(42)

teams = [
    "Mumbai Indians", "Chennai Super Kings", "Royal Challengers Bangalore",
    "Kolkata Knight Riders", "Delhi Capitals", "Sunrisers Hyderabad",
    "Rajasthan Royals", "Punjab Kings"
]

venues = [
    "Wankhede Stadium", "M.A. Chidambaram Stadium", "Eden Gardens",
    "Feroz Shah Kotla", "Rajiv Gandhi Stadium", "Sawai Mansingh Stadium",
    "Punjab Cricket Association Stadium", "M. Chinnaswamy Stadium"
]

players = {
    "Mumbai Indians": ["Rohit Sharma", "Hardik Pandya", "Suryakumar Yadav", "Jasprit Bumrah", "Ishan Kishan"],
    "Chennai Super Kings": ["MS Dhoni", "Ravindra Jadeja", "Ruturaj Gaikwad", "Deepak Chahar", "Ambati Rayudu"],
    "Royal Challengers Bangalore": ["Virat Kohli", "Glenn Maxwell", "Faf du Plessis", "Harshal Patel", "Dinesh Karthik"],
    "Kolkata Knight Riders": ["Andre Russell", "Sunil Narine", "Shubman Gill", "Pat Cummins", "Venkatesh Iyer"],
    "Delhi Capitals": ["Rishabh Pant", "Axar Patel", "Prithvi Shaw", "Anrich Nortje", "Mitchell Marsh"],
    "Sunrisers Hyderabad": ["David Warner", "Kane Williamson", "Rashid Khan", "Bhuvneshwar Kumar", "Nicholas Pooran"],
    "Rajasthan Royals": ["Sanju Samson", "Jos Buttler", "Shimron Hetmyer", "Yuzvendra Chahal", "Trent Boult"],
    "Punjab Kings": ["Shikhar Dhawan", "Liam Livingstone", "KL Rahul", "Kagiso Rabada", "Jonny Bairstow"]
}

# ── MATCHES DATASET ──────────────────────────────────────────────────────────
n_matches = 400
seasons = np.random.choice(range(2015, 2024), n_matches)
team1_list = np.random.choice(teams, n_matches)
team2_list = np.array([np.random.choice([t for t in teams if t != t1]) for t1 in team1_list])
toss_winner = np.array([np.random.choice([t1, t2]) for t1, t2 in zip(team1_list, team2_list)])
toss_decision = np.random.choice(["bat", "field"], n_matches, p=[0.4, 0.6])
match_winner = np.array([
    t1 if np.random.random() > 0.48 else t2
    for t1, t2 in zip(team1_list, team2_list)
])
win_by_runs = np.where(np.random.random(n_matches) > 0.5,
                        np.random.randint(1, 100, n_matches), 0)
win_by_wickets = np.where(win_by_runs == 0,
                           np.random.randint(1, 10, n_matches), 0)

matches_df = pd.DataFrame({
    "match_id": range(1, n_matches + 1),
    "season": seasons,
    "city": np.random.choice(["Mumbai", "Chennai", "Kolkata", "Delhi", "Hyderabad",
                               "Jaipur", "Chandigarh", "Bangalore"], n_matches),
    "venue": np.random.choice(venues, n_matches),
    "team1": team1_list,
    "team2": team2_list,
    "toss_winner": toss_winner,
    "toss_decision": toss_decision,
    "result": np.random.choice(["runs", "wickets", "tie"], n_matches, p=[0.45, 0.50, 0.05]),
    "winner": match_winner,
    "win_by_runs": win_by_runs,
    "win_by_wickets": win_by_wickets,
    "player_of_match": [
        np.random.choice(players[w]) for w in match_winner
    ]
})

# Introduce missing values for data cleaning demo
matches_df.loc[np.random.choice(matches_df.index, 15), "city"] = np.nan
matches_df.loc[np.random.choice(matches_df.index, 10), "player_of_match"] = np.nan

# ── DELIVERIES DATASET ───────────────────────────────────────────────────────
rows = []
for mid in matches_df["match_id"]:
    t1 = matches_df.loc[matches_df["match_id"] == mid, "team1"].values[0]
    t2 = matches_df.loc[matches_df["match_id"] == mid, "team2"].values[0]
    for inning, (batting, bowling) in enumerate([(t1, t2), (t2, t1)], 1):
        bat_players = players[batting]
        bowl_players = players[bowling]
        ball_num = 0
        for over in range(1, 21):
            bowler = np.random.choice(bowl_players)
            for ball in range(1, 7):
                ball_num += 1
                batsman = np.random.choice(bat_players)
                runs = np.random.choice([0,1,2,3,4,6], p=[0.35,0.28,0.12,0.03,0.15,0.07])
                wide = np.random.choice([0,1], p=[0.93,0.07])
                noball = np.random.choice([0,1], p=[0.97,0.03])
                is_wicket = np.random.choice([0,1], p=[0.93,0.07])
                rows.append({
                    "match_id": mid,
                    "inning": inning,
                    "over": over,
                    "ball": ball,
                    "batting_team": batting,
                    "bowling_team": bowling,
                    "batsman": batsman,
                    "bowler": bowler,
                    "batsman_runs": runs,
                    "extra_runs": wide + noball,
                    "total_runs": runs + wide + noball,
                    "is_wicket": is_wicket if wide == 0 else 0,
                    "wide_runs": wide,
                    "noball_runs": noball,
                })

deliveries_df = pd.DataFrame(rows)

# Save
os.makedirs(os.path.dirname(__file__), exist_ok=True)
matches_df.to_csv(os.path.join(os.path.dirname(__file__), "matches.csv"), index=False)
deliveries_df.to_csv(os.path.join(os.path.dirname(__file__), "deliveries.csv"), index=False)
print(f"✅ matches.csv    → {len(matches_df)} rows")
print(f"✅ deliveries.csv → {len(deliveries_df)} rows")
