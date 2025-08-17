import streamlit as st


def render_sidebar():
	"""Minimal placeholder sidebar to re-establish structure."""
	with st.sidebar:
		st.markdown('<div class="sidebar-title" style="font-size:16px; font-weight:800;">Dashboard Filters</div>', unsafe_allow_html=True)
		# Simple, non-breaking controls (wire up later to data)
		date = st.selectbox("Date Range", ["1 day", "1 week", "1 month", "3 months", "6 months", "1 year"], index=1)
		role = st.selectbox("Role Type", ["All Roles", "Developer", "Designer", "Product Manager", "DevOps", "Data Scientist"]) 
		seniority = st.multiselect("Seniority", ["Junior", "Mid", "Senior"], default=["Mid", "Senior"]) 
		skills_q = st.text_input("Skills", placeholder="Search skills…")
		company_q = st.text_input("Company", placeholder="Search company…")
		salary = st.selectbox("Salary Range", ["All Ranges", "$40k - $60k", "$60k - $80k", "$80k - $100k", "$100k+"])
		col_a, col_b = st.columns(2)
		with col_a:
			st.button("Apply Filters")
		with col_b:
			st.button("Clear")

import streamlit as st
from fake_data import sidebar_ui


def render_sidebar():
	"""
	Renders the sidebar with classic selects/inputs and enhanced styling
	"""
	with st.sidebar:
		# Header
		st.markdown('<div class="sidebar-title">Dashboard Filters</div>', unsafe_allow_html=True)
		st.markdown('<div class="sidebar" style="width:340px;">', unsafe_allow_html=True)

		# Date Range
		st.markdown('<div class="section-title">Date Range</div>', unsafe_allow_html=True)
		date_labels = [o["label"] for o in sidebar_ui["date_ranges"]]
		default_idx = next((i for i, o in enumerate(sidebar_ui["date_ranges"]) if o.get("selected")), 0)
		date_range = st.selectbox("Date Range", date_labels, index=default_idx, label_visibility="collapsed")

		# Role Type
		st.markdown('<div class="section-title">Role Type</div>', unsafe_allow_html=True)
		role_type = st.selectbox("Role Type", sidebar_ui["role_types"], label_visibility="collapsed")

		# Seniority
		st.markdown('<div class="section-title">Seniority</div>', unsafe_allow_html=True)
		seniority_labels = [s["label"] for s in sidebar_ui["seniority"]]
		seniority_default = [s["label"] for s in sidebar_ui["seniority"] if s.get("active")]
		selected_seniority = st.multiselect("Seniority", seniority_labels, default=seniority_default, label_visibility="collapsed")

		# Skills
		st.markdown('<div class="section-title">Skills</div>', unsafe_allow_html=True)
		skills_query = st.text_input("Skills", placeholder="Search skills...", label_visibility="collapsed")
		skills_list = [s for s in sidebar_ui["skills_suggestions"] if (skills_query or "").lower() in s.lower()]
		selected_skills = st.multiselect("Skills options", skills_list, label_visibility="collapsed")

		# Company
		st.markdown('<div class="section-title">Company</div>', unsafe_allow_html=True)
		company_query = st.text_input("Company", placeholder=sidebar_ui["companies_placeholder"], label_visibility="collapsed")
		companies = [c for c in sidebar_ui.get("companies", []) if (company_query or "").lower() in c.lower()]
		selected_company = st.selectbox("Company options", companies or ["All Companies"], label_visibility="collapsed")

		# Salary Range
		st.markdown('<div class="section-title">Salary Range</div>', unsafe_allow_html=True)
		salary_range = st.selectbox("Salary Range", sidebar_ui["salary_ranges"], label_visibility="collapsed")

		# Actions
		col_a, col_b = st.columns([1, 1])
		with col_a:
			apply_clicked = st.button("Apply Filters")
		with col_b:
			clear_clicked = st.button("Clear")

		# Close inner wrapper
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
				"skills_selected": selected_skills,
				"company_query": (company_query or "").strip(),
				"company_selected": selected_company,
				"salary_range": salary_range,
			}
			st.rerun()

		if clear_clicked:
			if "filters" in st.session_state:
				st.session_state.pop("filters")
			st.rerun()

