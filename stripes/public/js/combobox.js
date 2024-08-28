class Combobox {
	constructor(wrapper) {
		this.wrapper = document.querySelector(wrapper);
		this.dropdown = document.querySelector(".dropdown");
		this.dropdown_menu = document.querySelector(".dropdown-menu");
		this.dropdown_buttons = document.querySelectorAll(".dropdown-toggle");
		this.input = this.wrapper.querySelector("input");
		this.list_items_container = this.wrapper.querySelector("ul.list");
		this.list_items = Array.from(this.wrapper.querySelectorAll("ul.list li"));
		this.currentFocus = -1;

		this.initialize();
	}

	initialize() {
		this.items = this.list_items.map(item => ({ name: item.textContent.trim(), element: item }));

		this.fuse = new Fuse(this.items, {
			keys: ["name"],
			threshold: 0.0,
			includeMatches: true,
			minMatchCharLength: 1,
		});

		this.bind_events();
		this.show_items(this.list_items);
		this.toggle_item_selection();
	}

	bind_events() {
		this.input.addEventListener("input", () => this.filter_items());
		this.input.addEventListener('keydown', (e) => this.handle_keyboard_controls(e));
		this.wrapper.addEventListener('click', (e) => this.input.focus());
		this.dropdown_menu.addEventListener('click', (e) => {
			this.input.focus();
			this.remove_highlight(this.list_items);
		});

		// Input Search focus
		this.dropdown_buttons.forEach(dropdown => {
			dropdown.addEventListener("click", () => this.input.focus());
		});
	}

	filter_items() {
		const query = this.input.value.trim();
		const results = query ? this.fuse.search(query).map(result => result.item.element) : this.list_items;
		this.show_items(results);
	}

	show_items(items) {
		this.check_items_existence(items);

		this.list_items.forEach(item => item.style.display = "none");
		items.forEach(item => item.style.display = "flex");
	}

	check_items_existence(items) {
		this.clear_message();

		if (!items.length) {
			this.show_message("Item does not exist!");
		}
	}

	handle_keyboard_controls(e) {
		const items = this.list_items.filter(item => item.style.display === 'flex');

		if (e.key === "ArrowDown") {
			this.currentFocus++;
			if (this.currentFocus >= items.length) this.currentFocus = 0;
			this.set_highlight(items);
		}

		if (e.key === "ArrowUp") {
			this.currentFocus--;
			if (this.currentFocus < 0) this.currentFocus = items.length - 1;
			this.set_highlight(items);
		}

		if (e.key === "Enter") {
			if (this.currentFocus > -1) {
				items[this.currentFocus].click();
			}
		}

		if (e.key === "Escape") {
			this.input.blur();
			this.dropdown.classList.remove("show");
			this.dropdown_menu.classList.remove("show");
		}
	}

	set_highlight(items) {
		this.remove_highlight(items);
		if (this.currentFocus > -1 && this.currentFocus < items.length) {
			items[this.currentFocus].classList.add("active");
			items[this.currentFocus].scrollIntoView({ block: 'nearest' });
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

	toggle_item_selection() {
		this.list_items.forEach(item => {
			item.addEventListener("click", () => {
				const is_selected = item.classList.contains("selected");
	
				if(is_selected) {
					item.classList.remove("selected");
					item.querySelector("img")?.remove();
				} else {
					this._reset_item_selection();

					// Select the clicked item
					if (!item.querySelector("img")) {
						item.insertAdjacentHTML("beforeend", `<img src="/assets/stripes/images/icons/check.svg" alt="check">`);
					}
					item.classList.add("selected");
				}
			});
		});
	}

	_reset_item_selection() {
		this.list_items.forEach(i => {
			i.classList.remove("selected");
			i.querySelector("img")?.remove();
		});
	}
}
