# components/navbar.py
import streamlit as st
import os
from urllib.parse import quote


def _get_query_params_safe() -> dict:
	try:
		if hasattr(st, 'query_params'):
			return dict(st.query_params)
	except Exception:
		pass
	try:
		return st.experimental_get_query_params()
	except Exception:
		return {}


def render_navbar(header_data, theme):
	"""
	Renders the main header for the RemotelyX Dashboard
	"""
	# CSS: fixed navbar container with background; remove Streamlit top padding/margins
	st.markdown(f"""
<style>
	/* Navbar height variable */
	:root {{ --navbar-height: 54px; --tabs-height: 44px; }}

	/* Remove Streamlit default header and top padding so navbar can hug the top */
	.stApp > header {{ display: none !important; }}
	.stMain {{ padding-top: 0 !important; }}
	div.block-container {{ padding-top: 0 !important; padding-left: 0 !important; padding-right: 0 !important; }}
	body {{ margin: 0 !important; }}

	/* Ensure the left sidebar starts below the navbar AND the secondary tabs; inherit theme colors */
	section[data-testid="stSidebar"],
	[data-testid="stSidebar"] {{
		position: fixed !important;
		top: calc(var(--navbar-height) + var(--tabs-height)) !important;
		height: calc(100vh - var(--navbar-height) - var(--tabs-height)) !important;
		z-index: 500 !important; /* below navbar (1000) */
		background: var(--bg-secondary) !important;
		border-right: 1px solid var(--border-color) !important;
	}}
	/* Adjust inner sidebar container height if present */
	[data-testid="stSidebar"] > div {{
		height: 100% !important;
		background: var(--bg-secondary) !important;
	}}

	/* Fixed navbar that contains its content */
	.navbar-container {{
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		z-index: 1000;
		background: var(--bg-secondary);
		border-bottom: 1px solid var(--border-color);
		box-shadow: 0 2px 4px rgba(0,0,0,0.1);
		padding: 8px 17px;
		padding-bottom: 42px;
		padding-top: 43px;
		padding-left: 20px;
		height: var(--navbar-height);
		overflow: visible;
		box-sizing: border-box;
		display: flex; align-items: center;
	}}
	.navbar-container * {{ color: var(--text-primary) !important; }}

	/* Flex layout inside navbar to keep everything aligned and responsive */
	.navbar-flex {{
		display: flex;
		align-items: center;
		justify-content: space-between;
		max-width: 1600px;
		margin: 0 auto;
		width: 100%;
		flex-wrap: nowrap;
	}}
	.navbar-left {{ display: flex; align-items: center; gap: 10px; min-width: 0; flex: 1 1 auto; }}
	.navbar-right {{ display: inline-flex; align-items: center; gap: 8px; flex-shrink: 0; flex-wrap: nowrap; white-space: nowrap; flex: 0 0 auto; }}

	.logo-text {{ font-size: 120px; font-weight: 700; white-space: nowrap; }}
	.logo-mark {{ display: flex; align-items: center; overflow: visible; transform: scale(1.0); transform-origin: left center; }}
	.logo-mark img {{ height: 130px; width: auto; display: block; }}

	/* Last updated badge */
	.last-updated {{
		font-size: 14px;
		color: var(--text-muted);
		padding: 14px 13px;
		background: var(--input-bg);
		border-radius: 20px;
	}}

	@media (max-width: 992px) {{
		.last-updated {{ display: none; }}
	}}

	.user-profile {{
		display: flex; align-items: center; gap: 10px;
		padding: 6px 12px;
		background: var(--input-bg);
		border: 1px solid var(--input-border);
		border-radius: 25px;
		cursor: pointer;
	}}
	.avatar {{
		width: 28px; height: 28px; border-radius: 50%;
		display: flex; align-items: center; justify-content: center;
		background: linear-gradient(135deg, var(--brand-purple), var(--brand-purple-dark));
		color: #fff; font-weight: 700; font-size: 12px;
	}}

	/* Theme toggle button (mini inside user-profile) */
	.theme-toggle {{
		/* Override global fixed positioning */
		position: static !important;
		top: auto !important;
		right: auto !important;
		bottom: auto !important;
		left: auto !important;
		width: 32px; height: 32px; border-radius: 50%;
		background: var(--input-bg); border: 1px solid var(--input-border);
		display: flex; align-items: center; justify-content: center; cursor: pointer;
		font-size: 18px; text-decoration: none;
	}}
	.theme-toggle.mini {{
		width: 38px; height: 38px; font-size: 18px;
		margin-right: 0;
	}}

	/* Responsive tweaks: adjust navbar height variable */
	@media (max-width: 992px) {{
		:root {{ --navbar-height: 64px; --tabs-height: 40px; }}
		.logo-text {{ font-size: 24px; }}
		.avatar {{ width: 30px; height: 30px; font-size: 13px; }}
		.user-profile {{ padding: 6px 12px; gap: 8px; }}
		.user-name {{ display: none; }}
		.theme-toggle.mini {{ width: 30px; height: 30px; font-size: 14px; margin-right: 0; }}
		.navbar-right {{ gap: 6px; }}
	}}
	@media (max-width: 600px) {{
		:root {{ --navbar-height: 58px; --tabs-height: 36px; }}
		.logo-text {{ font-size: 20px; }}
	}}

	/* Navigation Tabs (secondary navbar under main) */
	.nav-tabs {{
		display: flex;
		gap: 0;
		padding: 0;
		margin: 0;
		position: fixed;
		top: var(--navbar-height);
		left: 0;
		right: 0;
		margin-top: 28px;
		z-index: 900; /* below navbar (1000), above sidebar (500) */
		background: var(--bg-secondary);
		border-bottom: 1px solid var(--border-color);

		
	}}
	.nav-tab {{
		padding: 12px 20px;
		padding-left: 20px;
		background: transparent;
		border: none;
		color: var(--text-secondary);
		font-size: 15px;
		font-weight: 500;
		cursor: pointer;
		text-decoration: none !important;
		position: relative;
		transition: all 0.2s ease;
		text-decoration: none;
		display: inline-block;
		margin-left: 10px;
	}}
	/* Remove underline on all link states */
	.nav-tab:link, .nav-tab:visited {{
		text-decoration: none !important;
		outline: none !important;
		color: var(--text-secondary) !important;
	}}
	.nav-tab:hover, .nav-tab:active, .nav-tab:focus {{
		text-decoration: none !important;
		outline: none !important;
		color: var(--brand-purple) !important;
	}}
	.nav-tab:last-child {{ border-right: none; }}
	.nav-tab:hover {{ color: var(--text-primary); background: var(--input-bg); }}
	.nav-tab.active {{ color: var(--brand-purple) !important; background: transparent; }}
	.nav-tab.active::after {{ content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 3px; background: var(--brand-purple); }}

	/* No special offset on smaller screens */
</style>
""", unsafe_allow_html=True)

	# Single toggle: show icon that switches to the opposite theme
	is_light = (theme == "light")
	next_theme = "dark" if is_light else "light"
	icon = "🌙" if is_light else "☀️"
	label = "Switch to dark" if is_light else "Switch to light"

	# Choose a much smaller logo height for light mode
	logo_height_px = 28 if is_light else 130

	# Load appropriate SVG logo and embed as data URI to avoid inline <style> rendering issues
	logo_img_html = None
	try:
		assets_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'html', 'Assets'))
		logo_file = 'logo dark.svg' if is_light else 'Remotley-x-white-logo.svg'
		logo_path = os.path.join(assets_dir, logo_file)
		with open(logo_path, 'r', encoding='utf-8') as f:
			svg_text = f.read()
		data_uri = f"data:image/svg+xml;utf8,{quote(svg_text)}"
		logo_img_html = f'<img src="{data_uri}" style="height: {logo_height_px}px; width: auto; display: block;" alt="RemotelyX logo" />'
	except Exception:
		logo_img_html = None

	navbar_html = f"""
	<div class=\"navbar-container\">
		<div class=\"navbar-flex\">
			<div class=\"navbar-left\">
				{(f'<div class="logo-mark">{logo_img_html}</div>' if logo_img_html else f'<span class="logo-text">{header_data["logo"]}<span style="color: var(--brand-blue); margin-left: 2px;">X</span></span>')}
			</div>
			<div class=\"navbar-right\">
				<div class=\"last-updated\">Last updated: {header_data['last_updated']}</div>
				<a class=\"theme-toggle mini\" href=\"?theme={next_theme}\" target=\"_self\" title=\"{label}\">{icon}</a>
				<div class=\"user-profile\">
					<div class=\"avatar\">{header_data['user']['avatar']}</div>
					<span class=\"user-name\">{header_data['user']['name']}</span>
					<span style=\"color: var(--text-muted);\">▼</span>
				</div>
			</div>
		</div>
	</div>
	"""
	st.markdown(navbar_html, unsafe_allow_html=True)

	# Spacer to prevent overlap with fixed navbar
	st.markdown('<div style="height: var(--navbar-height);"></div>', unsafe_allow_html=True)

	# Secondary navigation tabs (Overview, Job Listings, Reports)
	# Determine current view from query params (robust across Streamlit versions)
	qp = _get_query_params_safe()
	raw_view = qp.get('view') if qp is not None else None
	if isinstance(raw_view, (list, tuple)):
		current_view = raw_view[-1] if raw_view else None
	else:
		current_view = str(raw_view) if raw_view is not None else None
	if current_view not in ('overview', 'job-listings', 'reports'):
		current_view = 'overview'

	# Build links preserving theme
	base_theme = f"&theme={theme}" if theme in ("light", "dark") else ""
	links = [
		{"label": "Overview", "key": "overview"},
		{"label": "Job Listings", "key": "job-listings"},
		{"label": "Reports", "key": "reports"},
	]
	tabs_html = '<div class="nav-tabs">' + ''.join(
		f'<a class="nav-tab{(" active" if current_view==item["key"] else "")}" '
		f'aria-current="{("page" if current_view==item["key"] else "false")}" '
		f'href="?view={item["key"]}{base_theme}" target="_self">{item["label"]}</a>'
		for item in links
	) + '</div>'
	st.markdown(tabs_html, unsafe_allow_html=True)
	# Intercept tab clicks to navigate via full reload (most reliable across Streamlit versions)
	try:
		import streamlit.components.v1 as components
		components.html(
			"""
			<script>
			(function(){
			  function onReady(fn){ if(document.readyState!=='loading'){fn()} else { document.addEventListener('DOMContentLoaded', fn);} }
			  onReady(function(){
			    var tabs = document.querySelectorAll('.nav-tab');
			    tabs.forEach(function(tab){
			      tab.addEventListener('click', function(ev){
			        ev.preventDefault();
			        try {
			          var href = ev.currentTarget.getAttribute('href') || '';
			          var url = new URL(window.location.href);
			          var params = new URLSearchParams(href.split('?')[1] || '');
			          var view = params.get('view');
			          var theme = params.get('theme');
			          if(view){ url.searchParams.set('view', view); }
			          if(theme){ url.searchParams.set('theme', theme); }
			          window.location.href = url.toString();
			        } catch(e) {
			          try { window.location.href = ev.currentTarget.href; } catch(_) {}
			        }
			      }, { passive: false });
			    });
			  });
			})();
			</script>
			""",
			height=0,
			width=0,
		)
	except Exception:
		pass
	# Spacer to prevent content overlap with the secondary tabs
	st.markdown('<div style="height: var(--tabs-height);"></div>', unsafe_allow_html=True)
