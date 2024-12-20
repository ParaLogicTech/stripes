import Fuse from 'fuse.js';

class Combobox {
	constructor(wrapper, on_change) {
		this.wrapper = document.querySelector(wrapper);

		this.stripes_container = document.querySelector(".stripes-container");
		this.stripes = document.querySelector(".stripes-container .stripes");

		this.dropdown = this.wrapper.closest(".dropdown");
		this.dropdown_menu = this.dropdown.querySelector(".dropdown-menu");
		this.dropdown_button = this.dropdown.querySelector(".dropdown-toggle");
		this.button_label = this.dropdown_button.querySelector("span");
		this.default_label = this.dropdown_button.querySelector("span").dataset.default || "None";

		this.search = this.wrapper.querySelector("input");
		this.list_items_container = this.wrapper.querySelector("ul.list");
		this.list_items = Array.from(this.wrapper.querySelectorAll("ul.list li"));
		this.current_focus = -1;

		this.on_change = on_change;
		this.current_value = null;

		this.initialize();
		this.set_dropdown_position();
	}

	initialize() {
		this.items = this.list_items.map(item => ({ name: item.innerText.trim(), element: item } ));

		this.fuse = new Fuse(this.items, {
			keys: ["name"],
			threshold: 0.3,
			includeMatches: true,
			minMatchCharLength: 1,
			location: 0,
			distance: 10,
		});

		this.bind_events();
		this.render_items(this.list_items);
		this.set_selected_item_onload();
	}

	bind_events() {
		this.search?.addEventListener("input", () => this.filter_items());
		this.search?.addEventListener('keydown', (e) => this.handle_keyboard_controls(e));

		// Input Focus
		this.dropdown_menu.addEventListener("click", () => setTimeout(() => {this.search?.focus()}, 0));
		this.dropdown_button.addEventListener("click", () => setTimeout(() => {this.search?.focus()}, 0));

		// Bind Item Selection
		this.list_items.forEach(item => {
			item.addEventListener("click", (e) => {
				this.set_value(item.innerText);
				this.trigger_callback();
			});

			// Stop Event Bubbling
			item.addEventListener(("click"), (e) => e.stopPropagation());
		});

		// Adjust dropdown position on window resize
		window.addEventListener('resize', () => this.set_dropdown_position());
	}

	filter_items() {
		const query = this.search?.value.trim();
		const results = query ? this.fuse.search(query).map(result => result.item.element) : this.list_items;
		this.render_items(results);
	}

	render_items(items) {
		this.check_item_existence(items);

		this.list_items.forEach(item => item.style.display = "none");
		items.forEach(item => item.style.display = "flex");
	}

	check_item_existence(items) {
		this.clear_message();

		if (!items.length) {
			this.show_message("Item does not exist!");
		}
	}

	handle_keyboard_controls(e) {
		const items = this.list_items.filter(item => item.style.display === 'flex');

		if (e.key === "ArrowDown") {
			e.preventDefault();

			this.current_focus++;
			if (this.current_focus >= items.length) this.current_focus = 0;
			this.set_highlight(items);
		}

		if (e.key === "ArrowUp") {
			e.preventDefault();

			this.current_focus--;
			if (this.current_focus < 0) this.current_focus = items.length - 1;
			this.set_highlight(items);
		}

		if (e.key === "Enter") {
			e.preventDefault();

			if (this.current_focus > -1) {
				items[this.current_focus].click();
			}
		}

		if (e.key === "Escape") {
			this.search?.blur();

			// Hide Drop Down
			this.dropdown.classList.remove("show");
			this.dropdown_menu.classList.remove("show");
		}
	}

	set_highlight(items) {
		this.remove_highlight(items);
		if (this.current_focus > -1 && this.current_focus < items.length) {
			items[this.current_focus].classList.add("active");
			items[this.current_focus].scrollIntoView({ block: 'nearest' });
		}
	}

	remove_highlight(items) {
		items.forEach(item => {
			item.classList.remove("active");
		});
	}

	clear_message() {
		let message = this.list_items_container.querySelector("h4");
		if (message) {
			message.remove();
		}
	}

	show_message(text) {
		const h4 = document.createElement("h4");
		h4.innerText = text;
		this.list_items_container.appendChild(h4);
	}

	set_value(value) {
		this.current_value = value;
		this.update_selected_in_view();
	}

	trigger_callback() {
		this.on_change?.(this.current_value);
	}

	get_value() {
		if(!this.current_value) return "Global";
		return this.current_value;
	}

	update_selected_in_view() {
		for (let item of this.list_items) {
			const item_value = item.innerText;
			const is_selected = item.classList.contains("selected");

			if (this.current_value == item_value) {
				if(is_selected) {
					item.classList.remove("selected");
					item.querySelector("img")?.remove();
					this.button_label.innerText = this.default_label;
					this.current_value = null;
				} else {
					if (!item.querySelector("img")) item.insertAdjacentHTML("beforeend", `<img src="/assets/stripes/images/icons/check.svg" alt="check">`);
					item.classList.add("selected");
					this.button_label.innerText = this.current_value;
				}
			} else {
				item.classList.remove("selected");
				item.querySelector("img")?.remove();
			}
		}
	}

	set_selected_item_onload() {
		if(!this.current_value) {
			const selected_item = this.items.find(item => this.button_label.innerText === item.name);
			if(selected_item) this.set_value(selected_item.name);
		}
	}

	set_dropdown_position() {
		// Show dropdown before positioning
		this.dropdown_menu.style.display = 'block';

		const dropdown_rect = this.dropdown.getBoundingClientRect();
		const dropdown_width = this.dropdown_menu.offsetWidth;
		const offset = dropdown_rect.right - 25;

		const space_on_right = window.innerWidth - offset;
		const space_on_left = dropdown_rect.left;

		if (space_on_right >= dropdown_width) {
			this.dropdown_menu.style.left = '0';
			this.dropdown_menu.style.right = 'unset';
		} else if (space_on_left >= dropdown_width) {
			this.dropdown_menu.style.left = 'unset';
			this.dropdown_menu.style.right = '0';
		} else {
			this.dropdown_menu.style.left = '50%';
			this.dropdown_menu.style.right = '0';
			this.dropdown_menu.style.transform = 'translateX(-50%)';
		}

		// Hide the dropdown again after positioning
		this.dropdown_menu.style.display = '';
	}
}

// Add Combobox globally
window.Combobox = Combobox;
