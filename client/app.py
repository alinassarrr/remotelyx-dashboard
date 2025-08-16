import streamlit as st
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from components.navbar import render_navbar
from components.sidebar import render_sidebar
from components.rightpanel import render_right_panel
from components.stats_cards import render_stats_cards
from components.top_skills import render_top_skills
from components.job_listings import render_job_listings

from fake_data import header_data, sidebar_filters, metrics_data, top_skills, job_listings, trending_skills, hard_to_fill, recent_activity

# Page config
st.set_page_config(page_title="RemotelyX Dashboard", page_icon="🚀", layout="wide", initial_sidebar_state="expanded")

# Load CSS
def load_css():
    css_dir = os.path.join(os.path.dirname(__file__), 'assets')
    
    # Global styles
    try:
        with open(os.path.join(css_dir, 'styles.css')) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Global CSS file not found")
    
    # Component-specific styles
    css_files = [
        'navbar.css',
        'sidebar.css',
        'rightpanel.css',
        'stats_cards.css',
        'top_skills.css',
        'job_listings.css'
    ]
    
    for css_file in css_files:
        try:
            css_path = os.path.join(css_dir, 'component_styles', css_file)
            with open(css_path) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        except FileNotFoundError:
            st.warning(f"CSS file not found: {css_file}")

def main():
    # Load CSS
    load_css()
    
    # Get current theme class (default to light theme)
    theme_class = "theme-light"
    
    # Render navbar
    render_navbar(header_data, theme_class)
    
    # Layout
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        render_sidebar()
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        render_stats_cards()
        render_top_skills()
        render_job_listings()
    
    with col3:
        render_right_panel()

if __name__ == "__main__":
    main()
