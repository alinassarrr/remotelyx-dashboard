import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import random
import hashlib
import time

# Page configuration
st.set_page_config(
    page_title="RemotelyX Dashboard",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sample users (in production, this would be in a database)
USERS = {
    "admin": "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9",  # admin123
    "racile": "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f",  # password123
    "demo": "ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a1dc30e73f",   # secret123
    "user": "2c70e12b7a0646f92279f427c7b38e7334d8e5389cff167a1dc30e73f826b683"   # hello123
}

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_login(username, password):
    """Verify user credentials"""
    if username in USERS:
        hashed_password = hash_password(password)
        return USERS[username] == hashed_password
    return False

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'login_error' not in st.session_state:
    st.session_state.login_error = ""
if 'username' not in st.session_state:
    st.session_state.username = ""

# Authentication check - show login page if not authenticated
if not st.session_state.authenticated:
    # Login page CSS
    st.markdown("""
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
            --shadow-color: rgba(0, 0, 0, 0.3);
            --brand-purple: #7174ff;
            --brand-blue: #66b9ff;
            --brand-green: #66fe90;
            --brand-red: #ff2e00;
        }
        
        .main { 
            background: linear-gradient(135deg, var(--bg-primary) 0%, #1a1d23 100%);
            color: var(--text-primary); 
            min-height: 100vh;
            padding: 0 !important;
        }
        .stApp { 
            background: linear-gradient(135deg, var(--bg-primary) 0%, #1a1d23 100%);
        }
        
        .login-container {
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 20px;
        }
        
        .login-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 60px 50px;
            width: 100%;
            max-width: 450px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }
        
        .login-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--brand-purple), var(--brand-blue), var(--brand-green));
        }
        
        .logo-section {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .logo {
            font-size: 48px;
            font-weight: bold;
            color: var(--text-primary);
            margin-bottom: 16px;
        }
        
        .logo .x {
            color: var(--brand-blue);
        }
        
        .logo-subtitle {
            color: var(--text-muted);
            font-size: 16px;
            margin-bottom: 8px;
        }
        
        .welcome-text {
            color: var(--text-secondary);
            font-size: 18px;
            margin-bottom: 40px;
            text-align: center;
        }
        
        .demo-accounts {
            margin-top: 40px;
            padding-top: 30px;
            border-top: 1px solid var(--border-color);
        }
        
        .demo-title {
            color: var(--text-secondary);
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 16px;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .error-message {
            background: rgba(255, 46, 0, 0.1);
            border: 1px solid rgba(255, 46, 0, 0.3);
            color: var(--brand-red);
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 14px;
        }
        
        /* Hide sidebar for login */
        .css-1d391kg, .css-1rs6os, .css-17eq0hr, .css-1v0mbdj {
            display: none !important;
        }
        
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        
        /* Streamlit input overrides */
        .stTextInput > div > div > input {
            background: var(--input-bg) !important;
            border: 1px solid var(--input-border) !important;
            border-radius: 12px !important;
            color: var(--text-primary) !important;
            padding: 16px 20px !important;
            font-size: 16px !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: var(--brand-purple) !important;
            box-shadow: 0 0 0 3px rgba(113, 116, 255, 0.1) !important;
        }
        
        .stButton > button {
            width: 100% !important;
            padding: 16px 24px !important;
            background: linear-gradient(135deg, var(--brand-purple), var(--brand-blue)) !important;
            border: none !important;
            border-radius: 12px !important;
            color: white !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            margin-top: 8px !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(113, 116, 255, 0.3) !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Login page layout
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="login-card">
            <div class="logo-section">
                <div class="logo">Remotely<span class="x">X</span></div>
                <div class="logo-subtitle">Job Market Analytics Platform</div>
            </div>
            <div class="welcome-text">Welcome back! Please sign in to your account.</div>
        """, unsafe_allow_html=True)
        
        # Error message
        if st.session_state.login_error:
            st.markdown(f'<div class="error-message">{st.session_state.login_error}</div>', unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Enter your username", label_visibility="collapsed")
            password = st.text_input("Password", type="password", placeholder="Enter your password", label_visibility="collapsed")
            login_button = st.form_submit_button("Sign In")
            
            if login_button:
                if username and password:
                    if verify_login(username, password):
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.session_state.login_error = ""
                        st.success("Login successful! Redirecting to dashboard...")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.session_state.login_error = "❌ Invalid username or password. Please try again."
                else:
                    st.session_state.login_error = "⚠️ Please enter both username and password."
        
        # Demo accounts section
        st.markdown("""
        <div class="demo-accounts">
            <div class="demo-title">Quick Access - Demo Accounts</div>
        """, unsafe_allow_html=True)
        
        demo_accounts = [
            ("admin", "Administrator Access"),
            ("racile", "Manager Access"),
            ("demo", "Demo User"),
            ("user", "Standard User")
        ]
        
        for username, description in demo_accounts:
            if st.button(f"👤 {username} • {description}", key=f"demo_{username}", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.login_error = ""
                st.success(f"Logged in as {username}! Redirecting...")
                time.sleep(1)
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# If we reach here, user is authenticated - show the main dashboard

# Sample data generation
@st.cache_data
def generate_sample_data():
    # Skills data for charts
    skills_data = {
        'React': 45, 'Node.js': 38, 'Python': 32, 'AWS': 28, 'TypeScript': 24,
        'Vue.js': 35, 'Angular': 28, 'MongoDB': 25, 'PostgreSQL': 22
    }
    
    # Trending skills
    trending_skills = {
        'TypeScript': 25, 'Next.js': 18, 'GraphQL': 15, 'Tailwind CSS': 12, 'Rust': 10
    }
    
    # Seniority distribution
    seniority_data = {'Senior': 45, 'Mid': 35, 'Junior': 20}
    
    # Generate job listings
    job_titles = ['Senior Full-Stack Developer', 'Frontend Developer', 'Backend Engineer', 'DevOps Engineer', 
                  'UI/UX Designer', 'Product Manager', 'Data Scientist', 'Mobile Developer', 'QA Engineer']
    companies = ['TechCorp', 'SE Factory', 'Creative Studio', 'Enterprise Corp', 'StartupX', 'DataFlow Inc']
    locations = ['Remote', 'USA/Remote', 'Hybrid', 'On-site']
    skills_pool = ['React', 'Node.js', 'Python', 'AWS', 'TypeScript', 'Vue.js', 'Angular', 'MongoDB', 'PostgreSQL', 'Docker', 'Kubernetes', 'GraphQL']
    statuses = ['New', 'Analyzed', 'Matched']
    seniority_levels = ['Junior', 'Mid', 'Senior']
    
    jobs_data = []
    for i in range(1, 157):
        job = {
            'id': i,
            'title': random.choice(job_titles),
            'company': random.choice(companies),
            'location': random.choice(locations),
            'time_posted': f"{random.randint(1, 7)} days ago",
            'seniority': random.choice(seniority_levels),
            'skills': random.sample(skills_pool, random.randint(3, 6)),
            'salary': f"${random.randint(40, 120)}k - ${random.randint(60, 150)}k",
            'status': random.choice(statuses),
            'description': 'Looking for an experienced developer to join our dynamic team...'
        }
        jobs_data.append(job)
    
    return skills_data, trending_skills, seniority_data, jobs_data

# Load data
skills_data, trending_skills, seniority_data, jobs_data = generate_sample_data()

# CSS - Dashboard styles
st.markdown("""
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
        --shadow-color: rgba(0, 0, 0, 0.3);
        --brand-purple: #7174ff;
        --brand-blue: #66b9ff;
        --brand-green: #66fe90;
        --brand-red: #ff2e00;
        --brand-purple-dark: #47499e;
    }
    
    .main { background-color: var(--bg-primary); color: var(--text-primary); }
    .stApp { background-color: var(--bg-primary); }
    .css-1d391kg { background-color: var(--bg-primary); }
    
    /* Header */
    .header {
        background: var(--bg-secondary);
        border-bottom: 1px solid var(--border-color);
        padding: 20px 30px;
        margin-bottom: 0;
    }
    .header-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 100%;
    }
    .logo { font-size: 28px; font-weight: bold; color: var(--text-primary); }
    .logo .x { color: var(--brand-blue); }
    .header-right { display: flex; gap: 20px; align-items: center; }
    .last-updated {
        font-size: 12px; color: var(--text-muted); padding: 8px 16px;
        background: var(--input-bg); border-radius: 20px;
    }
    .theme-toggle {
        width: 42px; height: 42px; background: var(--input-bg);
        border: 1px solid var(--input-border); border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        cursor: pointer; transition: all 0.3s ease; color: var(--brand-purple);
    }
    .user-profile {
        display: flex; align-items: center; gap: 12px; padding: 8px 16px;
        background: var(--input-bg); border: 1px solid var(--input-border);
        border-radius: 25px; cursor: pointer;
    }
    .avatar {
        width: 34px; height: 34px;
        background: linear-gradient(135deg, var(--brand-purple), var(--brand-purple-dark));
        border-radius: 50%; display: flex; align-items: center; justify-content: center;
        color: white; font-weight: bold; font-size: 14px;
    }
    
    /* Sidebar */
    .sidebar-content {
        background: var(--bg-secondary); padding: 25px 20px; border-radius: 12px;
        border: 1px solid var(--border-color); margin-bottom: 20px;
    }
    .sidebar-title {
        font-size: 16px; font-weight: 600; color: var(--text-primary);
        margin-bottom: 20px; text-transform: uppercase; letter-spacing: 0.5px;
    }
    .filter-group { margin-bottom: 20px; }
    .filter-label {
        display: block; font-size: 13px; color: var(--text-muted);
        margin-bottom: 8px; font-weight: 500; text-transform: uppercase;
    }
    
    /* Metrics */
    .metrics-container { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
    .metric-card {
        background: var(--bg-card); border: 1px solid var(--border-color);
        border-radius: 12px; padding: 24px; position: relative; overflow: hidden;
        transition: all 0.3s ease; box-shadow: 0 2px 4px var(--shadow-color);
    }
    .metric-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px var(--shadow-color); }
    .metric-card::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, var(--brand-purple), var(--brand-blue));
    }
    .metric-label {
        font-size: 11px; color: var(--text-muted); text-transform: uppercase;
        letter-spacing: 1px; margin-bottom: 12px; font-weight: 600;
    }
    .metric-value {
        font-size: 36px; font-weight: bold; color: var(--text-primary); margin-bottom: 10px;
    }
    .metric-change {
        font-size: 13px; color: var(--brand-green); display: flex; align-items: center; gap: 5px;
    }
    
    /* Charts */
    .charts-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-bottom: 30px; }
    .chart-card {
        background: var(--bg-card); border: 1px solid var(--border-color);
        border-radius: 12px; padding: 24px; box-shadow: 0 2px 4px var(--shadow-color);
    }
    .chart-title { font-size: 18px; font-weight: 600; color: var(--text-primary); margin-bottom: 20px; }
    
    /* Job Listings */
    .job-listings-header {
        display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;
    }
    .job-stats { display: flex; gap: 20px; align-items: center; margin-bottom: 20px; }
    .stat-item {
        padding: 8px 16px; background: var(--input-bg); border-radius: 20px;
        font-size: 12px; color: var(--text-muted);
    }
    
    /* Job Cards */
    .jobs-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 20px; }
    .job-card {
        background: var(--bg-card); border: 1px solid var(--border-color);
        border-radius: 12px; padding: 24px; cursor: pointer; transition: all 0.3s ease;
        position: relative; box-shadow: 0 2px 4px var(--shadow-color);
    }
    .job-card:hover {
        transform: translateY(-3px); box-shadow: 0 6px 16px var(--shadow-color);
        border-color: var(--brand-purple);
    }
    .job-status {
        position: absolute; top: 20px; right: 20px; padding: 5px 14px;
        border-radius: 16px; font-size: 11px; text-transform: uppercase;
        font-weight: 600; letter-spacing: 0.5px;
    }
    .job-status.new { background: rgba(102, 254, 144, 0.15); color: var(--brand-green); border: 1px solid var(--brand-green); }
    .job-status.analyzed { background: rgba(113, 116, 255, 0.15); color: var(--brand-purple); border: 1px solid var(--brand-purple); }
    .job-status.matched { background: rgba(102, 185, 255, 0.15); color: var(--brand-blue); border: 1px solid var(--brand-blue); }
    .job-title {
        font-size: 18px; font-weight: 600; margin-bottom: 8px;
        color: var(--text-primary); padding-right: 80px;
    }
    .job-company { font-size: 14px; color: var(--text-secondary); margin-bottom: 16px; }
    .job-meta {
        display: flex; gap: 20px; margin-bottom: 16px;
        font-size: 13px; color: var(--text-muted);
    }
    .job-skills {
        display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px;
    }
    .skill-chip {
        padding: 4px 10px; background: var(--chip-bg); border: 1px solid var(--chip-border);
        border-radius: 12px; font-size: 11px; color: var(--text-secondary);
    }
    .job-salary {
        font-size: 16px; font-weight: 600; color: var(--brand-green); margin-bottom: 16px;
    }
    .job-actions { display: flex; gap: 12px; }
    .job-btn {
        padding: 8px 16px; border-radius: 8px; font-size: 12px; font-weight: 500;
        cursor: pointer; transition: all 0.3s ease; border: none;
    }
    .btn-save { background: var(--input-bg); color: var(--text-secondary); }
    .btn-analyze { background: var(--brand-purple); color: white; }
    .btn-details { background: var(--brand-green); color: var(--bg-primary); }
    
    /* Streamlit Overrides */
    .stSelectbox > div > div { background-color: var(--input-bg) !important; border: 1px solid var(--input-border) !important; }
    .stButton > button {
        background-color: var(--input-bg) !important; color: var(--text-secondary) !important;
        border: 1px solid var(--input-border) !important; border-radius: 8px !important;
    }
    .stButton > button[data-testid*="primary"] {
        background-color: var(--brand-purple) !important; color: white !important;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important; color: var(--text-secondary) !important;
        border-radius: 0 !important; padding: 16px 32px !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: rgba(113, 116, 255, 0.1) !important; color: var(--text-primary) !important;
        border-bottom: 3px solid var(--brand-purple) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for dashboard
if 'selected_skills' not in st.session_state:
    st.session_state.selected_skills = ['React']
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'grid'

# Header with logout functionality
st.markdown("""
<div class="header">
    <div class="header-content">
        <div class="logo">Remotely<span class="x">X</span></div>
        <div class="header-right">
            <span class="last-updated">Last updated: 2 mins ago</span>
            <div class="theme-toggle">🌙</div>
            <div class="user-profile">
                <div class="avatar">""" + (st.session_state.username[0].upper() if st.session_state.username else "U") + """</div>
                <span style="color: var(--text-primary); font-weight: 500;">""" + (st.session_state.username.title() if st.session_state.username else "User") + """</span>
                <span style="color: var(--text-muted);">▼</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Logout button in sidebar
with st.sidebar:
    st.markdown("---")
    if st.button("🚪 Logout", type="secondary", use_container_width=True):
        # Clear authentication
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.login_error = ""
        st.success("✅ Logged out successfully!")
        st.rerun()

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(["📊 Overview", "💼 Job Listings", "📈 Reports"])

with tab1:
    # Sidebar Filters
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">Dashboard Filters</div>', unsafe_allow_html=True)
        
        date_range = st.selectbox("📅 Date Range", ["1 day", "1 week", "1 month", "Custom"], index=1)
        role_type = st.selectbox("💼 Role Type", ["All Roles", "Developer", "Designer", "Product Manager", "DevOps"])
        
        st.markdown('<div class="filter-label">Seniority</div>', unsafe_allow_html=True)
        seniority_cols = st.columns(3)
        with seniority_cols[0]:
            st.button("Junior", type="secondary")
        with seniority_cols[1]:
            st.button("Mid", type="primary")
        with seniority_cols[2]:
            st.button("Senior", type="primary")
        
        st.markdown('<div class="filter-label">Skills</div>', unsafe_allow_html=True)
        new_skill = st.text_input("Type to filter...", placeholder="Add skills...")
        
        if st.session_state.selected_skills:
            for skill in st.session_state.selected_skills:
                st.markdown(f'<div style="display: inline-block; margin: 2px; padding: 4px 8px; background: var(--chip-bg); border-radius: 12px; font-size: 12px;">{skill}</div>', unsafe_allow_html=True)
        
        company = st.text_input("🏢 Company", placeholder="All companies")
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("Apply Filters", type="primary")
        with col2:
            st.button("Clear", type="secondary")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Filter
    st.text_input("🔍 Quick Filter", placeholder="Filter dashboard by job title, skill, or company", label_visibility="collapsed")
    
    # Metrics
    st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = [
        ("Active Jobs", "156", "↑ 12% from last week"),
        ("New This Week", "28", "↑ 8 more than usual"),
        ("Avg Processing", "2.3d", "↓ 0.5 days faster"),
        ("Success Rate", "87%", "↑ 3% improvement")
    ]
    
    for i, (label, value, change) in enumerate(metrics):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-change">{change}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts
    st.markdown('<div class="charts-grid">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Top Skills in Demand</div>', unsafe_allow_html=True)
        
        skills_df = pd.DataFrame(list(skills_data.items()), columns=['Skill', 'Jobs'])
        fig_skills = px.bar(skills_df, x='Jobs', y='Skill', orientation='h', 
                           color='Jobs', color_continuous_scale='Purples', title="")
        fig_skills.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'), showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0), height=400
        )
        st.plotly_chart(fig_skills, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Seniority Distribution</div>', unsafe_allow_html=True)
        
        fig_seniority = go.Figure(data=[go.Pie(
            labels=list(seniority_data.keys()), values=list(seniority_data.values()),
            hole=0.6, marker_colors=['#7174ff', '#66b9ff', '#47499e']
        )])
        fig_seniority.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'), showlegend=True, height=300,
            margin=dict(l=0, r=0, t=20, b=0)
        )
        st.plotly_chart(fig_seniority, use_container_width=True, config={'displayModeBar': False})
        
        # Trending Skills
        st.markdown('<div style="margin-top: 20px;">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title" style="font-size: 14px;">Top Trending Skills</div>', unsafe_allow_html=True)
        for skill, pct in trending_skills.items():
            st.markdown(f'<div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid var(--border-color);"><span style="color: var(--text-primary);">{skill}</span><span style="color: var(--brand-green); font-weight: 600;">↑ {pct}%</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    # Job Listings Header
    st.markdown("""
    <div class="job-listings-header">
        <h2 style="color: var(--text-primary); margin: 0;">Job Listings</h2>
        <div style="background: var(--input-bg); padding: 8px 16px; border-radius: 20px; font-size: 14px;">
            156 Total Jobs
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Job Stats
    st.markdown("""
    <div class="job-stats">
        <div class="stat-item">Showing 1-12 of 156 jobs</div>
        <div class="stat-item">New (12)</div>
        <div class="stat-item">Analyzed (45)</div>
        <div class="stat-item">Matched (99)</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Search and Controls
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        search_query = st.text_input("Search jobs", placeholder="🔍 Quick search jobs...", label_visibility="collapsed")
    with col2:
        sort_by = st.selectbox("Sort by", ["Newest", "Relevance", "Salary", "Company"], label_visibility="collapsed")
    with col3:
        view_mode = st.selectbox("View", ["Grid View", "Table View"], label_visibility="collapsed")
    
    # Job Cards Grid
    st.markdown('<div class="jobs-grid">', unsafe_allow_html=True)
    
    # Display first 12 jobs
    for i in range(0, min(12, len(jobs_data)), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(jobs_data):
                job = jobs_data[i + j]
                with col:
                    st.markdown(f"""
                    <div class="job-card">
                        <div class="job-status {job['status'].lower()}">{job['status']}</div>
                        <div class="job-title">{job['title']}</div>
                        <div class="job-company">{job['company']}</div>
                        <div class="job-meta">
                            <span>📍 {job['location']}</span>
                            <span>⏰ {job['time_posted']}</span>
                            <span>👤 {job['seniority']}</span>
                        </div>
                        <div class="job-skills">
                            {' '.join([f'<div class="skill-chip">{skill}</div>' for skill in job['skills'][:4]])}
                        </div>
                        <div class="job-salary">{job['salary']}</div>
                        <div class="job-actions">
                            <button class="job-btn btn-save">Save</button>
                            <button class="job-btn btn-analyze">Analyze</button>
                            <button class="job-btn btn-details">Details</button>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Pagination
    st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; gap: 20px; margin-top: 30px;">
        <button style="padding: 8px 16px; background: var(--input-bg); border: 1px solid var(--input-border); border-radius: 8px; color: var(--text-secondary);">← Previous</button>
        <span style="color: var(--text-muted);">Page 1 of 13</span>
        <button style="padding: 8px 16px; background: var(--brand-purple); border: none; border-radius: 8px; color: white;">Next →</button>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown('<div style="text-align: center; padding: 60px 20px;">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: var(--text-primary);">📈 Reports & Analytics</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: var(--text-secondary); font-size: 16px;">Advanced reporting features coming soon...</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    f'<div style="text-align: center; color: var(--text-muted); font-size: 12px; padding: 20px;">Welcome back, {st.session_state.username if st.session_state.username else "User"}! | Dashboard updates every 2 minutes</div>',
    unsafe_allow_html=True
) 