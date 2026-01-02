import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- CONFIG ---
st.set_page_config(page_title="Caldicot Town Hub", layout="wide")

# --- CUSTOM CSS FOR "CARDS" ---
st.markdown("""
<style>
    .event-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .event-title {
        color: #2E86C1;
        font-size: 20px;
        font-weight: bold;
    }
    .event-date {
        color: #555;
        font-weight: bold;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ⚠️ PASTE YOUR SHEET LINK HERE AGAIN
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/......YOUR_LINK_HERE..../pub?gid=0&single=true&output=csv"

@st.cache_data(ttl=10)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip()
        # Handle empty image columns by filling with a placeholder
        if 'Image_URL' not in df.columns: df['Image_URL'] = "https://via.placeholder.com/300"
        df['Image_URL'] = df['Image_URL'].fillna("https://via.placeholder.com/300")
        return df
    except:
        return pd.DataFrame()

df = load_data()

st.title("🏰 Caldicot Town Hub")

if df.empty:
    st.error("Could not load data. Check your Google Sheet link.")
else:
    tab1, tab2 = st.tabs(["🗺️ Interactive Map", "📰 Event Feed"])

    # --- TAB 1: MAP (Simple View) ---
    with tab1:
        st.write("Click a pin to see details.")
        m = folium.Map(location=[51.5923, -2.7505], zoom_start=14)
        
        for index, row in df.iterrows():
            # Create a rich popup with image
            popup_html = f"""
            <div style="width:200px">
                <b>{row['Event']}</b><br>
                {row['Date']}<br>
                <img src="{row['Image_URL']}" width="100%" style="margin-top:10px; border-radius:5px;">
            </div>
            """
            
            folium.Marker(
                [row['Lat'], row['Lon']],
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=row['Event'],
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)
            
        st_folium(m, width=1200, height=500)

    # --- TAB 2: RICH EVENT FEED (Detailed View) ---
    with tab2:
        st.subheader("Upcoming Events")
        
        # Display events as "Cards" (Image + Text side by side)
        for index, row in df.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Display the image
                    st.image(row['Image_URL'], use_container_width=True)
                
                with col2:
                    st.markdown(f'<div class="event-title">{row["Event"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="event-date">📅 {row["Date"]} | {row["Type"]}</div>', unsafe_allow_html=True)
                    st.write(row['Description']) # Full text description
                
                st.divider() # Line between events
