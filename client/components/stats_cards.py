import streamlit as st
from fake_data import metrics_data


def render_stats_cards():
	"""Render the metrics cards row using the SAME DESIGN as index.html."""
	cards_html = f"""
	<div class="metrics-row">
		<div class="metric-card">
			<div class="metric-label">Active Jobs</div>
			<div class="metric-value">{metrics_data.get('active_jobs', '')}</div>
			<div class="metric-change">↑ {metrics_data.get('new_this_week', 0)} new this week</div>
		</div>
		<div class="metric-card">
			<div class="metric-label">New This Week</div>
			<div class="metric-value">{metrics_data.get('new_this_week', '')}</div>
			<div class="metric-change">↑ 8 more than usual</div>
		</div>
		<div class="metric-card">
			<div class="metric-label">Avg Processing</div>
			<div class="metric-value">{metrics_data.get('avg_process_time', '')}</div>
			<div class="metric-change">↓ faster than last week</div>
		</div>
		<div class="metric-card">
			<div class="metric-label">Success Rate</div>
			<div class="metric-value">{metrics_data.get('success_rate', '')}%</div>
			<div class="metric-change">↑ improved</div>
		</div>
	</div>
	"""
	st.markdown(cards_html, unsafe_allow_html=True)
