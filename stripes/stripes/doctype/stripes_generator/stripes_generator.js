// Copyright (c) 2024, ParaLogic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Stripes Generator', {
	setup(frm) {
		frm.page.toggle_sidebar(false);
	},

	refresh(frm) {
		frm.disable_save();
		frm.events.get_stripes_svg(frm);
	},

	from_date(frm) {
		frm.events.get_stripes_svg(frm);
	},

	to_date(frm) {
		frm.events.get_stripes_svg(frm);
	},

	monitor_region(frm) {
		frm.events.get_stripes_svg(frm);
	},

	get_stripes_svg(frm) {
		if (!frm.doc.from_date || !frm.doc.to_date) {
			frm.events.set_message(frm, "Please set filters");
			return;
		}

		frm.events.set_message(frm, "Loading...");
		return frappe.call({
			method: "stripes.image.get_stripes_svg",
			args: {
				from_date: frm.doc.from_date,
				to_date: frm.doc.to_date,
				monitor_region: frm.doc.monitor_region,
			},
			callback(r) {
				let wrapper = $(frm.fields_dict.svg_display.wrapper);
				wrapper.empty();

				if (r.message) {
					$(r.message).appendTo(wrapper);
				}
			},
			error() {
				frm.events.set_message(frm, "An error occurred");
			},
		})
	},

	set_message(frm, message) {
		let wrapper = $(frm.fields_dict.svg_display.wrapper);

		wrapper.empty();
		$(`<div style="margin-bottom: 5px; color: var(--text-muted);">${message}</div>`).appendTo(wrapper);
	}
});
