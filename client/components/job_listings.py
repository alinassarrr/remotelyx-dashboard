import streamlit as st
import pandas as pd
from datetime import timedelta
from typing import List, Dict, Tuple
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
	with hdr_search_col:
		search = st.text_input("", placeholder="Quick search jobs...", key=f"{key_prefix}jobs_search")
	with hdr_view_col:
		view_mode = st.radio(
			"",
			["Card View", "Table View"],
			horizontal=True,
			index=0,
			key=f"{key_prefix}jobs_view",
		)

	sort_col1, sort_col2, sort_col3 = st.columns([1, 2, 2])
	with sort_col3:
		sort_by = st.selectbox(
			"Sort by:",
			["Newest First", "Oldest First", "Salary (High to Low)", "Salary (Low to High)", "Company A-Z"],
			key=f"{key_prefix}jobs_sort",
		)
	with sort_col2:
		per_page = st.select_slider(
			"Per page",
			options=[6, 9, 12],
			value=6,
			key=f"{key_prefix}jobs_per_page",
		)

	# Filter, sort, and compute pagination bounds BEFORE creating the page widget
	working = _filter_jobs(df, search)
	working = _sort_jobs(working, sort_by)
	total_pages = max(1, (len(working) + int(per_page) - 1) // int(per_page))

	# Clamp current page safely before widget creation
	current_page = int(st.session_state.get(page_key, 1))
	if current_page < 1:
		current_page = 1
	if current_page > total_pages:
		current_page = total_pages
	st.session_state[page_key] = current_page

	with sort_col1:
		page = st.number_input(
			"Page",
			min_value=1,
			max_value=total_pages,
			value=st.session_state[page_key],
			step=1,
			key=page_key,
		)

	# Paginate
	page_df, start_i, end_i = _paginate(working, page, int(per_page))

	# Pagination info
	pagination_html = textwrap.dedent(
		f"""
		<div class="pagination-info">
			<span class="showing-text">Showing {start_i}-{end_i} of {len(working)} jobs</span>
			<div class="sort-controls">
				<span class="sort-label">Sorted: {sort_by}</span>
			</div>
		</div>
		"""
	).strip()
	st.markdown(pagination_html, unsafe_allow_html=True)

	# Render view
	if view_mode == "Card View":
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

	# Pagination controls
	prev_col, pages_col, next_col = st.columns([1, 3, 1])
	with prev_col:
		if st.button("← Previous", disabled=page <= 1, key=f"{key_prefix}prev"):
			st.session_state[pending_key] = max(1, page - 1)
			# Prefer st.rerun if available, else fallback
			try:
				st.rerun()
			except Exception:
				st.experimental_rerun()
	with pages_col:
		st.write(f"Page {page} of {total_pages}")
	with next_col:
		if st.button("Next →", disabled=page >= total_pages, key=f"{key_prefix}next"):
			st.session_state[pending_key] = min(total_pages, page + 1)
			try:
				st.rerun()
			except Exception:
				st.experimental_rerun()

