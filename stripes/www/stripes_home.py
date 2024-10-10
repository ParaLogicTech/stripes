import frappe
from stripes.svg import get_stripes_svg

def get_context(context):
	# Extract the region from the URL path
	region = frappe.form_dict.get('region')

	# Default context values
	context.stripes = get_stripes_svg("2018-01-01", "2018-12-31")
	context.selected_region = "Global"

	if region:
		context.stripes = get_stripes_svg("2018-01-01", "2018-12-31", region)
		context.selected_region = region
