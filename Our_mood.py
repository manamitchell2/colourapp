import streamlit as st
import json
from google.oauth2.service_account import Credentials
import gspread
from datetime import datetime

# Define your Google Sheets scope
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Load credentials from Streamlit secrets (as JSON string)
creds_dict = json.loads(st.secrets["GCP_SERVICE_ACCOUNT"])

# Create credentials object from dict
creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)

# Authorize gspread client
gc = gspread.authorize(creds)

# Open your Google Sheet by name
SPREADSHEET_NAME = "colourapp"
WORKSHEET_NAME = "Sheet1"
sh = gc.open(SPREADSHEET_NAME)
worksheet = sh.worksheet(WORKSHEET_NAME)

# --- Streamlit UI ---
st.title("Colour Mood Tracker")

# Choose your name
user = st.selectbox("Select your name", ["Emily", "Mana"])

# Pick your colour (any format you want, here a simple text input)
colour = st.color_picker("Pick a colour")

# Show today's date (auto-filled)
date_str = datetime.today().strftime('%Y-%m-%d')

if st.button("Save entry"):
    # Append the data as a new row: [name, colour, date]
    worksheet.append_row([user, colour, date_str])
    st.success("Entry saved!")

# --- Display saved data for each user separately ---
st.header("Entries by Emily")
try:
    all_values = worksheet.get_all_values()  # list of lists
except Exception as e:
    st.error(f"Error loading data from Google Sheets: {e}")
    all_values = []

if all_values:
    # Assuming first row is headers
    headers = all_values[0]
    data_rows = all_values[1:]

    # Filter rows by user
    emily_rows = [row for row in data_rows if row[0] == "Emily"]
    mana_rows = [row for row in data_rows if row[0] == "Mana"]

    # Display Emily's entries
    if emily_rows:
        for r in emily_rows:
            st.write(f"Colour: {r[1]} on {r[2]}")
    else:
        st.write("No entries yet.")

    st.header("Entries by Mana")
    # Display Mana's entries
    if mana_rows:
        for r in mana_rows:
            st.write(f"Colour: {r[1]} on {r[2]}")
    else:
        st.write("No entries yet.")
else:
    st.write("No data found in the sheet yet.")
