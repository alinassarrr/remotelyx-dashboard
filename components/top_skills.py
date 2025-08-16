import streamlit as st
import pandas as pd
import plotly.express as px

def render_top_skills():
    """
    Renders the top skills demand visualization with seniority levels
    """
    st.subheader("🔥 Top Skills in Demand")
    
    # Sample data - replace with actual data from your backend
    skills_data = {
        'skill': ['Python', 'JavaScript', 'React', 'AWS', 'Docker', 'Kubernetes', 'SQL', 'Git'],
        'demand_score': [95, 88, 82, 78, 75, 72, 68, 65],
        'seniority': ['Senior', 'Mid-level', 'Senior', 'Senior', 'Mid-level', 'Senior', 'Mid-level', 'Mid-level'],
        'job_count': [156, 142, 128, 98, 87, 76, 134, 89]
    }
    
    df = pd.DataFrame(skills_data)
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["📊 Demand Overview", "🎯 By Seniority", "📈 Job Count"])
    
    with tab1:
        # Bar chart of top skills by demand score
        fig = px.bar(
            df.head(8), 
            x='skill', 
            y='demand_score',
            color='demand_score',
            color_continuous_scale='viridis',
            title="Top Skills by Demand Score"
        )
        fig.update_layout(
            xaxis_title="Skills",
            yaxis_title="Demand Score",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Group by seniority and show average demand
        seniority_stats = df.groupby('seniority')['demand_score'].mean().reset_index()
        seniority_stats = seniority_stats.sort_values('demand_score', ascending=False)
        
        fig2 = px.pie(
            seniority_stats,
            values='demand_score',
            names='seniority',
            title="Demand Distribution by Seniority Level"
        )
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
        
        # Show detailed breakdown
        st.subheader("📋 Detailed Breakdown")
        for _, row in seniority_stats.iterrows():
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write(f"**{row['seniority']}**")
            with col2:
                st.metric("Avg Demand", f"{row['demand_score']:.1f}")
    
    with tab3:
        # Scatter plot of demand vs job count
        fig3 = px.scatter(
            df,
            x='demand_score',
            y='job_count',
            size='job_count',
            color='seniority',
            hover_name='skill',
            title="Demand Score vs Job Count by Seniority"
        )
        fig3.update_layout(
            xaxis_title="Demand Score",
            yaxis_title="Job Count",
            height=400
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    # Skills table
    st.subheader("📋 All Skills Data")
    st.dataframe(
        df.sort_values('demand_score', ascending=False),
        use_container_width=True,
        hide_index=True
    )
