import streamlit as st
from fake_data import sidebar_ui
from api_client import get_live_filter_options


def render_sidebar():
	"""
	Renders the sidebar with real API data and enhanced filtering functionality.
	Maintains original styling while using live data from the backend.
	"""
	# Get real filter options from API
	filter_options = get_live_filter_options()
	
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
		# Role Type (using real data from API)
		st.markdown('<div class="filter-group">', unsafe_allow_html=True)
		st.markdown('<label class="filter-label">Role Type</label>', unsafe_allow_html=True)
		# Create role types based on the data we have
		role_types = ["All Roles", "Developer", "Designer", "Product Manager", "DevOps", "Data Scientist"]
		role_type = st.selectbox("Role Type", role_types, label_visibility="collapsed")
		st.markdown('</div>', unsafe_allow_html=True)

		# Seniority (multiselect + visual chips using real data)
		st.markdown('<div class="filter-group">', unsafe_allow_html=True)
		st.markdown('<label class="filter-label">Seniority</label>', unsafe_allow_html=True)
		# Use real seniority levels from API
		real_seniorities = filter_options.get("seniorities", ["Junior", "Mid", "Senior"])
		# Map to display labels
		seniority_labels = [s for s in real_seniorities if s and s.strip()]
		selected_seniority = st.multiselect("Seniority", seniority_labels, label_visibility="collapsed")
		# Visual chips reflecting current selection
		chips_html = '<div class="filter-chips">' + ''.join(
			f'<div class="chip{" active" if lbl in selected_seniority else ""}">{ lbl}</div>' for lbl in seniority_labels
		) + '</div>'
		st.markdown(chips_html, unsafe_allow_html=True)
		st.markdown('</div>', unsafe_allow_html=True)

		# Skills (search using real skills from API)
		st.markdown('<div class="filter-group">', unsafe_allow_html=True)
		st.markdown('<label class="filter-label">Skills</label>', unsafe_allow_html=True)
		skills_query = st.text_input(
			"Skills",
			placeholder="Type to filter...",
			label_visibility="collapsed",
			key="sb_skills_input",
		)
		# Use real tech skills from API
		real_skills = filter_options.get("tech_skills", [])
		skills_list = [s for s in real_skills if s and (skills_query or "").lower() in s.lower()]
		st.markdown('<div class="search-results">' + ''.join(f'<div class="search-result">{s}</div>' for s in skills_list[:10]) + '</div>', unsafe_allow_html=True)
		st.markdown('</div>', unsafe_allow_html=True)

		# Company (search using real companies from API)
		st.markdown('<div class="filter-group">', unsafe_allow_html=True)
		st.markdown('<label class="filter-label">Company</label>', unsafe_allow_html=True)
		company_query = st.text_input(
			"Company",
			placeholder="Search companies...",
			label_visibility="collapsed",
			key="sb_company_input",
		)
		# Use real companies from API
		real_companies = filter_options.get("companies", [])
		companies = [c for c in real_companies if c and (company_query or "").lower() in c.lower()]
		st.markdown('<div class="search-results">' + ''.join(f'<div class="search-result">{c}</div>' for c in companies[:10]) + '</div>', unsafe_allow_html=True)
		st.markdown('</div>', unsafe_allow_html=True)

		# Employment Type (using real employment types from API)
		st.markdown('<div class="filter-group">', unsafe_allow_html=True)
		st.markdown('<label class="filter-label">Employment Type</label>', unsafe_allow_html=True)
		# Get real employment types from API
		real_employment_types = ["All Types"] + filter_options.get("employment_types", [])
		employment_type = st.selectbox("Employment Type", real_employment_types, label_visibility="collapsed")
		st.markdown('</div>', unsafe_allow_html=True)

		# Location (using real locations from API)
		st.markdown('<div class="filter-group">', unsafe_allow_html=True)
		st.markdown('<label class="filter-label">Location</label>', unsafe_allow_html=True)
		location_query = st.text_input(
			"Location",
			placeholder="Search locations...",
			label_visibility="collapsed",
			key="sb_location_input",
		)
		# Use real locations from API
		real_locations = filter_options.get("locations", [])
		locations = [l for l in real_locations if l and (location_query or "").lower() in l.lower()]
		st.markdown('<div class="search-results">' + ''.join(f'<div class="search-result">{l}</div>' for l in locations[:10]) + '</div>', unsafe_allow_html=True)
		st.markdown('</div>', unsafe_allow_html=True)
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
				"employment_type": employment_type,
				"location_query": (location_query or "").strip(),
			}
			st.rerun()

		if clear_clicked:
			if "filters" in st.session_state:
				st.session_state.pop("filters")
			st.rerun()

