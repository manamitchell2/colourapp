import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Use the creds dict directly from secrets
creds_dict = dict(st.secrets["GCP_SERVICE_ACCOUNT"])

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)

# Connect to Google Sheets
client = gspread.authorize(creds)
sheet = client.open("colourapp").worksheet("Sheet1")

st.title("Mood & Colour Tracker")

# Select your name (you and your partner)
name = st.selectbox("Select your name:", ["Emily", "Mana"])

colour = st.color_picker("Pick a colour representing your mood")

if st.button("Save Entry"):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Append the entry as a new row: [name, colour, date]
    sheet.append_row([name, colour, now_str])
    st.success(f"Saved {name}'s mood colour!")

# Show last 10 entries
st.subheader("Recent entries")
data = sheet.get_all_records()
if data:
    for row in data[-10:]:
        st.write(f"{row['name']} picked {row['colour']} on {row['date']}")
else:
    st.write("No entries yet.")
