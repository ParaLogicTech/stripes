import frappe
from frappe import _
from frappe.utils import cint, date_diff, getdate, add_days, cstr
from aqp.air_quality.doctype.reading_aggregate.reading_aggregate import get_daily_reading_aggregates
import drawsvg as dw


@frappe.whitelist(allow_guest=True)
def get_stripes_svg_image(from_date, to_date, monitor_region=None):
	frappe.response.filecontent = get_stripes_svg(from_date, to_date, monitor_region=monitor_region)
	frappe.response.filename = "test.svg"  # Todo filename
	frappe.response.type = "download"
	frappe.response.display_content_as = "inline"


@frappe.whitelist(allow_guest=True)
def get_stripes_svg(from_date, to_date, monitor_region=None):
	daily_averages = get_daily_reading_aggregates(from_date, to_date, monitor_region=monitor_region)
	return draw_stripes_svg(daily_averages, from_date, to_date)


def draw_stripes_svg(daily_aggregates, from_date, to_date):
	from_date = getdate(from_date)
	to_date = getdate(to_date)
	if to_date < from_date:
		frappe.throw(_("To Date cannot be before From Date"))

	svg_width = 365 * 4
	height = cint(svg_width / 2.5)

	days = date_diff(to_date, from_date) + 1
	stripe_width = svg_width / days

	drawing = dw.Drawing(svg_width, height)  # Todo IDs
	group = dw.Group(fill="#ffffff")
	drawing.append(group)

	for day in range(days):
		current_date = add_days(from_date, day)
		date_dict = daily_aggregates.get(cstr(current_date)) or {}

		pollutant_value = date_dict.get("pm_2_5")
		color = pm_2_5_to_color(pollutant_value)

		x_offset = stripe_width * day

		rectange = dw.Rectangle(x_offset, 0, stripe_width, height, fill=color)
		group.append(rectange)

	return drawing.as_svg()


def pm_2_5_to_color(pollutant_value):
	if not pollutant_value:
		return "transparent"

	if pollutant_value < 20:
		return "#B2EBF2"  # lighter cyan
	elif pollutant_value < 40:
		return "#80DEEA"  # light turquoise
	elif pollutant_value < 60:
		return "#4DD0E1"  # turquoise
	elif pollutant_value < 80:
		return "#26C6DA"  # light teal
	elif pollutant_value < 100:
		return "#00BCD4"  # teal
	elif pollutant_value < 120:
		return "#00ACC1"  # muted teal
	elif pollutant_value < 140:
		return "#0097A7"  # muted cyan
	elif pollutant_value < 160:
		return "#F9A825"  # mustard yellow
	elif pollutant_value < 180:
		return "#FF8F00"  # amber
	elif pollutant_value < 200:
		return "#FF6F00"  # dark amber
	elif pollutant_value < 220:
		return "#E65100"  # dark orange
	elif pollutant_value < 240:
		return "#BF360C"  # dark burnt orange
	elif pollutant_value < 260:
		return "#D32F2F"  # red
	elif pollutant_value < 280:
		return "#C62828"  # dark red
	elif pollutant_value < 300:
		return "#B71C1C"  # darker red
	elif pollutant_value < 320:
		return "#8E0000"  # darkest red
	elif pollutant_value < 340:
		return "#5D0000"  # very dark red
	elif pollutant_value < 360:
		return "#7B1FA2"  # dark purple
	elif pollutant_value < 380:
		return "#6A1B9A"  # darker purple
	elif pollutant_value < 400:
		return "#4A148C"  # darkest purple
	elif pollutant_value < 420:
		return "#9B0F29"  # maroon
	elif pollutant_value < 440:
		return "#6D0E29"  # dark maroon
	elif pollutant_value < 460:
		return "#4A0E29"  # darker maroon
	elif pollutant_value < 480:
		return "#3E2723"  # dark brown
	else:
		return "#212121"  # charcoal gray
