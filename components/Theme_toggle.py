import streamlit as st

def init_theme():
    """Initialize theme in session state if it doesn't exist"""
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'

def toggle_theme():
    """Toggle between light and dark themes"""
    init_theme()  # Ensure theme is initialized
    if st.session_state.theme == 'dark':
        st.session_state.theme = 'light'
    else:
        st.session_state.theme = 'dark'

def render_theme_button():
    """Render the theme toggle button"""
    # Initialize theme if not exists
    init_theme()
    
    # Apply theme using CSS injection with higher specificity
    theme_class = get_theme_class()
    current_theme = st.session_state.theme
    
    # Define theme colors based on current theme
    if current_theme == 'light':
        bg_color = "#f5f7fa"
        text_color = "#1c2127"
        card_bg = "#ffffff"
        border_color = "#e2e8f0"
    else:  # dark theme
        bg_color = "#111417"
        text_color = "#ffffff"
        card_bg = "#1c2127"
        border_color = "rgba(102, 254, 144, 0.2)"
    
    st.markdown(f"""
    <style>
        /* Force theme application with !important and higher specificity */
        div[data-testid="stAppViewContainer"] {{
            background-color: {bg_color} !important;
        }}
        
        .main .block-container {{
            background-color: {bg_color} !important;
        }}
        
        .stMarkdown {{
            color: {text_color} !important;
        }}
        
        .stText {{
            color: {text_color} !important;
        }}
        
        .stButton > button {{
            background-color: {card_bg} !important;
            color: {text_color} !important;
            border: 1px solid {border_color} !important;
        }}
        
        .stButton > button:hover {{
            background-color: {border_color} !important;
            opacity: 0.8;
        }}
        
        /* Theme toggle button styling */
        .theme-toggle-btn {{
            background: {card_bg} !important;
            color: {text_color} !important;
            border: 2px solid {border_color} !important;
            border-radius: 50% !important;
            width: 50px !important;
            height: 50px !important;
            font-size: 20px !important;
            transition: all 0.3s ease !important;
        }}
        
        .theme-toggle-btn:hover {{
            transform: scale(1.1) !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
        }}
        
        /* Additional Streamlit element overrides */
        .stMetric {{
            color: {text_color} !important;
        }}
        
        .stSubheader {{
            color: {text_color} !important;
        }}
        
        .stCaption {{
            color: {text_color} !important;
        }}
        
        /* Force background on all main containers */
        section[data-testid="stSidebar"] {{
            background-color: {card_bg} !important;
        }}
        
        div[data-testid="stVerticalBlock"] {{
            background-color: {bg_color} !important;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    # Create theme toggle button with custom styling
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        button_text = "🌙" if current_theme == 'light' else "☀️"
        button_help = "Switch to dark mode" if current_theme == 'light' else "Switch to light mode"
        
        if st.button(
            button_text,
            help=button_help,
            key="theme_toggle",
            use_container_width=False
        ):
            toggle_theme()
            st.rerun()
    
    # Display current theme status
    st.caption(f"Current theme: {current_theme.title()}")
    
    # Debug info (you can remove this later)
    st.write(f"Debug: Theme is {current_theme}")
    st.write(f"Debug: Background color set to {bg_color}")

def get_theme_class():
    """Get the current theme class for CSS styling"""
    init_theme()  # Always ensure theme is initialized
    return f"theme-{st.session_state.theme}"
