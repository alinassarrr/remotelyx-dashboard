import streamlit as st


def render_stats_cards():
	"""Minimal placeholder cards area."""
	col1, col2, col3, col4 = st.columns(4)
	with col1:
		st.metric("Total Jobs", "1,247")
	with col2:
		st.metric("Active Jobs", "892")
	with col3:
		st.metric("Success Rate", "94.2%")
	with col4:
		st.metric("Avg Process", "3.2 days")


