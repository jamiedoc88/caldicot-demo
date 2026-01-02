import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import urllib.parse
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="Caldicot Town Hub", page_icon="🏰", layout="wide")

# --- ASSETS ---
CALDICOT_LOGO = "https://i0.wp.com/caldicottownteam.co.uk/wp-content/uploads/2025/07/TRWS-Logo-01-e1753868910696.png?ssl=1"

# --- SIDEBAR ---
st.sidebar.image(CALDICOT_LOGO, width=150)
st.sidebar.header("Filter Options")

# --- DATA LOADING ---
SHEET_ID = "1hdx13h_0u9Yln-tmRoZu8d_DIkThoE801MP1S3ohXms"
base_url = "https://docs.google.com/spreadsheets/d/"
query = "/gviz/tq?tqx=out:csv&sheet=Events"
SHEET_URL = base_url + SHEET_ID + query

@st.cache_data(ttl=10)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip()
        
        # Create missing columns
        required_cols = ['Image_URL', 'Description', 'Event', 'Date', 'Type', 'Lat', 'Lon']
        for col in required_cols:
            if col not in df.columns:
                df[col] = "" 

        # Fill missing data
        df['Image_URL'] = df['Image_URL'].fillna(CALDICOT_LOGO)
        df['Description'] = df['Description'].fillna("No additional details provided.")
        
        # Convert Data Types
        df['Date_Obj'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Lat'] = pd.to_numeric(df['Lat'], errors='coerce')
        df['Lon'] = pd.to_numeric(df['Lon'], errors='coerce')
        df = df.dropna(subset=['Lat', 'Lon'])
        
        return df
    except Exception:
        return pd.DataFrame()

df = load_data()

# --- DATE HELPER ---
def get_date_strings(date_obj):
    if pd.isna(date_obj): return "Upcoming", "Date"
    # Returns ("JUN", "15")
    return date_obj.strftime("%b").upper(), date_obj.strftime("%d")

# --- MAIN PAGE ---
st.title("What's On in Caldicot")
st.caption("Discover local markets, festivals and events.")

if df.empty:
    st.error("⚠️ Unable to load events. Please check the Google Sheet.")
else:
    # FILTERS
    if 'Type' in df.columns:
        all_types = ["All Events"] + list(df['Type'].unique())
        cat_filter = st.sidebar.selectbox("Category", all_types)
        if cat_filter != "All Events":
            df = df[df['Type'] == cat_filter]

    # TABS
    tab1, tab2 = st.tabs(["🎫 Event Feed", "🗺️ Interactive Map"])

    # --- TAB 1: EVENT FEED (Native Layout) ---
    with tab1:
        for index, row in df.iterrows():
            month, day = get_date_strings(row['Date_Obj'])
            
            # Validating Image URL
            img_link = str(row['Image_URL'])
            if len(img_link) < 5: img_link = CALDICOT_LOGO

            # --- THE CARD LAYOUT (Using Columns instead of HTML) ---
            with st.container(border=True):
                col_img, col_text = st.columns([1, 3])
                
                # Column 1: Image
                with col_img:
                    st.image(img_link, use_container_width=True)
                
                # Column 2: Text Details
                with col_text:
                    # Event Title
                    st.subheader(row['Event'])
                    
                    # Date & Type Badges
                    st.markdown(f"**📅 {month} {day}** &nbsp; | &nbsp; 🏷️ {row['Type']}")
                    st.write("📍 Caldicot Town Centre")
                    
                    # Read More Expander
                    with st.expander("📖 Read Details & Directions"):
                        st.write(row['Description'])
                        st.markdown("---")
                        
                        # Google Maps Link
                        map_link = f"http://maps.google.com/?q={row['Lat']},{row['Lon']}"
                        st.markdown(f"**[📍 Open in Google Maps]({map_link})**")
                        
                        # Share Links
                        share_text = urllib.parse.quote(f"Check out {row['Event']}!")
                        st.write("Share this event:")
                        st.markdown(f"""
                        [Facebook](https://www.facebook.com/sharer/sharer.php?u=caldicottownteam.co.uk) • 
                        [WhatsApp](https://api.whatsapp.com/send?text={share_text})
                        """)

    # --- TAB 2: MAP ---
    with tab2:
        m = folium.Map(location=[51.5923, -2.7505], zoom_start=14)
        
        for index, row in df.iterrows():
            folium.Marker(
                [row['Lat'], row['Lon']],
                popup=row['Event'],
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)
            
        # IMPORTANT: returned_objects=[] prevents crashes on cloud
        st_folium(m, width=1200, height=500, returned_objects=[])
