import streamlit as st
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# Set page config
st.set_page_config(page_title="Colour Tracker", page_icon="🎨")

st.title("🎨 Colour Tracker")

# Load Google Sheets credentials from Streamlit secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["google_sheets"]

credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)

# Open the spreadsheet and select the sheet
spreadsheet = client.open("colourapp")
sheet = spreadsheet.sheet1

# Form to add a new colour
with st.form("colour_form"):
    name = st.radio("Who is this for?", ["Emily", "Mana"])
    colour = st.color_picker("Pick a colour")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    submitted = st.form_submit_button("Add Colour")

    if submitted:
        # Append to Google Sheets
        sheet.append_row([name, colour, date])
        st.success(f"Colour saved for {name}!")

# Load all saved colours
records = sheet.get_all_records()

# Filter records
emily_colours = [r["Colour"] for r in records if r["Name"] == "Emily"]
mana_colours = [r["Colour"] for r in records if r["Name"] == "Mana"]

st.header("🎨 Emily's Colours")
if emily_colours:
    for col in emily_colours:
        st.markdown(f"<div style='background-color:{col};height:30px;width:100%;border-radius:5px;margin-bottom:5px'></div>", unsafe_allow_html=True)
else:
    st.write("No colours saved yet.")

st.header("🎨 Mana's Colours")
if mana_colours:
    for col in mana_colours:
        st.markdown(f"<div style='background-color:{col};height:30px;width:100%;border-radius:5px;margin-bottom:5px'></div>", unsafe_allow_html=True)
else:
    st.write("No colours saved yet.")
