from . import __version__ as app_version

app_name = "stripes"
app_title = "Stripes"
app_publisher = "ParaLogic"
app_description = "Pollution Stripes"
app_email = "info@paralogic.io"
app_license = "GNU General Public License (v3)"

required_apps = ["ParaLogicTech/aqp"]

web_include_css = ["/assets/stripes/css/fonts/inter/inter.css"]

website_context = {"custom_theme_bundle": "stripes_theme.bundle.css"}

home_page = "stripes_home"

update_website_context = ["stripes.overrides.update_website_context"]

website_route_rules = [
	{
		"from_route": "/region/<path:region>",
		"to_route": " stripes_home"
	},
]