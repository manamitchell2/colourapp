import streamlit as st
import pandas as pd
import os
from datetime import date

DATA_FILE = "mood_ratings.csv"

def calculate_color(anxiety, mood, productivity, energy):
    # Weight higher values more strongly by squaring
    a = (anxiety / 10) ** 2
    m = (mood / 10) ** 2
    p = (productivity / 10) ** 2
    e = (energy / 10) ** 2

    # Red reflects anxiety strongly
    red = min(int(255 * a), 255)
    # Green reflects mood, productivity, energy combined positively
    green = min(int(255 * (m * 0.6 + p * 0.2 + e * 0.2)), 255)
    # Blue is less dominant, influenced by productivity and energy
    blue = min(int(255 * (p * 0.5 + e * 0.5)), 255)

    return (red, green, blue)

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def save_rating(data):
    if os.path.exists(DATA_FILE):
        df_existing = pd.read_csv(DATA_FILE)
        df = pd.concat([df_existing, pd.DataFrame([data])], ignore_index=True)
    else:
        df = pd.DataFrame([data])
    df.to_csv(DATA_FILE, index=False)

def load_ratings():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame()

st.title("Our Mood Tracker")

anxiety = st.number_input("Anxiety (1.0 - 10.0)", min_value=1.0, max_value=10.0, step=0.1, format="%.1f")
mood = st.number_input("Mood (1.0 - 10.0)", min_value=1.0, max_value=10.0, step=0.1, format="%.1f")
productivity = st.number_input("Productivity (1.0 - 10.0)", min_value=1.0, max_value=10.0, step=0.1, format="%.1f")
energy = st.number_input("Energy (1.0 - 10.0)", min_value=1.0, max_value=10.0, step=0.1, format="%.1f")

if st.button("Save Rating"):
    rgb = calculate_color(anxiety, mood, productivity, energy)
    data = {
        "date": str(date.today()),
        "anxiety": anxiety,
        "mood": mood,
        "productivity": productivity,
        "energy": energy,
        "rgb": f"RGB{rgb}",
        "hex_color": rgb_to_hex(rgb)
    }
    save_rating(data)
    st.success(f"Saved with color {data['rgb']}")

st.write("### Past Ratings")

ratings_df = load_ratings()
if ratings_df.empty:
    st.write("No ratings saved yet.")
else:
    # Display colored box for each row
    def color_row(row):
        return [f"background-color: {row['hex_color']}"] * len(row)

    # Show the table with color backgrounds for rows
    styled_df = ratings_df.style.apply(color_row, axis=1)
    st.dataframe(styled_df, height=300)

    # Also show the raw data table with RGB codes
    st.write(ratings_df[["date", "anxiety", "mood", "productivity", "energy", "rgb"]])
