import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import urllib.parse

# --- CONFIGURATION ---
st.set_page_config(page_title="What's On", layout="wide")

# --- BRAND COLORS ---
TEAL = "#009BB9"
NAVY = "#1D2D3D"
GRAY = "#F4F6F7"
LOGO = "https://i0.wp.com/caldicottownteam.co.uk/wp-content/uploads/2025/07/TRWS-Logo-01-e1753868910696.png?ssl=1"

# --- CSS STYLES (Vertical Safe Mode) ---
# We build the style list line-by-line to prevent copy-paste errors
s = []
s.append("<style>")

# 1. Fonts
s.append("@import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;700;900&display=swap');")
s.append("html, body, [class*='css'] {")
s.append("  font-family: 'Lato', sans-serif;")
s.append(f"  color: {NAVY};")
s.append("}")

# 2. Header Container
s.append(".header-container {")
s.append(f"  background-color: {NAVY};")
s.append("  padding: 40px 0;")
s.append("  margin-bottom: 40px;")
s.append("  text-align: center;")
s.append("}")

s.append(".header-title {")
s.append("  color: white;")
s.append("  font-size: 42px;")
s.append("  font-weight: 900;")
s.append("  margin: 0;")
s.append("  text-transform: uppercase;")
s.append("  letter-spacing: 1px;")
s.append("}")

s.append(".header-breadcrumb {")
s.append("  color: #aaa;")
s.append("  font-size: 14px;")
s.append("  margin-top: 10px;")
s.append("}")

# 3. Discover Card
s.append(".discover-card {")
s.append("  background: white;")
s.append("  box-shadow: 0 2px 15px rgba(0,0,0,0.05);")
s.append("  margin-bottom: 30px;")
s.append("  height: 100%;")
s.append("  display: flex;")
s.append("  flex-direction: column;")
s.append("}")

s.append(".card-img-top {")
s.append("  height: 220px;")
s.append("  width: 100%;")
s.append("  background-size: cover;")
s.append("  background-position: center;")
s.append("}")

s.append(".card-body {")
s.append("  padding: 25px;")
s.append("  flex-grow: 1;")
s.append("  display: flex;")
s.append("  flex-direction: column;")
s.append("}")

# 4. Typography
s.append(".event-date {")
s.append(f"  color: {TEAL};")
s.append("  font-weight: 700;")
s.append("  font-size: 14px;")
s.append("  margin-bottom: 5px;")
s.append("}")

s.append(".event-title {")
s.append(f"  color: {NAVY};")
s.append("  font-size: 20px;")
s.append("  font-weight: 900;")
s.append("  margin-bottom: 10px;")
s.append("  line-height: 1.3;")
s.append("}")

s.append(".event-loc {")
s.append("  color: #777;")
s.append("  font-size: 14px;")
s.append("  margin-bottom: 20px;")
s.append("}")

# 5. Buttons
s.append(".btn-discover {")
s.append(f"  background-color: {TEAL};")
s.append("  color: white;")
s.append("  text-decoration: none;")
s.append("  padding: 10px 20px;")
s.append("  font-weight: 700;")
s.append("  font-size: 14px;")
s.append("  text-transform: uppercase;")
s.append("  display: inline-block;")
s.append("  text-align: center;")
s.append("  margin-top: auto;")
s.append("}")

# 6. Single Page
s.append(".single-event-container {")
s.append("  background: white;")
s.append("  padding: 40px;")
s.append("  box-shadow: 0 4px 20px rgba(0,0,0,0.05);")
s.append("}")

s.append(".single-title {")
s.append("  font-size: 32px;")
s.append("  font-weight: 900;")
s.append("  margin-bottom: 10px;")
s.append("}")

s.append(".single-date {")
s.append(f"  color: {TEAL};")
s.append("  font-weight: 700;")
s.append("  font-size: 18px;")
s.append("  margin-bottom: 20px;")
s.append("}")

# 7. Sidebar Info Box
s.append(".info-box {")
s.append(f"  background-color: {GRAY};")
s.append("  padding: 30px;")
s.append(f"  border-left: 4px solid {TEAL};")
s.append("}")

s.append(".info-label {")
s.append("  font-weight: 900;")
s.append("  font-size: 13px;")
s.append("  text-transform: uppercase;")
s.append("  color: #888;")
s.append("  margin-bottom: 5px;")
s.append("}")

s.append(".info-value {")
s.append("  font-size: 16px;")
s.append("  font-weight: 700;")
s.append(f"  color: {NAVY};")
s.append("  margin-bottom: 20px;")
s.append("}")

s.append("</style>")
st.markdown("".join(s), unsafe_allow_html=True)

# --- HELPER: HTML GENERATOR ---
def create_card_html(img_url, date_str, title):
    # Short lines to prevent breaks
    h = []
    h.append('<div class="discover-card">')
    h.append(f'<div class="card-img-top" style="background-image: url(\'{img_url}\');"></div>')
    h.append('<div class="card-body">')
    h.append(f'<div class="event-date">{date_str}</div>')
    h.append(f'<div class="event-title">{title}</div>')
    h.append('<div class="event-loc">📍 Caldicot Town Centre</div>')
    h.append('<div style="margin-top:auto;">')
    h.append('<span class="btn-discover">Read More</span>')
    h.append('</div>')
    h.append('</div></div>')
    return "".join(h)

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

# --- DATE HELPER ---
def get_date_str(d):
    if pd.isna(d): return "Upcoming Date"
    return d.strftime("%d.%m.%Y")

# --- HEADER ---
st.markdown("""
<div class="header-container">
    <div class="header-title">What's On</div>
    <div class="header-breadcrumb">Home • What's On • Events</div>
</div>
""", unsafe_allow_html=True)

# --- MAIN APP ---
if df.empty:
    st.error("Unable to connect to Google Sheet.")
else:
    # FILTERS
    c1, c2 = st.columns([3, 1])
    with c2:
        if 'Type' in df.columns:
            opts = ["All Categories"] + list(df['Type'].unique())
            sel = st.selectbox("Filter", opts, label_visibility="collapsed")
            if sel != "All Categories": df = df[df['Type'] == sel]

    tab1, tab2 = st.tabs(["List View", "Map View"])

    # --- LIST VIEW ---
    with tab1:
        # Loop in chunks of 3 for grid
        for i in range(0, len(df), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(df):
                    row = df.iloc[i + j]
                    
                    with cols[j]:
                        d_str = get_date_str(row['Date_Obj'])
                        img = str(row['Image_URL'])
                        if len(img) < 5: img = LOGO
                        
                        # Generate Card
                        html = create_card_html(img, d_str, str(row['Event']))
                        st.markdown(html, unsafe_allow_html=True)
                        
                        # View Details
                        with st.expander("View Details"):
                            desc = str(row['Description']).replace('\n', '<br><br>')
                            
                            # Build Detail HTML
                            dh = []
                            dh.append('<div class="single-event-container">')
                            dh.append(f'<h1 class="single-title">{row["Event"]}</h1>')
                            dh.append(f'<div class="single-date">{d_str}</div>')
                            dh.append(f'<div style="font-size:16px; line-height:1.6;">{desc}</div>')
                            dh.append('</div>')
                            st.markdown("".join(dh), unsafe_allow_html=True)
                            
                            st.write("")
                            
                            # Info & Map
                            ci, cm = st.columns([1, 2])
                            with ci:
                                ib = []
                                ib.append('<div class="info-box">')
                                ib.append('<div class="info-label">Date</div>')
                                ib.append(f'<div class="info-value">{d_str}</div>')
                                ib.append('<div class="info-label">Location</div>')
                                ib.append('<div class="info-value">Town Centre</div>')
                                ib.append('<div class="info-label">Cost</div>')
                                ib.append('<div class="info-value">Free</div>')
                                ib.append('</div>')
                                st.markdown("".join(ib), unsafe_allow_html=True)
                                
                                txt = urllib.parse.quote("Check out " + str(row['Event']))
                                wa = "https://api.whatsapp.com/send?text=" + txt
                                st.markdown(f'<a href="{wa}" target="_blank" class="btn-discover" style="width:100%; margin-top:10px;">Share</a>', unsafe_allow_html=True)

                            with cm:
                                m_s = folium.Map(location=[row['Lat'], row['Lon']], zoom_start=15)
                                folium.Marker([row['Lat'], row['Lon']]).add_to(m_s)
                                st_folium(m_s, height=300, width=700, key=f"map_{i}_{j}", returned_objects=[])

            st.write("") 

    # --- MAP VIEW ---
    with tab2:
        m = folium.Map(location=[51.5923, -2.7505], zoom_start=14)
        for i, row in df.iterrows():
            folium.Marker(
                [row['Lat'], row['Lon']],
                popup=str(row['Event']),
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)
        st_folium(m, width="100%", height=600, returned_objects=[])
