import frappe
from stripes.image import get_stripes_svg
from urllib.parse import quote, urljoin

def get_context(context):
	context.title = "Pollution Stripes"

	# Extract the region from the URL path
	region = frappe.form_dict.get('region')

	context.selected_region = region or "Global"

	context.from_date = "2018-01-01"
	context.to_date = "2018-12-31"

	context.image_api = f"/api/method/stripes.image.get_stripes_png_image"
	context.image_params = f"?from_date={context.from_date}&to_date={context.to_date}"
	if region:
		context.image_params += f"&monitor_region={quote(region)}"

	context.image_url = f"{context.image_api}{context.image_params}"
	context.image = frappe.utils.get_url(context.image_api) + context.image_params

	try:
		context.stripes_svg = get_stripes_svg(context.from_date, context.to_date, monitor_region=region)
	except frappe.DoesNotExistError:
		raise frappe.PageDoesNotExistError
