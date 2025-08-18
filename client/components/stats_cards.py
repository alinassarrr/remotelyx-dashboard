import streamlit as st
from live_data import get_metrics_data


def render_stats_cards():
	"""Render the metrics cards row using REAL DATABASE DATA."""
	# Get live metrics from database
	metrics_data = get_metrics_data()
	
	# Calculate additional metrics for display
	active_jobs = metrics_data.get('active_jobs', 0)
	new_this_week = metrics_data.get('new_this_week', 0)
	total_companies = metrics_data.get('total_companies', 0)
	total_skills = metrics_data.get('total_skills', 0)
	
	# Calculate percentage change (mock for now)
	change_percentage = round((new_this_week / max(active_jobs, 1)) * 100, 1)
	
	cards_html = f"""
	<div class="metrics-row">
		<div class="metric-card">
			<div class="metric-label">Active Jobs</div>
			<div class="metric-value">{active_jobs:,}</div>
			<div class="metric-change">↑ {new_this_week} new this week</div>
		</div>
		<div class="metric-card">
			<div class="metric-label">Total Companies</div>
			<div class="metric-value">{total_companies}</div>
			<div class="metric-change">hiring actively</div>
		</div>
		<div class="metric-card">
			<div class="metric-label">Tech Skills</div>
			<div class="metric-value">{total_skills}</div>
			<div class="metric-change">in demand</div>
		</div>
		<div class="metric-card">
			<div class="metric-label">Matching Percentage</div>
			<div class="metric-value">{metrics_data.get('match_rate', 0):.1f}%</div>
			<div class="metric-change">↑ {change_percentage}% this week</div>
		</div>
	</div>
	"""
	st.markdown(cards_html, unsafe_allow_html=True)
