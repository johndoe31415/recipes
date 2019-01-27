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
	if ((text == "1/4") || (text == "¼")) {
		return 0.25;
	} else if ((text == "1/2") || (text == "½")) {
		return 0.5;
	} else if ((text == "3/4") || (text == "¾")) {
		return 0.75;
	} else {
		return text * 1.0;
	}
}

function absfract(value) {
	return Math.abs(value - Math.trunc(value));
}

function round_to_nearest(value, nearest) {
	return Math.round(value / nearest) * nearest;
}

function value_to_text(value, do_round) {
	if (Math.abs(value - 0.25) < 0.1) {
		return "¼";
	} else if (Math.abs(value - 0.5) < 0.1) {
		return "½";
	} else if (Math.abs(value - 0.75) < 0.1) {
		return "¾";
	} else if (value < 1) {
		return value.toFixed(2);
	} else if (value < 10) {
		if ((absfract(value) < 0.2) || (absfract(value) > 0.8)) {
			return value.toFixed(0);
		} else {
			return value.toFixed(1);
		}
	} else if (value < 100) {
		if (do_round) {
			return round_to_nearest(value, 5.0).toFixed(0);
		} else {
			return value.toFixed(0);
		}
	} else {
		if (do_round) {
			return round_to_nearest(value, 10.0).toFixed(0);
		} else {
			return value.toFixed(0);
		}
	}
	return value;
}

function determine_singular_plural(node, value) {
	if (node == null) {
		return;
	}
	const singular = node.getAttribute("singular");
	const plural = node.getAttribute("plural");
	if (singular && plural) {
		if (value == 1) {
			node.innerHTML = singular;
		} else {
			node.innerHTML = plural;
		}
	}
}

function scaletext_scaleby(scaletext, scale_factor) {
	const scalar = scaletext.querySelector(".scalar");

	const new_value = scalar.getAttribute("value") * scale_factor;
	scalar.setAttribute("value", new_value);
	scalar.innerHTML = value_to_text(new_value, true);

	const unit = scaletext.querySelector(".unit");
	const name = scaletext.querySelector(".name");
	determine_singular_plural(unit, scalar.innerHTML);
	determine_singular_plural(name, scalar.innerHTML);
}

function scaletext_callback(scaletext) {
	const scalar = scaletext.querySelector(".scalar");

	const old_value = scalar.getAttribute("value") * 1.0;
	const new_value_text = prompt("Enter new value", value_to_text(old_value, false));
	if ((new_value_text == null) || (new_value_text <= 0)) {
		return;
	}
	const new_value = text_to_value(new_value_text);
	const scale_factor = new_value / old_value;

	document.querySelectorAll(".scaletext").forEach(function(node) {
		scaletext_scaleby(node, scale_factor);
	});
}

function scaletext_event_callback(event) {
	/* We get the event that we registered for scaletext, but the target can be
	 * one of the subordinate <span>s. Therefore, we search the event path for
	 * the right parent. */
	for (let element of event.path) {
		if (element.classList.contains("scaletext")) {
			/* Got the right element */
			scaletext_callback(element);
			return;
		}
	}
}

function initialize_recipe() {
	document.querySelectorAll(".scalar").forEach(function(node) {
		node.setAttribute("value", text_to_value(node.innerHTML));
	});
	document.querySelectorAll(".scaletext").forEach(function(node) {
		scaletext_scaleby(node, 1.0);
		node.onclick = scaletext_event_callback;
	});
}
