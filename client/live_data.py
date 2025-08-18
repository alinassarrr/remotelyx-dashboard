# Live data for RemotelyX Dashboard - fetches from backend API
from api_client import get_live_jobs, get_live_filter_options, get_live_metrics, get_live_top_skills, get_api_client
import streamlit as st
from fake_data import (
    header_data, sidebar_ui, trending_skills, hard_to_fill, 
    recent_activity, seniority_distribution, salary_ranges_by_level, skills_by_role
)

# Header data (unchanged from fake_data)
header_data = header_data

# Get live filter options from API
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_sidebar_filters():
    """Get sidebar filter options from API"""
    filter_options = get_live_filter_options()
    
    return {
        "date_range": ["Last 7 days", "Last 30 days", "Last 90 days", "Custom"],
        "job_types": filter_options.get("employment_types", ["Full-time", "Part-time", "Contract", "Freelance"]),
        "experience_levels": filter_options.get("seniorities", ["Junior", "Mid", "Senior", "Lead", "Executive"]),
        "locations": filter_options.get("locations", ["Remote", "US", "Europe", "Asia"]),
        "skills": filter_options.get("tech_skills", ["Python", "JavaScript", "React", "AWS"])[:20]  # Top 20 skills
    }

# Cache the sidebar filters
sidebar_filters = get_sidebar_filters()

# Get live metrics data from API
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_metrics_data():
    """Get comprehensive metrics data from dashboard API (includes all counts)"""
    return get_live_metrics()

# Cache the metrics data
metrics_data = get_metrics_data()

# Get live top skills data from API
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_top_skills_data():
    """Get top skills data from API"""
    return get_live_top_skills()

# Cache the top skills data
top_skills = get_top_skills_data()

# Get live job listings from API
@st.cache_data(ttl=60)  # Cache for 1 minute (more frequent updates for jobs)
def get_job_listings(limit=50, **filters):
    """Get job listings from API with optional filters"""
    return get_live_jobs(limit=limit, **filters)

# Default job listings (cached)
job_listings = get_job_listings()

# Keep the static data that doesn't come from API yet
trending_skills = trending_skills
hard_to_fill = hard_to_fill  
recent_activity = recent_activity
seniority_distribution = seniority_distribution
salary_ranges_by_level = salary_ranges_by_level
skills_by_role = skills_by_role
sidebar_ui = sidebar_ui

# Helper function to refresh data
def refresh_live_data():
    """Clear cache and refresh all live data"""
    get_sidebar_filters.clear()
    get_metrics_data.clear()
    get_top_skills_data.clear()
    get_job_listings.clear()
    
    # Update global variables
    global sidebar_filters, metrics_data, top_skills, job_listings
    sidebar_filters = get_sidebar_filters()
    metrics_data = get_metrics_data()
    top_skills = get_top_skills_data()
    job_listings = get_job_listings()

# Check API connectivity and show status
def check_api_status():
    """Check if API is connected and show status"""
    client = get_api_client()
    health = client.health_check()
    
    if health.get("status") == "healthy":
        return True
    else:
        st.sidebar.error("❌ API Disconnected - Using cached data")
        return False
