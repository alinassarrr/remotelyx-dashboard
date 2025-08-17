#!/usr/bin/env python3
"""
Test script to verify the RemotelyX Dashboard components work correctly.
"""

import sys
import traceback

def test_imports():
    """Test if all required packages can be imported."""
    print("🧪 Testing package imports...")
    
    try:
        import streamlit as st
        print(f"✅ Streamlit {st.__version__} imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Streamlit: {e}")
        return False
    
    try:
        import pandas as pd
        print(f"✅ Pandas {pd.__version__} imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Pandas: {e}")
        return False
    
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        print("✅ Plotly imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Plotly: {e}")
        return False
    
    try:
        import numpy as np
        print(f"✅ NumPy {np.__version__} imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import NumPy: {e}")
        return False
    
    return True

def test_data_generation():
    """Test if the sample data generation works."""
    print("\n🧪 Testing data generation...")
    
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("app", "app.py")
        app_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app_module)
        
        # Test the generate_sample_data function
        skills_data, trending_skills, seniority_data, jobs_data = app_module.generate_sample_data()
        
        print(f"✅ Skills data generated: {len(skills_data)} skills")
        print(f"✅ Trending skills generated: {len(trending_skills)} skills")
        print(f"✅ Seniority data generated: {len(seniority_data)} levels")
        print(f"✅ Job listings generated: {len(jobs_data)} jobs")
        
        return True
    except Exception as e:
        print(f"❌ Failed to generate sample data: {e}")
        traceback.print_exc()
        return False

def test_job_listings():
    """Test if job listings can be generated."""
    print("\n🧪 Testing job listings generation...")
    
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("app", "app.py")
        app_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app_module)
        
        # Test job listings generation
        _, _, _, jobs_data = app_module.generate_sample_data()
        
        if len(jobs_data) > 0:
            job = jobs_data[0]
            print(f"✅ Job listings generated: {len(jobs_data)} jobs")
            print(f"✅ Job has id: {job['id']}")
            print(f"✅ Job has title: {job['title']}")
            print(f"✅ Job has company: {job['company']}")
            print(f"✅ Job has location: {job['location']}")
            print(f"✅ Job has time_posted: {job['time_posted']}")
            print(f"✅ Job has seniority: {job['seniority']}")
            print(f"✅ Job has skills: {job['skills']}")
            print(f"✅ Job has salary: {job['salary']}")
            print(f"✅ Job has status: {job['status']}")
            print(f"✅ Sample job: {job['title']} at {job['company']}")
            print(f"✅ Skills: {', '.join(job['skills'][:3])}...")
            print(f"✅ Status: {job['status']}")
        else:
            print("❌ No job listings generated")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Failed to generate job listings: {e}")
        traceback.print_exc()
        return False

def test_chart_creation():
    """Test if charts can be created."""
    print("\n🧪 Testing chart creation...")
    
    try:
        import pandas as pd
        import plotly.express as px
        import plotly.graph_objects as go
        
        # Test horizontal bar chart
        skills_data = {'React': 45, 'Node.js': 38, 'Python': 32}
        df = pd.DataFrame(list(skills_data.items()), columns=['Skill', 'Jobs'])
        fig = px.bar(df, x='Jobs', y='Skill', orientation='h')
        print("✅ Horizontal bar chart created successfully")
        
        # Test donut chart
        seniority_data = {'Senior': 45, 'Mid': 35, 'Junior': 20}
        fig_donut = go.Figure(data=[go.Pie(
            labels=list(seniority_data.keys()),
            values=list(seniority_data.values()),
            hole=0.6
        )])
        print("✅ Donut chart created successfully")
        
        return True
    except Exception as e:
        print(f"❌ Failed to create charts: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🚀 RemotelyX Dashboard Test Suite")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_data_generation,
        test_job_listings,
        test_chart_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The dashboard is ready to run.")
        print("\nTo start the dashboard, run:")
        print("  source venv/bin/activate && streamlit run app.py")
        print("  # or use the launcher script:")
        print("  ./run_dashboard.sh")
        print("\n✨ Features Available:")
        print("  - Clean, professional dashboard design")
        print("  - Overview tab with metrics and charts")
        print("  - Job Listings tab with filtering")
        print("  - Exact HTML design replication")
        print("  - Interactive elements and animations")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 