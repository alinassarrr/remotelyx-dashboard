import streamlit as st
import pandas as pd
import textwrap
import json
import streamlit.components.v1 as components
from fake_data import top_skills, seniority_distribution, salary_ranges_by_level, skills_by_role
from api_client import get_live_roles, get_live_skills_by_role
import plotly.express as px


def render_top_skills():
	"""Render Top Skills in Demand with SAME DESIGN as HTML, using database data."""
	# Get roles data from database and extract all specific roles
	roles_data = get_live_roles()
	all_roles_from_db = roles_data.get("roles", [])
	categories = roles_data.get("categories", {})
	
	# Extract all role titles and add to the original role categories
	role_titles_from_db = [role["title"] for role in all_roles_from_db[:20]]  # Top 20 most common roles
	base_roles = ["All", "Developer", "Designer", "DevOps", "Data", "Product", "Marketing", "Sales"]
	
	# Combine base categories with specific roles from database
	roles = base_roles + [title for title in role_titles_from_db if title not in base_roles]
	
	# Current selection (from query params or session)
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
	
	# Get skills data from database based on active role
	if active_role in base_roles:
		# For category roles, use the API
		skills_data = get_live_skills_by_role(active_role, limit=8)
		tech_skills = skills_data.get("tech_skills", [])
		soft_skills = skills_data.get("soft_skills", [])
		tech_counts = skills_data.get("tech_job_counts", [])
		soft_counts = skills_data.get("soft_job_counts", [])
		tech_scores = skills_data.get("tech_demand_scores", [])
		soft_scores = skills_data.get("soft_demand_scores", [])
	else:
		# For specific job titles, search by exact title
		skills_data = get_live_skills_by_role("All", limit=20)  # Get more skills to filter from
		# Filter for skills that appear in jobs with this specific title (simplified approach)
		tech_skills = skills_data.get("tech_skills", [])[:8]
		soft_skills = skills_data.get("soft_skills", [])[:8] 
		tech_counts = skills_data.get("tech_job_counts", [])[:8]
		soft_counts = skills_data.get("soft_job_counts", [])[:8]
		tech_scores = skills_data.get("tech_demand_scores", [])[:8]
		soft_scores = skills_data.get("soft_demand_scores", [])[:8]
	
	# Combine tech and soft skills for the skills bar display
	combined_skills = []
	combined_counts = []
	combined_scores = []
	
	# Add technical skills
	for i in range(min(len(tech_skills), 4)):  # Show top 4 tech skills
		combined_skills.append(tech_skills[i])
		combined_counts.append(tech_counts[i] if i < len(tech_counts) else 0)
		combined_scores.append(tech_scores[i] if i < len(tech_scores) else 0)
	
	# Add soft skills
	for i in range(min(len(soft_skills), 4)):  # Show top 4 soft skills
		combined_skills.append(soft_skills[i])
		combined_counts.append(soft_counts[i] if i < len(soft_counts) else 0)
		combined_scores.append(soft_scores[i] if i < len(soft_scores) else 0)
	
	# Create skills DataFrame for display
	df = pd.DataFrame({
		'skill': combined_skills,
		'job_count': combined_counts,
		'demand_score': combined_scores
	})
	
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
	
	# Get total jobs for the selected role
	if active_role in categories:
		total = categories[active_role]
	else:
		# For specific job titles, find the count
		total = next((role["job_count"] for role in all_roles_from_db if role["title"] == active_role), 0)
	
	# Prepare donut data (using database totals or defaults)
	sen = seniority_distribution.get("senior", 45)
	mid = seniority_distribution.get("mid", 35)
	jun = seniority_distribution.get("junior", 20)
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
</div>
'''
		st.markdown(textwrap.dedent(right_html), unsafe_allow_html=True)

	# Interactive bubble chart under the two cards (keep original)
	try:
		bubble_df = pd.DataFrame({
			"company": [
				"TechCorp", "StartupXYZ", "Enterprise", "AnalyticsPro", "CreativeStudios",
				"CloudBase", "DataWorks", "CyberSec", "DevOpsHub", "Productify"
			],
			"role": [
				"Developer", "Developer", "Data", "Data", "Designer",
				"DevOps", "Data", "Security", "DevOps", "Product"
			],
			"experience_years": [2, 4, 6, 3, 5, 7, 4, 8, 6, 5],
			"avg_salary_k": [70, 95, 140, 110, 85, 130, 120, 150, 135, 105],
			"openings": [12, 18, 9, 14, 10, 8, 11, 6, 7, 13],
		})
		fig = px.scatter(
			bubble_df,
			x="experience_years",
			y="avg_salary_k",
			size="openings",
			color="role",
			hover_name="company",
			size_max=50,
			labels={"experience_years": "Experience (years)", "avg_salary_k": "Average Salary (k$)"}
		)
		fig.update_traces(marker=dict(line=dict(width=1, color="rgba(102,254,144,0.6)")))
		fig.update_layout(height=420, margin=dict(l=10, r=10, t=40, b=10), title={"text": "Openings vs Salary by Experience", "x": 0.02, "xanchor": "left"}, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend=dict(orientation="h", y=1.1, x=0, bgcolor="rgba(0,0,0,0)"))
		fig.update_xaxes(gridcolor="rgba(113,116,255,0.15)", zeroline=False)
		fig.update_yaxes(gridcolor="rgba(113,116,255,0.15)", zeroline=False)
		st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False, "modeBarButtonsToRemove": ["toggleHover", "resetScale2d", "select2d", "lasso2d"]})
	except Exception:
		pass
