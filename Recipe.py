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
				return self._create_converted_to(self._meta.volume_units(mass_grams, "l", unit), unit)

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
		if self.is_unitary:
			return "%.0f %s" % (self.cardinality, self.ingredient_id)
		else:
			return "%.1f %s %s" % (self.cardinality, self.unit_id, self.ingredient_id)

class IngredientList():
	def __init__(self, node, metadata):
		self._node = node
		self._meta = metadata

	@property
	def name(self):
		return self._node["name"]

	def __iter__(self):
		for ingredient in self._node.ingredient:
			yield Ingredient.from_xmlnode(ingredient, self._meta)

	def dump(self):
		for ingredient in self:
			print("%s" % (ingredient))
			if ingredient.get_mass() is not None:
				print("    mass: %.0fg" % (ingredient.get_mass("g")))
			if ingredient.get_volume() is not None:
				print("    vol : %.0fml" % (ingredient.get_volume("ml")))
			if ingredient.get_unitary_units() is not None:
				print("    unit: %.1f" % (ingredient.get_unitary_units()))
			print()

class Recipe():
	def __init__(self, xml_filename, metadata):
		self._xml = XMLParser().parsefile(xml_filename)
		self._meta = metadata

	@property
	def name(self):
		return self._xml["name"]

	@property
	def ingredient_class_cnt(self):
		return len(list(node for node in self._xml.ingredients.getallchildren() if node.getname() != "#cdata"))

	@property
	def ingredient_classes(self):
		for node in self._xml.ingredients.getallchildren():
			if node.getname() != "#cdata":
				yield IngredientList(node, self._meta)

	@property
	def serves(self):
		if self._xml.getchild("serves") is not None:
			return [ (node["count"], self._meta.getservingname(node["value"])) for node in self._xml.serves.option ]

	@property
	def preparation(self):
		return self._xml.preparation

