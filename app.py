import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import urllib.parse

# --- CONFIG ---
st.set_page_config(page_title="Caldicot Town Hub", layout="wide")

# --- ASSETS ---
LOGO = "https://i0.wp.com/caldicottownteam.co.uk/wp-content/uploads/2025/07/TRWS-Logo-01-e1753868910696.png?ssl=1"

# --- CSS STYLES (Built safely line-by-line) ---
s = []
s.append("<style>")
# Fonts
s.append("@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');")
s.append("html, body, [class*='css'] { font-family: 'Inter', sans-serif; }")

# The Ticket Card Container
s.append(".ticket-card {")
s.append("  background: white;")
s.append("  border: 1px solid #e0e0e0;")
s.append("  border-radius: 12px;")
s.append("  box-shadow: 0 4px 10px rgba(0,0,0,0.05);")
s.append("  margin-bottom: 25px;")
s.append("  overflow: hidden;")
s.append("}")

# Flex Layout (Image Left, Text Right)
s.append(".card-flex { display: flex; flex-direction: row; height: 240px; }")
s.append(".card-img { width: 35%; background-size: cover; background-position: center; }")
s.append(".card-body { width: 65%; padding: 25px; display: flex; flex-direction: column; justify-content: center; }")

# Mobile Responsiveness
s.append("@media (max-width: 768px) {")
s.append("  .card-flex { flex-direction: column; height: auto; }")
s.append("  .card-img { width: 100%; height: 200px; }")
s.append("  .card-body { width: 100%; padding: 20px; }")
s.append("}")

# Typography (The "Ticketmaster" Look)
s.append(".date-badge { color: #d1410c; font-weight: 800; font-size: 14px; text-transform: uppercase; margin-bottom: 8px; }")
s.append(".event-title { color: #1a1a1a; font-size: 22px; font-weight: 800; line-height: 1.2; margin-bottom: 10px; }")
s.append(".category-tag { background: #f4f4f4; color: #555; font-size: 11px; font-weight: 600; padding: 4px 10px; border-radius: 100px; }")
s.append(".location-text { color: #666; font-size: 14px; margin-top: 10px; }")

# Read More Section
s.append(".article-box { background-color: #fcfcfc; border-top: 1px solid #eee; padding: 30px; }")
s.append(".article-box img { max-width: 100%; border-radius: 8px; margin: 15px 0; }")
s.append("</style>")

# Apply the styles
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
        
        # Ensure necessary columns exist
        req = ['Image_URL', 'Description', 'Event', 'Date', 'Type', 'Lat', 'Lon']
        for c in req:
            if c not in df.columns: df[c] = ""

        # Defaults
        df['Image_URL'] = df['Image_URL'].fillna(LOGO)
        df['Description'] = df['Description'].fillna("No details provided.")
        
        # Data Cleaning
        df['Date_Obj'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Lat'] = pd.to_numeric(df['Lat'], errors='coerce')
        df['Lon'] = pd.to_numeric(df['Lon'], errors='coerce')
        df = df.dropna(subset=['Lat', 'Lon'])
        return df
    except:
        return pd.DataFrame()

df = load_data()

# --- HELPER FUNCTION ---
def get_date_parts(d):
    if pd.isna(d): return "UPCOMING", "DATE"
    return d.strftime("%b").upper(), d.strftime("%d")

# --- MAIN LAYOUT ---
st.sidebar.image(LOGO, width=150)
st.sidebar.header("Explore Caldicot")

st.title("What's On in Caldicot")

if df.empty:
    st.error("Data error. Please check the Google Sheet link.")
else:
    # Sidebar Filter
    if 'Type' in df.columns:
        opts = ["All Events"] + list(df['Type'].unique())
        sel = st.sidebar.selectbox("Category", opts)
        if sel != "All Events": df = df[df['Type'] == sel]

    tab1, tab2 = st.tabs(["🎫 Event Feed", "🗺️ Interactive Map"])

    # --- TAB 1: THE TICKETMASTER FEED ---
    with tab1:
        for i, row in df.iterrows():
            mon, day = get_date_parts(row['Date_Obj'])
            img = str(row['Image_URL'])
            # Validation: If link is too short, use Logo
            if len(img) < 5: img = LOGO
            
            # --- CARD HTML CONSTRUCTION ---
            # We build this as a list of strings to prevent syntax errors
            h = []
            h.append('<div class="ticket-card">')
            h.append('  <div class="card-flex">')
            # The Image Side
            h.append(f'    <div class="card-img" style="background-image: url(\'{img}\');"></div>')
            # The Text Side
            h.append('    <div class="card-body">')
            h.append(f'      <div class="date-badge">{mon} {day}</div>')
            h.append(f'      <div class="event-title">{row["Event"]}</div>')
            h.append(f'      <div><span class="category-tag">{row["Type"]}</span></div>')
            h.append('      <div class="location-text">📍 Caldicot Town Centre</div>')
            h.append('    </div>')
            h.append('  </div>')
            h.append('</div>')
            
            # Render the Card
            st.markdown("".join(h), unsafe_allow_html=True)

            # --- READ MORE EXPANDER ---
            with st.expander(f"📖 Details for {row['Event']}"):
                # Article Content
                a = []
                a.append('<div class="article-box">')
                a.append('<h3>Event Details</h3>')
                a.append(str(row['Description']))
                a.append('</div>')
                st.markdown("".join(a), unsafe_allow_html=True)
                
                st.markdown("---")
                c1, c2 = st.columns(2)
                
                # Links
                with c1:
                    lat, lon = row['Lat'], row['Lon']
                    lnk = f"http://maps.google.com/?q={lat},{lon}"
                    st.link_button("📍 Open Google Maps", lnk)
                
                with c2:
                    txt = urllib.parse.quote(f"Check out {row['Event']}!")
                    wa = f"https://api.whatsapp.com/send?text={txt}"
                    st.link_button("💬 Share on WhatsApp", wa)

            st.write("") # Spacer

    # --- TAB 2: MAP ---
    with tab2:
        m = folium.Map(location=[51.5923, -2.7505], zoom_start=14)
        for i, row in df.iterrows():
            folium.Marker(
                [row['Lat'], row['Lon']],
                popup=str(row['Event']),
                icon=folium.Icon(color="red", icon="calendar")
            ).add_to(m)
        st_folium(m, width=1200, height=500, returned_objects=[])
