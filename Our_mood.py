import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime
import json

# Set up the scope and authorize credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

# Load credentials from Streamlit Secrets
creds_dict = json.loads(st.secrets["google_sheets"])

credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)

# Open the spreadsheet and worksheet
spreadsheet_name = "colourapp"
worksheet_name = "Sheet1"
sheet = client.open(spreadsheet_name).worksheet(worksheet_name)

# App Title
st.title("Our Mood Tracker")

# Input fields
name = st.text_input("Your name:")
date = st.date_input("Date:", datetime.today())
mood = st.slider("Rate your mood (1-10):", 1, 10, 5)
comment = st.text_area("Additional comments:")

# Submit button
if st.button("Submit"):
    # Save data to Google Sheet
    new_row = [str(date), name, mood, comment]
    sheet.append_row(new_row)
    st.success("Your mood has been saved!")

# Display current data
st.subheader("Mood History")
data = sheet.get_all_values()
headers = data.pop(0)  # Remove the header row
df = pd.DataFrame(data, columns=headers)
st.dataframe(df)

