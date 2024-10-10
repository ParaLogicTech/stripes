import frappe
from stripes.svg import get_stripes_svg

def get_context(context):
	region = frappe.local.request.path.split("/")[-1]
	if region:
		context.stripes = get_stripes_svg("2018-01-01", "2018-12-31", region)
		context.selected_region = region
	else:
		context.stripes = get_stripes_svg("2018-01-01", "2018-12-31")
		context.selected_region = "Global"
