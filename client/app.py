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


def apply_theme(theme: str) -> None:
    """Inject CSS variables for the selected theme (dark/light)."""
    theme = "light" if theme == "light" else "dark"
    if theme == "light":
        theme_css = """
        <style>
        :root {
            --bg-primary: #f5f7fa;
            --bg-secondary: #ffffff;
            --bg-card: #ffffff;
            --text-primary: #1c2127;
            --text-secondary: rgba(28, 33, 39, 0.7);
            --text-muted: rgba(28, 33, 39, 0.5);
            --border-color: #e2e8f0;
            --border-hover: #cbd5e0;
            --input-bg: #f7fafc;
            --input-border: #e2e8f0;
            --chip-bg: #f7fafc;
            --chip-border: #e2e8f0;
            --skill-bar-bg: #f0f4f8;
            --shadow-color: rgba(0, 0, 0, 0.1);
            --brand-purple: #7174ff;
            --brand-blue: #66b9ff;
            --brand-green: #66fe90;
            --brand-red: #ff2e00;
            --brand-purple-dark: #47499e;
        }
        </style>
        """
    else:
        theme_css = """
        <style>
        :root {
            --bg-primary: #111417;
            --bg-secondary: #1c2127;
            --bg-card: #1c2127;
            --text-primary: #ffffff;
            --text-secondary: rgba(255, 255, 255, 0.7);
            --text-muted: rgba(255, 255, 255, 0.5);
            --border-color: rgba(102, 254, 144, 0.2);
            --border-hover: rgba(102, 254, 144, 0.4);
            --input-bg: rgba(113, 116, 255, 0.1);
            --input-border: rgba(113, 116, 255, 0.3);
            --chip-bg: rgba(113, 116, 255, 0.1);
            --chip-border: rgba(113, 116, 255, 0.3);
            --skill-bar-bg: rgba(113, 116, 255, 0.1);
            --shadow-color: rgba(0, 0, 0, 0.3);
            --brand-purple: #7174ff;
            --brand-blue: #66b9ff;
            --brand-green: #66fe90;
            --brand-red: #ff2e00;
            --brand-purple-dark: #47499e;
        }
        </style>
        """
    st.markdown(theme_css, unsafe_allow_html=True)


def get_current_theme() -> str:
    raw = st.query_params.get("theme") if hasattr(st, "query_params") else None
    value = None
    if raw is not None:
        # Query param may be a list or a string
        if isinstance(raw, (list, tuple)):
            value = raw[-1] if raw else None
        else:
            value = str(raw)
    if value in ("light", "dark"):
        st.session_state["theme"] = value
    theme = st.session_state.get("theme", "dark")
    if theme not in ("light", "dark"):
        theme = "dark"
    return theme


def main():
    # Select and persist theme from query params robustly
    current_theme = get_current_theme()

    # Load CSS and apply theme overrides
    load_css()
    apply_theme(current_theme)

    # Render navbar (pass current theme)
    render_navbar(header_data, current_theme)
    
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
