# components/navbar.py
import streamlit as st
import os

def render_navbar(header_data, theme):
	"""
	Renders the main header for the RemotelyX Dashboard
	"""
	# CSS: fixed navbar container with background; remove Streamlit top padding/margins
	st.markdown(f"""
<style>
	/* Navbar height variable */
	:root {{ --navbar-height: 70px; --tabs-height: 44px; }}

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
		padding: 0 24px;
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

	.logo-text {{ font-size: 88px; font-weight: 700; white-space: nowrap; }}
	.logo-mark {{ display: flex; align-items: center; overflow: visible; }}
	.logo-mark svg {{ height: calc(var(--navbar-height) * 1.4); width: auto; display: block; }}

	/* Last updated badge */
	.last-updated {{
		font-size: 12px;
		color: var(--text-muted);
		padding: 8px 16px;
		background: var(--input-bg);
		border-radius: 20px;
	}}

	@media (max-width: 992px) {{
		.last-updated {{ display: none; }}
	}}

	.user-profile {{
		display: flex; align-items: center; gap: 10px;
		padding: 8px 16px;
		background: var(--input-bg);
		border: 1px solid var(--input-border);
		border-radius: 25px;
		cursor: pointer;
	}}
	.avatar {{
		width: 34px; height: 34px; border-radius: 50%;
		display: flex; align-items: center; justify-content: center;
		background: linear-gradient(135deg, var(--brand-purple), var(--brand-purple-dark));
		color: #fff; font-weight: 700; font-size: 14px;
	}}

	/* Theme toggle button (mini inside user-profile) */
	.theme-toggle {{
		/* Override global fixed positioning */
		position: static !important;
		top: auto !important;
		right: auto !important;
		bottom: auto !important;
		left: auto !important;
		width: 42px; height: 42px; border-radius: 50%;
		background: var(--input-bg); border: 1px solid var(--input-border);
		display: flex; align-items: center; justify-content: center; cursor: pointer;
		font-size: 18px; text-decoration: none;
	}}
	.theme-toggle.mini {{
		width: 34px; height: 34px; font-size: 16px;
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

	# Load appropriate inline SVG logo (white for dark theme, dark variant for light theme)
	logo_svg = None
	try:
		assets_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'html', 'Assets'))
		logo_file = 'logo dark.svg' if is_light else 'Remotley-x-white-logo.svg'
		logo_path = os.path.join(assets_dir, logo_file)
		with open(logo_path, 'r', encoding='utf-8') as f:
			logo_svg = f.read()
		# Inject inline style to ensure the SVG scales larger regardless of internal attributes
		try:
			if '<svg' in logo_svg:
				logo_svg = logo_svg.replace('<svg ', '<svg style="height: calc(var(--navbar-height) * 1.4); width: auto; display: block;" ', 1)
		except Exception:
			pass
	except Exception:
		logo_svg = None

	navbar_html = f"""
	<div class=\"navbar-container\">
		<div class=\"navbar-flex\">
			<div class=\"navbar-left\">
				{(f'<div class="logo-mark">{logo_svg}</div>' if logo_svg else f'<span class="logo-text">{header_data["logo"]}<span style="color: var(--brand-blue); margin-left: 2px;">X</span></span>')}
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
	# Determine current view from query params
	current_view = None
	try:
		qp = st.query_params if hasattr(st, 'query_params') else {}
		raw_view = qp.get('view') if qp is not None else None
		if isinstance(raw_view, (list, tuple)):
			current_view = raw_view[-1] if raw_view else None
		else:
			current_view = str(raw_view) if raw_view is not None else None
	except Exception:
		current_view = None
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
		f'<a class="nav-tab{(" active" if current_view==item["key"] else "")}" href="?view={item["key"]}{base_theme}" target="_self">{item["label"]}</a>'
		for item in links
	) + '</div>'
	st.markdown(tabs_html, unsafe_allow_html=True)
	# Intercept tab clicks to avoid full browser reload; update URL and request Streamlit rerun
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
			          history.replaceState(null, '', url.toString());
			          window.parent.postMessage({ type: 'streamlit:rerun' }, '*');
			        } catch(e) { console.warn('tab nav handler error', e); }
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
