#	recipes - Python-based HTML5 generation for cooking recipes
#	Copyright (C) 2019-2019 Johannes Bauer
#
#	This file is part of recipes.
#
#	recipes is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	recipes is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with recipes; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>

import collections
from XMLParser import XMLParser
from Tools import Tools

class Ingredient():
	def __init__(self, ingredient_id, cardinality, unit_id, metadata, original_cardinality = None):
		self._ingredient_id = ingredient_id
		self._cardinality = cardinality
		if (original_cardinality is None) and (cardinality is not None):
			original_cardinality = "%.2f" % (cardinality)
		self._original_cardinality = original_cardinality
		self._unit_id = unit_id
		self._meta = metadata

	@classmethod
	def from_xmlnode(cls, node, metadata):
		ingredient_id = node.get("name")
		if node.get("count") is not None:
			original_cardinality = node["count"]
			cardinality = Tools.str2float(node["count"])
		else:
			original_cardinality = None
			cardinality = None
		unit_id = node.get("unit")
		return cls(ingredient_id = ingredient_id, cardinality = cardinality, unit_id = unit_id, metadata = metadata, original_cardinality = original_cardinality)

	def _create_converted_to(self, new_cardinality, new_unit_id):
		return Ingredient(ingredient_id = self.ingredient_id, cardinality = new_cardinality, unit_id = new_unit_id, metadata = self._meta)

	@property
	def ingredient_id(self):
		return self._ingredient_id

	@property
	def original_cardinality(self):
		return self._original_cardinality

	@property
	def cardinality(self):
		return self._cardinality

	@property
	def unit_id(self):
		return self._unit_id

	@property
	def ingredient_name(self):
		return self._meta.getingredientname(self.ingredient_id)

	@property
	def unit_name(self):
		return self._meta.getunitname(self.unit_id)

	@property
	def is_unitary(self):
		return self.unit_id is None

	@property
	def is_mass(self):
		return self._meta.mass_units.is_known(self.unit_id)

	@property
	def is_volume(self):
		return self._meta.volume_units.is_known(self.unit_id)

	def _get_as_mass(self, unit = "g"):
		if self.is_unitary:
			# Check if there's a unitary lookup
			grams_per_unit = self._meta.get_grams_per_unit_of(self.ingredient_id)
			if grams_per_unit is not None:
				return self._create_converted_to(self._meta.mass_units(self.cardinality * grams_per_unit, "g", unit), unit)
		elif self.is_volume:
			# Check if there's a density defined
			density_g_per_l = self._meta.get_density_of(self.ingredient_id)
			if density_g_per_l is not None:
				volume_liters = self._meta.volume_units(self.cardinality, self.unit_id, "l")
				mass_grams = density_g_per_l * volume_liters
				return self._create_converted_to(self._meta.mass_units(mass_grams, "g", unit), unit)
		elif self.is_mass:
			# Just convert
			return self._create_converted_to(self._meta.mass_units(self.cardinality, self.unit_id, unit), unit)

	def _get_as_volume(self, unit = "ml"):
		if self.is_volume:
			# Just convert
			return self._create_converted_to(self._meta.volume_units(self.cardinality, self.unit_id, unit), unit)
		elif self.is_mass:
			density_g_per_l = self._meta.get_density_of(self.ingredient_id)
			if density_g_per_l is not None:
				mass_grams = self._meta.mass_units(self.cardinality, self.unit_id, "g")
				volume_liters = mass_grams / density_g_per_l
				return self._create_converted_to(self._meta.volume_units(volume_liters, "l", unit), unit)

	def _get_as_unitary(self):
		if self.is_unitary:
			# Just return this
			return self
		elif self.is_mass:
			grams_per_unit = self._meta.get_grams_per_unit_of(self.ingredient_id)
			if grams_per_unit is not None:
				return self._create_converted_to(self._meta.mass_units(self.cardinality, self.unit_id, "g") / grams_per_unit, None)

	def get_as(self, unit):
		if self._meta.mass_units.is_known(unit):
			return self._get_as_mass(unit)
		elif self._meta.volume_units.is_known(unit):
			return self._get_as_volume(unit)
		elif unit == "#":
			return self._get_as_unitary()
		else:
			return None

	def get_preferred(self):
		preferred = self._meta.get_preferred_unit_of(self.ingredient_id)
		alt = None
		if (preferred is not None):
			alt = self.get_as(unit = preferred)
		alt = alt or self
		return alt

	def __str__(self):
		if self.cardinality is None:
			return "%s" % (self.ingredient_id)
		else:
			if self.is_unitary:
				return "%.0f %s" % (self.cardinality, self.ingredient_id)
			else:
				return "%.1f %s %s" % (self.cardinality, self.unit_id, self.ingredient_id)

class IngredientList():
	def __init__(self, name, items, metadata):
		self._name = name
		self._items = items
		self._meta = metadata

	@classmethod
	def from_xmlnode(cls, node, metadata):
		items = [ Ingredient.from_xmlnode(ingredient_node, metadata) for ingredient_node in node.ingredient ]
		return cls(name = node["name"], items = items, metadata = metadata)

	@property
	def name(self):
		return self._name

	def __iadd__(self, other):
		def merge_items(ingredients):
			by_mass = None
			by_volume = None
			remainder = [ ]
			for ingredient in ingredients:
				as_mass = ingredient.get_as("g")
				if as_mass is not None:
					# Can convert to mass!
					if by_mass is None:
						by_mass = as_mass
					else:
						by_mass._cardinality += as_mass.cardinality
					continue

				as_volume = ingredient.get_as("ml")
				if as_volume is not None:
					# Can convert to volume!
					if by_volume is None:
						by_volume = as_volume
					else:
						by_volume._cardinality += as_volume.cardinality
					continue

				# Can convert neither to mass nor volume
				remainder.append(ingredient)

			result = [ by_mass, by_volume ] + remainder
			result = [ ing for ing in result if ing is not None ]
			return result

		new_list = collections.defaultdict(list)
		for ingredient in self:
			new_list[ingredient.ingredient_id].append(ingredient)
		for ingredient in other:
			new_list[ingredient.ingredient_id].append(ingredient)

		new_items = [ ]
		for ingredients in new_list.values():
			new_items += merge_items(ingredients)
		self._items = new_items
		return self

	def __iter__(self):
		return iter(self._items)

	def dump(self):
		for ingredient in self:
			print("%s" % (ingredient))
			if ingredient.cardinality is not None:
				if ingredient.get_as("g") is not None:
					print("    mass: %.0fg" % (ingredient.get_as("g").cardinality))
				if ingredient.get_as("ml") is not None:
					print("    vol : %.0fml" % (ingredient.get_as("ml").cardinality))
				if ingredient.get_as("#") is not None:
					print("    unit: %.1f" % (ingredient.get_as("#").cardinality))

class Recipe():
	def __init__(self, xml_filename, metadata):
		self._xml = XMLParser().parsefile(xml_filename)
		self._meta = metadata
		self._shopping_list = self._create_shopping_list()

	def _create_shopping_list(self):
		slist = IngredientList("Shopping List", [ ], self._meta)
		for ingredient_list in self.ingredient_classes:
			slist += ingredient_list
		return slist

	@property
	def name(self):
		return self._xml["name"]

	@property
	def shopping_list(self):
		return self._shopping_list

	@property
	def ingredient_class_cnt(self):
		return len(list(node for node in self._xml.ingredients.getallchildren() if node.getname() != "#cdata"))

	@property
	def ingredient_classes(self):
		for node in self._xml.ingredients.getallchildren():
			if node.getname() != "#cdata":
				yield IngredientList.from_xmlnode(node, self._meta)

	@property
	def serves(self):
		if self._xml.getchild("serves") is not None:
			return [ (node["count"], self._meta.getservingname(node["value"])) for node in self._xml.serves.option ]

	@property
	def preparation(self):
		return self._xml.preparation
