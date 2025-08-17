import streamlit as st
import pandas as pd
import textwrap
import json
import streamlit.components.v1 as components
from fake_data import top_skills, seniority_distribution, salary_ranges_by_level, skills_by_role


def render_top_skills():
	"""Render Top Skills in Demand with SAME DESIGN as HTML, using fake data."""
	# Roles and current selection (from query params or session)
	roles = ["All", "Developer", "Designer", "DevOps", "Data", "Product", "Marketing", "Sales"]
	qp = st.query_params if hasattr(st, 'query_params') else {}
	raw = qp.get('top_role') if qp is not None else None
	if isinstance(raw, (list, tuple)):
		selected = raw[-1] if raw else None
	else:
		selected = str(raw) if raw is not None else None
	# Normalize selection (trim/case-insensitive match to known roles)
	selected_norm = None
	if selected is not None:
		try:
			val = selected.strip()
			for r in roles:
				if r.lower() == val.lower():
					selected_norm = r
					break
		except Exception:
			selected_norm = None
	active_role = selected_norm if selected_norm in roles else st.session_state.get("top_skills_role", "All")
	st.session_state["top_skills_role"] = active_role
	
	# Prepare top skills DataFrame
	df_all = pd.DataFrame(top_skills)
	df = df_all.copy()
	# If a specific role is selected and we have a mapping, filter the skills; 'All' restores full list
	if active_role and active_role != "All":
		allowed = skills_by_role.get(active_role, [])
		if allowed:
			df = df[df['skill'].isin(allowed)]
	else:
		df = df_all.copy()
	
	def pct(v):
		try:
			v = float(v)
			return max(0, min(100, v))
		except Exception:
			return 0
	
	skills_items_list = []
	for _, row in df.head(8).iterrows():
		name = row.get('skill', '')
		jobs = int(row.get('job_count', 0))
		width = pct(row.get('demand_score', 0))
		skills_items_list.append(
			f'<div class="skill-item" data-role="all"><span class="skill-name">{name}</span><div class="skill-bar"><div class="skill-fill" style="width: {width}%"></div><span class="skill-count">{jobs} jobs</span></div></div>'
		)
	skills_items = ''.join(skills_items_list)
	
	# Prepare donut data
	sen = seniority_distribution.get("senior", 45)
	mid = seniority_distribution.get("mid", 35)
	jun = seniority_distribution.get("junior", 20)
	total = seniority_distribution.get("total_jobs", 156)
	salary_sen = salary_ranges_by_level.get('Senior', '')
	salary_mid = salary_ranges_by_level.get('Mid', '')
	salary_jun = salary_ranges_by_level.get('Junior', '')
	
	# Build dropdown HTML for roles (server-side filter via query params)
	# Preserve existing query params for view/theme
	cur_view = qp.get('view') if qp is not None else None
	cur_theme = qp.get('theme') if qp is not None else None
	def href_for(role: str) -> str:
		parts = [f"top_role={role}"]
		if cur_view:
			val = cur_view[-1] if isinstance(cur_view, (list, tuple)) else str(cur_view)
			parts.append(f"view={val}")
		if cur_theme:
			val = cur_theme[-1] if isinstance(cur_theme, (list, tuple)) else str(cur_theme)
			parts.append(f"theme={val}")
		return "?" + "&".join(parts)
	dropdown_menu = ''.join(
		f'<a class="dropdown-item" href="{href_for(r)}" target="_self">{r}</a>' for r in roles
	)
	dropdown_html = (
		'<details class="role-filter-dropdown">'
		f'<summary class="dropdown-trigger"><span class="selected-role">{active_role}</span><span class="dropdown-arrow">▼</span></summary>'
		f'<div class="dropdown-menu">{dropdown_menu}</div>'
		'</details>'
	)
	
	# Two columns: left 2fr, right 1fr
	left_col, right_col = st.columns([2, 1], gap="large")
	
	with left_col:
		left_html = f'''
<div class="chart-card">
	<div class="chart-header">
		<div class="chart-title">Top Skills in Demand</div>
		{dropdown_html}
	</div>
	<div class="skills-list">
		{skills_items}
	</div>
</div>
'''
		st.markdown(textwrap.dedent(left_html), unsafe_allow_html=True)
		# No client-side script; anchors trigger a fast rerun with updated query param
	
	with right_col:
		right_html = f'''
<div class="chart-card">
	<div class="chart-title">Seniority Distribution &amp; Insights</div>
	<div class="seniority-stats">
		<div class="donut-chart-container">
			<div class="donut-chart">
				<svg width="200" height="200" viewBox="0 0 200 200">
					<path d="M 100 20 A 80 80 0 0 1 180 100" fill="none" stroke="var(--brand-purple)" stroke-width="40" stroke-linecap="round"/>
					<path d="M 180 100 A 80 80 0 0 1 100 180" fill="none" stroke="var(--brand-blue)" stroke-width="40" stroke-linecap="round"/>
					<path d="M 100 180 A 80 80 0 0 1 20 100" fill="none" stroke="var(--brand-purple-dark)" stroke-width="40" stroke-linecap="round"/>
					<path d="M 20 100 A 80 80 0 0 1 100 20" fill="none" stroke="var(--brand-purple)" stroke-width="40" stroke-linecap="round"/>
				</svg>
				<div class="donut-center">
					<div class="total-jobs">{total}</div>
					<div class="total-label">TOTAL JOBS</div>
				</div>
			</div>
			<div class="donut-legend">
				<div class="legend-item"><span class="legend-color senior"></span><span class="legend-text">Senior: {sen}%</span></div>
				<div class="legend-item"><span class="legend-color mid"></span><span class="legend-text">Mid: {mid}%</span></div>
				<div class="legend-item"><span class="legend-color junior"></span><span class="legend-text">Junior: {jun}%</span></div>
			</div>
		</div>
		<div class="salary-info">
			<div class="salary-title">Average Salary by Level</div>
			<div class="salary-ranges">
				<div class="salary-item"><span class="salary-level">Senior</span><span class="salary-amount">{salary_sen}</span></div>
				<div class="salary-item"><span class="salary-level">Mid</span><span class="salary-amount">{salary_mid}</span></div>
				<div class="salary-item"><span class="salary-level">Junior</span><span class="salary-amount">{salary_jun}</span></div>
			</div>
		</div>
	</div>
'''
		st.markdown(textwrap.dedent(right_html), unsafe_allow_html=True)
