#!/usr/bin/env python3
"""
Test script to verify the new top skills functionality
"""

import streamlit as st
from api_client import get_live_roles, get_live_skills_by_role

def test_top_skills_api():
    st.title("🧪 Top Skills API Test")
    
    st.header("1. Test Role Categories API")
    roles_data = get_live_roles()
    
    if roles_data:
        st.success("✅ Successfully fetched roles data!")
        st.json(roles_data)
        
        categories = roles_data.get("categories", {})
        st.subheader("Available Role Categories:")
        for role, count in categories.items():
            st.write(f"- **{role}**: {count} jobs")
    else:
        st.error("❌ Failed to fetch roles data")
    
    st.header("2. Test Skills by Role API")
    
    # Test different roles
    test_roles = ["All", "Developer", "Data", "Designer", "DevOps"]
    
    for role in test_roles:
        st.subheader(f"Testing {role} Role")
        skills_data = get_live_skills_by_role(role, limit=5)
        
        if skills_data:
            st.success(f"✅ Successfully fetched skills for {role}!")
            
            tech_skills = skills_data.get("tech_skills", [])
            soft_skills = skills_data.get("soft_skills", [])
            
            if tech_skills:
                st.write(f"**Tech Skills ({len(tech_skills)})**: {', '.join(tech_skills)}")
            else:
                st.write("No tech skills found")
                
            if soft_skills:
                st.write(f"**Soft Skills ({len(soft_skills)})**: {', '.join(soft_skills)}")
            else:
                st.write("No soft skills found")
        else:
            st.error(f"❌ Failed to fetch skills for {role}")
        
        st.markdown("---")

if __name__ == "__main__":
    st.set_page_config(page_title="Top Skills API Test", page_icon="🧪")
    test_top_skills_api()
