import streamlit as st

def render_sidebar():
    """
    Renders the sidebar with navigation and filtering options
    """
    with st.sidebar:
        st.header("📊 Dashboard Controls")
        
        # Date range selector
        st.subheader("📅 Date Range")
        date_range = st.date_input(
            "Select Date Range",
            value=(st.date_input("Start Date"), st.date_input("End Date")),
            key="date_range"
        )
        
        # Job type filter
        st.subheader("💼 Job Type")
        job_types = st.multiselect(
            "Select Job Types",
            ["Full-time", "Part-time", "Contract", "Freelance"],
            default=["Full-time", "Contract"]
        )
        
        # Experience level filter
        st.subheader("🎯 Experience Level")
        experience_levels = st.multiselect(
            "Select Experience Levels",
            ["Entry", "Mid-level", "Senior", "Lead", "Executive"],
            default=["Mid-level", "Senior"]
        )
        
        # Location filter
        st.subheader("🌍 Location")
        locations = st.multiselect(
            "Select Locations",
            ["Remote", "US", "Europe", "Asia", "Other"],
            default=["Remote", "US"]
        )
        
        # Apply filters button
        if st.button("🔄 Apply Filters", type="primary"):
            st.success("Filters applied successfully!")
            
        st.divider()
        
        # Quick stats
        st.subheader("📈 Quick Stats")
        st.metric("Total Jobs", "1,247")
        st.metric("Active Jobs", "892")
        st.metric("Success Rate", "94.2%")
