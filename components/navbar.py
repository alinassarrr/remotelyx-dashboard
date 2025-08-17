# components/navbar.py
import streamlit as st

def render_navbar(header_data, theme):
	"""
	Renders the main header for the RemotelyX Dashboard
	"""
	# CSS: fixed navbar container with background; remove Streamlit top padding/margins
	st.markdown(f"""
<style>
	/* Navbar height variable */
	:root {{ --navbar-height: 70px; }}

	/* Remove Streamlit default header and top padding so navbar can hug the top */
	.stApp > header {{ display: none !important; }}
	.stMain {{ padding-top: 0 !important; }}
	div.block-container {{ padding-top: 0 !important; padding-left: 0 !important; padding-right: 0 !important; }}
	body {{ margin: 0 !important; }}

	/* Ensure the left sidebar starts below the navbar and inherits theme colors */
	section[data-testid="stSidebar"],
	[data-testid="stSidebar"] {{
		position: fixed !important;
		top: var(--navbar-height) !important;
		height: calc(100vh - var(--navbar-height)) !important;
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
		padding: 14px 24px;
		box-sizing: border-box;
		min-height: var(--navbar-height);
		display: flex; align-items: center;
	}}
	.navbar-container * {{ color: var(--text-primary) !important; }}

	/* Flex layout inside navbar to keep everything aligned and responsive */
	.navbar-flex {{
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 16px;
		max-width: 1600px;
		margin: 0 auto;
		width: 100%;
		flex-wrap: nowrap;
	}}
	.navbar-left {{ display: flex; align-items: center; gap: 10px; min-width: 0; flex: 1 1 auto; }}
	.navbar-right {{ display: inline-flex; align-items: center; gap: 8px; flex-shrink: 0; flex-wrap: nowrap; white-space: nowrap; flex: 0 0 auto; }}

	.logo-text {{ font-size: 28px; font-weight: 700; white-space: nowrap; }}

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
		width: 42px; height: 42px; border-radius: 50%;
		background: var(--input-bg); border: 1px solid var(--input-border);
		display: flex; align-items: center; justify-content: center; cursor: pointer;
		font-size: 18px; text-decoration: none;
	}}
	.theme-toggle.mini {{
		width: 34px; height: 34px; font-size: 16px;
		margin-right: 6px;
	}}

	/* Responsive tweaks: adjust navbar height variable */
	@media (max-width: 992px) {{
		:root {{ --navbar-height: 64px; }}
		.logo-text {{ font-size: 24px; }}
		.avatar {{ width: 30px; height: 30px; font-size: 13px; }}
		.user-profile {{ padding: 6px 12px; gap: 8px; }}
		.user-name {{ display: none; }}
		.theme-toggle.mini {{ width: 30px; height: 30px; font-size: 14px; margin-right: 4px; }}
		.navbar-right {{ gap: 6px; }}
	}}
	@media (max-width: 600px) {{
		:root {{ --navbar-height: 58px; }}
		.logo-text {{ font-size: 20px; }}
	}}
</style>
""", unsafe_allow_html=True)

	# Single toggle: show icon that switches to the opposite theme
	is_light = (theme == "light")
	next_theme = "dark" if is_light else "light"
	icon = "🌙" if is_light else "☀️"
	label = "Switch to dark" if is_light else "Switch to light"

	navbar_html = f"""
	<div class=\"navbar-container\">
		<div class=\"navbar-flex\">
			<div class=\"navbar-left\">
				<span class=\"logo-text\">{header_data['logo']}<span style=\"color: var(--brand-blue); margin-left: 2px;\">X</span></span>
			</div>
			<div class=\"navbar-right\">
				<div class=\"user-profile\">
					<div class=\"avatar\">{header_data['user']['avatar']}</div>
					<a class=\"theme-toggle mini\" href=\"?theme={next_theme}\" target=\"_self\" title=\"{label}\">{icon}</a>
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
