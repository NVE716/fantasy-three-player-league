import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime
# Minor update to trigger gitdewdwdwwdwdw

# ----------------------------
# Google Sheets setup
# ----------------------------
SHEET_NAME = "3 Man League test"
##SERVICE_ACCOUNT_FILE = "effective-fire-480702-m7-bfed8322b65c.json"
credentials_info = st.secrets["gcp_service_account"]


scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, scope)
#
##credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
client = gspread.authorize(credentials)
#sdxsxs
sheet = client.open(SHEET_NAME)

# ----------------------------
# Players sheet
# ----------------------------
players_ws = sheet.worksheet("Players")
players_df = pd.DataFrame(players_ws.get_all_records())

# Make sure column names are consistent
players_df.columns = players_df.columns.str.strip().str.lower()

##player_team = players_df.loc[players_df["player"] == selected_player, "team"].values[0]
# ----------------------------
# Schedule sheet
# ----------------------------
schedule_ws = sheet.worksheet("Schedule")
schedule_data = schedule_ws.get_all_values()
schedule_df = pd.DataFrame(schedule_data)

# Skip header row and get team names
teams = schedule_df.iloc[1:, 0].dropna().tolist()

# ----------------------------
# Picks sheet
# ----------------------------
picks_ws = sheet.worksheet("Picks")
picks_data = picks_ws.get_all_values()
if len(picks_data) <= 1:  # only headers or empty
    picks_df = pd.DataFrame(columns=["timestamp", "week", "user", "position", "player", "team"])
else:
    picks_df = pd.DataFrame(picks_ws.get_all_records())
    picks_df.columns = picks_df.columns.str.strip().str.lower()

# ----------------------------
# Streamlit UI
# ----------------------------
st.title("3 Man League Draft")

# Select your team
selected_team = st.selectbox("Select your name", teams)

# Select position
positions = sorted(players_df["position"].dropna().unique())
selected_position = st.selectbox("Select position", positions)

# Available players for this position
available_players = players_df[players_df["position"] == selected_position]["player"].tolist()

if available_players:
    selected_player = st.selectbox("Select a player to draft", available_players)

    if st.button("Confirm Pick"):
        player_team = players_df.loc[players_df["player"] == selected_player, "team"].values[0]
        # Append pick to Picks sheet
        new_pick = [datetime.now().isoformat(), 1, selected_team, selected_position, selected_player,player_team ]
        picks_ws.append_row(new_pick)
        st.success(f"{selected_player} drafted for {selected_team}!")
else:
    st.info("No available players for this position.")
