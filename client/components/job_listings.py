import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


def render_job_listings(key_prefix: str = ""):
	"""
	Renders the job listings in both table and card formats
	Multiple instances can be rendered by providing a unique key_prefix
	"""
	st.subheader("💼 Job Listings")
	
	# Sample job data - replace with actual data from your backend
	jobs_data = [
		{
			"id": "J001",
			"title": "Senior Python Developer",
			"company": "TechCorp Inc.",
			"location": "Remote",
			"type": "Full-time",
			"experience": "Senior",
			"salary": "$120k - $150k",
			"posted_date": "2024-01-15",
			"status": "Active",
			"applications": 24,
			"skills": ["Python", "Django", "AWS", "Docker"]
		},
		{
			"id": "J002",
			"title": "Frontend Engineer",
			"company": "StartupXYZ",
			"location": "San Francisco, CA",
			"type": "Full-time",
			"experience": "Mid-level",
			"salary": "$90k - $110k",
			"posted_date": "2024-01-14",
			"status": "Active",
			"applications": 18,
			"skills": ["React", "JavaScript", "TypeScript", "CSS"]
		},
		{
			"id": "J003",
			"title": "DevOps Specialist",
			"company": "Enterprise Solutions",
			"location": "Remote",
			"type": "Contract",
			"experience": "Senior",
			"salary": "$130k - $160k",
			"posted_date": "2024-01-13",
			"status": "Active",
			"applications": 15,
			"skills": ["Kubernetes", "Docker", "AWS", "Terraform"]
		},
		{
			"id": "J004",
			"title": "Data Scientist",
			"company": "Analytics Pro",
			"location": "New York, NY",
			"type": "Full-time",
			"experience": "Senior",
			"salary": "$140k - $170k",
			"posted_date": "2024-01-12",
			"status": "Active",
			"applications": 31,
			"skills": ["Python", "Machine Learning", "SQL", "Statistics"]
		}
	]
	
	df = pd.DataFrame(jobs_data)
	
	# View toggle with unique key
	view_mode = st.radio(
		"Select View:",
		["📊 Table View", "🎴 Card View"],
		horizontal=True,
		key=f"{key_prefix}job_listings_view_mode",
	)
	
	# Apply sidebar filters if present
	filtered_df = df.copy()
	filters = st.session_state.get("filters")
	if filters:
		# Date range: keep items within last N days relative to max date in data (or today)
		try:
			if filters.get("date_days"):
				# Coerce posted_date to datetime
				filtered_df["posted_date_dt"] = pd.to_datetime(filtered_df["posted_date"]) \
					.dt.tz_localize(None)
				cutoff = filtered_df["posted_date_dt"].max() - timedelta(days=int(filters["date_days"]))
				filtered_df = filtered_df[filtered_df["posted_date_dt"] >= cutoff].drop(columns=["posted_date_dt"])
		except Exception:
			pass
		
		# Role type: map to "type" when not "All Roles"
		role = filters.get("role_type")
		if role and role != "All Roles":
			filtered_df = filtered_df[filtered_df["type"].str.contains(role.split()[0], case=False, na=False)]
		
		# Statuses (any match)
		sel_status = filters.get("statuses") or []
		if sel_status:
			filtered_df = filtered_df[filtered_df["status"].isin(sel_status)]
		
		# Seniority (any match)
		sel_sen = filters.get("seniority") or []
		if sel_sen:
			filtered_df = filtered_df[filtered_df["experience"].isin(sel_sen)]
		
		# Skills/company text contains
		q = (filters.get("skills_query") or "").lower()
		if q:
			filtered_df = filtered_df[
				filtered_df["title"].str.lower().str.contains(q) |
				filtered_df["company"].str.lower().str.contains(q) |
				filtered_df["skills"].apply(lambda xs: any(q in s.lower() for s in xs))
			]
		cq = (filters.get("company_query") or "").lower()
		if cq:
			filtered_df = filtered_df[filtered_df["company"].str.lower().str.contains(cq)]
		
		# Salary band rough match
		band = filters.get("salary_range")
		if band and band != "All Ranges":
			filtered_df = filtered_df[filtered_df["salary"].str.contains(band.split()[0].replace("$", ""), na=False)]
	
	# Display based on view mode
	if view_mode == "📊 Table View":
		st.dataframe(
			filtered_df,
			use_container_width=True,
			hide_index=True,
			column_config={
				"skills": st.column_config.ListColumn("Required Skills"),
				"posted_date": st.column_config.DateColumn("Posted Date"),
				"applications": st.column_config.NumberColumn("Applications")
			}
		)
	else:  # Card View
		st.markdown("<br>", unsafe_allow_html=True)
		# Create a grid layout for cards
		cols = st.columns(2)
		for idx, (_, job) in enumerate(filtered_df.iterrows()):
			col_idx = idx % 2
			with cols[col_idx]:
				with st.container():
					st.markdown(f"""
					<div class="job-card">
						<div class="job-header">
							<h3>{job['title']}</h3>
							<span class="company">{job['company']}</span>
						</div>
						<div class="job-details">
							<p><strong>📍 Location:</strong> {job['location']}</p>
							<p><strong>💼 Type:</strong> {job['type']}</p>
							<p><strong>🎯 Experience:</strong> {job['experience']}</p>
							<p><strong>💰 Salary:</strong> {job['salary']}</p>
							<p><strong>📅 Posted:</strong> {job['posted_date']}</p>
							<p><strong>📊 Status:</strong> <span class="status-{job['status'].lower()}">{job['status']}</span></p>
							<p><strong>👥 Applications:</strong> {job['applications']}</p>
						</div>
						<div class="job-skills">
							<strong>🛠️ Skills:</strong>
							{', '.join(job['skills'])}
						</div>
						<div class="job-actions">
							<button class="btn-primary">View Details</button>
							<button class="btn-secondary">Quick Apply</button>
						</div>
					</div>
					""", unsafe_allow_html=True)
					st.markdown("<br>", unsafe_allow_html=True)
	
	# Summary stats
	st.divider()
	col1, col2, col3, col4 = st.columns(4)
	
	with col1:
		st.metric("Total Jobs", len(filtered_df))
	
	with col2:
		st.metric("Active Jobs", len(filtered_df[filtered_df['status'] == 'Active']))
	
	with col3:
		st.metric("Avg Applications", f"{filtered_df['applications'].mean():.1f}")
	
	with col4:
		st.metric("Latest Post", filtered_df['posted_date'].min() if not filtered_df.empty else "N/A")

