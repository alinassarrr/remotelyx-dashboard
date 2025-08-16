# components/navbar.py
import streamlit as st

def render_navbar(header_data, theme_class):
    """
    Renders the main header for the RemotelyX Dashboard
    """
    # Add navbar container styling
    st.markdown(f"""
<style>
    /* Navbar container */
    .navbar-container {{
        background: var(--bg-secondary) !important;
        border-bottom: 1px solid var(--border-color);
        padding: 15px 30px;
        margin: -1rem -1rem 1rem -1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: background 0.3s ease, color 0.3s ease;
    }}

    /* Force children to inherit text color */
    .navbar-container * {{
        color: var(--text-primary) !important;
    }}

    /* Buttons inside Streamlit (optional clean-up) */
    .stButton > button {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}
</style>
""", unsafe_allow_html=True)

    
    # Create the navbar using Streamlit components instead of raw HTML
    with st.container():
        st.markdown('<div class="navbar-container">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        # Logo section
        st.markdown(f"""
        <div class="logo">
            <span style="font-size: 28px; font-weight: bold; color: var(--text-primary);">
                {header_data['logo']}<span style="color: var(--brand-blue); margin-left: 2px;">X</span>
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Search section
        st.markdown(f"""
        <div style="text-align: center;">
            <input type="text" class="global-search" placeholder="{header_data['search_placeholder']}" 
                   style="width: 100%; height: 42px; background: var(--input-bg); border: 1px solid var(--input-border); 
                          border-radius: 21px; padding: 0 20px; color: var(--text-primary); font-size: 14px;">
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Right section with notifications and user profile
        col_notif, col_user = st.columns([1, 2])
        
        with col_notif:
            # Notification badge
            st.markdown(f"""
            <div class="notification-badge" style="width: 42px; height: 42px; background: var(--input-bg); 
                                                border: 1px solid var(--input-border); border-radius: 50%; 
                                                display: flex; align-items: center; justify-content: center; 
                                                position: relative; cursor: pointer; color: var(--brand-purple); font-size: 18px;">
                🔔
                <span class="badge-count" style="position: absolute; top: -5px; right: -5px; 
                                               background: var(--brand-red); color: white; border-radius: 10px; 
                                               padding: 2px 7px; font-size: 11px; font-weight: bold;">
                    {header_data['user']['notifications']}
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        with col_user:
            # User profile
            st.markdown(f"""
            <div class="user-profile" style="display: flex; align-items: center; gap: 12px; padding: 8px 16px; 
                                           background: var(--input-bg); border: 1px solid var(--input-border); 
                                           border-radius: 25px; cursor: pointer;">
                <div class="avatar" style="width: 34px; height: 34px; background: linear-gradient(135deg, var(--brand-purple), var(--brand-purple-dark)); 
                                         border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                                         color: white; font-weight: bold; font-size: 14px;">
                    {header_data['user']['avatar']}
                </div>
                <span class="user-name" style="color: var(--text-primary); font-size: 14px; font-weight: 500;">
                    {header_data['user']['name']}
                </span>
                <span style="color: var(--text-muted);">▼</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Close the navbar container
    st.markdown('</div>', unsafe_allow_html=True)
