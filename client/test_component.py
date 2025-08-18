#!/usr/bin/env python3
"""
Simple test of the top skills component
"""

import streamlit as st
from components.top_skills import render_top_skills

def main():
    st.set_page_config(page_title="Top Skills Test", page_icon="🧪", layout="wide")
    
    st.title("🧪 Top Skills Component Test")
    
    try:
        render_top_skills()
        st.success("✅ Top Skills component rendered successfully!")
    except Exception as e:
        st.error(f"❌ Error rendering Top Skills component: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main()
