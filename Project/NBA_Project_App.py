import streamlit as st
import pandas as pd
import mysql.connector

# How to run application
# 1. Copy and paste this line into the terminal
# python -m streamlit run NBA_Project_App.py
# 2. After you're done running it, create a new terminal
# 3. Rinse and repeat
# -----------------------------
# DB CONNECTION
# -----------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Carter05!",
        database="NBA_Project"
    )

# -----------------------------
# TEAM MAPPINGS
# -----------------------------

POSITION_MAP = {
    "G": "PG",
    "F": "SF",
    "C": "C",

    "G-F": "SG",
    "F-G": "SF",

    "F-C": "PF",
    "C-F": "C",

    "GF": "SG",
    "FG": "SF",
    "FC": "PF",
    "CG": "C",
    "CF": "C",

    "PG": "PG",
    "SG": "SG",
    "SF": "SF",
    "PF": "PF",
}

TEAM_LOGO_MAP = {
    "Atl": "atl", "Bos": "bos", "Bro": "bkn", "Chi": "chi", "Cle": "cle",
    "Dal": "dal", "Den": "den", "Det": "det", "Gol": "gsw", "Hou": "hou",
    "Ind": "ind", "Lac": "lac", "Lal": "lal", "Mem": "mem", "Mia": "mia",
    "Mil": "mil", "Min": "min", "Nor": "nop", "Nyk": "nyk", "Okc": "okc",
    "Orl": "orl", "Phi": "phi", "Pho": "phx", "Por": "por", "Sac": "sac",
    "San": "sas", "Tor": "tor", "Uta": "uta", "Was": "was", "Cha": "cha",
}

TEAM_FULL_NAME_MAP = {
    "Atl": "Atlanta Hawks",
    "Bos": "Boston Celtics",
    "Bro": "Brooklyn Nets",
    "Cha": "Charlotte Hornets",
    "Chi": "Chicago Bulls",
    "Cle": "Cleveland Cavaliers",
    "Dal": "Dallas Mavericks",
    "Den": "Denver Nuggets",
    "Det": "Detroit Pistons",
    "Gol": "Golden State Warriors",
    "Hou": "Houston Rockets",
    "Ind": "Indiana Pacers",
    "Lac": "Los Angeles Clippers",
    "Lal": "Los Angeles Lakers",
    "Mem": "Memphis Grizzlies",
    "Mia": "Miami Heat",
    "Mil": "Milwaukee Bucks",
    "Min": "Minnesota Timberwolves",
    "Nor": "New Orleans Pelicans",
    "Nyk": "New York Knicks",
    "Okc": "Oklahoma City Thunder",
    "Orl": "Orlando Magic",
    "Phi": "Philadelphia 76ers",
    "Pho": "Phoenix Suns",
    "Por": "Portland Trail Blazers",
    "Sac": "Sacramento Kings",
    "San": "San Antonio Spurs",
    "Tor": "Toronto Raptors",
    "Uta": "Utah Jazz",
    "Was": "Washington Wizards",
}

def get_team_logo_url(team_code: str) -> str | None:
    code = TEAM_LOGO_MAP.get(team_code)
    if not code:
        return None
    return f"https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/{code}.png"

def get_player_image_url(name: str) -> str:
    # Always returns a readable avatar image based on player name
    # (so you never get a broken image)
    return f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&background=0D8ABC&color=ffffff&size=256"

# -----------------------------
# DATA HELPERS
# -----------------------------
@st.cache_data
def load_raw_stats():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM NBA_Stats_Raw;", conn)
    conn.close()
    return df

# -----------------------------
# PAGE CONFIG & CUSTOM STYLE
# -----------------------------
st.set_page_config(page_title="NBA Advanced Stats Explorer", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f9fafb, #e5f0ff);
        color: #111827;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3, h4 {
        color: #111827;
    }
    .stMetric {
        background-color: #ffffff !important;
        border-radius: 10px;
        padding: 10px;
        border: 1px solid #e5e7eb;
    }
    .stDataFrame {
        background-color: #ffffff !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #e5e7eb;
        border-radius: 999px;
        padding: 0.5rem 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title(" NBA Advanced Stats Explorer 2024-2025 Season ")

# -----------------------------
# LOAD & PREP DATA
# -----------------------------
df = load_raw_stats()
if df.empty:
    st.error("No data found in NBA_Stats_Raw.")
    st.stop()

# now df exists, so this is valid:
df["POS_STD"] = df["POS"].map(POSITION_MAP).fillna(df["POS"])

numeric_cols = [
    "AGE", "GP", "MpG", "USG%", "TO%", "FTA", "FT%", "2PA", "2P%", "3PA", "3P%",
    "eFG%", "TS%", "PpG", "RpG", "ApG", "SpG", "BpG", "TOpG",
    "P+R", "P+A", "P+R+A", "VI", "ORtg", "DRtg"
]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Round ages to nearest whole number
df["AGE_INT"] = df["AGE"].round().astype("Int64")

# Add full team name column
df["TEAM_FULL"] = df["TEAM"].map(TEAM_FULL_NAME_MAP).fillna(df["TEAM"])

teams_codes = sorted(df["TEAM"].unique().tolist())
teams_full = ["All"] + [TEAM_FULL_NAME_MAP.get(t, t) for t in teams_codes]

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

team_choice_full = st.sidebar.selectbox("Team", teams_full)

min_age = int(df["AGE_INT"].min())
max_age = int(df["AGE_INT"].max())
age_range = st.sidebar.slider("Age range", min_age, max_age, (min_age, max_age))

min_usg = float(df["USG%"].min())
max_usg = float(df["USG%"].max())
usg_range = st.sidebar.slider("USG% range", float(min_usg), float(max_usg), (min_usg, max_usg))

min_ts = float(df["TS%"].min())
max_ts = float(df["TS%"].max())
ts_range = st.sidebar.slider("TS% range", float(min_ts), float(max_ts), (min_ts, max_ts))

filtered = df.copy()

# Map full team name back to code
if team_choice_full != "All":
    team_code = None
    for code, full in TEAM_FULL_NAME_MAP.items():
        if full == team_choice_full:
            team_code = code
            break
    if team_code:
        filtered = filtered[filtered["TEAM"] == team_code]

filtered = filtered[
    (filtered["AGE_INT"].between(age_range[0], age_range[1])) &
    (filtered["USG%"].between(usg_range[0], usg_range[1])) &
    (filtered["TS%"].between(ts_range[0], ts_range[1]))
]

# -----------------------------
# TABS
# -----------------------------
tab_team, tab_player, tab_league = st.tabs(["Team Overview", "Player Stats", "League Leaders"])

# -----------------------------
# TEAM OVERVIEW
# -----------------------------
with tab_team:
    st.header("Team Overview")

    if team_choice_full == "All":
        st.info("Select a specific team in the sidebar to see team overview.")
    else:
        team_code = None
        for code, full in TEAM_FULL_NAME_MAP.items():
            if full == team_choice_full:
                team_code = code
                break

        if not team_code:
            st.warning("Team mapping not found.")
        else:
            logo_url = get_team_logo_url(team_code)
            if logo_url:
                st.image(logo_url, width=150)

            team_df = df[df["TEAM"] == team_code].copy()
            if team_df.empty:
                st.warning("No players found for this team.")
            else:
                leaders = team_df.sort_values("PpG", ascending=False).reset_index(drop=True)
                leaders_display = leaders[
                    ["NAME", "POS", "GP", "MpG", "PpG", "RpG", "ApG", "SpG", "BpG", "2P%", "3P%"]
                ].copy()
                leaders_display.rename(
                    columns={
                        "PpG": "PPG",
                        "RpG": "RPG",
                        "ApG": "APG",
                        "SpG": "SPG",
                        "BpG": "BPG",
                        "2P%": "FG%",
                        "3P%": "3PT FG%",
                    },
                    inplace=True,
                )
                leaders_display.index = leaders_display.index + 1
                leaders_display.index.name = "Rank"

                top = leaders.iloc[0]
                st.metric("Leading Scorer", top["NAME"], f"{top['PpG']:.1f} PPG")

                st.subheader("Team Leaders (Per Game)")
                st.dataframe(
                    leaders_display.style.format({
                        "GP": "{:.0f}",
                        "MpG": "{:.1f}",
                        "PPG": "{:.1f}",
                        "RPG": "{:.1f}",
                        "APG": "{:.1f}",
                        "SPG": "{:.1f}",
                        "BPG": "{:.1f}",
                        "FG%": "{:.3f}",
                        "3PT FG%": "{:.3f}",
                    }),
                    use_container_width=True
                )

# -----------------------------
# PLAYER STATS
# -----------------------------
with tab_player:
    st.header("Player Stats")

    player_search = st.text_input("Search player by name")

    players_df = filtered.copy()
    if player_search.strip():
        players_df = players_df[players_df["NAME"].str.contains(player_search.strip(), case=False, na=False)]

    if players_df.empty:
        st.warning("No players match the current filters/search.")
    else:
        player_names = sorted(players_df["NAME"].unique().tolist())
        player_choice = st.selectbox("Select Player", player_names)

        player_row = players_df[players_df["NAME"] == player_choice].iloc[0]
        img_url = get_player_image_url(player_choice)

        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(img_url, width=180)
        with col2:
            st.markdown(f"## {player_choice}")
            st.markdown(f"**Team:** {player_row['TEAM_FULL']}")
            st.markdown(f"**Position:** {player_row['POS']}")
            st.markdown(f"**Age:** {int(player_row['AGE_INT'])}")
            st.markdown(f"**Games Played:** {int(player_row['GP'])}")
            st.markdown(f"**Minutes per Game:** {player_row['MpG']:.1f}")

        st.subheader("Key Per-Game Stats")
        fg_pct = player_row["2P%"] if pd.notna(player_row["2P%"]) else None
        three_pct = player_row["3P%"]

        k1, k2, k3, k4, k5, k6, k7 = st.columns(7)
        k1.metric("PPG", f"{player_row['PpG']:.1f}")
        k2.metric("APG", f"{player_row['ApG']:.1f}")
        k3.metric("RPG", f"{player_row['RpG']:.1f}")
        k4.metric("SPG", f"{player_row['SpG']:.1f}")
        k5.metric("BPG", f"{player_row['BpG']:.1f}")
        k6.metric("FG%", f"{fg_pct:.3f}" if fg_pct is not None else "N/A")
        k7.metric("3PT FG%", f"{three_pct:.3f}" if pd.notna(three_pct) else "N/A")

        st.subheader("Full Advanced Stat Line")
        stats_series = player_row.copy()
        stats_df = stats_series.to_frame().reset_index()
        stats_df.columns = ["Stat", "Value"]

        def fmt_value(row):
            stat = row["Stat"]
            val = row["Value"]
            if stat in numeric_cols and pd.notna(val):
                if stat.endswith("%"):
                    return f"{float(val):.3f}"
                else:
                    return f"{float(val):.1f}"
            return val

        stats_df["Value"] = stats_df.apply(fmt_value, axis=1)
        st.dataframe(stats_df, use_container_width=True)

# -----------------------------
# LEAGUE LEADERS
# -----------------------------
with tab_league:
    st.header("League Leaders — Top 20")

    metric_choice = st.selectbox(
        "Select leaderboard metric",
        [
            "Most Points Per Game",
            "Most Assists Per Game",
            "Most Rebounds Per Game",
            "Most Steals Per Game",
            "Most Blocks Per Game",
            "Best Field Goal Percentage",
            "Best 3-Point Percentage",
        ]
    )

    metric_map = {
        "Most Points Per Game": "PpG",
        "Most Assists Per Game": "ApG",
        "Most Rebounds Per Game": "RpG",
        "Most Steals Per Game": "SpG",
        "Most Blocks Per Game": "BpG",
        "Best Field Goal Percentage": "2P%",   # proxy FG%
        "Best 3-Point Percentage": "3P%",
    }
    metric_col = metric_map[metric_choice]

    leaders = df.sort_values(metric_col, ascending=False).head(20).copy()
    leaders_display = leaders[
        ["NAME", "TEAM_FULL", "POS", "GP", "MpG", "PpG", "RpG", "ApG", "SpG", "BpG", "2P%", "3P%", "TS%", "ORtg", "DRtg", "VI"]
    ]
    leaders_display.rename(
        columns={
            "TEAM_FULL": "Team",
            "PpG": "PPG",
            "RpG": "RPG",
            "ApG": "APG",
            "SpG": "SPG",
            "BpG": "BPG",
            "2P%": "FG%",
            "3P%": "3PT FG%",
        },
        inplace=True,
    )
    leaders_display.index = range(1, len(leaders_display) + 1)
    leaders_display.index.name = "Rank"

    st.dataframe(
        leaders_display.style.format({
            "GP": "{:.0f}",
            "MpG": "{:.1f}",
            "PPG": "{:.1f}",
            "RPG": "{:.1f}",
            "APG": "{:.1f}",
            "SPG": "{:.1f}",
            "BPG": "{:.1f}",
            "FG%": "{:.3f}",
            "3PT FG%": "{:.3f}",
            "TS%": "{:.3f}",
            "ORtg": "{:.1f}",
            "DRtg": "{:.1f}",
            "VI": "{:.1f}",
        }),
        use_container_width=True
    )