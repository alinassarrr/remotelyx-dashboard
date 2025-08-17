import streamlit as st
from fake_data import sidebar_ui
from fake_data import job_listings as FAKE_JOBS


def render_sidebar():
	"""
	Renders the sidebar with classic selects/inputs and enhanced styling
	to match the provided HTML design structure (labels, groups, chips, actions).
	"""
	with st.sidebar:
		st.markdown('<div class="sidebar">', unsafe_allow_html=True)
		st.markdown('<div class="sidebar-title">Dashboard Filters</div>', unsafe_allow_html=True)
		st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)

		# Date Range
		st.markdown('<div class="filter-group">', unsafe_allow_html=True)
		st.markdown('<label class="filter-label">Date Range</label>', unsafe_allow_html=True)
		date_labels = [o["label"] for o in sidebar_ui["date_ranges"]]
		default_idx = next((i for i, o in enumerate(sidebar_ui["date_ranges"]) if o.get("selected")), 0)
		date_range = st.selectbox("Date Range", date_labels, index=default_idx, label_visibility="collapsed")
		st.markdown('</div>', unsafe_allow_html=True)

		# Role Type
		st.markdown('<div class="filter-group">', unsafe_allow_html=True)
		st.markdown('<label class="filter-label">Role Type</label>', unsafe_allow_html=True)
		role_type = st.selectbox("Role Type", sidebar_ui["role_types"], label_visibility="collapsed")
		st.markdown('</div>', unsafe_allow_html=True)

		# Seniority (multiselect + visual chips)
		st.markdown('<div class="filter-group">', unsafe_allow_html=True)
		st.markdown('<label class="filter-label">Seniority</label>', unsafe_allow_html=True)
		seniority_labels = [s["label"] for s in sidebar_ui["seniority"]]
		seniority_default = [s["label"] for s in sidebar_ui["seniority"] if s.get("active")]
		selected_seniority = st.multiselect("Seniority", seniority_labels, default=seniority_default, label_visibility="collapsed")
		# Visual chips reflecting current selection
		chips_html = '<div class="filter-chips">' + ''.join(
			f'<div class="chip{" active" if lbl in selected_seniority else ""}">{lbl}</div>' for lbl in seniority_labels
		) + '</div>'
		st.markdown(chips_html, unsafe_allow_html=True)
		st.markdown('</div>', unsafe_allow_html=True)

		# Skills (search only + results)
		st.markdown('<div class="filter-group">', unsafe_allow_html=True)
		st.markdown('<label class="filter-label">Skills</label>', unsafe_allow_html=True)
		skills_query = st.text_input(
			"Skills",
			placeholder="Type to filter...",
			label_visibility="collapsed",
			key="sb_skills_input",
		)
		skills_list = [s for s in sidebar_ui["skills_suggestions"] if (skills_query or "").lower() in s.lower()]
		st.markdown('<div class="search-results">' + ''.join(f'<div class="search-result">{s}</div>' for s in skills_list[:6]) + '</div>', unsafe_allow_html=True)
		st.markdown('</div>', unsafe_allow_html=True)

		# Company (search only + results)
		st.markdown('<div class="filter-group">', unsafe_allow_html=True)
		st.markdown('<label class="filter-label">Company</label>', unsafe_allow_html=True)
		company_query = st.text_input(
			"Company",
			placeholder=sidebar_ui.get("companies_placeholder", "All Companies"),
			label_visibility="collapsed",
			key="sb_company_input",
		)
		# Build dynamic company suggestions from job listings if no static list provided
		static_companies = sidebar_ui.get("companies", []) or []
		if not static_companies:
			try:
				unique_companies = sorted({j.get("company", "").strip() for j in FAKE_JOBS if j.get("company")})
			except Exception:
				unique_companies = []
			companies = [c for c in unique_companies if (company_query or "").lower() in c.lower()]
		else:
			companies = [c for c in static_companies if (company_query or "").lower() in c.lower()]
		st.markdown('<div class="search-results">' + ''.join(f'<div class="search-result">{c}</div>' for c in companies[:6]) + '</div>', unsafe_allow_html=True)
		st.markdown('</div>', unsafe_allow_html=True)

		# Salary Range
		st.markdown('<div class="filter-group">', unsafe_allow_html=True)
		st.markdown('<label class="filter-label">Salary Range</label>', unsafe_allow_html=True)
		salary_range = st.selectbox("Salary Range", sidebar_ui["salary_ranges"], label_visibility="collapsed")
		st.markdown('</div>', unsafe_allow_html=True)

		# Close section wrapper
		st.markdown('</div>', unsafe_allow_html=True)

		# Actions
		st.markdown('<div class="filter-actions">', unsafe_allow_html=True)
		col_a, col_b = st.columns([1, 1])
		with col_a:
			apply_clicked = st.button("Apply Filters")
		with col_b:
			clear_clicked = st.button("Clear")
		st.markdown('</div>', unsafe_allow_html=True)

		# Close wrapper
		st.markdown('</div>', unsafe_allow_html=True)

		# Map date label to days for filtering
		label_to_days = {
			"1 day": 1,
			"1 week": 7,
			"1 month": 30,
			"3 months": 90,
			"6 months": 180,
			"1 year": 365,
		}

		if apply_clicked:
			st.session_state["filters"] = {
				"date_days": label_to_days.get(date_range),
				"role_type": role_type,
				"seniority": selected_seniority,
				"skills_query": (skills_query or "").strip(),
				"company_query": (company_query or "").strip(),
				"salary_range": salary_range,
			}
			st.rerun()

		if clear_clicked:
			if "filters" in st.session_state:
				st.session_state.pop("filters")
			st.rerun()

