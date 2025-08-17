import streamlit as st
from typing import List, Dict

# Data sources
from fake_data import trending_skills, hard_to_fill, recent_activity


def _render_trending(skills: List[Dict]):
	st.markdown("<div class='insights-section'>" \
				"<div class='insights-title'>Top Trending Skills</div>", unsafe_allow_html=True)
	for item in skills:
		skill = item.get("skill", "-")
		trend = str(item.get("trend", ""))
		is_negative = trend.strip().startswith("-")
		arrow = "↓" if is_negative else "↑"
		value = trend.replace("+", "").replace("-", "")
		cls = "trending-change negative" if is_negative else "trending-change"
		st.markdown(
			f"""
			<div class="trending-item">
				<span class="trending-skill">{skill}</span>
				<span class="{cls}">{arrow} {value}</span>
			</div>
			""",
			unsafe_allow_html=True,
		)
	st.markdown("</div>", unsafe_allow_html=True)


def _render_hard_to_fill(rows: List[Dict]):
	st.markdown("<div class='insights-section'>" \
				"<div class='insights-title'>Positions Taking Longest</div>", unsafe_allow_html=True)
	for row in rows:
		position = row.get("position", "-")
		days = row.get("days_open", "-")
		st.markdown(
			f"""
			<div class="trending-item">
				<span class="trending-skill">{position}</span>
				<span class="trending-change">{days} days avg</span>
			</div>
			""",
			unsafe_allow_html=True,
		)
	st.markdown("</div>", unsafe_allow_html=True)


def _render_activity(rows: List[Dict]):
	st.markdown("<div class='insights-section'>" \
				"<div class='insights-title'>Recent Updates</div>", unsafe_allow_html=True)
	for row in rows:
		action = row.get("action", "")
		details = row.get("details", "")
		time = row.get("time", "")
		body = f"{action}"
		if details:
			body += f" — {details}"
		st.markdown(
			f"""
			<div class="activity-item">
				{body}
				<div class="activity-time">{time}</div>
			</div>
			""",
			unsafe_allow_html=True,
		)
	st.markdown("</div>", unsafe_allow_html=True)


def render_right_panel():
	"""Render the right insights panel with tabs and fake data using a wrapper div."""
	# Open wrapper
	st.markdown("<div class='right-panel'>", unsafe_allow_html=True)

	tabs = st.tabs(["Trending", "Hard to Fill", "Activity"])
	with tabs[0]:
		_render_trending(trending_skills)
	with tabs[1]:
		_render_hard_to_fill(hard_to_fill)
	with tabs[2]:
		_render_activity(recent_activity)

	# Close wrapper
	st.markdown("</div>", unsafe_allow_html=True)


