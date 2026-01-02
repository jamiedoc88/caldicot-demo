import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import urllib.parse
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="Caldicot Town Hub", page_icon="🏰", layout="wide")

# --- 🔗 ASSETS ---
CALDICOT_LOGO = "https://i0.wp.com/caldicottownteam.co.uk/wp-content/uploads/2025/07/TRWS-Logo-01-e1753868910696.png?ssl=1"

# --- 🎨 MODERN UI (TICKETMASTER STYLE) ---
st.markdown("""
<style>
    /* GLOBAL FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* CARD CONTAINER */
    .ticket-card {
        background-color: white;
        border-radius: 12px;
        padding: 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border: 1px solid #f0f0f0;
        margin-bottom: 25px;
        overflow: hidden; /* Keeps image corners rounded */
    }
    .ticket-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.12);
    }

    /* FLEX LAYOUT FOR DESKTOP (Image Left, Content Right) */
    .card-content {
        display: flex;
        flex-direction: row;
        align-items: stretch;
    }
    
    /* MOBILE RESPONSIVENESS */
    @media (max-width: 768px) {
        .card-content { flex-direction: column; }
        .card-image { width: 100% !important; height: 200px !important; }
    }

    /* IMAGE STYLING */
    .card-image {
        width: 35%;
        min-height: 220px;
        background-size: cover;
        background-position: center;
        position: relative;
    }

    /* CONTENT SIDE */
    .card-details {
        padding: 25px;
        width: 65%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    /* DATE BADGE (The "Stubhub" Look) */
    .date-badge {
        display: inline-block;
        color: #d1410c; /* Ticketmaster Orange/Red */
        font-weight: 700;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }

    /* TITLE */
    .event-title {
        font-size: 22px;
        font-weight: 800;
        color: #1a1a1a;
        margin: 0 0 10px 0;
        line-height: 1.3;
    }

    /* CATEGORY PILL */
    .category-pill {
        display: inline-block;
        background-color: #f2f2f2;
        color: #555;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 15px;
    }

    /* METADATA (Location) */
    .event-meta {
        color: #666;
        font-size: 14px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* SHARE BUTTONS (Clean & Minimal) */
    .share-row { margin-top: 15px; display: flex; gap: 10px; }
    .share-icon {
        text-decoration: none;
        color: #555;
        font-size: 12px;
        font-weight: 600;
        padding: 6px 12px;
        border: 1px solid #ddd;
        border-radius: 6px;
        transition: all 0.2s;
    }
    .share-icon:hover { background-color: #f7f7f7; border-color: #aaa; color: #333; }

    /* READ MORE BOX */
    .read-more-box {
        background: #f9f9f9;
        padding: 20px;
        border-top: 1px solid #eee;
        font-size: 15px;
        line-height:
