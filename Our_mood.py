import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Google Sheets setup
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS_FILE = "creds.json"  # Make sure this file is uploaded to Streamlit Cloud

# Authenticate and initialize client
creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Open your sheet by name
SPREADSHEET_NAME = "colourapp"
WORKSHEET_NAME = "Sheet1"

sheet = client.open(SPREADSHEET_NAME).worksheet(WORKSHEET_NAME)

# Streamlit app UI
st.title("Mood Tracker")

# Select user
user = st.selectbox("Who is logging their mood?", ["Emily", "Mana"])

# Input fields
mood = st.slider("Mood (1-10)", 1, 10, 5)
anxiety = st.slider("Anxiety (1-10)", 1, 10, 5)
productivity = st.slider("Productivity (1-10)", 1, 10, 5)

if st.button("Submit"):

    # Timestamp
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Append data row: [name, mood, anxiety, productivity, datetime]
    row = [user, str(mood), str(anxiety), str(productivity), now]

    try:
        sheet.append_row(row)
        st.success("Data saved successfully!")
    except Exception as e:
        st.error(f"Failed to save data: {e}")

# Display last 5 entries for each user
st.header("Recent entries")

def get_recent_entries(name):
    try:
        data = sheet.get_all_records()
        user_entries = [entry for entry in data if entry['name'] == name]
        return user_entries[-5:]  # Last 5 entries
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        return []

cols = st.columns(2)
with cols[0]:
    st.subheader("Emily")
    for entry in get_recent_entries("Emily"):
        st.write(f"{entry['date']} — Mood: {entry['mood']}, Anxiety: {entry['anxiety']}, Productivity: {entry['productivity']}")

with cols[1]:
    st.subheader("Mana")
    for entry in get_recent_entries("Mana"):
        st.write(f"{entry['date']} — Mood: {entry['mood']}, Anxiety: {entry['anxiety']}, Productivity: {entry['productivity']}")
