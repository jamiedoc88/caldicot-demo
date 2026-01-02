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

# --- 🎨 MODERN UI (SAFE CSS) ---
# We define CSS as a simple string to avoid Syntax Errors
css_code = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* CARD CONTAINER */
    .ticket-card {
        background-color: white;
        border-radius: 12px;
        padding: 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border: 1px solid #f0f0f0;
        margin-bottom: 25px;
        overflow: hidden; 
    }
    .ticket-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.12);
    }

    /* LAYOUT */
    .card-content {
        display: flex;
        flex-direction: row;
        align-items: stretch;
    }
    
    /* MOBILE RESPONSIVENESS */
    @media (max-width: 768px) {
        .card-content { flex-direction: column; }
        .card-image { width: 100% !important; height: 200px !important; }
        .card-details { width: 100% !important; }
    }

    /* IMAGE STYLING */
    .card-image {
        width: 35%;
        min-height: 220px;
        background-size: cover;
        background-position: center;
        position: relative;
    }

    /* CONTENT SIDE */
    .card-details {
        padding: 25px;
        width: 65%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    /* DATE BADGE */
    .date-badge {
        display: inline-block;
        color: #d1410c; 
        font-weight: 700;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }

    /* TITLE */
    .event-title {
        font-size: 22px;
        font-weight: 800;
        color: #1a1a1a;
        margin: 0 0 10px 0;
        line-height: 1.3;
    }

    /* CATEGORY PILL */
    .category-pill {
        display: inline-block;
        background-color: #f2f2f2;
        color: #555;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 15px;
    }

    /* METADATA */
    .event-meta {
        color: #666;
        font-size: 14px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* SHARE BUTTONS */
    .share-row { margin-top: 15px; display: flex; gap: 10px; }
    .share-icon {
        text-decoration: none;
        color: #555;
        font-size: 12px;
        font-weight: 600;
        padding: 6px 12px;
        border: 1px solid #ddd;
        border-radius: 6px;
        transition: all 0.2s;
    }
    .share-icon:hover { background-color: #f7f7f7; border-color: #aaa; color: #333; }

    /* READ MORE BOX */
    .read-more-box {
        background: #f9f9f9;
        padding: 20px;
        border-top: 1px solid #eee;
        font-size: 15px;
        line-height: 1.6;
        color: #333;
    }
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# --- SIDEBAR & SETUP ---
st.sidebar.image(CALDICOT_LOGO, width=150)
st.sidebar.markdown("### 🏰 Explore Caldicot")
st.sidebar.info("Use the filters to find markets, events, and festivals.")

# --- DATA LOADING ---
SHEET_ID = "1hdx13h_0u9Yln-tmRoZu8d_DIkThoE801MP1S3ohXms"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Events"

@st.cache_data(ttl=10)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip()
        
        # Robustness checks
        required = ['Image_URL', 'Description', 'Event', 'Date', 'Type', 'Lat', 'Lon']
        for col in required:
            if col not in df.columns: df[col] = ""
            
        df['Image_URL'] = df['Image_URL'].fillna(CALDICOT_LOGO)
        df['Description'] = df['Description'].fillna("Details coming soon.")
        
        # Parse Dates safely
        df['Date_Obj'] = pd.to_datetime(df['Date'], errors='coerce')
        
        # Numeric Coords safely
        df['Lat'] = pd.to_numeric(df['Lat'], errors='coerce')
        df['Lon'] = pd.to_numeric(df['Lon'], errors='coerce')
        df = df.dropna(subset=['Lat', 'Lon'])
        
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data()

# --- HELPER: FORMAT DATE ---
def get_date_strings(date_obj):
    if pd.isna(date_obj): return "UPCOMING", "DATE", "Soon"
    return date_obj.strftime("%b").upper(), date_obj.strftime("%d"), date_obj.strftime("%a")

# --- MAIN APP ---
st.title("What's On in Caldicot")
st.markdown("Discover the latest markets, festivals, and community gatherings.")

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

    # --- TAB 1: THE TICKETMASTER FEED ---
    with tab1:
        for index, row in df.iterrows():
            month, day, weekday = get_date_strings(row['Date_Obj'])
            img_url = row['Image
