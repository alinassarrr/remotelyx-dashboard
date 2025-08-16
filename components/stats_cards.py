import streamlit as st
import pandas as pd

def render_stats_cards():
    """
    Renders the main statistics cards showing key metrics
    """
    # Sample data - replace with actual data from your backend
    stats_data = {
        "active_jobs": 892,
        "new_this_week": 47,
        "avg_process_time": "3.2 days",
        "success_rate": 94.2
    }
    
    # Create four columns for the stats cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stats-card active-jobs">
            <div class="stats-icon">💼</div>
            <div class="stats-content">
                <div class="stats-number">{}</div>
                <div class="stats-label">Active Jobs</div>
            </div>
        </div>
        """.format(stats_data["active_jobs"]), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-card new-jobs">
            <div class="stats-icon">🆕</div>
            <div class="stats-content">
                <div class="stats-number">{}</div>
                <div class="stats-label">New This Week</div>
            </div>
        </div>
        """.format(stats_data["new_this_week"]), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stats-card avg-process">
            <div class="stats-icon">⏱️</div>
            <div class="stats-content">
                <div class="stats-number">{}</div>
                <div class="stats-label">Avg Process Time</div>
            </div>
        </div>
        """.format(stats_data["avg_process_time"]), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stats-card success-rate">
            <div class="stats-icon">📈</div>
            <div class="stats-content">
                <div class="stats-number">{}%</div>
                <div class="stats-label">Success Rate</div>
            </div>
        </div>
        """.format(stats_data["success_rate"]), unsafe_allow_html=True)
    
    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Trend indicators
    st.subheader("📊 Trends")
    trend_col1, trend_col2, trend_col3, trend_col4 = st.columns(4)
    
    with trend_col1:
        st.metric("Active Jobs", "892", "+12%", delta_color="normal")
    
    with trend_col2:
        st.metric("New Jobs", "47", "+8%", delta_color="normal")
    
    with trend_col3:
        st.metric("Process Time", "3.2 days", "-0.5 days", delta_color="inverse")
    
    with trend_col4:
        st.metric("Success Rate", "94.2%", "+2.1%", delta_color="normal")
