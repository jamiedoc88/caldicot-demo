import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import urllib.parse
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Caldicot Town Hub", page_icon="🏰", layout="wide")

# --- 🔗 ASSETS ---
CALDICOT_LOGO = "https://i0.wp.com/caldicottownteam.co.uk/wp-content/uploads/2025/07/TRWS-Logo-01-e1753868910696.png?ssl=1"

# --- 🎨 1. THE DESIGN SYSTEM (CSS) ---
# We define all the styling here. This gives it the "Ticketmaster" look.
STYLES = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* THE CARD CONTAINER */
    .ticket-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        overflow: hidden;
        transition: transform 0.2s;
    }
    .ticket-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        border-color: #d0d0d0;
    }

    /* FLEX LAYOUT (Desktop) */
    .card-flex {
        display: flex;
        flex-direction: row;
        height: 240px; /* Fixed height for uniformity */
    }

    /* LEFT SIDE: IMAGE */
    .card-img {
        width: 35%;
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }

    /* RIGHT SIDE: CONTENT */
    .card-body {
        width: 65%;
        padding: 25px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    /* MOBILE LAYOUT */
    @media (max-width: 768px) {
        .card-flex { flex-direction: column; height: auto; }
        .card-img { width: 100%; height: 200px; }
        .card-body { width: 100%; padding: 20px; }
    }

    /* TYPOGRAPHY */
    .date-badge {
        color: #d1410c; /* Ticketmaster Red */
        font-weight: 800;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .event-title {
        color: #1a1a1a;
        font-size: 22px;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 10px;
    }
    .category-tag {
        display: inline-block;
        background: #f4f4f4;
        color: #555;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        padding: 4px 10px;
        border-radius: 100px;
        margin-bottom: 12px;
    }
    .location-text {
        color: #666;
        font-size: 14px;
        display: flex;
        align-items: center;
        gap: 5px;
    }

    /* READ MORE SECTION */
    .article-container {
        background
