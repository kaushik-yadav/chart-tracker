import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import datetime
import json
import os

# Page Config
st.set_page_config(
    page_title="Immunity Pattern Viewer",
    page_icon="🧬",
    layout="centered"
)

# Hide Streamlit header & footer
hide_streamlit_style = """
  <style> header {visibility: hidden;} footer {visibility: hidden;} [data-testid="stToolbar"] {display: none;} [data-testid="stDecoration"] {display: none;} [data-testid="stStatusWidget"] {display: none;} [data-testid="stHeader"] {display: none; height: 0;} [class*="st-emotion-cache"] {display: none;} [class^="st-emotion-cache"] {display: none;} [class$="st-emotion-cache"] {display: none;} [class*="^st-emotion-cache"] * {display: none;} [data-testid="stElementContainer"] {display: visible;} div.block-container {padding-top: 0;} </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Data
days = np.arange(1, 23)
immunity = [
    85, 82, 80, 78, 70, 60, 45, 30, 25, 25, 30,
    35, 45, 55, 65, 70, 75, 80, 85, 88, 90, 92
]
base_date = datetime.date(2025, 11, 1)
num_days = len(immunity)
CACHE_FILE = "user_cache.json"

# Local Cache Handling
def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_cache(data):
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f)

cache_data = load_cache()

# Get or Create Browser ID
from streamlit_javascript import st_javascript

browser_id = st_javascript(
    """(function() {
        let id = localStorage.getItem("browser_id");
        if (!id) {
            id = self.crypto.randomUUID();
            localStorage.setItem("browser_id", id);
        }
        return id;
    })();"""
)

if browser_id not in cache_data:
    cache_data[browser_id] = {"last_date": base_date.isoformat()}
    save_cache(cache_data)

# UI
st.title("🧬 R-CHOP Immunity")
st.write("Select your chemotherapy start date.")

last_date = datetime.date.fromisoformat(cache_data[browser_id]["last_date"])

selected_date = st.date_input(
    "📅 Choose chemo start date:",
    value=last_date,
    min_value=base_date - datetime.timedelta(days=365),
    max_value=base_date + datetime.timedelta(days=365)
)

# Update browser-specific cache
if selected_date != last_date:
    cache_data[browser_id]["last_date"] = selected_date.isoformat()
    save_cache(cache_data)

# Generate Dates
date_labels = [(selected_date + datetime.timedelta(days=i)).strftime("%b %d") for i in range(num_days)]

# Determine if today's line should appear
today = datetime.date.today()
cycle_start = selected_date
cycle_end = selected_date + datetime.timedelta(days=num_days - 1)
show_today = cycle_start <= today <= cycle_end

# Plot
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(date_labels, immunity, marker='o', linewidth=2, color="#4B8BBE")

if show_today:
    red_line_index = (today - selected_date).days
    ax.axvline(date_labels[red_line_index], color='red', linestyle='--', label="Today")

ax.set_facecolor("#FAFAFA")
ax.set_xlabel("Date", fontsize=10)
ax.set_ylabel("Relative Immunity Level (0–100)", fontsize=10)
ax.set_title("R-CHOP Immunity Pattern (Aligned with Your Cycle)", fontsize=13, weight="bold")
if show_today:
    ax.legend()
ax.grid(True, linestyle='--', alpha=0.5)
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)
