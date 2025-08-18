import streamlit as st
import pandas as pd
from datetime import timedelta
from typing import List, Dict, Tuple
from urllib.parse import urlencode
import textwrap

# Import live data functions
from live_data import get_job_listings
from api_client import update_job_status


def _parse_date(df: pd.DataFrame) -> pd.DataFrame:
	if "posted_date" in df.columns:
		try:
			df = df.copy()
			df["posted_date_dt"] = pd.to_datetime(df["posted_date"], errors="coerce").dt.tz_localize(None)
		except Exception:
			pass
	return df


def _filter_jobs(df: pd.DataFrame, search: str | None) -> pd.DataFrame:
	if search:
		q = search.lower().strip()
		if q:
			df = df[
				df["title"].str.lower().str.contains(q)
				| df["company"].str.lower().str.contains(q)
				| df["location"].str.lower().str.contains(q)
				| df["skills"].apply(lambda xs: any(q in str(s).lower() for s in (xs or [])))
			]
	return df


def _apply_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
	"""Apply filters stored in st.session_state['filters'] to the jobs DataFrame."""
	filters = st.session_state.get("filters")
	if not filters:
		return df

	working = df.copy()

	# Date range (days)
	try:
		days = filters.get("date_days")
		if days and "posted_date_dt" in working:
			# Use the most recent posted date as the reference so fake data filters sensibly
			ref = pd.to_datetime(working["posted_date_dt"].max(), errors="coerce")
			if pd.notna(ref):
				cutoff = ref - pd.Timedelta(days=int(days))
				working = working[working["posted_date_dt"] >= cutoff]
	except Exception:
		pass

	# Company contains
	try:
		company_q = (filters.get("company_query") or "").strip().lower()
		if company_q:
			# Search across multiple fields when company search is provided
			def _matches_company_any(row) -> bool:
				return (
					company_q in str(row.get("title", "")).lower()
					or company_q in str(row.get("company", "")).lower()
					or company_q in str(row.get("location", "")).lower()
					or any(company_q in str(s).lower() for s in (row.get("skills", []) or []))
					or company_q in str(row.get("salary", "")).lower()
				)
			working = working[working.apply(_matches_company_any, axis=1)]
	except Exception:
		pass

	# Skills substring (also search all key fields when provided)
	try:
		skills_q = (filters.get("skills_query") or "").strip().lower()
		if skills_q:
			def _matches_skills_any(row) -> bool:
				return (
					skills_q in str(row.get("title", "")).lower()
					or skills_q in str(row.get("company", "")).lower()
					or skills_q in str(row.get("location", "")).lower()
					or any(skills_q in str(s).lower() for s in (row.get("skills", []) or []))
					or skills_q in str(row.get("salary", "")).lower()
				)
			working = working[working.apply(_matches_skills_any, axis=1)]
	except Exception:
		pass

	# Seniority mapping
	try:
		selected_levels = filters.get("seniority") or []
		if selected_levels:
			junior_keys = {"entry", "junior"}
			mid_keys = {"mid", "mid-level"}
			senior_keys = {"senior", "lead", "executive"}

			allowed: set[str] = set()
			if any(l.lower().startswith("junior") for l in selected_levels):
				allowed |= junior_keys
			if any(l.lower().startswith("mid") for l in selected_levels):
				allowed |= mid_keys
			if any(l.lower().startswith("senior") for l in selected_levels):
				allowed |= senior_keys

			def _exp_ok(v: str) -> bool:
				lv = str(v or "").lower()
				return any(k in lv for k in allowed) if allowed else True

			working = working[working["experience"].apply(_exp_ok)]
	except Exception:
		pass

	# Role type (best-effort mapping over title and skills)
	try:
		role_type = (filters.get("role_type") or "").strip()
		if role_type and role_type.lower() not in {"all roles", "all"}:
			role_map = {
				"developer": ["developer", "engineer", "frontend", "backend", "full", "mobile"],
				"designer": ["designer", "design", "ui", "ux"],
				"product manager": ["product"],
				"devops": ["devops", "sre", "site reliability", "infrastructure"],
				"data scientist": ["data", "ml", "machine", "ai", "analyst"],
			}
			needles = role_map.get(role_type.lower(), [])
			if needles:
				def _matches_role(row) -> bool:
					title = str(row.get("title", "")).lower()
					sk = [str(s).lower() for s in (row.get("skills", []) or [])]
					return any(any(n in title for n in needles) or any(n in s for s in sk) for n in needles)
				working = working[working.apply(_matches_role, axis=1)]
	except Exception:
		pass

	# Salary range contains (best-effort)
	try:
		salary_sel = filters.get("salary_range")
		if salary_sel and isinstance(salary_sel, str) and salary_sel.lower() != "all ranges":
			token = salary_sel.replace(" ", "").lower()
			working = working[working["salary"].str.replace(" ", "").str.lower().str.contains(token.split("-")[0].replace("+", ""))]
	except Exception:
		pass
		
	return working


def _sort_jobs(df: pd.DataFrame, sort_by: str) -> pd.DataFrame:
	# Supported: Newest First, Oldest First, Salary (High to Low/Low to High), Company A-Z
	if sort_by == "Newest First":
		if "posted_date_dt" in df:
			return df.sort_values("posted_date_dt", ascending=False)
	elif sort_by == "Oldest First":
		if "posted_date_dt" in df:
			return df.sort_values("posted_date_dt", ascending=True)
	elif sort_by.startswith("Salary"):
		# Parse the low end of salary range numbers for rough sorting
		def _low(s: str) -> float:
			# Expect like "$90k - $110k" -> 90
			try:
				num = str(s).split("-")[0].strip().replace("$", "").lower().replace("k", "")
				return float(num)
			except Exception:
				return -1.0

		df = df.copy()
		df["_salary_low"] = df["salary"].apply(_low)
		return df.sort_values("_salary_low", ascending=("Low" in sort_by)).drop(columns=["_salary_low"])
	elif sort_by == "Company A-Z":
		return df.sort_values("company", ascending=True)
	return df


def _paginate(df: pd.DataFrame, page: int, per_page: int) -> Tuple[pd.DataFrame, int, int]:
	total = len(df)
	start = (page - 1) * per_page
	end = min(start + per_page, total)
	return df.iloc[start:end], start + 1 if total else 0, end


def render_job_listings(key_prefix: str = ""):
	"""
	Render Job Listings with live data from the API.
	Includes header, search, view toggle, sort, pagination, and cards/table rendering.
	"""
	# Get live jobs data from API
	live_jobs = get_job_listings(limit=100)  # Get more jobs for better pagination
	if not live_jobs:
		# Fallback message if no API data
		st.warning("🔌 Backend API not available. Please check the connection.")
		return
	
	df = pd.DataFrame(live_jobs)
	df = _parse_date(df)

	# Keys for session state
	page_key = f"{key_prefix}jobs_page"
	pending_key = f"{key_prefix}jobs_page_pending"

	# Apply any pending page change BEFORE creating widgets
	if pending_key in st.session_state:
		st.session_state[page_key] = int(st.session_state[pending_key])
		del st.session_state[pending_key]

	# Ensure page key exists
	if page_key not in st.session_state:
		st.session_state[page_key] = 1

	# Controls state
	hdr_title_col, hdr_search_col, hdr_view_col = st.columns([3, 3, 2])
	# Read search from query params for HTML input
	def _get_qp_value(name: str) -> str:
		try:
			val = st.query_params.get(name)
			if isinstance(val, list):
				return str(val[0]) if val else ""
			return str(val) if val is not None else ""
		except Exception:
			return ""

	search = _get_qp_value("jobs_search")

	with hdr_search_col:
		# Native Streamlit input; on change, update query param and rerun
		def _update_search_qp():
			val = st.session_state.get(f"{key_prefix}jobs_search_input", "")
			try:
				st.query_params["jobs_search"] = val
			except Exception:
				try:
					qp = st.experimental_get_query_params()
					qp["jobs_search"] = [val]
					st.experimental_set_query_params(**qp)
				except Exception:
					pass
			try:
				st.rerun()
			except Exception:
				st.experimental_rerun()

		# Wrap the Streamlit input within jobs-controls to apply styling
		st.markdown('<div class="jobs-controls">', unsafe_allow_html=True)
		
		st.text_input(
			"",
			value=search,
			placeholder="Quick search jobs...",
			key=f"{key_prefix}jobs_search_input",
			label_visibility="collapsed",
			on_change=_update_search_qp,
		)
		st.markdown('</div>', unsafe_allow_html=True)
	# Determine current view from query params (card/table)
	view_param = None
	try:
		view_param = st.query_params.get("jobs_view")
		if isinstance(view_param, list):
			view_param = view_param[0] if view_param else None
	except Exception:
		view_param = None
	current_view = "card" if (not view_param or str(view_param).lower() not in {"card", "table"}) else str(view_param).lower()

	def _build_view_url(target_view: str) -> str:
		try:
			qp = dict(st.query_params)
			clean_qp: Dict[str, str] = {}
			for k, v in qp.items():
				if k == "jobs_view":
					continue
				if isinstance(v, list):
					if v:
						clean_qp[k] = str(v[-1])
				else:
					clean_qp[k] = str(v)
			clean_qp["jobs_view"] = target_view
			return "?" + urlencode(clean_qp)
		except Exception:
			return f"?jobs_view={target_view}"

	with hdr_view_col:
		# Custom view toggle to match design
		toggle_html = textwrap.dedent(
			f"""
			<div class=\"view-toggle\">
				<a class=\"toggle-btn{' active' if current_view=='card' else ''}\" href=\"{_build_view_url('card')}\">Card View</a>
				<a class=\"toggle-btn{' active' if current_view=='table' else ''}\" href=\"{_build_view_url('table')}\">Table View</a>
			</div>
			"""
		).strip()
		st.markdown(toggle_html, unsafe_allow_html=True)

	# Removed: Sort by / Per page controls
	sort_by = "Newest First"

	# Filter and sort only
	working = _filter_jobs(df, search)
	# Apply sidebar filters if present
	try:
		working = _apply_sidebar_filters(working)
	except Exception:
		pass
	working = _sort_jobs(working, sort_by)

	# Header (title + total jobs) with design, using filtered count
	with hdr_title_col:
		header_html = textwrap.dedent(
			"""
			<div class="jobs-header">
				<div class="jobs-title-section">
					<h2 class="section-title">Job Listings</h2>
					<span class="job-count">{count} Total Jobs</span>
				</div>
			</div>
			"""
		).format(count=len(working)).strip()
		st.markdown(header_html, unsafe_allow_html=True)

	# Pagination (fixed page size)
	per_page = 6

	# If a page is present in the URL query, sync it into session state
	try:
		qp_val = st.query_params.get("jobs_page")
		if isinstance(qp_val, list):
			qp_val = qp_val[0] if qp_val else None
		if qp_val:
			st.session_state[page_key] = int(qp_val)
	except Exception:
		pass
	# Clamp current page safely
	current_page = int(st.session_state.get(page_key, 1))
	total_pages = max(1, (len(working) + per_page - 1) // per_page)
	if current_page < 1:
		current_page = 1
	if current_page > total_pages:
		current_page = total_pages
	st.session_state[page_key] = current_page
	# Slice current page
	page_df, _start_i, _end_i = _paginate(working, current_page, per_page)

	# Removed pagination info display

	# No results state
	if page_df.empty:
		no_results_html = textwrap.dedent(
			"""
			<div style="background: var(--bg-card); border:1px solid var(--border-color); border-radius:12px; padding:24px; text-align:center; color: var(--text-secondary);">
				<div style="font-size:18px; font-weight:600; color: var(--text-primary); margin-bottom:6px;">No results</div>
				<div>Try adjusting your search or clearing filters.</div>
			</div>
			"""
		).strip()
		st.markdown(no_results_html, unsafe_allow_html=True)
		return

	# Render view
	if current_view == "card":
		# Create clean job cards with integrated status dropdown
		for idx, (_, job) in enumerate(page_df.iterrows()):
			current_status = job.get('status', 'NEW')  # Default to NEW
			
			# Ensure current_status is one of the valid options
			if current_status.upper() not in ["NEW", "ANALYZED", "MATCHED"]:
				current_status = "NEW"
			
			# Create skills HTML
			skills_html = "".join([f"<span class='skill-tag'>{s}</span>" for s in job.get("skills", [])])
			
			# Check if we have an updated status in session state
			updated_jobs = st.session_state.get("updated_jobs", {})
			display_status = updated_jobs.get(job['id'], current_status.upper())
			
			# Create the clean job card with integrated status dropdown
			card_html = textwrap.dedent(
				f"""
				<div class="job-card-clean">
					<div class="job-title">{job['title']}</div>
					<div class="job-company">{job['company']}</div>
					<div class="job-meta">
						<span><span class="location-icon"></span> {job['location']}</span>
						<span><span class="time-icon"></span> {job.get('posted_date','')}</span>
						<span><span class="seniority-icon"></span> {job['experience']}</span>
					</div>
					<div class="job-skills">{skills_html}</div>
					<div class="job-footer">
						<span class="salary-range">{job['salary']}</span>
						<div class="status-dropdown-container">
							<label class="status-label">Status:</label>
							<div class="status-dropdown-wrapper">
								<select class="status-dropdown" data-job-id="{job['id']}" data-current-status="{display_status}">
									<option value="NEW" {"selected" if display_status == "NEW" else ""}>NEW</option>
									<option value="ANALYZED" {"selected" if display_status == "ANALYZED" else ""}>ANALYZED</option>
									<option value="MATCHED" {"selected" if display_status == "MATCHED" else ""}>MATCHED</option>
								</select>
							</div>
						</div>
					</div>
				</div>
				"""
			).strip()
			
			st.markdown(card_html, unsafe_allow_html=True)
			
			# Add JavaScript for the integrated status dropdown
			js_code = f"""
			<script>
			document.addEventListener('DOMContentLoaded', function() {{
				const statusDropdown = document.querySelector('.status-dropdown[data-job-id="{job['id']}"]');
				if (statusDropdown) {{
					statusDropdown.addEventListener('change', function() {{
						const newStatus = this.value;
						const jobId = this.getAttribute('data-job-id');
						
						// Update the dropdown styling based on selected status
						this.className = 'status-dropdown status-' + newStatus.toLowerCase();
						
						// Show status change indicator
						showStatusChangeIndicator(jobId, newStatus);
					}});
					
					// Set initial status styling
					const currentStatus = this.getAttribute('data-current-status');
					this.className = 'status-dropdown status-' + currentStatus.toLowerCase();
				}}
			}});
			
			function showStatusChangeIndicator(jobId, newStatus) {{
				// Create or update status indicator
				let indicator = document.getElementById('status-indicator-' + jobId);
				if (!indicator) {{
					indicator = document.createElement('div');
					indicator.id = 'status-indicator-' + jobId;
					indicator.className = 'status-change-indicator';
					indicator.innerHTML = `
						<span class="indicator-text">Status changed to {display_status}</span>
						<button class="update-status-btn" onclick="updateJobStatus('${{jobId}}', '${{newStatus}}')">
							Update Status
						</button>
					`;
					
					// Insert after the job card
					const jobCard = document.querySelector('.job-card-clean');
					if (jobCard) {{
						jobCard.parentNode.insertBefore(indicator, jobCard.nextSibling);
					}}
				}} else {{
					indicator.querySelector('.indicator-text').textContent = `Status changed to ${{newStatus}}`;
				}}
			}}
			
			function updateJobStatus(jobId, newStatus) {{
				// Here you would typically make an API call to update the status
				// For now, we'll just show a success message
				const indicator = document.getElementById('status-indicator-' + jobId);
				if (indicator) {{
					indicator.innerHTML = '<span class="indicator-success">✅ Status updated successfully!</span>';
					setTimeout(() => {{
						indicator.remove();
					}}, 3000);
				}}
			}}
			</script>
			"""
			st.markdown(js_code, unsafe_allow_html=True)
			
			# Add separator between job cards
			st.markdown("---")
	else:
		# Table view - simplified with status dropdown in table
		st.markdown('<div class="jobs-table active"><table>', unsafe_allow_html=True)
		
		# Table header
		header_html = textwrap.dedent(
			"""
			<thead>
				<tr>
					<th>Job Title</th>
					<th>Company</th>
					<th>Location</th>
					<th>Seniority</th>
					<th>Skills</th>
					<th>Salary</th>
					<th>Posted</th>
					<th>Status</th>
				</tr>
			</thead>
			<tbody>
			"""
		).strip()
		st.markdown(header_html, unsafe_allow_html=True)
		
		# Table rows with integrated status dropdowns
		for idx, (_, j) in enumerate(page_df.iterrows()):
			current_status = j.get('status', 'NEW')
			skills_html = "".join([f"<span class='table-skill'>{s}</span>" for s in j.get("skills", [])])
			
			# Create status badge for table view
			status_badge_html = f'<span class="status-badge" data-status="{current_status.upper()}">{current_status.upper()}</span>'
			
			# Static row content with status badge
			row_html = textwrap.dedent(
				f"""
				<tr>
					<td class="job-title-cell">{j['title']}</td>
					<td>{j['company']}</td>
					<td>{j['location']}</td>
					<td>{j['experience']}</td>
					<td><div class="table-skills">{skills_html}</div></td>
					<td>{j['salary']}</td>
					<td>{j.get('posted_date','')}</td>
					<td>{status_badge_html}</td>
				</tr>
				"""
			).strip()
			st.markdown(row_html, unsafe_allow_html=True)
			
			# Status dropdown and update button below the table row
			col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
			
			with col7:
				# Empty space to align with salary column
				pass
			
			with col8:
				# Status dropdown - simple 3 options
				table_status_key = f"table_status_{j['id']}_{idx}"
				
				# Check if we have an updated status in session state
				updated_jobs = st.session_state.get("updated_jobs", {})
				table_display_status = updated_jobs.get(j['id'], current_status.upper())
				
				# Use callback to handle status changes
				def _handle_table_status_change():
					new_val = st.session_state[table_status_key]
					if new_val != table_display_status:
						# Update the status in backend
						success = update_job_status(j['id'], new_val)
						if success:
							# Store the updated status in session state
							if "updated_jobs" not in st.session_state:
								st.session_state.updated_jobs = {}
							st.session_state.updated_jobs[j['id']] = new_val
							# Set a success flag
							st.session_state[f"table_status_success_{j['id']}"] = new_val
						else:
							# Set an error flag
							st.session_state[f"table_status_error_{j['id']}"] = True
				
				new_status = st.selectbox(
					"Status",
					options=["NEW", "ANALYZED", "MATCHED"],
					index=["NEW", "ANALYZED", "MATCHED"].index(table_display_status) if table_display_status in ["NEW", "ANALYZED", "MATCHED"] else 0,
					key=table_status_key,
					label_visibility="collapsed",
					on_change=_handle_table_status_change
				)
				
				# Show status messages
				if f"table_status_success_{j['id']}" in st.session_state:
					success_status = st.session_state[f"table_status_success_{j['id']}"]
					st.success(f"✅ Status updated to {success_status}!", icon="✅")
					# Clear the success flag after showing
					del st.session_state[f"table_status_success_{j['id']}"]
				
				if f"table_status_error_{j['id']}" in st.session_state:
					st.error("❌ Failed to update status", icon="❌")
					# Clear the error flag after showing
					del st.session_state[f"table_status_error_{j['id']}"]
		
		st.markdown('</tbody></table></div>', unsafe_allow_html=True)

	# Styled numeric pagination controls (HTML) at bottom
	def _build_page_url(target_page: int) -> str:
		try:
			qp = dict(st.query_params)
			clean_qp: Dict[str, str] = {}
			for k, v in qp.items():
				if k == "jobs_page":
					continue
				if isinstance(v, list):
					if v:
						clean_qp[k] = str(v[-1])
				else:
					clean_qp[k] = str(v)
			clean_qp["jobs_page"] = str(target_page)
			return "?" + urlencode(clean_qp)
		except Exception:
			return f"?jobs_page={target_page}"

	max_buttons = 9
	start_page = max(1, current_page - max_buttons // 2)
	end_page = min(total_pages, start_page + max_buttons - 1)
	start_page = max(1, end_page - max_buttons + 1)

	prev_disabled = "style=\"opacity:0.5;pointer-events:none;\"" if current_page <= 1 else ""
	next_disabled = "style=\"opacity:0.5;pointer-events:none;\"" if current_page >= total_pages else ""

	page_links = []
	for p in range(start_page, end_page + 1):
		active_cls = " active" if p == current_page else ""
		page_links.append(f"<a class=\"page-btn{active_cls}\" href=\"{_build_page_url(p)}\">{p}</a>")

	pagination_html = textwrap.dedent(
		f"""
		<div class=\"pagination\">
			<a class=\"page-btn\" {prev_disabled} href=\"{_build_page_url(max(1, current_page-1))}\">← Previous</a>
			<div class=\"page-numbers\">{''.join(page_links)}</div>
			<a class=\"page-btn\" {next_disabled} href=\"{_build_page_url(min(total_pages, current_page+1))}\">Next →</a>
		</div>
		"""
	).strip()
	st.markdown(pagination_html, unsafe_allow_html=True)

