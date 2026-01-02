import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import urllib.parse

# --- CONFIGURATION ---
st.set_page_config(page_title="What's On - Discover Inverclyde", layout="wide")

# --- BRAND COLORS (Discover Inverclyde Palette) ---
BRAND_TEAL = "#009BB9"
BRAND_NAVY = "#1D2D3D"
BG_GRAY = "#F4F6F7"
LOGO = "https://i0.wp.com/caldicottownteam.co.uk/wp-content/uploads/2025/07/TRWS-Logo-01-e1753868910696.png?ssl=1"

# --- CSS STYLES ---
# We use a simple join to prevent syntax errors with long strings
s = []
s.append("<style>")
s.append("@import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;700;900&display=swap');")
s.append("html, body, [class*='css'] { font-family: 'Lato', sans-serif; color: " + BRAND_NAVY + "; }")

# HEADER
s.append(".header-container { background-color: " + BRAND_NAVY + "; padding: 40px 0; margin-bottom: 40px; text-align: center; }")
s.append(".header-title { color: white; font-size: 42px; font-weight: 900; margin: 0; text-transform: uppercase; letter-spacing: 1px; }")
s.append(".header-breadcrumb { color: #aaa; font-size: 14px; margin-top: 10px; }")

# CARDS
s.append(".discover-card { background: white; box-shadow: 0 2px 15px rgba(0,0,0,0.05); margin-bottom: 30px; height: 100%; display: flex; flex-direction: column; }")
s.append(".card-img-top { height: 220px; width: 100%; background-size: cover; background-position: center; }")
s.append(".card-body { padding: 25px; flex-grow: 1; display: flex; flex-direction: column; }")

# TEXT
s.append(".event-date { color: " + BRAND_TEAL + "; font-weight: 700; font-size: 14px; margin-bottom: 5px; }")
s.append(".event-title { color: " + BRAND_NAVY + "; font-size: 20px; font-weight: 900; margin-bottom: 10px; line-height: 1.3; }")
s.append(".event-loc { color: #777; font-size: 14px; margin-bottom: 20
