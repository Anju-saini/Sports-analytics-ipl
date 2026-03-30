# Sports-analytics-ipl
# PL Sports Analytics Project

> **End-to-end Data Analytics & Machine Learning project on Indian Premier League (IPL) cricket data.**  
> Covers Data Cleaning → EDA → Visualizations → ML Prediction — all in Python.

---

##  Project Overview

This project analyses IPL (Indian Premier League) match and ball-by-ball delivery data across 9 seasons (2015–2023).  
We answer key sports analytics questions such as:

- Which teams dominate the IPL?
- Does winning the toss actually help you win the match?
- Who are the top batsmen and bowlers?
- Can we predict the match winner using machine learning?

---

##  Project Structure

```
sports-analytics-project/
│
├── data/
│   ├── generate_data.py        # Script to create the dataset
│   ├── matches.csv             # Raw match-level data (400 matches)
│   ├── deliveries.csv          # Raw ball-by-ball data (96,000 rows)
│   ├── matches_clean.csv       # Cleaned matches data
│   └── deliveries_clean.csv    # Cleaned deliveries data
│
├── src/
│   ├── 01_data_cleaning.py     # Data cleaning & preprocessing
│   ├── 02_eda.py               # Exploratory Data Analysis
│   ├── 03_visualizations.py    # All charts and plots
│   └── 04_ml_model.py          # ML model — match winner prediction
│
├── visualizations/             # All saved PNG charts (auto-generated)
│
├── run_all.py                  # Run the entire pipeline in one command
├── requirements.txt
└── README.md
```

---

## 📊 Dataset

| File | Rows | Columns | Description |
|---|---|---|---|
| `matches.csv` | 400 | 13 | One row per IPL match |
| `deliveries.csv` | 96,000 | 14 | One row per ball bowled |

**Key columns — matches:**
`season`, `team1`, `team2`, `toss_winner`, `toss_decision`, `winner`, `win_by_runs`, `win_by_wickets`, `player_of_match`

**Key columns — deliveries:**
`over`, `ball`, `batting_team`, `bowler`, `batsman`, `batsman_runs`, `is_wicket`, `phase`

---

## 🔧 Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/ipl-sports-analytics.git
cd ipl-sports-analytics
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the full pipeline
```bash
python run_all.py
```

Or run individual scripts step by step:
```bash
python data/generate_data.py        # Step 1 – Generate dataset
python src/01_data_cleaning.py      # Step 2 – Clean data
python src/02_eda.py                # Step 3 – EDA
python src/03_visualizations.py     # Step 4 – Generate charts
python src/04_ml_model.py           # Step 5 – ML model
```

---

## 🧹 Step 1 — Data Cleaning (`01_data_cleaning.py`)

| Issue | Fix Applied |
|---|---|
| Missing `city` values | Filled from `venue` using a mapping dictionary |
| Missing `player_of_match` | Filled with `"Not Awarded"` |
| Outlier `batsman_runs` > 6 | Clipped to 6 |
| Duplicate rows | Dropped using `drop_duplicates()` |
| Binary columns with NaN | Filled with 0 and cast to `int` |

**New features added:**
- `toss_win_match_win` — Did the toss winner also win the match?
- `phase` — Labelled each over as `Powerplay`, `Middle`, or `Death`

---

## 🔍 Step 2 — EDA (`02_eda.py`)

Key findings:
- Teams choosing to **field first** after winning the toss = **63%** of decisions
- Toss winner wins the match only **~50%** of the time — **toss is mostly luck**
- **Death overs** (16–20) have the highest average run rate
- Strike rate leaders are all-rounders and hard-hitters

---

## 📈 Step 3 — Visualizations (`03_visualizations.py`)

13 charts are auto-generated into the `/visualizations/` folder:

| # | Chart | Insight |
|---|---|---|
| 01 | Team Total Wins (bar) | Which team has won the most |
| 02 | Matches per Season (line) | Tournament growth over time |
| 03 | Toss Decision vs Outcome (grouped bar) | Does fielding first help? |
| 04 | Top 10 Run Scorers | Best batsmen all-time |
| 05 | Top 10 Wicket Takers | Best bowlers all-time |
| 06 | Avg Runs/Over by Phase | Powerplay vs Middle vs Death |
| 07 | Run Distribution Heatmap | Over-by-over scoring patterns |
| 08 | Feature Correlation Matrix | How numeric features relate |
| 09 | Win % Batting First by Team | Team strength batting first |
| 10 | Confusion Matrices (both models) | Prediction accuracy |
| 11 | ROC Curves comparison | Model discrimination ability |
| 12 | Feature Importance (RF) | What drives predictions most |
| 13 | Model Performance Comparison | Accuracy & AUC side-by-side |

---

## 🤖 Step 4 — ML Model (`04_ml_model.py`)

### Problem
Binary classification: **Predict which team wins** a given IPL match.

### Features Used
| Feature | Description |
|---|---|
| `team1_enc` / `team2_enc` | Label-encoded team identifiers |
| `venue_enc` | Encoded venue |
| `team1_won_toss` | Did team1 win the toss? |
| `decision_bat` | Did toss winner choose to bat? |
| `team1_win_rate` | Rolling historical win rate of team1 |
| `team2_win_rate` | Rolling historical win rate of team2 |
| `win_rate_diff` | Difference in form between two teams |

> **No data leakage** — win rates are computed using only past matches (rolling, not full-history).

### Models Trained

| Model | Accuracy | ROC-AUC |
|---|---|---|
| Logistic Regression | ~51% | ~0.53 |
| Random Forest | ~62% | ~0.71 |

### Evaluation
- 80/20 train-test split with `stratify=y`
- 5-Fold Stratified Cross-Validation
- Classification Report + Confusion Matrix + ROC Curve

---

## 💡 Key Insights

1. **Toss ≠ Win** — Teams that win the toss win only 50% of matches. Toss advantage is minimal.
2. **Death overs are decisive** — Highest scoring rate; bowler quality here is critical.
3. **Form matters** — Historical win rate is the strongest predictor of match outcome (per feature importance).
4. **Random Forest beats Logistic Regression** — Non-linear relationships in cricket data benefit from tree models.

---

## 🛠️ Tech Stack

| Library | Version | Purpose |
|---|---|---|
| `pandas` | ≥ 1.5 | Data loading, cleaning, aggregation |
| `numpy` | ≥ 1.23 | Numerical operations |
| `matplotlib` | ≥ 3.6 | Base plotting |
| `seaborn` | ≥ 0.12 | Statistical visualisations |
| `scikit-learn` | ≥ 1.2 | ML models, preprocessing, evaluation |

---

## 📁 Output Files

After running `run_all.py`:

```
data/
  matches_clean.csv
  deliveries_clean.csv

visualizations/
  01_team_wins.png
  02_matches_per_season.png
  03_toss_vs_outcome.png
  04_top_scorers.png
  05_top_wicket_takers.png
  06_runs_by_phase.png
  07_over_run_heatmap.png
  08_correlation_heatmap.png
  09_bat_first_win_pct.png
  10_confusion_matrices.png
  11_roc_curves.png
  12_feature_importance.png
  13_model_comparison.png
```

---

## 🚀 Future Improvements

- [ ] Use real IPL dataset from Kaggle
- [ ] Add player-level performance prediction
- [ ] Build an interactive Streamlit dashboard
- [ ] Try XGBoost / LightGBM for better accuracy
- [ ] Add NLP analysis on match commentary

---

## 👤 Author

**[Your Name]**  
Data Analyst | Python • Pandas • Scikit-learn  
[LinkedIn](https://linkedin.com/in/yourprofile) | [GitHub](https://github.com/yourusername)

---

## 📄 License

This project is open source under the [MIT License](LICENSE).
