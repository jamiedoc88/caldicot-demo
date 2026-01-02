import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- PAGE CONFIG ---
st.set_page_config(page_title="Caldicot Town Hub", layout="wide")

# --- CUSTOMER DATABASE LINK ---
# PASTE YOUR GOOGLE SHEET CSV LINK INSIDE THE QUOTES BELOW:
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR9123Uwb863QUp-7O_35WzfRQdDsuXD29UIQFFhnvNLgWIpN2nyOdiHpbf4tK09-KPFntrdgX-K7LE/pub?gid=0&single=true&output=csv"

# --- CACHED DATA LOADER ---
# ttl=10 means the app checks for new spreadsheet rows every 10 seconds
@st.cache_data(ttl=10)
def load_data():
    try:
        # Read the CSV from the URL
        df = pd.read_csv(SHEET_URL)
        # Clean whitespace from column names just in case
        df.columns = df.columns.str.strip()
        return df
    except Exception:
        return pd.DataFrame()

df = load_data()

# --- APP INTERFACE ---
# The "Sales Pitch" Info Box
st.info("""
ℹ️ **Prototype Demo for Caldicot Town Team**
This tool demonstrates a new way to manage your website. 
Instead of logging into WordPress, your team simply adds events to a secure Spreadsheet, 
and this map updates automatically.
""")

st.title("🏰 Caldicot Town Hub")

if df.empty:
    st.error("⚠️ Could not load data. Check your Google Sheet link in the code.")
else:
    # --- TABS LAYOUT ---
    tab1, tab2 = st.tabs(["🗺️ Interactive Map", "📅 Event List"])

    # --- TAB 1: THE MAP ---
    with tab1:
        st.write("Explore upcoming events in the town centre.")
        
        # 1. Create Base Map centered on Caldicot
        m = folium.Map(location=[51.5923, -2.7505], zoom_start=14)

        # 2. Add Pins from the Spreadsheet
        for index, row in df.iterrows():
            # Color code the pins
            color = "blue"
            if "Market" in str(row['Type']): color = "orange"
            if "Culture" in str(row['Type']): color = "purple"
            if "Volunteer" in str(row['Type']): color = "green"

            folium.Marker(
                [row['Lat'], row['Lon']],
                popup=f"<b>{row['Event']}</b><br>{row['Date']}",
                tooltip=row['Event'],
                icon=folium.Icon(color=color, icon="info-sign")
            ).add_to(m)

        # 3. Render the Map
        st_folium(m, width=1200, height=500)

    # --- TAB 2: THE LIST ---
    with tab2:
        st.subheader("Upcoming Events")
        # Show a clean table
        st.dataframe(
            df[['Date', 'Event', 'Type']], 
            use_container_width=True, 
            hide_index=True
        )