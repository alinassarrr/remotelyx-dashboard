import streamlit as st
import pandas as pd
from datetime import timedelta
from typing import List, Dict, Tuple
from urllib.parse import urlencode
import textwrap

from fake_data import job_listings as FAKE_JOBS


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
	Render Job Listings with the provided design, reading data from fake_data.job_listings.
	Includes header, search, view toggle, sort, pagination, and cards/table rendering.
	"""
	df = pd.DataFrame(FAKE_JOBS)
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
		).format(count=len(df)).strip()
		st.markdown(header_html, unsafe_allow_html=True)
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
		# Build hidden inputs to preserve existing query params while submitting search
		try:
			qp_items = list(dict(st.query_params).items())
		except Exception:
			qp_items = []
		hidden_parts = []
		for k, v in qp_items:
			if k == "jobs_search":
				continue
			if isinstance(v, list):
				if v:
					hidden_parts.append(f"<input type='hidden' name='{k}' value='{str(v[-1]).replace("'", '&#39;').replace('"', '&quot;')}'>")
			else:
				hidden_parts.append(f"<input type='hidden' name='{k}' value='{str(v).replace("'", '&#39;').replace('"', '&quot;')}'>")
		search_value = (search or "").replace("'", "&#39;").replace('"', '&quot;')
		search_html = textwrap.dedent(
			f"""
			<form method='get' class='jobs-controls'>
				<input type='text' class='search-box' name='jobs_search' placeholder='Quick search jobs...' value='{search_value}'>
				{''.join(hidden_parts)}
			</form>
			"""
		).strip()
		st.markdown(search_html, unsafe_allow_html=True)
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
	working = _sort_jobs(working, sort_by)

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

	# Render view
	if current_view == "card":
		# Build all cards and emit inside one grid container so CSS grid works
		cards = []
		for _, job in page_df.iterrows():
			status_class = (
				"new" if "new" in job.get("status", "").lower() else
				"analyzed" if "analy" in job.get("status", "").lower() else
				"matched" if "match" in job.get("status", "").lower() else ""
			)
			skills_html = "".join([f"<span class='skill-tag'>{s}</span>" for s in job.get("skills", [])])
			card_html = textwrap.dedent(
				f"""
					<div class="job-card">
					<span class="job-status {status_class}">{job.get('status','').upper()}</span>
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
						<div class="job-actions">
							<button class="action-btn">Save</button>
							<button class="action-btn">Analyze</button>
							<button class="action-btn">Details</button>
						</div>
					</div>
				</div>
				"""
			).strip()
			cards.append(card_html)
		grid_html = f"<div class='jobs-grid'>{''.join(cards)}</div>"
		st.markdown(grid_html, unsafe_allow_html=True)
	else:
		# Simple HTML table to match styles
		rows = []
		for _, j in page_df.iterrows():
			skills = "".join([f"<span class='table-skill'>{s}</span>" for s in j.get("skills", [])])
			row_html = textwrap.dedent(
				f"""
				<tr>
					<td class="job-title-cell">{j['title']}</td>
					<td>{j['company']}</td>
					<td>{j['location']}</td>
					<td>{j['experience']}</td>
					<td><div class="table-skills">{skills}</div></td>
					<td>{j['salary']}</td>
					<td>{j.get('posted_date','')}</td>
					<td><span class="table-status">{j.get('status','')}</span></td>
					<td>
						<div class="table-actions">
							<button class="table-action-btn">Analyze</button>
							<button class="table-action-btn">View</button>
						</div>
					</td>
				</tr>
				"""
			).strip()
			rows.append(row_html)

		table_html = textwrap.dedent(
			f"""
			<div class="jobs-table active">
				<table>
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
							<th>Actions</th>
						</tr>
					</thead>
					<tbody>
						{''.join(rows)}
					</tbody>
				</table>
			</div>
			"""
		).strip()
		st.markdown(table_html, unsafe_allow_html=True)

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

