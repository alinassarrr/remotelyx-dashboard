import streamlit as st

def render_right_panel():
    """
    Renders the right panel with additional information and quick actions
    """
    with st.container():
        st.header("⚡ Quick Actions")
        
        # Action buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📝 New Job Post", type="primary"):
                st.info("Opening new job post form...")
            
            if st.button("📊 Generate Report"):
                st.info("Generating report...")
        
        with col2:
            if st.button("📧 Send Notifications"):
                st.info("Sending notifications...")
            
            if st.button("🔄 Refresh Data"):
                st.info("Refreshing dashboard data...")
        
        st.divider()
        
        # Recent activity
        st.subheader("🕒 Recent Activity")
        
        activities = [
            {"time": "2 min ago", "action": "New job posted", "details": "Senior Python Developer"},
            {"time": "15 min ago", "action": "Application received", "details": "Frontend Engineer"},
            {"time": "1 hour ago", "action": "Interview scheduled", "details": "DevOps Specialist"},
            {"time": "3 hours ago", "action": "Offer sent", "details": "Data Scientist"}
        ]
        
        for activity in activities:
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.caption(activity["time"])
                with col2:
                    st.write(f"**{activity['action']}**: {activity['details']}")
            st.divider()
        
        # System status
        st.subheader("🔧 System Status")
        st.success("✅ All systems operational")
        st.info("📡 Last sync: 2 minutes ago")
        st.warning("⚠️ 3 pending notifications")
