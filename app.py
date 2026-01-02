import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import urllib.parse

# --- CONFIG ---
st.set_page_config(page_title="Caldicot Town Hub", layout="wide")

# --- ASSETS ---
# Using the town team logo
LOGO = "https://i0.wp.com/caldicottownteam.co.uk/wp-content/uploads/2025/07/TRWS-Logo-01-e1753868910696.png?ssl=1"

# --- CSS STYLES (Commercial Grade) ---
s = []
s.append("<style>")
# Import Inter font for that "Tech Startup" look
s.append("@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');")
s.append("html, body, [class*='css'] { font-family: 'Inter', sans-serif; }")

# 1. HERO HEADER STYLE
s.append(".hero-container {")
s.append("  background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);") # Professional Dark Gradient
s.append("  padding: 40px 20px;")
s.append("  border-radius: 0 0 20px 20px;")
s.append("  color: white;")
s.append("  margin-bottom: 40px;")
s.append("  text-align: center;")
s.append("}")
s.append(".hero-title { font-size: 3rem; font-weight: 800; margin: 0; letter-spacing: -1px; }")
s.append(".hero-subtitle { font-size: 1.2rem; opacity: 0.9; font-weight: 400; margin-top: 10px; }")

# 2. TICKET CARD (Deep Shadows & Hover Effects)
s.append(".ticket-card {")
s.append("  background: white;")
s.append("  border: 1px solid #e0e0e0;")
s.append("  border-radius: 16px;") # Softer corners
s.append("  box-shadow: 0 4px 20px rgba(0,0,0,0.08);") # Deep, expensive looking shadow
s.append("  margin-bottom: 30px;")
s.append("  overflow: hidden;")
s.append("  transition: all 0.3s ease;")
s.append("}")
s.append(".ticket-card:hover { transform: translateY(-5px); box-shadow: 0 12px 30px rgba(0,0,0,0.15); }")

# Flex Layout
s.append(".card-flex { display: flex; flex-direction: row; height: 260px; }")
s.append(".card-img { width: 40%; background-size: cover; background-position: center; }")
s.append(".card-body { width: 60%; padding: 30px; display: flex; flex-direction: column; justify-content: center; position: relative; }")

# Mobile Responsiveness
s.append("@media (max-width: 768px) {")
s.append("  .card-flex { flex-direction: column; height: auto; }")
s.append("  .card-img { width: 100%; height: 220px; }")
s.append("  .card-body { width: 100%; padding: 25px; }")
s.append("}")

# Typography Elements
s.append(".date-badge { color: #d1410c; font-weight: 900; font-size: 15px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }")
s.append(".event-title { color: #111; font-size: 26px; font-weight: 800; line-height: 1.1; margin-bottom: 12px; }")
s.append(".location-row { display: flex; align-items: center; gap: 6px; color: #666; font-size: 14px; font-weight: 500; margin-bottom: 15px; }")

# Category Tag
s.append(".category-pill {")
s.append("  display: inline-block; background: #f0f2f5; color: #555;")
s.append("  font-size: 12px; font-weight: 700; text-transform: uppercase;")
s.append("  padding: 6px 12px; border-radius: 100px; letter-spacing: 0.5px;")
s.append("}")

# 3. "READ MORE" ARTICLE STYLE (The WordPress Look)
s.append(".article-wrapper {")
s.append("  background-color: white;")
s.append("  border: 1px solid #eee;")
s.append("  border-radius: 12px;")
s.append("  padding: 30px;")
s.append("  margin-top: 15px;")
s.append("}")
s.append(".article-content { font-size: 16px; line-height: 1.7; color: #333; }")
s.append(".article-content h1, .article-content h2, .article-content h3 { color: #111; font-weight: 800; margin-top: 20px; }")
s.append(".article-content img { width: 100%; border-radius: 12px; margin: 20px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }")

# Buttons
s.append(".action-btn {")
s.append("  display: inline-block; text-decoration: none;")
s.append("  padding: 10px 20px; border-radius: 8px;")
s.append("  font-weight: 700; font-size: 14px; text-align: center;")
s.append("  transition: opacity 0.2s;")
s.append("}")
s.append(".btn-primary { background-color: #000; color: white !important; }")
s.append(".btn-secondary { background-color: #f0f2f5; color: #333 !important; }")
s.append(".btn-whatsapp { background-color: #25D366; color: white !important; }")
s.append("</style>")

st.markdown("".join(s), unsafe_allow_html=True)

# --- HERO BANNER ---
st.markdown("""
<div class="hero-container">
    <div class="hero-title">What's On in Caldicot</div>
    <div class="hero-subtitle">Live Events, Markets & Community Gatherings</div>
</div>
""", unsafe_allow_html=True)

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
def get_date_parts(d):
    if pd.isna(d): return "SOON", ""
    return d.strftime("%b").upper(), d.strftime("%d")

# --- MAIN LAYOUT ---
if df.empty:
    st.error("Unable to connect to Google Sheet.")
else:
    # Sidebar
    st.sidebar.image(LOGO, width=140)
    st.sidebar.markdown("### 🏰 Filter Events")
    if 'Type' in df.columns:
        opts = ["All Events"] + list(df['Type'].unique())
        sel = st.sidebar.selectbox("Category", opts, label_visibility="collapsed")
        if sel != "All Events": df = df[df['Type'] == sel]

    tab1, tab2 = st.tabs(["🎫 EVENT FEED", "🗺️ EVENT MAP"])

    # --- TAB 1: THE PREMIUM FEED ---
    with tab1:
        for i, row in df.iterrows():
            mon, day = get_date_parts(row['Date_Obj'])
            img = str(row['Image_URL'])
            if len(img) < 5: img = LOGO
            
            # 1. THE CARD (HTML)
            h = []
            h.append('<div class="ticket-card">')
            h.append('  <div class="card-flex">')
            h.append(f'    <div class="card-img" style="background-image: url(\'{img}\');"></div>')
            h.append('    <div class="card-body">')
            h.append(f'      <div class="date-badge">{mon} {day}</div>')
            h.append(f'      <div class="event-title">{row["Event"]}</div>')
            h.append(f'      <div class="location-row">📍 Caldicot Town Centre</div>')
            h.append(f'      <div><span class="category-pill">{row["Type"]}</span></div>')
            h.append('    </div>')
            h.append('  </div>')
            h.append('</div>')
            
            st.markdown("".join(h), unsafe_allow_html=True)

            # 2. THE RICH DETAILS (HTML)
            # This is where we solve the "Basic Text" issue. 
            # We wrap the content in a beautiful "Article" div.
            with st.expander(f"📖 Read Full Details & Info"):
                
                # We inject the description as raw HTML. 
                # This allows BOLD text, Headers, and extra Images to render properly if they are in your sheet.
                d_html = []
                d_html.append('<div class="article-wrapper">')
                d_html.append('<div class="article-content">')
                # We convert newlines to <br> so paragraphs show up nicely
                desc_text = str(row['Description']).replace('\n', '<br><br>')
                d_html.append(desc_text)
                d_html.append('</div>')
                
                # Action Buttons Row
                d_html.append('<div style="margin-top: 30px; display: flex; gap: 10px;">')
                
                # Map Button
                lat, lon = row['Lat'], row['Lon']
                map_url = f"http://maps.google.com/?q={lat},{lon}"
                d_html.append(f'<a href="{map_url}" target="_blank" class="action-btn btn-primary">📍 Get Directions</a>')
                
                # WhatsApp Button
                share_txt = urllib.parse.quote(f"Check out {row['Event']}!")
                wa_url = f"https://api.whatsapp.com/send?text={share_txt}"
                d_html.append(f'<a href="{wa_url}" target="_blank" class="action-btn btn-whatsapp">💬 Share</a>')
                
                d_html.append('</div>') # End buttons
                d_html.append('</div>') # End wrapper
                
                st.markdown("".join(d_html), unsafe_allow_html=True)

            st.write("") # Spacer

    # --- TAB 2: MAP ---
    with tab2:
        m = folium.Map(location=[51.5923, -2.7505], zoom_start=14)
        for i, row in df.iterrows():
            folium.Marker(
                [row['Lat'], row['Lon']],
                popup=str(row['Event']),
                icon=folium.Icon(color="black", icon="star")
            ).add_to(m)
        st_folium(m, width="100%", height=500, returned_objects=[])
