import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import urllib.parse

# --- CONFIG ---
st.set_page_config(page_title="Caldicot Town Hub", page_icon="🏰", layout="wide")

# --- 🔗 YOUR SPECIFIC IMAGE (Used as Logo & Fallback) ---
CALDICOT_LOGO = "https://i0.wp.com/caldicottownteam.co.uk/wp-content/uploads/2025/07/TRWS-Logo-01-e1753868910696.png?ssl=1"

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .event-title {
        color: #2E86C1;
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .event-meta {
        color: #666;
        font-size: 14px;
        margin-bottom: 15px;
        font-family: sans-serif;
    }
    .share-btn {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 4px;
        text-decoration: none;
        color: white !important;
        font-size: 13px;
        font-weight: bold;
        margin-right: 8px;
        transition: opacity 0.3s;
    }
    .fb { background-color: #1877F2; }
    .wa { background-color: #25D366; }
    .tw { background-color: #1DA1F2; }
    .share-btn:hover { opacity: 0.8; }
    
    /* Make the images look neat */
    img {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR LOGO ---
st.sidebar.image(CALDICOT_LOGO, width=150)
st.sidebar.header("Filter Options")

# --- 🔗 DATABASE LINK ---
SHEET_ID = "1hdx13h_0u9Yln-tmRoZu8d_DIkThoE801MP1S3ohXms"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Events"

@st.cache_data(ttl=10)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip()
        
        # Robustness: Create missing columns
        required_cols = ['Image_URL', 'Description', 'Event', 'Date', 'Type', 'Lat', 'Lon']
        for col in required_cols:
            if col not in df.columns:
                df[col] = "" 

        # --- FALLBACK IMAGES ---
        # If the cell is empty, use the Caldicot Logo
        df['Image_URL'] = df['Image_URL'].fillna(CALDICOT_LOGO)
        
        # If the description is empty, put a placeholder
        df['Description'] = df['Description'].fillna("No additional details provided for this event.")
        
        return df
    except Exception as e:
        st.error(f"Data Connection Error: {e}")
        return pd.DataFrame()

df = load_data()

st.title("🏰 Caldicot Town Hub")
st.caption("Live Event Feed & Interactive Map")

if df.empty:
    st.warning("⚠️ Loading data... If this persists, check the Google Sheet link.")
else:
    # --- FILTERS (Sidebar) ---
    # Optional: Filter by event type
    if 'Type' in df.columns:
        types = ["All"] + list(df['Type'].unique())
        selected_type = st.sidebar.selectbox("Filter by Category", types)
        if selected_type != "All":
            df = df[df['Type'] == selected_type]

    # --- TABS: FEED FIRST, THEN MAP ---
    tab1, tab2 = st.tabs(["📰 Latest News & Events", "🗺️ Interactive Map"])

    # --- TAB 1: THE RICH FEED ---
    with tab1:
        # Loop through events (reversed so newest might be at top if sorted)
        for index, row in df.iterrows():
            with st.container():
                c1, c2 = st.columns([1, 2], gap="medium")
                
                # LEFT: IMAGE
                with c1:
                    img_link = row['Image_URL']
                    # Sanity check the link (if it's too short, use logo)
                    if not isinstance(img_link, str) or len(img_link) < 5:
                        img_link = CALDICOT_LOGO
                    
                    st.image(img_link, use_container_width=True)

                # RIGHT: CONTENT
                with c2:
                    st.markdown(f'<div class="event-title">{row["Event"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="event-meta">📅 {row["Date"]} &nbsp; • &nbsp; 🏷️ {row["Type"]}</div>', unsafe_allow_html=True)
                    
                    # Description Snippet
                    desc_text = str(row['Description'])
                    # If text is long (>200 chars), cut it off. If short, show all.
                    short_desc = (desc_text[:200] + '...') if len(desc_text) > 200 else desc_text
                    st.write(short_desc)
                    
                    # EXPANDER for "Read More"
                    with st.expander("📖 Read Full Details"):
                        st.write(desc_text)
                        st.markdown("---")
                        # Add a Google Maps link for directions
                        maps_link = f"https://www.google.com/maps/search/?api=1&query={row['Lat']},{row['Lon']}"
                        st.markdown(f"**📍 Location:** [Get Directions]({maps_link})")

                    # SHARE BUTTONS
                    share_text = urllib.parse.quote(f"Check out {row['Event']} in Caldicot! 🏰")
                    share_url = urllib.parse.quote("https://caldicottownteam.co.uk") 
                    
                    st.markdown(f"""
                        <div style="margin-top: 10px;">
                            <a href="https://www.facebook.com/sharer/
