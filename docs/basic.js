/*
	recipes - Python-based HTML5 generation for cooking recipes
	Copyright (C) 2019-2019 Johannes Bauer

	This file is part of recipes.

	recipes is free software; you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation; this program is ONLY licensed under
	version 3 of the License, later versions are explicitly excluded.

	recipes is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with recipes; if not, write to the Free Software
	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

	Johannes Bauer <JohannesBauer@gmx.de>
*/

function text_to_value(text) {
	if (text == "1/4") {
		return 0.25;
	} else if (text == "1/2") {
		return 0.5;
	} else if (text == "3/4") {
		return 0.75;
	} else {
		return text | 0;
	}
}

function value_to_text(value) {
	if (Math.abs(value - 0.25) < 0.1) {
		return "1/4";
	} else if (Math.abs(value - 0.5) < 0.1) {
		return "1/2";
	} else if (Math.abs(value - 0.75) < 0.1) {
		return "3/4";
	} else if (value < 1) {
		return value.toFixed(2);
	} else if (value < 10) {
		return value.toFixed(1);
	} else if (value < 100) {
		return (Math.round(value / 5) * 5).toString();
	} else {
		return (Math.round(value / 10) * 10).toString();
	}
	return value;
}

function scalar_callback(event) {
	let scalar = null;
	if (event.target.getAttribute("original") == undefined) {
		scalar = event.target.querySelector(".scalar");
	} else {
		scalar = event.target;
	}

	const old_value = scalar.getAttribute("value") | 0;
	const new_value_text = prompt("Enter new value", value_to_text(old_value));
	if (new_value_text == null) {
		return;
	}
	const new_value = text_to_value(new_value_text);
	const scale_factor = new_value / old_value;

	document.querySelectorAll(".scalar").forEach(function(node) {
		const new_value = node.getAttribute("value") * scale_factor;
		node.setAttribute("value", new_value);
		node.innerHTML = value_to_text(new_value);
	});
}

function initialize_scalar(node) {
	node.onclick = scalar_callback;
}

function initialize_recipe() {
	document.querySelectorAll(".scalar").forEach(function(node) {
		node.setAttribute("value", text_to_value(node.innerHTML));
	});
	document.querySelectorAll(".scaletext").forEach(function(node) {
		initialize_scalar(node);
	});
}
