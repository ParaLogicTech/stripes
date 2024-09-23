import frappe

def update_website_context(context):
	get_monitor_regions(context)

def get_monitor_regions(context):
	context.monitor = frappe._dict()

	country = frappe.get_all("Monitor Region", filters={"type": "Country"}, order_by="creation desc")
	context.monitor.country = [frappe.get_cached_doc("Monitor Region", d) for d in country]

	region = frappe.get_all("Monitor Region", filters={"type": "Province/State"}, order_by="creation desc")
	context.monitor.region = [frappe.get_cached_doc("Monitor Region", d) for d in region]

	city = frappe.get_all("Monitor Region", filters={"type": "City"}, order_by="creation desc")
	context.monitor.city = [frappe.get_cached_doc("Monitor Region", d) for d in city]
