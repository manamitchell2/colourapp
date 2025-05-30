import streamlit as st
import datetime
import json
import os

st.set_page_config(page_title="Mood Tracker", layout="centered")
st.title("Mood Tracker")

# --- Select user from dropdown ---
user = st.selectbox("Select user", ["Mana", "Emily"])
st.markdown(f"**Current user: {user}**")

# --- Load or initialize data ---
data_file = "mood_data.json"

if os.path.exists(data_file):
    with open(data_file, "r") as f:
        all_data = json.load(f)
else:
    all_data = {}

if user not in all_data:
    all_data[user] = []

# --- Input fields ---
with st.form("mood_form"):
    st.markdown(f"### Enter today's ratings for {user}")
    anxiety = st.number_input("Anxiety", min_value=1.0, max_value=10.0, step=0.1, format="%.1f")
    mood = st.number_input("Mood", min_value=1.0, max_value=10.0, step=0.1, format="%.1f")
    productivity = st.number_input("Productivity", min_value=1.0, max_value=10.0, step=0.1, format="%.1f")
    energy = st.number_input("Energy", min_value=1.0, max_value=10.0, step=0.1, format="%.1f")
    submitted = st.form_submit_button("Submit")

# --- Colour conversion with weighted emphasis ---
def to_rgb(anxiety, mood, productivity):
    def emphasize(value):
        # Exponential scaling to emphasize high values
        return int((value / 10) ** 2 * 255)
    r = emphasize(anxiety)
    g = emphasize(mood)
    b = emphasize(productivity)
    return (r, g, b)

# --- Save entry if submitted ---
if submitted:
    color = to_rgb(anxiety, mood, productivity)
    entry = {
        "date": str(datetime.date.today()),
        "anxiety": anxiety,
        "mood": mood,
        "productivity": productivity,
        "energy": energy,
        "color": color
    }
    all_data[user].append(entry)

    # Save to file
    with open(data_file, "w") as f:
        json.dump(all_data, f, indent=4)

    st.success(f"Rating saved for {user}!")

# --- Show saved history for both users ---
st.markdown("## Rating History")

cols = st.columns(2)
for idx, name in enumerate(["Mana", "Emily"]):
    cols[idx].markdown(f"### {name}")
    if name in all_data and all_data[name]:
        for entry in reversed(all_data[name]):
            color = entry["color"]
            r, g, b = color
            box_color = f"rgb({r}, {g}, {b})"
            cols[idx].markdown(
                f"<div style='background-color:{box_color}; padding:10px; border-radius:8px; color:black; margin-bottom:10px;'>"
                f"<b>{entry['date']}</b><br>"
                f"Anxiety: {entry['anxiety']}<br>"
                f"Mood: {entry['mood']}<br>"
                f"Productivity: {entry['productivity']}<br>"
                f"Energy: {entry['energy']}<br>"
                f"RGB: {color}"
                f"</div>",
                unsafe_allow_html=True,
            )
    else:
        cols[idx].info("No data yet.")
