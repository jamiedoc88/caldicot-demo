import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import urllib.parse
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="Caldicot Town Hub", page_icon="🏰", layout="wide")

# --- 🔗 ASSETS ---
CALDICOT_LOGO = "https://i0.wp.com/caldicottownteam.co.uk/wp-content/uploads/2025/07/TRWS-Logo-01-e1753868910696.png?ssl=1"

# --- 🎨 SAFE CSS (Compressed to prevent errors) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .ticket-card { background-color: white; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); border: 1px solid #f0f0f0; margin-bottom: 25px; overflow: hidden; }
    .card-content { display: flex; flex-direction: row; }
    @media (max-width: 768px) { .card-content { flex-direction: column; } .card-image { width: 100% !important; height: 200px !important; } .card-details { width: 100% !important; } }
    .card-image { width: 35%; min-height: 220px; background-size: cover; background-position: center; }
    .card-details { padding: 25px; width: 65%; display: flex; flex-direction: column; justify-content: center; }
    .date-badge { color: #d1410c; font-weight: 700; font-size: 14px; margin-bottom: 8px; }
    .event-title { font-size: 22px; font-weight: 800; color: #1a1a1a; margin-bottom: 10px; }
    .category-pill { background-color: #f2f2f2; color: #555; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }
    .event-meta { color: #666; font-size: 14px; margin-top: 10px; }
    .read-more-box { background: #f9f9f9; padding: 20px; border-top: 1px solid #eee; }
    .share-row { margin-top: 15px; display: flex; gap: 10px; }
    .share-icon { text-decoration: none; color: #555; border: 1px solid #ddd; padding: 5px 10px; border-radius: 5px; font-size: 12px; }
</style>
""", unsafe_allow_html=
