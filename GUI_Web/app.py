#!/usr/bin/env python3
"""
SocialBoost Facebook AutoPoster v3 - Web GUI
Streamlit-based web interface for managing Facebook automated posting
"""

import os
import sys
from pathlib import Path
import streamlit as st

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Page configuration
st.set_page_config(
    page_title="SocialBoost v3",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .status-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 0.5rem 0;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""",
    unsafe_allow_html=True,
)

# Main header
st.markdown(
    '<div class="main-header">🚀 SocialBoost v3 - Facebook AutoPoster</div>',
    unsafe_allow_html=True,
)

# Sidebar navigation
with st.sidebar:
    st.image("https://via.placeholder.com/150x50?text=SocialBoost", use_column_width=True)
    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "📊 Control & Status",
            "📅 Programare",
            "📁 Assets",
            "✍️ Generare Text",
            "📝 Logs",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    env = {"CODESPACE_NAME": os.environ.get("CODESPACE_NAME", None)}
    st.caption(f"User: {os.environ.get('USER', 'unknown')}")
    st.caption(f"Environment: {'Codespaces' if env.get('CODESPACE_NAME') else 'Local'}")

# Load selected page
if page == "📊 Control & Status":
    from pages import control

    control.render()
elif page == "📅 Programare":
    from pages import schedule

    schedule.render()
elif page == "📁 Assets":
    from pages import assets

    assets.render()
elif page == "✍️ Generare Text":
    from pages import generate

    generate.render()
elif page == "📝 Logs":
    from pages import logs

    logs.render()
