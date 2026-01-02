import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import urllib.parse

# --- CONFIGURATION ---
st.set_page_config(page_title="What's On - Discover Inverclyde", layout="wide")

# --- BRAND ASSETS (Discover Inverclyde Style) ---
# We use the specific Teal/Navy palette found on their site
BRAND_TEAL = "#009BB9"  # The specific 'Discover' blue/cyan
BRAND_NAVY = "#1D2D3D"  # The dark footer/header color
BG_GRAY    = "#F4F6F7"  # The light background used in their sections

# Placeholder for the Logo (You would replace this with the actual Discover Inverclyde logo URL if you had rights)
LOGO = "https://i0.wp.com/caldicottownteam.co.uk/wp-content/uploads/2025/07/TRWS-Logo-01-e1753868910696.png?ssl=1" 

# --- CSS STYLES (Exact Replica) ---
s = []
s.append("<style>")
# 1. GLOBAL FONTS & RESETS
s.append("@import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;700;900&display=swap');")
s.append(f"html, body, [class*='css'] {{ font-family: 'Lato', sans-serif; color: {BRAND_NAVY}; }}")

# 2. HEADER / HERO SECTION (Matches the 'Events' page header)
s.append(".header-container {")
s.append(f"  background-color: {BRAND_NAVY};")
s.append("  padding: 40px 0;")
s.append("  margin-bottom: 40px;")
s.append("  text-align: center;")
s.append("}")
s.append(".header-title { color: white; font-size: 42px; font-weight: 900; margin: 0; text-transform: uppercase; letter-spacing: 1px; }")
s.append(".header-breadcrumb { color: #aaa; font-size: 14px; margin-top: 10px; }")

# 3. EVENT CARD (The 'Discover Inverclyde' Grid Style)
# Their cards are tall, white, with the image on top and a teal button at the bottom.
s.append(".discover-card {")
s.append("  background: white;")
s.append("  border: none;") # They don't use visible borders, just shadow
s.append("  box-shadow: 0 2px 15px rgba(0,0,0,0.05);")
s.append("  margin-bottom: 30px;")
s.append("  height: 100%;")
s.append("  display: flex; flex-direction: column;")
s.append("  transition: transform 0.2s;")
s.append("}")
s.append(".discover-card:hover { transform: translateY(-5px); }")

s.append(".card-img-top {")
s.append("  height: 220px; width: 100%;")
s.append("  background-size: cover; background-position: center;")
s.append("}")

s.append(".card-body { padding: 25px; flex-grow: 1; display: flex; flex-direction: column; }")

# Typography matches their site
s.append(f".event-date {{ color: {BRAND_TEAL}; font-weight: 700; font-size: 14px; margin-bottom: 5px; }}")
s.append(f".event-title {{ color: {BRAND_NAVY}; font-size: 20px; font-weight: 900; margin-bottom: 10px; line-height: 1.3; }}")
s.append(".event-loc {{ color: #777; font-size: 14px; margin-bottom: 20px; display: flex; align-items: center; gap: 5px; }}")

# The specific 'Read More' button style
s.append(".btn-discover {")
s.append(f"  background-color: {BRAND_TEAL}; color: white; text-decoration: none;")
s.append("  padding: 10px 20px; font-weight: 700; font-size: 14px;")
s.append("  text-transform: uppercase; letter-spacing: 1px;")
s.append("  display: inline-block; text-align: center; margin-top: auto;")
s.append("  transition: background 0.2s;")
s.append("}")
s.append(f".btn-discover:hover {{ background-color: {BRAND_NAVY}; color: white; }}")

# 4. SINGLE EVENT PAGE (Hero & Details)
s.append(".single-event-container { background: white; padding: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }")
s.append(".single-title { font-size: 32px; font-weight: 900; margin-bottom: 10px; }")
s.append(f".single-date {{ color: {BRAND_TEAL}; font-weight: 700; font-size: 18px; margin-bottom: 20px; }}")

# The 'Key Info' sidebar box style
s.append(".info-box {")
s.append(f"  background-color: {BG_GRAY};")
s.append("  padding: 30px;")
s.append(f"  border-left: 4px solid {BRAND_TEAL};")
s.append("}")
s.append(".info-label { font-weight: 900; font-size: 13px; text-transform: uppercase; color: #888; margin-bottom: 5px; }")
s.append(f".info-value {{ font-size: 16px; font-weight: 700; color: {BRAND_NAVY}; margin-bottom: 20px; }}")

s.append("</style>")
st.markdown("".join(s), unsafe_allow_html=True)

# --- DATA LOADING ---
SHEET_ID = "1hdx13h_0u9Yln-tmRoZu8d_DIkThoE801MP1S3ohXms"
base = "https://docs.google.com/spreadsheets/d/"
query = "/gviz/tq?tqx=out:csv&sheet=Events"
URL = base + SHEET_ID + query

@st.cache_data(ttl=10)
def load_data():
    try:
        df = pd.read_csv(URL)
        df.columns = df.columns.str.strip()
        req = ['Image_URL', 'Description', 'Event', 'Date', 'Type', 'Lat', 'Lon']
        for c in req:
            if c not in df.columns: df[c] = ""
        df['Image_URL'] = df['Image_URL'].fillna(LOGO)
        df['Description'] = df['Description'].fillna("No details provided.")
        df['Date_Obj'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Lat'] = pd.to_numeric(df['Lat'], errors='coerce')
        df['Lon'] = pd.to_numeric(df['Lon'], errors='coerce')
        df = df.dropna(subset=['Lat', 'Lon'])
        return df
    except:
        return pd.DataFrame()

df = load_data()

# --- HELPER ---
def get_date_str(d):
    if pd.isna(d): return "Upcoming Date"
    return d.strftime("%d.%m.%Y") # Format matches '14.02.2026' style from site

# --- HEADER SECTION (Replicates the dark navy banner) ---
st.markdown("""
<div class="header-container">
    <div class="header-title">What's On</div>
    <div class="header-breadcrumb">Home • What's On • Events</div>
</div>
""", unsafe_allow_html=True)

# --- MAIN CONTENT ---
if df.empty:
    st.error("Unable to connect to Google Sheet.")
else:
    
    # 1. FILTER BAR (Matches the pill buttons style)
    # We use columns to make it look like a top bar
    c1, c2 = st.columns([3, 1])
    with c1:
        st.write("") # Spacer
    with c2:
        if 'Type' in df.columns:
            opts = ["All Categories"] + list(df['Type'].unique())
            sel = st.selectbox("Filter Events", opts, label_visibility="collapsed")
            if sel != "All Categories": df = df[df['Type'] == sel]

    tab1, tab2 = st.tabs(["List View", "Map View"])

    # --- LIST VIEW (Grid Layout) ---
    with tab1:
        # We create a grid using Streamlit columns
        # We loop through data in chunks of 3 for a 3-column grid
        for i in range(0, len(df), 3):
            cols = st.columns(3)
            # Inner loop for the 3 items
            for j in range(3):
                if i + j < len(df):
                    row = df.iloc[i + j]
                    
                    with cols[j]:
                        date_str = get_date_str(row['Date_Obj'])
                        img = str(row['Image_URL'])
                        if len(img) < 5: img = LOGO
                        
                        # --- DISCOVER CARD HTML ---
                        # Exact replica of the card structure
                        html = []
                        html.append('<div class="discover-card">')
                        html.append(f'  <div class="card-img-top" style="background-image: url(\'{img}\');"></div>')
                        html.append('  <div class="card-body">')
                        html.append(f'    <div class="event-date">{date_str}</div>')
                        html.append(f'    <div class="event-title">{row["Event"]}</div>')
                        html.append(f'    <div class="event-loc">📍 Greenock / Inverclyde</div>')
                        html.append('    <div style="margin-top:auto;">') # Pushes button to bottom
                        # We use a fake button visual that doesn't actually link yet
                        html.append('      <span class="btn-discover">Read More</span>') 
                        html.append('    </div>')
                        html.append('  </div>')
                        html.append('</div>')
                        st.markdown("".join(html), unsafe_allow_html=True)
                        
                        # --- INTERACTION ---
                        # We put the expander invisible "under" the card logic
                        with st.expander(f"View Details:
