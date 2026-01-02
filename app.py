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

        # Fallback Logic
        df['Image_URL'] = df['Image_URL'].fillna(CALDICOT_LOGO)
        df['Description'] = df['Description'].fillna("No additional details provided.")
        
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
    # --- FILTERS ---
    if 'Type' in df.columns:
        types = ["All"] + list(df['Type'].unique())
        selected_type = st.sidebar.selectbox("Filter by Category", types)
        if selected_type != "All":
            df = df[df['Type'] == selected_type]

    # --- TABS ---
    tab1, tab2 = st.tabs(["📰 Latest News & Events", "🗺️ Interactive Map"])

    # --- TAB 1: THE RICH FEED ---
    with tab1:
        for index, row in df.iterrows():
            with st.container():
                c1, c2 = st.columns([1, 2], gap="medium")
                
                # LEFT: IMAGE
                with c1:
                    img_link = row['Image_URL']
                    if not isinstance(img_link, str) or len(img_link) < 5:
                        img_link = CALDICOT_LOGO
                    st.image(img_link, use_container_width=True)

                # RIGHT: CONTENT
                with c2:
                    st.markdown(f'<div class="event-title">{row["Event"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="event-meta">📅 {row["Date"]}   •   🏷️ {row["Type"]}</div>', unsafe_allow_html=True)
                    
                    desc_text = str(row['Description'])
                    short_desc = (desc_text[:200] + '...') if len(desc_text) > 200 else desc_text
                    st.write(short_desc)
                    
                    with st.expander("📖 Read Full Details"):
                        st.write(desc_text)
                        st.markdown("---")
                        maps_link = f"https://www.google.com/maps/search/?api=1&query={row['Lat']},{row['Lon']}"
                        st.markdown(f"**📍 Location:** [Get Directions]({maps_link})")

                    # --- FIX: SIMPLIFIED HTML GENERATION ---
                    share_text = urllib.parse.quote(f"Check out {row['Event']} in Caldicot! 🏰")
                    share_url = urllib.parse.quote("https://caldicottownteam.co.uk") 
                    
                    # We use simple string addition instead of triple quotes to avoid indentation errors
                    html_block = '<div style="margin-top: 10px;">'
                    html_block += f'<a href="https://www.facebook.com/sharer/sharer.php?u={share_url}" target="_blank" class="share-btn fb">Facebook</a>'
                    html_block += f'<a href="https://api.whatsapp.com/send?text={share_text}%20{share_url}" target="_blank" class="share-btn wa">WhatsApp</a>'
                    html_block += f'<a href="https://twitter.com/intent/tweet?text={share_text}&url={share_url}" target="_blank" class="share-btn tw">X / Twitter</a>'
                    html_block += '</div>'
                    
                    st.markdown(html_block, unsafe_allow_html=True)
                
                st.divider()

    # --- TAB 2: THE MAP ---
    with tab2:
        st.info("📍 Click any pin for details.")
        m = folium.Map(location=[51.5923, -2.7505], zoom_start=14)
        
        for index, row in df.iterrows():
            popup_html = f"""
            <div style="width:180px; font-family:sans-serif;">
                <img src="{CALDICOT_LOGO}" width="50px" style="margin-bottom:5px;"><br>
                <b>{row['Event']}</b><br>
                <span style="color:gray;">{row['Date']}</span>
            </div>
            """
            
            folium.Marker(
                [row['Lat'], row['Lon']],
                popup=folium.Popup(popup_html, max_width=200),
                tooltip=row['Event'],
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)
            
        st_folium(m, width=1200, height=500)
