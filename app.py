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

# --- 🎨 SAFE CSS DEFINITION ---
# We define the style here as a variable to prevent Syntax Errors
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* Card Styling */
    .ticket-card { background-color: white; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); border: 1px solid #f0f0f0; margin-bottom: 25px; overflow: hidden; }
    
    /* Responsive Flexbox */
    .card-content { display: flex; flex-direction: row; }
    @media (max-width: 768px) { 
        .card-content { flex-direction: column; } 
        .card-image { width: 100% !important; height: 200px !important; } 
        .card-details { width: 100% !important; } 
    }
    
    .card-image { width: 35%; min-height: 220px; background-size: cover; background-position: center; }
    .card-details { padding: 25px; width: 65%; display: flex; flex-direction: column; justify-content: center; }
    
    /* Text Styling */
    .date-badge { color: #d1410c; font-weight: 700; font-size: 14px; margin-bottom: 8px; }
    .event-title { font-size: 22px; font-weight: 800; color: #1a1a1a; margin-bottom: 10px; }
    .category-pill { background-color: #f2f2f2; color: #555; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }
    .event-meta { color: #666; font-size: 14px; margin-top: 10px; }
    
    /* Interactive Elements */
    .read-more-box { background: #f9f9f9; padding: 20px; border-top: 1px solid #eee; }
    .share-row { margin-top: 15px; display: flex; gap: 10px; }
    .share-icon { text-decoration: none; color: #555; border: 1px solid #ddd; padding: 5px 10px; border-radius: 5px; font-size: 12px; }
</style>
"""

# Inject the CSS safely
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.image(CALDICOT_LOGO, width=150)
st.sidebar.markdown("### 🏰 Explore Caldicot")

# --- DATA LOADING ---
SHEET_ID = "1hdx13h_0u9Yln-tmRoZu8d_DIkThoE801MP1S3ohXms"
# Safe URL construction
base_url = "https://docs.google.com/spreadsheets/d/"
query = "/gviz/tq?tqx=out:csv&sheet=Events"
SHEET_URL = base_url + SHEET_ID + query

@st.cache_data(ttl=10)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip()
        
        required = ['Image_URL', 'Description', 'Event', 'Date', 'Type', 'Lat', 'Lon']
        for col in required:
            if col not in df.columns: df[col] = ""
            
        df['Image_URL'] = df['Image_URL'].fillna(CALDICOT_LOGO)
        df['Description'] = df['Description'].fillna("Details coming soon.")
        
        # Parse Dates
        df['Date_Obj'] = pd.to_datetime(df['Date'], errors='coerce')
        
        # Parse Coords
        df['Lat'] = pd.to_numeric(df['Lat'], errors='coerce')
        df['Lon'] = pd.to_numeric(df['Lon'], errors='coerce')
        df = df.dropna(subset=['Lat', 'Lon'])
        
        return df
    except Exception:
        return pd.DataFrame()

df = load_data()

# --- DATE HELPER ---
def get_date_strings(date_obj):
    if pd.isna(date_obj): return "UPCOMING", "DATE", "Soon"
    return date_obj.strftime("%b").upper(), date_obj.strftime("%d"), date_obj.strftime("%a")

# --- MAIN APP ---
st.title("What's On in Caldicot")

if df.empty:
    st.warning("Loading events...")
else:
    # FILTERS
    if 'Type' in df.columns:
        all_types = ["All Events"] + list(df['Type'].unique())
        cat_filter = st.sidebar.selectbox("Category", all_types)
        if cat_filter != "All Events":
            df = df[df['Type'] == cat_filter]

    tab1, tab2 = st.tabs(["🎫 Event Feed", "🗺️ Interactive Map"])

    # --- TAB 1: FEED ---
    with tab1:
        for index, row in df.iterrows():
            month, day, weekday = get_date_strings(row['Date_Obj'])
            img_url = row['Image_URL']
            if len(str(img_url)) < 5: img_url = CALDICOT_LOGO
            
            # --- CARD HTML ---
            # Using simple string concatenation to avoid F-String/Syntax Errors
            html = '<div class="ticket-card"><div class="card-content">'
            html += '<div class="card-image" style="background-image: url(\'' + str(img_url) + '\');"></div>'
            html += '<div class="card-details">'
            html += '<div class="date-badge">' + str(weekday) + ', ' + str(month) + ' ' + str(day) + '</div>'
            html += '<div class="event-title">' + str(row["Event"]) + '</div>'
            html += '<div><span class="category-pill
