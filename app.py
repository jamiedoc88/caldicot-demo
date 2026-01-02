import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import urllib.parse

# --- CONFIGURATION ---
st.set_page_config(page_title="Caldicot Town Hub", page_icon="🏰", layout="wide")

# --- ASSETS ---
CALDICOT_LOGO = "https://i0.wp.com/caldicottownteam.co.uk/wp-content/uploads/2025/07/TRWS-Logo-01-e1753868910696.png?ssl=1"

# --- 1. SAFE CSS LOADER (No Triple Quotes) ---
# We build the style one line at a time to prevent Syntax Errors
css = []
css.append("<style>")
css.append("@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');")
css.append("html, body, [class*='css'] { font-family: 'Inter', sans-serif; }")
css.append(".ticket-card { background: white; border: 1px solid #e0e0e0; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 25px; overflow: hidden; }")
css.append(".card-flex { display: flex; flex-direction: row; height: 240px; }")
css.append(".card-img { width: 35%; background-size: cover; background-position: center; }")
css.append(".card-body { width: 65%; padding: 25px; display: flex; flex-direction: column; justify-content: center; }")
css.append("@media (max-width: 768px) { .card-flex { flex-direction: column; height: auto; } .card-img { width: 100%; height: 200px; } .card-body { width: 100%; padding: 20px; } }")
css.append(".date-badge { color: #d1410c; font-weight: 800; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }")
css.append(".event-title { color: #1a1a1a; font-size: 22px; font-weight: 800; line-
