import frappe
from frappe import _
from frappe.utils import cint, date_diff, getdate, add_days, cstr, flt, format_date
from aqp.air_quality.doctype.reading_aggregate.reading_aggregate import get_daily_reading_aggregates
from aqp.air_quality.doctype.monitor_region.monitor_region import get_root_region
from dateutil import relativedelta
from werkzeug.utils import send_file
import drawsvg as dw
import io


@frappe.whitelist(allow_guest=True)
def get_stripes_svg_image(from_date, to_date, monitor_region=None):
	monitor_region = validate_monitor_region(monitor_region)
	file_name = get_file_name(from_date, to_date, monitor_region)

	output = get_stripes_svg(from_date, to_date, monitor_region=monitor_region)

	frappe.response.filecontent = output
	frappe.response.filename = f"{file_name}.svg"
	frappe.response.type = "download"
	frappe.response.display_content_as = "inline"


@frappe.whitelist(allow_guest=True)
def get_stripes_png_image(from_date, to_date, monitor_region=None):
	monitor_region = validate_monitor_region(monitor_region)
	file_name = get_file_name(from_date, to_date, monitor_region)

	output = get_stripes_png(from_date, to_date, monitor_region=monitor_region)

	return send_file(
		output,
		environ=frappe.local.request.environ,
		mimetype="image/png",
		download_name=f"{file_name}.png",
	)


@frappe.whitelist(allow_guest=True)
def get_stripes_svg(from_date, to_date, monitor_region=None):
	monitor_region = validate_monitor_region(monitor_region)
	daily_averages = get_daily_reading_aggregates(from_date, to_date, monitor_region=monitor_region)

	drawing = draw_stripes(daily_averages, from_date, to_date)
	drawing.render_width = '100%'
	drawing.render_height = '100%'
	return drawing.as_svg()


def get_stripes_png(from_date, to_date, monitor_region=None):
	monitor_region = validate_monitor_region(monitor_region)
	daily_averages = get_daily_reading_aggregates(from_date, to_date, monitor_region=monitor_region)

	output = io.BytesIO()

	drawing = draw_stripes(daily_averages, from_date, to_date)
	drawing.save_png(output)
	output.seek(0)

	return output


def draw_stripes(daily_aggregates, from_date, to_date):
	from_date = getdate(from_date)
	to_date = getdate(to_date)
	if to_date < from_date:
		frappe.throw(_("To Date cannot be before From Date"))

	svg_width = 365 * 4
	height = cint(svg_width / 2.5)

	days = date_diff(to_date, from_date) + 1
	stripe_width = cint(flt(svg_width / days, 0))

	drawing = dw.Drawing(svg_width, height)  # Todo IDs
	group = dw.Group()
	drawing.append(group)

	for day in range(days):
		current_date = add_days(from_date, day)
		date_dict = daily_aggregates.get(cstr(current_date)) or {}

		pollutant_value = date_dict.get("pm_2_5")
		color = pm_2_5_to_color(pollutant_value)

		x_offset = stripe_width * day

		rectange = dw.Rectangle(x_offset, 0, stripe_width, height, fill=color, data_date=current_date, data_pollutant=pollutant_value)
		group.append(rectange)

	return drawing


def pm_2_5_to_color(pollutant_value):
	if not pollutant_value:
		return "#ffffff"

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


def validate_monitor_region(monitor_region):
	if not monitor_region:
		monitor_region = get_root_region()

	if not monitor_region:
		frappe.throw(_("Monitor Region not provided"))

	if not frappe.db.exists("Monitor Region", monitor_region, cache=True):
		frappe.throw(_("Monitor Region {0} not found").format(monitor_region), exc=frappe.DoesNotExistError)

	return monitor_region


def get_file_name(from_date, to_date, monitor_region):
	monitor_region = validate_monitor_region(monitor_region)
	from_date = getdate(from_date)
	to_date = getdate(to_date)

	delta = relativedelta.relativedelta(add_days(to_date, 1), from_date)

	if from_date == to_date:
		# Full date Only
		date_str = f"{format_date(from_date, 'yyyyMMdd')}"
	elif delta.years == 1 and delta.months == 0 and delta.days == 0 and from_date.month == 1 and from_date.day == 1:
		# Year Only
		date_str = format_date(from_date, 'yyyy')
	elif delta.years > 1 and delta.months == 0 and delta.days == 0 and from_date.month == 1 and from_date.day == 1:
		# Year range
		date_str = f"{format_date(from_date, 'yyyy')}-{format_date(to_date, 'yyyy')}"
	elif delta.years == 0 and delta.months == 1 and delta.days == 0 and from_date.day == 1:
		# Year and Month only
		date_str = format_date(from_date, 'yyyyMM')
	elif delta.days == 0 and from_date.day == 1:
		# Year and Month range
		date_str = f"{format_date(from_date, 'yyyyMM')}-{format_date(to_date, 'yyyyMM')}"
	else:
		# Full date range
		date_str = f"{format_date(from_date, 'yyyyMMdd')}-{format_date(to_date, 'yyyyMMdd')}"

	return f"{monitor_region}_{date_str}"
