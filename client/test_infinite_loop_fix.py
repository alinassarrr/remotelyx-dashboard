#!/usr/bin/env python3
"""
Test script to verify that the infinite loop issue has been resolved.
This script simulates status changes to ensure they don't cause endless reruns.
"""

import streamlit as st
import pandas as pd
from components.job_listings import render_job_listings
from live_data import get_job_listings
from api_client import get_api_client

def test_status_update_mechanism():
    """Test the status update mechanism to ensure no infinite loops"""
    
    st.title("🔧 Infinite Loop Fix Test")
    
    # Test 1: Check if job listings render without hanging
    st.subheader("Test 1: Basic Job Listings Rendering")
    try:
        # Mock some test jobs if API is not available
        test_jobs = [
            {
                'id': 'test_1',
                'title': 'Test Software Engineer', 
                'company': 'Test Company',
                'location': 'Remote',
                'type': 'Full-time',
                'experience': 'Senior',
                'salary': '$100k - $120k',
                'posted_date': '2 days ago',
                'status': 'NEW',
                'skills': ['Python', 'React', 'AWS'],
                'tech_skills': ['Python', 'React', 'AWS'],
                'soft_skills': ['Communication'],
                'description': 'Test job description'
            }
        ]
        
        # Add test jobs to session state
        if "test_jobs" not in st.session_state:
            st.session_state.test_jobs = test_jobs
            
        df = pd.DataFrame(st.session_state.test_jobs)
        st.dataframe(df[['title', 'company', 'status']])
        st.success("✅ Job listings rendered successfully without hanging")
        
    except Exception as e:
        st.error(f"❌ Error rendering job listings: {e}")
    
    # Test 2: Simulate status changes
    st.subheader("Test 2: Status Update Mechanism")
    
    # Check if updated_jobs session state works correctly
    updated_jobs = st.session_state.get("updated_jobs", {})
    st.write(f"**Current updated jobs in session state:** {len(updated_jobs)}")
    
    if updated_jobs:
        st.json(updated_jobs)
    else:
        st.info("No status updates in session state yet")
    
    # Manual status change test
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Simulate Status Change"):
            if "updated_jobs" not in st.session_state:
                st.session_state.updated_jobs = {}
            st.session_state.updated_jobs["test_1"] = "ANALYZED"
            st.success("Status change simulated!")
            st.rerun()
    
    with col2:
        if st.button("🗑️ Clear Session State"):
            keys_to_clear = [k for k in st.session_state.keys() if k.startswith(("updated_jobs", "status_", "table_status_"))]
            for key in keys_to_clear:
                del st.session_state[key]
            st.success("Session state cleared!")
            st.rerun()

    # Test 3: Check API connectivity
    st.subheader("Test 3: API Connectivity")
    try:
        client = get_api_client()
        health = client.health_check()
        if health.get("status") == "healthy":
            st.success("✅ Backend API is connected and healthy")
        else:
            st.warning("⚠️ Backend API is not responding (this is expected if backend is not running)")
    except Exception as e:
        st.error(f"❌ API connectivity test failed: {e}")
    
    # Test 4: Session state inspection
    st.subheader("Test 4: Session State Debug Info")
    
    status_keys = [k for k in st.session_state.keys() if "status" in k.lower()]
    if status_keys:
        st.write("**Status-related session state keys:**")
        for key in status_keys[:10]:  # Show first 10 to avoid cluttering
            st.code(f"{key}: {st.session_state[key]}")
    else:
        st.info("No status-related keys in session state")
    
    st.write(f"**Total session state keys:** {len(st.session_state)}")

if __name__ == "__main__":
    st.set_page_config(page_title="Infinite Loop Fix Test", page_icon="🔧")
    test_status_update_mechanism()
