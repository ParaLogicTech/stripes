import frappe
from stripes.svg import get_stripes_svg

def get_context(context):
	context.stripes = get_stripes_svg("2017-01-01", "2018-12-31", "Punjab")
