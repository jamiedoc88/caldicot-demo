import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import urllib.parse

# --- CONFIGURATION ---
st.set_page_config(page_title="What's On - Discover Inverclyde", layout="wide")

# --- BRAND COLORS ---
TEAL = "#009BB9"
NAVY = "#1D2D3D"
GRAY = "#F4F6F7"
LOGO = "https://i0.wp.com/caldicottownteam.co.uk/wp-content/uploads/2025/07/TRWS-Logo-01-e1753868910696.png?ssl=1"

# --- CSS STYLES (Vertical Mode to prevent Syntax Errors) ---
s = []
s.append("<style>")
# Fonts
s.append("@import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;700;900&display=swap');")
s.append("html, body, [class*='css'] { font-family: 'Lato', sans-serif; color: #1D2D3D; }")

# Header Section
s.append(".header-container {")
s.append("  background-color: #1D2D3D;")
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
s.append(".header-breadcrumb { color: #aaa; font-size: 14px; margin-top: 10px; }")

# Event Card
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
s
