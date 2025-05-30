import streamlit as st
import json
from google.oauth2.service_account import Credentials
import gspread
from datetime import datetime

# Google Sheets API scope
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Load creds from Streamlit secrets (stored as JSON string)
creds_dict = json.loads(st.secrets["GCP_SERVICE_ACCOUNT"])

# Create credentials object from in-memory dict
creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)

# Authorize gspread client
gc = gspread.authorize(creds)

# Open your spreadsheet and worksheet
SPREADSHEET_NAME = "colourapp"
WORKSHEET_NAME = "Sheet1"

sh = gc.open(SPREADSHEET_NAME)
worksheet = sh.worksheet(WORKSHEET_NAME)

st.title("Colour Mood Tracker")

# User input form
with st.form("entry_form"):
    name = st.selectbox("Who is logging?", ["Emily", "Mana"])
    colour = st.color_picker("Pick your colour")
    submitted = st.form_submit_button("Submit")

if submitted:
    # Prepare new row data: [name, colour, date]
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = [name, colour, date_str]

    # Append the new row to the sheet
    worksheet.append_row(new_row)

    st.success(f"Entry saved: {name} - {colour} at {date_str}")

# Show last 10 entries sorted by date descending
data = worksheet.get_all_records()
if data:
    # Sort entries by date descending
    data_sorted = sorted(data, key=lambda x: x['date'], reverse=True)
    recent = data_sorted[:10]

    st.subheader("Recent entries")
    for entry in recent:
        st.markdown(f"**{entry['name']}** picked color {entry['colour']} at {entry['date']}")
else:
    st.info("No entries yet.")

